# SIME_360/backend/graph_data.py
import asyncio

from backend.graph_api_simulator import (
    usuarios_miembros_object,
    usuarios_actividad_object,
    licencias_disponibles_object,
    sitios_sharepoint_object,
    USER_PROFILES,
    generate_dynamic_report_data,
    get_informe_sharepoint_uso_sitios
)

async def obtener_usuarios_miembros():
    """Devuelve el objeto de usuarios miembros del simulador con una demora de 1s."""
    print("SIMULADOR: Solicitando datos de usuarios miembros (1s)...")
    await asyncio.sleep(1)
    print("SIMULADOR: Devolviendo datos de usuarios miembros.")
    return usuarios_miembros_object['value']

async def obtener_usuarios_con_actividad():
    """Devuelve el objeto de actividad de usuarios del simulador con una demora de 1s."""
    print("SIMULADOR: Solicitando datos de actividad de usuarios (1s)...")
    await asyncio.sleep(1)
    print("SIMULADOR: Devolviendo datos de actividad de usuarios.")
    return usuarios_actividad_object['value']

async def obtener_licencias_disponibles():
    """Devuelve el objeto de licencias disponibles del simulador con una demora de 1s."""
    print("SIMULADOR: Solicitando datos de licencias disponibles (1s)...")
    await asyncio.sleep(1)
    return licencias_disponibles_object

async def obtener_sitios_sharepoint():
    """Devuelve el objeto de sitios de SharePoint del simulador con una demora de 1s."""
    print("SIMULADOR: Solicitando datos de sitios de SharePoint (1s)...")
    await asyncio.sleep(1)
    print("SIMULADOR: Devolviendo datos de sitios de SharePoint.")
    return sitios_sharepoint_object['value']

async def obtener_usuario_por_correo(correo: str):
    """
    Busca un usuario en los datos simulados y devuelve su información
    con una demora de 1s.
    """
    print(f"SIMULADOR: Buscando al usuario '{correo}' (1s)...")
    await asyncio.sleep(1)
    
    usuario_encontrado = next((user for user in USER_PROFILES 
                               if user.get("mail") == correo), None)

    if not usuario_encontrado:
        raise Exception("Usuario no encontrado en los datos simulados.")

    usuario_encontrado['manager'] = {
        "displayName": "Líder de Equipo Ficticio",
        "mail": "lider.equipo@empresa.com.co",
        "jobTitle": "Gerente de Proyectos",
    }
    print(f"SIMULADOR: Usuario '{correo}' encontrado.")
    return usuario_encontrado

async def obtener_informe_actividad(servicio, dias):
    """
    Devuelve datos de informe simulados con una demora de 1s.
    """
    print(f"SIMULADOR: Obteniendo informe para '{servicio}' de los últimos {dias} días (1s)...")
    await asyncio.sleep(1)
    
    # Genera datos dinámicos para el rango de días especificado
    all_user_data = generate_dynamic_report_data(USER_PROFILES, dias)

    # Mapea y devuelve los datos específicos para el servicio solicitado
    if servicio == "outlook_actividad":
        return [{"User Principal Name": u["User Principal Name"], "Last Activity Date": u["Last Activity Date"], "Receive Count": u["Receive Count"], "Send Count": u["Send Count"], "Report Refresh Date": u["Report Refresh Date"]} for u in all_user_data]
    if servicio == "buzon_uso":
        return [{"User Principal Name": u["User Principal Name"], "Item Count": u["Item Count"], "Storage Used (Byte)": u["Storage Used (Byte)"], "Prohibit Send Quota (Byte)": u["Prohibit Send Quota (Byte)"], "Has Archive": u["Has Archive"]} for u in all_user_data]
    if servicio == "onedrive_actividad":
        return [{"User Principal Name": u["User Principal Name"], "Last Activity Date": u["Last Activity Date"], "Viewed Or Edited File Count": u["Viewed Or Edited File Count"], "Synced File Count": u["Synced File Count"]} for u in all_user_data]
    if servicio == "onedrive_uso":
        return [{"Owner Principal Name": u["User Principal Name"], "File Count": u["File Count"], "Active File Count": u["Active File Count"], "Storage Used (Byte)": u["Storage Used (Byte) OD"], "Storage Allocated (Byte)": u["Storage Allocated (Byte) OD"]} for u in all_user_data]
    if servicio == "teams_actividad":
        return [{"User Principal Name": u["User Principal Name"], "Last Activity Date": u["Last Activity Date"], "Private Chat Message Count": u["Private Chat Message Count"], "Call Count": u["Call Count"], "Meeting Count": u["Meeting Count"], "Report Refresh Date": u["Report Refresh Date"]} for u in all_user_data]
    if servicio == "sharepoint_actividad":
         return [{"User Principal Name": u["User Principal Name"], "Last Activity Date": u["Last Activity Date"], "Viewed Or Edited File Count": u["Viewed Or Edited File Count SP"], "Synced File Count": u["Synced File Count SP"], "Visited Page Count": u["Visited Page Count SP"], "Report Refresh Date": u["Report Refresh Date"]} for u in all_user_data]
    if servicio == "sharepoint_uso":
        return get_informe_sharepoint_uso_sitios(dias)
        
    return []