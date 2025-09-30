# ─────────────────────────────────────────────────────────────
# 📦 IMPORTACIÓN DE LIBRERÍAS Y MÓDulos NECESARIOS
# ─────────────────────────────────────────────────────────────
import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
)

from backend.auth import permission_required
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash
from config import app_config
from models.modelos import db, Usuario
from backend.routes import api
from backend.login_microsoft import microsoft_auth
from flask_wtf.csrf import CSRFProtect, CSRFError 

# ─────────────────────────────────────────────────────────────
# 🚀 INICIALIZACIÓN DE LA APLICACIÓN FLASK
# ─────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(app_config)
csrf = CSRFProtect(app) 

# ─────────────────────────────────────────────────────────────
# 🗃️ CONFIGURACIÓN DE LA BASE DE DATOS
# ─────────────────────────────────────────────────────────────
db.init_app(app)

# ─────────────────────────────────────────────────────────────
# 🔄 REGISTRO DE BLUEPRINTS
# ─────────────────────────────────────────────────────────────
app.register_blueprint(api)
app.register_blueprint(microsoft_auth)

# ─────────────────────────────────────────────────────────────
# 🚨 MANEJADORES DE ERRORES
# ─────────────────────────────────────────────────────────────

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template(
        "error.html", 
        titulo_error="Error de Verificación", 
        mensaje_error="Tu solicitud no pudo ser procesada por seguridad. Por favor, recarga la página e inténtalo de nuevo."
    ), 400
        
@app.errorhandler(HTTPException)
def handle_error(e):
    return (
        render_template(
            "error.html", titulo_error=f"Error {e.code}", mensaje_error=e.description
        ),
        e.code,
    )

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    print(f"Error inesperado: {e}")
    return (
        render_template(
            "error.html",
            titulo_error="Error Inesperado",
            mensaje_error="Ocurrió un error inesperado en el servidor. Por favor, recarga la página e inténtalo de nuevo.",
        ),
        500,
    )

# ─────────────────────────────────────────────────────────────
# 🔐 RUTAS DE AUTENTICACIÓN
# ─────────────────────────────────────────────────────────────
@app.route("/")
def login():
    if "usuario" in session:
        return redirect(url_for("pagina_inicio"))
    return render_template("login.html")

@app.route("/autenticar", methods=["POST"])
def autenticar():
    usuario_input = request.form["usuario"].strip().lower()
    contrasena = request.form["contrasena"]
    user = Usuario.query.filter_by(usuario=usuario_input).first()

    if user and check_password_hash(user.contrasena, contrasena):
        session["usuario"] = user.usuario
        session["nombre"] = user.nombre_completo
        session["usuario_id"] = user.id
        session["rol"] = "admin_local"

        # --- AJUSTE IMPORTANTE ---
        # 1. Obtener permisos de los roles.
        permissions_from_roles = {p.name for role in user.roles for p in role.permissions}
        
        # 2. Obtener permisos individuales.
        permissions_individual = {p.name for p in user.permissions}
        
        # 3. Unir ambos conjuntos de permisos para eliminar duplicados.
        all_permissions = permissions_from_roles.union(permissions_individual)
        
        # 4. Añadir el permiso de inicio por defecto a la sesión.
        all_permissions.add('acceso:inicio')
        
        # 5. Guardar la lista final en la sesión.
        session['permissions'] = list(all_permissions)
        # -----------------------

        return redirect(
            url_for("control", mensaje="Iniciando sesión...", icono="fa-circle-check", destino=url_for("pagina_inicio"))
        )

    flash("Usuario o contraseña incorrectos.", category="error")
    return redirect(url_for("login"))

# ─────────────────────────────────────────────────────────────
# ⏳ PANTALLA DE TRANSICIÓN
# ─────────────────────────────────────────────────────────────
@app.route("/control")
def control():
    icono = request.args.get("icono", "fa-spinner")
    mensaje = request.args.get("mensaje", "Cargando...")
    destino = request.args.get("destino", url_for("pagina_inicio"))
    return render_template(
        "control.html", icono=icono, mensaje=mensaje, destino=destino
    )

# ─────────────────────────────────────────────────────────────
# 🏠 PÁGINA PRINCIPAL DE LA APLICACIÓN
# ─────────────────────────────────────────────────────────────
@app.route("/index")
def pagina_inicio():
    if "cerrar" in request.args:
        logout_url = (
            url_for("microsoft_auth.logout_microsoft")
            if session.get("rol") != "admin_local"
            else url_for("login")
        )
        session.clear()
        flash("Sesión cerrada correctamente.", category="success")
        return redirect(logout_url)

    if "usuario" not in session:
        flash("Acceso restringido: se necesita iniciar sesión.", category="error")
        return redirect(url_for("login"))

    return render_template(
        "index.html", nombre=session.get("nombre"), usuario=session.get("usuario")
    )


# ─────────────────────────────────────────────────────────────
# 🧩 CARGA DE MÓDulos DINÁMICOS
# ─────────────────────────────────────────────────────────────
@app.route("/modulos_index/<modulo>.html")
def cargar_modulo(modulo):

    if "usuario" not in session:
        abort(401, description="Acceso no autorizado.")

    permission_needed = f"acceso:{modulo}"
    user_id = session.get('usuario_id')
    user = Usuario.query.get(user_id)

    if not user or not user.has_permission(permission_needed):
        abort(403, description="No tienes permiso para acceder a este módulo.")

    ruta = os.path.join(app.template_folder, "modulos_index", f"{modulo}.html")
    if os.path.isfile(ruta):
        return render_template(f"modulos_index/{modulo}.html", nombre=session.get("nombre"))
    
    abort(404, description="Módulo no encontrado")

# ─────────────────────────────────────────────────────────────
# 🛠️ INICIALIZACIÓN DE LA BASE DE DATOS
# ─────────────────────────────────────────────────────────────
with app.app_context():
    db.create_all()