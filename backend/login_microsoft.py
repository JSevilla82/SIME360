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
AbGHQBeVrOVYOSMIfKtzBpaGRZwysBtu = Blueprint("microsoft_auth", __name__)
@AbGHQBeVrOVYOSMIfKtzBpaGRZwysBtu.route("/verify-microsoft-email", methods=["POST"])
def SXhlIwBBbrCKaQDePTXBVMDQKPwiPLdr():
    uBWCDkEeFEmUMDERbUGheyFVNVgeVQlM = request.form.get("email", "").strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", uBWCDkEeFEmUMDERbUGheyFVNVgeVQlM):
        return jsonify({"valid": False, "message": "El formato del correo electrónico no es válido."}), 400
    try:
        pBkbENKNDOawFvemyFbKtLtUZHMcrLzq = uBWCDkEeFEmUMDERbUGheyFVNVgeVQlM.split('@')[1]
    except IndexError:
        return jsonify({"valid": False, "message": "El formato del correo no es válido."}), 400
    BLqlrHjwCXNTRzszHgDXVWSBfdVkYnHk = os.getenv("AZURE_DOMINIOS_AUTORIZADOS", "")
    if not BLqlrHjwCXNTRzszHgDXVWSBfdVkYnHk:
        return jsonify({"valid": False, "message": "No hemos podido encontrar ninguna cuenta con ese nombre de usuario."}), 403
    zajfIyBEtnbSDnjRsozTSHEArDXcOtRR = {kmNeJLaxkiuAKcXzjhTUagqlPuZTbccr.strip().lower() for kmNeJLaxkiuAKcXzjhTUagqlPuZTbccr in BLqlrHjwCXNTRzszHgDXVWSBfdVkYnHk.split(',')}
    if pBkbENKNDOawFvemyFbKtLtUZHMcrLzq not in zajfIyBEtnbSDnjRsozTSHEArDXcOtRR:
        return jsonify({"valid": False, "message": "No hemos podido encontrar ninguna cuenta con ese nombre de usuario."}), 403
    session["login_email"] = uBWCDkEeFEmUMDERbUGheyFVNVgeVQlM
    return jsonify({"valid": True})
@AbGHQBeVrOVYOSMIfKtzBpaGRZwysBtu.route("/login_microsoft", methods=["GET"])
def RuXdQnvJNkwoCyyinevNmEqWaRgVNIYS():
    GYjIQVChqjkUlQOZNbexnMRZmVOWGOUY = os.getenv("AZURE_TENANT_ID_LOGIN")
    EflziiNERTszqWTDsPMiivZzOCSRFbHY = os.getenv("AZURE_CLIENT_ID_LOGIN")
    PhcPvGWUHOnQvFUZhzsOQrSkuECciYQf = os.getenv("AZURE_CLIENT_SECRET_LOGIN")
    if not all([GYjIQVChqjkUlQOZNbexnMRZmVOWGOUY, EflziiNERTszqWTDsPMiivZzOCSRFbHY, PhcPvGWUHOnQvFUZhzsOQrSkuECciYQf]):
        flash("La aplicación no está configurada correctamente. Contacte al administrador.", "error")
        return redirect(url_for("login"))
    mtQnviSiKyddFiXaZPonlumEozPVATzR = f"https://login.microsoftonline.com/{tenant_id}"
    SMVJXMMGURPqFYiqZNKwSPAOMIdmraXE = ConfidentialClientApplication(
        EflziiNERTszqWTDsPMiivZzOCSRFbHY, mtQnviSiKyddFiXaZPonlumEozPVATzR=mtQnviSiKyddFiXaZPonlumEozPVATzR, client_credential=PhcPvGWUHOnQvFUZhzsOQrSkuECciYQf
    )
    session["state"] = str(uuid.uuid4())
    JjyHSWHhRQTlRZVkKBJiwnNxJJVuwaYL = url_for("microsoft_auth.authorized", _external=True)
    miBOTYultAZqByqLspvhZXPpjdBEKQTs = SMVJXMMGURPqFYiqZNKwSPAOMIdmraXE.get_authorization_request_url(
        current_app.config["SCOPE"],
        mtJESuxTdVoogUhuEHFqaCMptRXkuVYg=session["state"],
        JjyHSWHhRQTlRZVkKBJiwnNxJJVuwaYL=JjyHSWHhRQTlRZVkKBJiwnNxJJVuwaYL,
        VYCKYthgbreKDCLjilEkZmakqTyQMYzr=session.get("login_email", ""),
    )
    return redirect(miBOTYultAZqByqLspvhZXPpjdBEKQTs)
@AbGHQBeVrOVYOSMIfKtzBpaGRZwysBtu.route("/callback")
def FeGeTjdQZjpvoEhIxQsukthZitBiulAZ():
    if request.args.get("state") != session.get("state"):
        return render_template("error.html", titulo_error="Error de Seguridad", mensaje_error="El estado de la sesión no es válido."), 403
    if "error" in request.args:
        return render_template("error.html", titulo_error="Error de Autenticación", mensaje_error=request.args.get("error_description"))
    if not request.args.get("code"):
        return render_template("error.html", titulo_error="Error de Autenticación", mensaje_error="No se recibió el código de autorización.")
    return render_template(
        "control.html",
        zrqAYvOqvKlxGPzhqgmePOPiLKEbuakQ="Validando acceso con Microsoft...",
        GeLOCbKHKDpTkceBGUTVMoDifUSgMiXi="fa-shield-alt",
        wVtIiogAGJhoJDLfxHahLGNhoYbIYvyM=url_for("microsoft_auth.procesar_callback", KFqzHUuISZRyjOqErIEXAyEbPATtlZyU=request.args.get("code")),
    )
@AbGHQBeVrOVYOSMIfKtzBpaGRZwysBtu.route("/procesar_callback")
def qEpMZOUHJUaDxzfHAluMJLKIIOTdldxi():
    KFqzHUuISZRyjOqErIEXAyEbPATtlZyU = request.args.get("code")
    GYjIQVChqjkUlQOZNbexnMRZmVOWGOUY = os.getenv("AZURE_TENANT_ID_LOGIN")
    EflziiNERTszqWTDsPMiivZzOCSRFbHY = os.getenv("AZURE_CLIENT_ID_LOGIN")
    PhcPvGWUHOnQvFUZhzsOQrSkuECciYQf = os.getenv("AZURE_CLIENT_SECRET_LOGIN")
    mtQnviSiKyddFiXaZPonlumEozPVATzR = f"https://login.microsoftonline.com/{tenant_id}"
    SMVJXMMGURPqFYiqZNKwSPAOMIdmraXE = ConfidentialClientApplication(EflziiNERTszqWTDsPMiivZzOCSRFbHY, mtQnviSiKyddFiXaZPonlumEozPVATzR=mtQnviSiKyddFiXaZPonlumEozPVATzR, client_credential=PhcPvGWUHOnQvFUZhzsOQrSkuECciYQf)
    JjyHSWHhRQTlRZVkKBJiwnNxJJVuwaYL = url_for("microsoft_auth.authorized", _external=True)
    MYtMJVXTJMkOKHuTNIgoRZeOKFncWaJe = SMVJXMMGURPqFYiqZNKwSPAOMIdmraXE.acquire_token_by_authorization_code(
        KFqzHUuISZRyjOqErIEXAyEbPATtlZyU, jDnZXpbTvUvKebzZOGGwAlCBoTSSVFkY=current_app.config["SCOPE"], JjyHSWHhRQTlRZVkKBJiwnNxJJVuwaYL=JjyHSWHhRQTlRZVkKBJiwnNxJJVuwaYL
    )
    if "access_token" not in MYtMJVXTJMkOKHuTNIgoRZeOKFncWaJe:
        flash(MYtMJVXTJMkOKHuTNIgoRZeOKFncWaJe.get("error_description", "No se pudo obtener el token de acceso."), "error")
        return redirect(url_for("login"))
    YHKQdxDjUSGydNzATCXGTyrdzPwsqnYD = {"Authorization": f"Bearer {result['access_token']}"}
    JHmofSMSfLInDrDmwKniKoIpSMjRqdpc = requests.get(
        "https://graph.microsoft.com/v1.0/me?$select=id,displayName,mail,userPrincipalName",
        YHKQdxDjUSGydNzATCXGTyrdzPwsqnYD=YHKQdxDjUSGydNzATCXGTyrdzPwsqnYD,
    )
    if JHmofSMSfLInDrDmwKniKoIpSMjRqdpc.status_code != 200:
        flash("No se pudo obtener la información del usuario desde Microsoft.", "error")
        return redirect(url_for("login"))
    FwzHovTVNoFKDAxiIjrFRwzKkDYrtxEB = JHmofSMSfLInDrDmwKniKoIpSMjRqdpc.json()
    sKqIQGmnoTrfdrQeCyzsWQwxJDDUUfWb = FwzHovTVNoFKDAxiIjrFRwzKkDYrtxEB.get("id")
    EXZCCbXwCSqHbcRgnMGAABQUUHgOEFpq = FwzHovTVNoFKDAxiIjrFRwzKkDYrtxEB.get("mail") or FwzHovTVNoFKDAxiIjrFRwzKkDYrtxEB.get("userPrincipalName")
    DgNNnfFrsavKOhKAMsQAUMhYoetqXiTg = Usuario.query.filter_by(microsoft_object_id=sKqIQGmnoTrfdrQeCyzsWQwxJDDUUfWb).first()
    session.pop("login_email", None)
    session.pop("state", None)
    if DgNNnfFrsavKOhKAMsQAUMhYoetqXiTg and DgNNnfFrsavKOhKAMsQAUMhYoetqXiTg.estado == 'Activo':
        session["nombre"] = FwzHovTVNoFKDAxiIjrFRwzKkDYrtxEB.get("displayName")
        session["usuario"] = EXZCCbXwCSqHbcRgnMGAABQUUHgOEFpq
        session["usuario_id"] = DgNNnfFrsavKOhKAMsQAUMhYoetqXiTg.id 
        session["rol"] = "usuario_microsoft"  
        zAgbPzQwWYgIvSnfHftTHIOlynOxbOPJ = {tiFpRaTHbdWPYhvpkLtxzDYVHEQZWzkk.name for OiHQRZeybzjQYLluAfGlvRFaCEwmhYZO in DgNNnfFrsavKOhKAMsQAUMhYoetqXiTg.roles for tiFpRaTHbdWPYhvpkLtxzDYVHEQZWzkk in OiHQRZeybzjQYLluAfGlvRFaCEwmhYZO.permissions}
        zUZKBdNmjAfEAQbdybbrYDmeaAvRJKHn = {tiFpRaTHbdWPYhvpkLtxzDYVHEQZWzkk.name for tiFpRaTHbdWPYhvpkLtxzDYVHEQZWzkk in DgNNnfFrsavKOhKAMsQAUMhYoetqXiTg.permissions}
        dYwSqyteiMHNnlgRAnaUiqiWamYiIGPb = zAgbPzQwWYgIvSnfHftTHIOlynOxbOPJ.union(zUZKBdNmjAfEAQbdybbrYDmeaAvRJKHn)
        dYwSqyteiMHNnlgRAnaUiqiWamYiIGPb.add('acceso:inicio')
        session['permissions'] = list(dYwSqyteiMHNnlgRAnaUiqiWamYiIGPb)
        return redirect(
            url_for("control", zrqAYvOqvKlxGPzhqgmePOPiLKEbuakQ="Iniciando sesión...", GeLOCbKHKDpTkceBGUTVMoDifUSgMiXi="fa-circle-check", wVtIiogAGJhoJDLfxHahLGNhoYbIYvyM=url_for("pagina_inicio"))
        )
    else:
        if DgNNnfFrsavKOhKAMsQAUMhYoetqXiTg and DgNNnfFrsavKOhKAMsQAUMhYoetqXiTg.estado != 'Activo':
             flash(f"Acceso denegado. Su cuenta se encuentra en estado '{DgNNnfFrsavKOhKAMsQAUMhYoetqXiTg.estado}'.", "error")
        else:
             flash("Acceso denegado. Su cuenta no tiene permisos para utilizar esta aplicación.", "error")
        return redirect(url_for("login"))
@AbGHQBeVrOVYOSMIfKtzBpaGRZwysBtu.route("/logout_microsoft")
def gsobkYBzrOKPXmMlcqeXPjMcFOXyloNl():
    session.clear()
    VJjnLqkkXMXxLAObiTRjDgeXiRQyZGoM = f"https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri={url_for('login', _external=True)}"
    return redirect(VJjnLqkkXMXxLAObiTRjDgeXiRQyZGoM)
