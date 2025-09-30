import os
import uuid
import re
import requests
from flask import (
    Blueprint,
    redirect,
    url_for,
    session,
    request,
    current_app,
    flash,
    render_template,
    jsonify,
)
from msal import ConfidentialClientApplication
from models.modelos import Usuario, db

microsoft_auth = Blueprint("microsoft_auth", __name__)


@microsoft_auth.route("/verify-microsoft-email", methods=["POST"])
def verify_microsoft_email():
    """
    Paso 1: Verifica si el correo electrónico proporcionado por el usuario pertenece a un dominio autorizado.
    """
    # 1.1. Obtener y validar el formato del correo electrónico.
    email = request.form.get("email", "").strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"valid": False, "message": "El formato del correo electrónico no es válido."}), 400

    # 1.2. Extraer el dominio del correo.
    try:
        domain = email.split('@')[1]
    except IndexError:
        return jsonify({"valid": False, "message": "El formato del correo no es válido."}), 400

    # 1.3. Cargar la lista de dominios permitidos desde las variables de entorno.
    dominios_autorizados_str = os.getenv("AZURE_DOMINIOS_AUTORIZADOS", "")
    
    # --- AJUSTE REALIZADO ---
    # Si no hay dominios configurados, se trata como si el dominio no fuera válido.
    if not dominios_autorizados_str:
        return jsonify({"valid": False, "message": "No hemos podido encontrar ninguna cuenta con ese nombre de usuario."}), 403
        
    dominios_permitidos = {d.strip().lower() for d in dominios_autorizados_str.split(',')}

    # 1.4. Comparar el dominio del usuario con la lista de dominios permitidos.
    if domain not in dominios_permitidos:
        return jsonify({"valid": False, "message": "No hemos podido encontrar ninguna cuenta con ese nombre de usuario."}), 403

    # 1.5. Si es válido, guardar el correo en la sesión para el siguiente paso.
    session["login_email"] = email
    return jsonify({"valid": True})


@microsoft_auth.route("/login_microsoft", methods=["GET"])
def login_microsoft():
    """
    Paso 2: Prepara y redirige al usuario a la página de inicio de sesión de Microsoft.
    """
    # 2.1. Cargar las credenciales de la aplicación desde las variables de entorno.
    tenant_id = os.getenv("AZURE_TENANT_ID_LOGIN")
    client_id = os.getenv("AZURE_CLIENT_ID_LOGIN")
    client_secret = os.getenv("AZURE_CLIENT_SECRET_LOGIN")

    if not all([tenant_id, client_id, client_secret]):
        flash("La aplicación no está configurada correctamente. Contacte al administrador.", "error")
        return redirect(url_for("login"))

    # 2.2. Construir la URL de la autoridad de Microsoft y crear un cliente MSAL.
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    msal_app = ConfidentialClientApplication(
        client_id, authority=authority, client_credential=client_secret
    )

    # 2.3. Generar un 'state' único para proteger contra ataques CSRF.
    session["state"] = str(uuid.uuid4())
    redirect_uri = url_for("microsoft_auth.authorized", _external=True)

    # 2.4. Crear la URL de autorización con los permisos (SCOPE) requeridos.
    auth_url = msal_app.get_authorization_request_url(
        current_app.config["SCOPE"],
        state=session["state"],
        redirect_uri=redirect_uri,
        login_hint=session.get("login_email", ""),
    )

    # 2.5. Redirigir al usuario a Microsoft.
    return redirect(auth_url)


@microsoft_auth.route("/callback")
def authorized():
    """
    Paso 3: Microsoft redirige aquí después de que el usuario se autentica.
    Se realizan validaciones de seguridad antes de procesar el token.
    """
    # 3.1. Validar que el 'state' de la respuesta coincida con el que se envió para evitar CSRF.
    if request.args.get("state") != session.get("state"):
        return render_template("error.html", titulo_error="Error de Seguridad", mensaje_error="El estado de la sesión no es válido."), 403

    # 3.2. Comprobar si Microsoft devolvió algún error (ej. el usuario canceló el login).
    if "error" in request.args:
        return render_template("error.html", titulo_error="Error de Autenticación", mensaje_error=request.args.get("error_description"))

    # 3.3. Verificar que se recibió un código de autorización.
    if not request.args.get("code"):
        return render_template("error.html", titulo_error="Error de Autenticación", mensaje_error="No se recibió el código de autorización.")

    # 3.4. Redirigir a una página intermedia para procesar el código y mantener la URL limpia.
    return render_template(
        "control.html",
        mensaje="Validando acceso con Microsoft...",
        icono="fa-shield-alt",
        destino=url_for("microsoft_auth.procesar_callback", code=request.args.get("code")),
    )


@microsoft_auth.route("/procesar_callback")
def procesar_callback():
    """
    Paso 4: Procesa el código de autorización, obtiene los datos del usuario y crea la sesión en la aplicación.
    """
    # 4.1. Obtener el código y las credenciales para intercambiarlo por un token de acceso.
    code = request.args.get("code")
    tenant_id = os.getenv("AZURE_TENANT_ID_LOGIN")
    client_id = os.getenv("AZURE_CLIENT_ID_LOGIN")
    client_secret = os.getenv("AZURE_CLIENT_SECRET_LOGIN")

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    msal_app = ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)

    # 4.2. Intercambiar el código de autorización por un token de acceso.
    redirect_uri = url_for("microsoft_auth.authorized", _external=True)
    result = msal_app.acquire_token_by_authorization_code(
        code, scopes=current_app.config["SCOPE"], redirect_uri=redirect_uri
    )

    if "access_token" not in result:
        flash(result.get("error_description", "No se pudo obtener el token de acceso."), "error")
        return redirect(url_for("login"))

    # 4.3. Usar el token de acceso para solicitar los datos del usuario a Microsoft Graph API.
    headers = {"Authorization": f"Bearer {result['access_token']}"}
    user_info_response = requests.get(
        "https://graph.microsoft.com/v1.0/me?$select=id,displayName,mail,userPrincipalName",
        headers=headers,
    )

    if user_info_response.status_code != 200:
        flash("No se pudo obtener la información del usuario desde Microsoft.", "error")
        return redirect(url_for("login"))

    user_info = user_info_response.json()
    microsoft_id = user_info.get("id")
    user_mail = user_info.get("mail") or user_info.get("userPrincipalName")

    # 4.4. Verificar si el usuario existe en la base de datos local usando su ID de Microsoft.
    usuario_autorizado = Usuario.query.filter_by(microsoft_object_id=microsoft_id).first()

    # 4.5. Limpiar datos temporales de la sesión.
    session.pop("login_email", None)
    session.pop("state", None)

    # 4.6. Si el usuario está autorizado y activo, crear la sesión en la aplicación.
    if usuario_autorizado and usuario_autorizado.estado == 'Activo':
        session["nombre"] = user_info.get("displayName")
        session["usuario"] = user_mail
        session["usuario_id"] = usuario_autorizado.id 
        session["rol"] = "usuario_microsoft"  

        # 1. Obtener permisos de los roles.
        permissions_from_roles = {p.name for role in usuario_autorizado.roles for p in role.permissions}
        
        # 2. Obtener permisos individuales.
        permissions_individual = {p.name for p in usuario_autorizado.permissions}
        
        # 3. Unir ambos conjuntos de permisos.
        all_permissions = permissions_from_roles.union(permissions_individual)
        
        # 4. Añadir el permiso de inicio por defecto a la sesión.
        all_permissions.add('acceso:inicio')
        
        # 5. Guardar la lista final en la sesión.
        session['permissions'] = list(all_permissions)
        # -----------------------

        return redirect(
            url_for("control", mensaje="Iniciando sesión...", icono="fa-circle-check", destino=url_for("pagina_inicio"))
        )
    else:
        # 4.8. Si no está autorizado o no está activo, redirigir al login con un mensaje de error.
        if usuario_autorizado and usuario_autorizado.estado != 'Activo':
             flash(f"Acceso denegado. Su cuenta se encuentra en estado '{usuario_autorizado.estado}'.", "error")
        else:
             flash("Acceso denegado. Su cuenta no tiene permisos para utilizar esta aplicación.", "error")

        return redirect(url_for("login"))


@microsoft_auth.route("/logout_microsoft")
def logout_microsoft():
    """
    Paso 5: Cierra la sesión del usuario tanto en la aplicación local como en Microsoft.
    """
    # 5.1. Limpiar la sesión de Flask.
    session.clear()
    
    # 5.2. Redirigir al endpoint de cierre de sesión de Microsoft.
    logout_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri={url_for('login', _external=True)}"
    return redirect(logout_url)
