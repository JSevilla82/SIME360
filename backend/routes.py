from flask import Blueprint, jsonify, session, request
import asyncio
from . import data_services as logic

api = Blueprint("api", __name__)

# ----------------- FUNCIONES AUXILIARES -----------------
def validar_sesion():
    if "usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401
    return None

def handle_response(result):
    if isinstance(result, dict) and result.get("error"):
        return jsonify(result), result.get("status", 500)
    return jsonify(result), 200 if not isinstance(result, dict) else result.get("status", 200)

# ----------------- RUTAS DE DATOS GRAPH -----------------
@api.route("/api/usuariosMiembros", methods=["GET"])
def api_usuarios_miembros():
    if (auth_error := validar_sesion()): return auth_error
    datos = asyncio.run(logic.obtener_usuarios_miembros())
    return jsonify(datos)

@api.route("/api/usuariosMiembrosActividad", methods=["GET"])
def api_usuarios_actividad():
    if (auth_error := validar_sesion()): return auth_error
    datos = asyncio.run(logic.obtener_usuarios_con_actividad())
    return jsonify(datos)

@api.route("/api/licenciasDisponibles", methods=["GET"])
def api_licencias_disponibles():
    if (auth_error := validar_sesion()): return auth_error
    datos = asyncio.run(logic.buscar_detalles_licencias())
    return jsonify(datos)

@api.route("/api/licenciasConocidas", methods=["GET"])
def api_licencias_conocidas():
    if (auth_error := validar_sesion()): return auth_error
    datos = logic.cargar_datos_identificador_licencias()
    return jsonify(datos)

@api.route("/api/informe/<string:tipo>/<int:dias>", methods=["GET"])
def api_informe_individual(tipo, dias):
    if (auth_error := validar_sesion()): return auth_error
    datos = asyncio.run(logic.obtener_informes_consolidados(tipo, dias))
    return jsonify(datos)

@api.route("/api/sitiosSharePoint", methods=["GET"])
def api_sitios_sharepoint():
    if (auth_error := validar_sesion()): return auth_error
    datos = asyncio.run(logic.obtener_sitios_sharepoint_procesados())
    return jsonify(datos)

# ----------------- CONFIGURACIÓN - LICENCIAS -----------------
@api.route("/api/licencias", methods=["GET", "POST"])
def handle_licencias():
    if (auth_error := validar_sesion()): return auth_error
    if request.method == "GET":
        result = logic.get_all_licencias()
    elif request.method == "POST":
        result = logic.create_new_licencia(request.get_json())
    return handle_response(result)

@api.route("/api/licencias/<string:licencia_id>", methods=["PUT", "DELETE"])
def handle_single_licencia(licencia_id):
    if (auth_error := validar_sesion()): return auth_error
    if request.method == "PUT":
        result = logic.update_existing_licencia(licencia_id, request.get_json())
    elif request.method == "DELETE":
        result = logic.delete_existing_licencia(licencia_id)
    return handle_response(result)

# ----------------- CONFIGURACIÓN - ACCESO A LA APP -----------------
@api.route("/api/usuario", methods=["GET"])
def api_usuario_por_correo():
    if (auth_error := validar_sesion()): return auth_error
    correo = request.args.get("correo")
    if not correo: return jsonify({"error": "El parámetro 'correo' es obligatorio"}), 400
    try:
        datos = asyncio.run(logic.procesar_usuario_por_correo(correo))
        session["ultimo_user_id_consultado"] = datos.get("userId")
        session["ultimo_correo_consultado"] = datos.get("correo")
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/api/autorizar", methods=["POST"])
def autorizar_acceso_usuario():
    if (auth_error := validar_sesion()): return auth_error
    result = logic.authorize_user_access(session.get("ultimo_user_id_consultado"), session.get("ultimo_correo_consultado"))
    if "success" in result:
        session.pop("ultimo_user_id_consultado", None)
        session.pop("ultimo_correo_consultado", None)
    return handle_response(result)

@api.route("/api/accesos", methods=["GET"])
def obtener_accesos():
    if (auth_error := validar_sesion()): return auth_error
    result = logic.get_all_access_records()
    return handle_response(result)

@api.route("/api/accesos/toggle-estado", methods=["POST"])
def alternar_estado_acceso():
    if (auth_error := validar_sesion()): return auth_error
    result = logic.toggle_user_access_status(request.get_json())
    return handle_response(result)