import asyncio
from models.modelos import Licencia, Usuario, db
from sqlalchemy.exc import IntegrityError
from backend.graph_data import (
    obtener_licencias_disponibles,
    obtener_usuarios_miembros as graph_usuarios_miembros,
    obtener_usuarios_con_actividad as graph_usuarios_actividad,
    obtener_sitios_sharepoint,
    obtener_usuario_por_correo,
    obtener_informe_actividad,
)

# ----------------- OBTENCIÓN Y PROCESAMIENTO DE DATOS DE GRAPH -----------------

def cargar_datos_identificador_licencias():
    licencias = Licencia.query.all()
    return {
        lic.LicenciaSkuId: {
            "NombreLicencia": lic.NombreLicencia,
            "LicenciaPrincipal": int(lic.LicenciaPrincipal),
            "LicenciaDePago": int(lic.LicenciaDePago),
        }
        for lic in licencias
    }

async def buscar_detalles_licencias():
    datos_licencias_api = await obtener_licencias_disponibles()
    if datos_licencias_api and "value" in datos_licencias_api:
        return [
            {
                "skuPartNumber": lic.get("skuPartNumber", "Sin skuPartNumber"),
                "skuId": lic.get("skuId"),
                "prepaidUnits": {
                    "enabled": lic.get("prepaidUnits", {}).get("enabled", 0),
                    "warning": lic.get("prepaidUnits", {}).get("warning", 0),
                },
            }
            for lic in datos_licencias_api["value"]
        ]
    return []

async def obtener_usuarios_miembros():
    datos_usuarios = await graph_usuarios_miembros()
    return datos_usuarios if datos_usuarios else []

async def obtener_usuarios_con_actividad():
    datos_usuarios = await graph_usuarios_actividad()
    return datos_usuarios if datos_usuarios else []

async def procesar_usuario_por_correo(correo: str):
    datos_usuario = await obtener_usuario_por_correo(correo)
    resultado = {
        "userId": datos_usuario.get("id"),
        "nombreCompleto": datos_usuario.get("displayName"),
        "correo": datos_usuario.get("mail") or datos_usuario.get("userPrincipalName"),
        "oficina": datos_usuario.get("officeLocation", "No especificada"),
        "cargo": datos_usuario.get("jobTitle", "No especificado"),
        "estadoCuenta": "Activo" if datos_usuario.get("accountEnabled") else "Inactivo",
        "jefe": None
    }
    jefe = datos_usuario.get("manager")
    if jefe:
        resultado["jefe"] = {
            "nombreCompleto": jefe.get("displayName", "Desconocido"),
            "correo": jefe.get("mail") or jefe.get("userPrincipalName"),
            "cargo": jefe.get("jobTitle", "No especificado")
        }
    return resultado

def convertir_bytes_a_gb_str(valor):
    try:
        return f"{round(int(valor) / (1024 ** 3), 2)} GB"
    except (TypeError, ValueError):
        return "0 GB"
        
async def obtener_informes_consolidados(tipo: str, dias: int):
    servicios_map = {
        "outlook": ["outlook_actividad", "buzon_uso"],
        "onedrive": ["onedrive_actividad", "onedrive_uso"],
        "sharepoint": ["sharepoint_uso"],
        "todos": [
            "outlook_actividad", "buzon_uso", "onedrive_actividad", "onedrive_uso",
            "sharepoint_actividad", "sharepoint_uso", "teams_actividad", "teams_dispositivos"
        ]
    }
    servicios = servicios_map.get(tipo, [tipo] if tipo in servicios_map["todos"] else [])

    if not servicios:
        return {"error": "Tipo de informe no válido", "datos": None}
        
    tareas = [obtener_informe_actividad(servicio, dias) for servicio in servicios]
    resultados = await asyncio.gather(*tareas, return_exceptions=True)
    
    informes_consolidados = {}

    if tipo == "onedrive":
        actividad, uso = resultados
        if isinstance(actividad, Exception) or isinstance(uso, Exception):
            return {"error": str(actividad if isinstance(actividad, Exception) else uso), "datos": None}
        datos = []
        for item_actividad in actividad:
            correo = item_actividad.get("User Principal Name")
            item_uso = next((u for u in uso if u.get("Owner Principal Name") == correo), {})
            clave_fecha = next((k for k in item_actividad if "Report Refresh Date" in k), None)
            fecha_informe = item_actividad.get(clave_fecha, "Fecha no disponible")
            datos.append({
                "Usuario Principal (User Principal Name)": correo or "N/A",
                "Archivos visualizados o editados (Viewed Or Edited File Count)": item_actividad.get("Viewed Or Edited File Count", "0"),
                "Archivos sincronizados (Synced File Count)": item_actividad.get("Synced File Count", "0"),
                "Compartidos internamente (Shared Internally File Count)": item_actividad.get("Shared Internally File Count", "0"),
                "Compartidos externamente (Shared Externally File Count)": item_actividad.get("Shared Externally File Count", "0"),
                "Cantidad de archivos (File Count)": item_uso.get("File Count", "0"),
                "Archivos activos (Active File Count)": item_uso.get("Active File Count", "0"),
                "Última actividad (Last Activity Date)": item_uso.get("Last Activity Date") or item_actividad.get("Last Activity Date", "Sin actividad"),
                "Almacenamiento usado (Storage Used)": convertir_bytes_a_gb_str(item_uso.get("Storage Used (Byte)")),
                "Almacenamiento asignado (Storage Allocated)": convertir_bytes_a_gb_str(item_uso.get("Storage Allocated (Byte)")),
                "Fecha de Informe (Report Refresh Date)": fecha_informe,
            })
        return {"error": None, "datos": datos}

    if tipo == "outlook":
        actividad, buzon = resultados
        if isinstance(actividad, Exception) or isinstance(buzon, Exception):
            return {"error": str(actividad if isinstance(actividad, Exception) else buzon), "datos": None}
        datos = []
        for act in actividad:
            correo = act.get("User Principal Name")
            uso = next((u for u in buzon if u.get("User Principal Name") == correo), {})
            clave_fecha = next((k for k in act if "Report Refresh Date" in k), None)
            fecha_informe = act.get(clave_fecha, "Fecha no disponible")
            datos.append({
                "Usuario Principal (User Principal Name)": correo,
                "Nombre para mostrar (Display Name)": act.get("Display Name"),
                "Productos asignados (Assigned Products)": act.get("Assigned Products"),
                "Última actividad (Last Activity Date)": act.get("Last Activity Date") or uso.get("Last Activity Date") or "Sin actividad",
                "Correos recibidos (Receive Count)": act.get("Receive Count"),
                "Correos enviados (Send Count)": act.get("Send Count"),
                "Cantidad de elementos (Item Count)": uso.get("Item Count"),
                "Almacenamiento usado (Storage Used)": convertir_bytes_a_gb_str(uso.get("Storage Used (Byte)")),
                "Cuota para enviar prohibido (Prohibit Send Quota)": convertir_bytes_a_gb_str(uso.get("Prohibit Send Quota (Byte)")),
                "¿Tiene archivo en línea? (Has Archive)": uso.get("Has Archive"),
                "Fecha de Informe (Report Refresh Date)": fecha_informe,
            })
        return {"error": None, "datos": datos}
        
    for servicio, resultado in zip(servicios, resultados):
        if isinstance(resultado, Exception):
            informes_consolidados[servicio] = {"error": str(resultado), "datos": None}
        elif servicio == "teams_actividad":
            datos = []
            for usuario in resultado:
                clave_fecha = next((k for k in usuario if "Report Refresh Date" in k), None)
                fecha_informe = usuario.get(clave_fecha, "Fecha no disponible")
                datos.append({
                    "Usuario (User Principal Name)": usuario.get("User Principal Name", "N/A"),
                    "Llamadas Realizadas (Call Count)": usuario.get("Call Count", "0"),
                    "Reuniones (Meeting Count)": usuario.get("Meeting Count", "0"),
                    "Mensajes en Chats Privados (Private Chat Message Count)": usuario.get("Private Chat Message Count", "0"),
                    "Última actividad Teams (Last Activity Date)": usuario.get("Last Activity Date", "Sin actividad"),
                    "Fecha de Informe (Report Refresh Date)": fecha_informe,
                })
            informes_consolidados[servicio] = {"error": None, "datos": datos}
        elif servicio == "sharepoint_uso":
            datos = []
            for item in resultado:
                clave_fecha = next((k for k in item if "Report Refresh Date" in k), None)
                fecha_informe = item.get(clave_fecha, "N/A")
                datos.append({
                    "Fecha de actualización del reporte": fecha_informe,
                    "ID del sitio (Site Id)": item.get("Site Id", "N/A"),
                    "URL del sitio (Site URL)": item.get("Site URL", "N/A"),
                    "Nombre del propietario (Owner Display Name)": item.get("Owner Display Name", "N/A"),
                    "Correo del propietario (Owner Principal Name)": item.get("Owner Principal Name", "N/A"),
                    "¿Eliminado? (Is Deleted)": ("Sí" if item.get("Is Deleted") == "True" else "No"),
                    "Última actividad (Last Activity Date)": item.get("Last Activity Date", "Sin actividad"),
                    "Cantidad de archivos (File Count)": item.get("File Count", "0"),
                    "Archivos activos (Active File Count)": item.get("Active File Count", "0"),
                    "Cantidad de visitas (Page View Count)": item.get("Page View Count", "0"),
                    "Páginas visitadas (Visited Page Count)": item.get("Visited Page Count", "0"),
                    "Almacenamiento usado (Storage Used GB)": convertir_bytes_a_gb_str(item.get("Storage Used (Byte)")),
                    "Almacenamiento asignado (Storage Allocated GB)": convertir_bytes_a_gb_str(item.get("Storage Allocated (Byte)")),
                    "Plantilla raíz (Root Web Template)": item.get("Root Web Template", "N/A"),
                    "Periodo del reporte (días)": item.get("Report Period", "N/A"),
                })
            informes_consolidados[servicio] = {"error": None, "datos": datos}
        elif servicio == "sharepoint_actividad":
            datos = []
            for usuario in resultado:
                clave_fecha = next((k for k in usuario if "Report Refresh Date" in k), None)
                fecha_informe = usuario.get(clave_fecha, "Fecha no disponible")
                datos.append({
                    "Nombre de Usuario (User Principal Name)": usuario.get("User Principal Name", "N/A"),
                    "Última Actividad (Last Activity Date)": usuario.get("Last Activity Date", "Sin actividad"),
                    "Archivos Vistos o Editados (Viewed Or Edited File Count)": usuario.get("Viewed Or Edited File Count", "0"),
                    "Archivos Sincronizados (Synced File Count)": usuario.get("Synced File Count", "0"),
                    "Archivos Compartidos Internamente (Shared Internally File Count)": usuario.get("Shared Internally File Count", "0"),
                    "Archivos Compartidos Externamente (Shared Externally File Count)": usuario.get("Shared Externally File Count", "0"),
                    "Páginas Visitadas (Visited Page Count)": usuario.get("Visited Page Count", "0"),
                    "Periodo del Informe (Report Period)": usuario.get("Report Period", "0"),
                    "Fecha de Informe (Report Refresh Date)": fecha_informe,
                })
            informes_consolidados[servicio] = {"error": None, "datos": datos}
        else:
            informes_consolidados[servicio] = {"error": None, "datos": resultado}

    if len(servicios) == 1:
        return informes_consolidados[servicios[0]]
    else:
        return informes_consolidados

async def obtener_sitios_sharepoint_procesados():
    try:
        sitios = await obtener_sitios_sharepoint()
        datos = []
        for item in sitios:
            partes_id = item.get("id", "").split(",")
            site_id = partes_id[1] if len(partes_id) >= 2 else "N/A"
            datos.append({
                "Fecha de creación": item.get("createdDateTime", "N/A"),
                "ID del sitio (Site Id)": site_id,
                "URL del sitio (Site URL)": item.get("webUrl", "N/A"),
                "Nombre del sitio": item.get("displayName", "N/A"),
            })
        return {"error": None, "datos": datos}
    except Exception as e:
        return {"error": str(e), "datos": None}

# ----------------- LÓGICA DE NEGOCIO - GESTIÓN DE LICENCIAS (CRUD) -----------------
def get_all_licencias():
    try:
        licencias = Licencia.query.order_by(Licencia.LicenciaPrincipal.desc(), Licencia.NombreLicencia.asc()).all()
        licencias_list = [{"id": lic.id, "LicenciaSkuId": lic.LicenciaSkuId, "NombreLicencia": lic.NombreLicencia, "LicenciaPrincipal": lic.LicenciaPrincipal, "LicenciaDePago": lic.LicenciaDePago} for lic in licencias]
        return {"licencias": licencias_list, "status": 200}
    except Exception as e:
        return {"error": str(e), "status": 500}

def create_new_licencia(data):
    try:
        if not data.get("LicenciaSkuId"): return {"error": "El SKU ID es requerido", "status": 400}
        if not data.get("NombreLicencia"): return {"error": "El nombre comercial es requerido", "status": 400}
        if data.get("LicenciaPrincipal") and not data.get("LicenciaDePago"): return {"error": "Las licencias principales deben ser de pago", "status": 400}
        if Licencia.query.filter_by(LicenciaSkuId=data.get("LicenciaSkuId")).first(): return {"error": "La licencia ya existe", "status": 409}

        nueva_licencia = Licencia(LicenciaSkuId=data["LicenciaSkuId"], NombreLicencia=data["NombreLicencia"], LicenciaPrincipal=bool(data.get("LicenciaPrincipal", False)), LicenciaDePago=bool(data.get("LicenciaDePago", False)))
        db.session.add(nueva_licencia)
        db.session.commit()
        return {"message": "Licencia creada", "status": 201, "licencia": {"id": nueva_licencia.id, "LicenciaSkuId": nueva_licencia.LicenciaSkuId}}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e), "status": 500}

def update_existing_licencia(licencia_id, data):
    try:
        if not data.get("NombreLicencia"): return {"error": "El nombre comercial es requerido", "status": 400}
        if data.get("LicenciaPrincipal") and not data.get("LicenciaDePago"): return {"error": "Las licencias principales deben ser de pago", "status": 400}

        licencia = Licencia.query.filter_by(LicenciaSkuId=licencia_id).first()
        if not licencia: return {"error": "Licencia no encontrada", "status": 404}

        licencia.NombreLicencia = data["NombreLicencia"]
        licencia.LicenciaPrincipal = bool(data.get("LicenciaPrincipal", False))
        licencia.LicenciaDePago = bool(data.get("LicenciaDePago", False))
        db.session.commit()
        return {"message": "Licencia actualizada", "status": 200}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e), "status": 500}

def delete_existing_licencia(licencia_id):
    try:
        licencia = Licencia.query.filter_by(LicenciaSkuId=licencia_id).first()
        if not licencia: return {"error": "Licencia no encontrada", "status": 404}

        db.session.delete(licencia)
        db.session.commit()
        return {"message": "Licencia eliminada", "status": 200}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e), "status": 500}

# ----------------- LÓGICA DE NEGOCIO - GESTIÓN DE ACCESO A LA APP -----------------
def authorize_user_access(user_id_sesion, correo_sesion):
    if not user_id_sesion or not correo_sesion:
        return {"error": "No hay usuario consultado en sesión", "status": 400}
    try:
        datos_usuario = asyncio.run(procesar_usuario_por_correo(correo_sesion))
        if user_id_sesion != datos_usuario.get("userId"):
            return {"error": "La identidad del usuario no coincide", "status": 403}

        nuevo_usuario = Usuario(
            usuario=correo_sesion,
            nombre_completo=datos_usuario.get("nombreCompleto", "Desconocido"),
            microsoft_object_id=datos_usuario.get("userId"),
            auth_type='microsoft',
            estado="Activo"
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"success": "Acceso autorizado correctamente", "status": 200}
    except IntegrityError:
        db.session.rollback()
        return {"error": "El usuario ya ha sido autorizado previamente", "status": 409}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Error al autorizar: {str(e)}", "status": 500}

def get_all_access_records():
    try:
        registros = Usuario.query.filter_by(auth_type='microsoft').order_by(Usuario.fecha_creacion.desc()).all()
        return [
            {
                "fecha_autorizacion": reg.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": reg.nombre_completo,
                "correo": reg.usuario,
                "estado": reg.estado
            } for reg in registros
        ]
    except Exception as e:
        return {"error": str(e), "status": 500}

def toggle_user_access_status(data):
    try:
        correo = data.get("correo")
        if not correo:
            return {"error": "Correo no proporcionado", "status": 400}

        usuario = Usuario.query.filter_by(usuario=correo, auth_type='microsoft').first()
        if not usuario:
            return {"error": "Usuario no encontrado", "status": 404}

        usuario.estado = "Inactivo" if usuario.estado == "Activo" else "Activo"
        db.session.commit()
        return {"success": True, "nuevo_estado": usuario.estado}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e), "status": 500}