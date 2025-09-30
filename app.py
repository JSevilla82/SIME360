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
pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva = Flask(__name__)
pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.config.from_object(app_config)
JJxBXBQKBtyETBlPyEolplYFUumNdTeP = CSRFProtect(pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva) 
db.init_app(pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva)
pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.register_blueprint(api)
pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.register_blueprint(microsoft_auth)
@pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.errorhandler(CSRFError)
def FWYqgrfAQeAkTUVdOMqwwxKSPnotADov(e):
    return render_template(
        "error.html", 
        yxgWxQIbXqHfAPMANCfHOFLTEaRgwKXp="Error de Verificación", 
        ZfJonesIzLSkEdXvBVOCcRzYmOSdOGdI="Tu solicitud no pudo ser procesada por seguridad. Por favor, recarga la página e inténtalo de nuevo."
    ), 400
@pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.errorhandler(HTTPException)
def lGcoiREDKAYjPfCzzQqVqkzPjGsBRuIx(e):
    return (
        render_template(
            "error.html", yxgWxQIbXqHfAPMANCfHOFLTEaRgwKXp=f"Error {e.code}", ZfJonesIzLSkEdXvBVOCcRzYmOSdOGdI=e.description
        ),
        e.code,
    )
@pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.errorhandler(Exception)
def kjizviAJLgbWljQwPOCmpcniXEGkejaI(e):
    print(f"Error inesperado: {e}")
    return (
        render_template(
            "error.html",
            yxgWxQIbXqHfAPMANCfHOFLTEaRgwKXp="Error Inesperado",
            ZfJonesIzLSkEdXvBVOCcRzYmOSdOGdI="Ocurrió un error inesperado en el servidor. Por favor, recarga la página e inténtalo de nuevo.",
        ),
        500,
    )
@pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.route("/")
def HoanYZrwvKTaVujfpDtiKUeibYtJoOya():
    if "usuario" in session:
        return redirect(url_for("pagina_inicio"))
    return render_template("login.html")
@pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.route("/autenticar", methods=["POST"])
def OXKMnNOdZMUCcXzbDlfRabYVKYzGbNex():
    XTHRZjSwdCckoHOVyaLmZaBvyBELtxHq = request.form["usuario"].strip().lower()
    uUDucsFLDUvMSqxfpMFVFmyIuoBAKKuK = request.form["contrasena"]
    XumcIukJBTvGigyFNkfVnNjbEGZZJDIT = Usuario.query.filter_by(usuario=XTHRZjSwdCckoHOVyaLmZaBvyBELtxHq).first()
    if XumcIukJBTvGigyFNkfVnNjbEGZZJDIT and check_password_hash(XumcIukJBTvGigyFNkfVnNjbEGZZJDIT.uUDucsFLDUvMSqxfpMFVFmyIuoBAKKuK, uUDucsFLDUvMSqxfpMFVFmyIuoBAKKuK):
        session["usuario"] = XumcIukJBTvGigyFNkfVnNjbEGZZJDIT.usuario
        session["nombre"] = XumcIukJBTvGigyFNkfVnNjbEGZZJDIT.nombre_completo
        session["usuario_id"] = XumcIukJBTvGigyFNkfVnNjbEGZZJDIT.id
        session["rol"] = "admin_local"
        XwwGLEQYIynsCBIbFArejQZKryNnIRzQ = {FNFqWbKFkPqHwjBXgGlWAqWKhmbfoxuD.name for IWLrtlOlCwUTCnoYVrDsBoIYHmGFiNtu in XumcIukJBTvGigyFNkfVnNjbEGZZJDIT.roles for FNFqWbKFkPqHwjBXgGlWAqWKhmbfoxuD in IWLrtlOlCwUTCnoYVrDsBoIYHmGFiNtu.permissions}
        deyrAjsnDmTvoDvraBCBkBYJyGjAxMGu = {FNFqWbKFkPqHwjBXgGlWAqWKhmbfoxuD.name for FNFqWbKFkPqHwjBXgGlWAqWKhmbfoxuD in XumcIukJBTvGigyFNkfVnNjbEGZZJDIT.permissions}
        RDNuNEzwdHrxsTiQqpXsHYRLQDVNYxcY = XwwGLEQYIynsCBIbFArejQZKryNnIRzQ.union(deyrAjsnDmTvoDvraBCBkBYJyGjAxMGu)
        RDNuNEzwdHrxsTiQqpXsHYRLQDVNYxcY.add('acceso:inicio')
        session['permissions'] = list(RDNuNEzwdHrxsTiQqpXsHYRLQDVNYxcY)
        return redirect(
            url_for("control", vCeMdxQtPJqTXbAhZRViuVsZXZvGhLZo="Iniciando sesión...", MvBRGWEvSfUALjmenHWtXEZXBLhxJuEi="fa-circle-check", bozneUUvWuMlrOiCvrFPBlWXtlpcMfZs=url_for("pagina_inicio"))
        )
    flash("Usuario o contraseña incorrectos.", category="error")
    return redirect(url_for("login"))
@pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.route("/control")
def EvkgYYaCqpFuvWGNMCIIjskqLxUFVfkE():
    MvBRGWEvSfUALjmenHWtXEZXBLhxJuEi = request.args.get("icono", "fa-spinner")
    vCeMdxQtPJqTXbAhZRViuVsZXZvGhLZo = request.args.get("mensaje", "Cargando...")
    bozneUUvWuMlrOiCvrFPBlWXtlpcMfZs = request.args.get("destino", url_for("pagina_inicio"))
    return render_template(
        "control.html", MvBRGWEvSfUALjmenHWtXEZXBLhxJuEi=MvBRGWEvSfUALjmenHWtXEZXBLhxJuEi, vCeMdxQtPJqTXbAhZRViuVsZXZvGhLZo=vCeMdxQtPJqTXbAhZRViuVsZXZvGhLZo, bozneUUvWuMlrOiCvrFPBlWXtlpcMfZs=bozneUUvWuMlrOiCvrFPBlWXtlpcMfZs
    )
@pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.route("/index")
def dzIGHyAVRkMZoTGCXMGGqBOXqcQvOOaw():
    if "cerrar" in request.args:
        PKbDwSqksvNNiuHoxEPaykCKDfhXHOdW = (
            url_for("microsoft_auth.logout_microsoft")
            if session.get("rol") != "admin_local"
            else url_for("login")
        )
        session.clear()
        flash("Sesión cerrada correctamente.", category="success")
        return redirect(PKbDwSqksvNNiuHoxEPaykCKDfhXHOdW)
    if "usuario" not in session:
        flash("Acceso restringido: se necesita iniciar sesión.", category="error")
        return redirect(url_for("login"))
    return render_template(
        "index.html", nombre=session.get("nombre"), usuario=session.get("usuario")
    )
@pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.route("/modulos_index/<modulo>.html")
def wVlGKDdJntFiIJcRscxHYtyjDMhDExRt(modulo):
    if "usuario" not in session:
        abort(401, description="Acceso no autorizado.")
    WhjiEinnnApCUUuThDyadsEtwyLwEmNd = f"acceso:{modulo}"
    djfdXGShEqTXkQQXceuqZWwpYlGLBBlW = session.get('usuario_id')
    XumcIukJBTvGigyFNkfVnNjbEGZZJDIT = Usuario.query.get(djfdXGShEqTXkQQXceuqZWwpYlGLBBlW)
    if not XumcIukJBTvGigyFNkfVnNjbEGZZJDIT or not XumcIukJBTvGigyFNkfVnNjbEGZZJDIT.has_permission(WhjiEinnnApCUUuThDyadsEtwyLwEmNd):
        abort(403, description="No tienes permiso para acceder a este módulo.")
    LpqBfCFrsqgSwKusHwNSezTwgQsEYhbI = os.path.join(pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.template_folder, "modulos_index", f"{modulo}.html")
    if os.path.isfile(LpqBfCFrsqgSwKusHwNSezTwgQsEYhbI):
        return render_template(f"modulos_index/{modulo}.html", nombre=session.get("nombre"))
    abort(404, description="Módulo no encontrado")
with pdrzPzlEuKXPGHmVBYPtBVtbEiGTgZva.app_context():
    db.create_all()