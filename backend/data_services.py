import asyncio
from models.modelos import Licencia, Usuario, db
from sqlalchemy.exc import IntegrityError
from backend.graph_data import (
    obtener_licencias_disponibles,
    FRTrsYlAtUUhnxhFvXKWTXNPgOotmOBc as graph_usuarios_miembros,
    FYxtFitKsOZTpAqzqJYLgvgVhGsQRYON as graph_usuarios_actividad,
    obtener_sitios_sharepoint,
    obtener_usuario_por_correo,
    obtener_informe_actividad,
)
def RByVXQDkQWUtFjlzxAecnPStfytAoRpi():
    gZKIVkJsVZzWCZonBKaCQjGwIgFRUZoW = Licencia.query.all()
    return {
        IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.LicenciaSkuId: {
            "NombreLicencia": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.NombreLicencia,
            "LicenciaPrincipal": int(IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.LicenciaPrincipal),
            "LicenciaDePago": int(IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.LicenciaDePago),
        }
        for IPohplcztfcTlFhPZBaDVBYzSDsNZXGt in gZKIVkJsVZzWCZonBKaCQjGwIgFRUZoW
    }
async def hlINDQCfwKIGcXyLBOjvbZGZlTVsdkem():
    MUBxQaZXmfShHHwdYtvUZBlaElaSMMzn = await obtener_licencias_disponibles()
    if MUBxQaZXmfShHHwdYtvUZBlaElaSMMzn and "value" in MUBxQaZXmfShHHwdYtvUZBlaElaSMMzn:
        return [
            {
                "skuPartNumber": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.get("skuPartNumber", "Sin skuPartNumber"),
                "skuId": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.get("skuId"),
                "prepaidUnits": {
                    "enabled": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.get("prepaidUnits", {}).get("enabled", 0),
                    "warning": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.get("prepaidUnits", {}).get("warning", 0),
                },
            }
            for IPohplcztfcTlFhPZBaDVBYzSDsNZXGt in MUBxQaZXmfShHHwdYtvUZBlaElaSMMzn["value"]
        ]
    return []
async def FRTrsYlAtUUhnxhFvXKWTXNPgOotmOBc():
    KryvjzatdfSYpJTlwOGGbTULUaFBUtJY = await graph_usuarios_miembros()
    return KryvjzatdfSYpJTlwOGGbTULUaFBUtJY if KryvjzatdfSYpJTlwOGGbTULUaFBUtJY else []
async def FYxtFitKsOZTpAqzqJYLgvgVhGsQRYON():
    KryvjzatdfSYpJTlwOGGbTULUaFBUtJY = await graph_usuarios_actividad()
    return KryvjzatdfSYpJTlwOGGbTULUaFBUtJY if KryvjzatdfSYpJTlwOGGbTULUaFBUtJY else []
async def eMoDGEBToAFtxgBFaOVPgFBsOmfEpFGh(krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm: str):
    YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd = await obtener_usuario_por_correo(krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm)
    yGrmlRDlOxCLsXiferoclBMkprOdnfmY = {
        "userId": YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("id"),
        "nombreCompleto": YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("displayName"),
        "correo": YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("mail") or YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("userPrincipalName"),
        "oficina": YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("officeLocation", "No especificada"),
        "cargo": YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("jobTitle", "No especificado"),
        "estadoCuenta": "Activo" if YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("accountEnabled") else "Inactivo",
        "jefe": None
    }
    pbEyvVXJcmCtejYywnrhqFtHXBMDLRoN = YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("manager")
    if pbEyvVXJcmCtejYywnrhqFtHXBMDLRoN:
        yGrmlRDlOxCLsXiferoclBMkprOdnfmY["jefe"] = {
            "nombreCompleto": pbEyvVXJcmCtejYywnrhqFtHXBMDLRoN.get("displayName", "Desconocido"),
            "correo": pbEyvVXJcmCtejYywnrhqFtHXBMDLRoN.get("mail") or pbEyvVXJcmCtejYywnrhqFtHXBMDLRoN.get("userPrincipalName"),
            "cargo": pbEyvVXJcmCtejYywnrhqFtHXBMDLRoN.get("jobTitle", "No especificado")
        }
    return yGrmlRDlOxCLsXiferoclBMkprOdnfmY
def FaLIRFbSWRoOpUbsdNxLJPKkFbKvGNNM(valor):
    try:
        return f"{round(int(valor) / (1024 ** 3), 2)} GB"
    except (TypeError, ValueError):
        return "0 GB"
async def KfSYZZvKzFuOxaGWaUfBpjslQIZxeFTN(tipo: str, dias: int):
    CHZSIzaOQPwSwmekVMXtsElRvzJswoOJ = {
        "outlook": ["outlook_actividad", "buzon_uso"],
        "onedrive": ["onedrive_actividad", "onedrive_uso"],
        "sharepoint": ["sharepoint_uso"],
        "todos": [
            "outlook_actividad", "buzon_uso", "onedrive_actividad", "onedrive_uso",
            "sharepoint_actividad", "sharepoint_uso", "teams_actividad", "teams_dispositivos"
        ]
    }
    GLJibTTSWvWfARmnLHOsLFdeQxasLhMZ = CHZSIzaOQPwSwmekVMXtsElRvzJswoOJ.get(tipo, [tipo] if tipo in CHZSIzaOQPwSwmekVMXtsElRvzJswoOJ["todos"] else [])
    if not GLJibTTSWvWfARmnLHOsLFdeQxasLhMZ:
        return {"error": "Tipo de informe no válido", "datos": None}
    iHwMNFSjKvgyiEIWZMJoHrkZpKuNqqjz = [obtener_informe_actividad(BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu, dias) for BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu in GLJibTTSWvWfARmnLHOsLFdeQxasLhMZ]
    GsmdAiudjhqwBuUrEutGRPuSoJHgzYwO = await asyncio.gather(*iHwMNFSjKvgyiEIWZMJoHrkZpKuNqqjz, return_exceptions=True)
    NinuaiRVRRKrHYAysgOpYbRIAqrSpWXp = {}
    if tipo == "onedrive":
        mLZctpICCNXbZIWSmVGFWanheqGElcsz, ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF = GsmdAiudjhqwBuUrEutGRPuSoJHgzYwO
        if isinstance(mLZctpICCNXbZIWSmVGFWanheqGElcsz, Exception) or isinstance(ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF, Exception):
            return {"error": str(mLZctpICCNXbZIWSmVGFWanheqGElcsz if isinstance(mLZctpICCNXbZIWSmVGFWanheqGElcsz, Exception) else ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF), "datos": None}
        FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh = []
        for OqEgJuNnFfVRvPkRCSLnhMwlEonnLBTX in mLZctpICCNXbZIWSmVGFWanheqGElcsz:
            krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm = OqEgJuNnFfVRvPkRCSLnhMwlEonnLBTX.get("User Principal Name")
            nEnMhgnLkUjIzSDvNfeIHEUgWHcKBRQP = next((u for u in ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF if u.get("Owner Principal Name") == krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm), {})
            xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ = next((lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa for lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa in OqEgJuNnFfVRvPkRCSLnhMwlEonnLBTX if "Report Refresh Date" in lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa), None)
            RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb = OqEgJuNnFfVRvPkRCSLnhMwlEonnLBTX.get(xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ, "Fecha no disponible")
            FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh.append({
                "Usuario Principal (User Principal Name)": krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm or "N/A",
                "Archivos visualizados o editados (Viewed Or Edited File Count)": OqEgJuNnFfVRvPkRCSLnhMwlEonnLBTX.get("Viewed Or Edited File Count", "0"),
                "Archivos sincronizados (Synced File Count)": OqEgJuNnFfVRvPkRCSLnhMwlEonnLBTX.get("Synced File Count", "0"),
                "Compartidos internamente (Shared Internally File Count)": OqEgJuNnFfVRvPkRCSLnhMwlEonnLBTX.get("Shared Internally File Count", "0"),
                "Compartidos externamente (Shared Externally File Count)": OqEgJuNnFfVRvPkRCSLnhMwlEonnLBTX.get("Shared Externally File Count", "0"),
                "Cantidad de archivos (File Count)": nEnMhgnLkUjIzSDvNfeIHEUgWHcKBRQP.get("File Count", "0"),
                "Archivos activos (Active File Count)": nEnMhgnLkUjIzSDvNfeIHEUgWHcKBRQP.get("Active File Count", "0"),
                "Última actividad (Last Activity Date)": nEnMhgnLkUjIzSDvNfeIHEUgWHcKBRQP.get("Last Activity Date") or OqEgJuNnFfVRvPkRCSLnhMwlEonnLBTX.get("Last Activity Date", "Sin actividad"),
                "Almacenamiento usado (Storage Used)": FaLIRFbSWRoOpUbsdNxLJPKkFbKvGNNM(nEnMhgnLkUjIzSDvNfeIHEUgWHcKBRQP.get("Storage Used (Byte)")),
                "Almacenamiento asignado (Storage Allocated)": FaLIRFbSWRoOpUbsdNxLJPKkFbKvGNNM(nEnMhgnLkUjIzSDvNfeIHEUgWHcKBRQP.get("Storage Allocated (Byte)")),
                "Fecha de Informe (Report Refresh Date)": RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb,
            })
        return {"error": None, "datos": FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh}
    if tipo == "outlook":
        mLZctpICCNXbZIWSmVGFWanheqGElcsz, bEkbtmUlXxyLIFUgxZeyJVFdDdLuWOIk = GsmdAiudjhqwBuUrEutGRPuSoJHgzYwO
        if isinstance(mLZctpICCNXbZIWSmVGFWanheqGElcsz, Exception) or isinstance(bEkbtmUlXxyLIFUgxZeyJVFdDdLuWOIk, Exception):
            return {"error": str(mLZctpICCNXbZIWSmVGFWanheqGElcsz if isinstance(mLZctpICCNXbZIWSmVGFWanheqGElcsz, Exception) else bEkbtmUlXxyLIFUgxZeyJVFdDdLuWOIk), "datos": None}
        FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh = []
        for hBsvUFSIcWsvpQuWTTMGZvVwCqLQhoQm in mLZctpICCNXbZIWSmVGFWanheqGElcsz:
            krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm = hBsvUFSIcWsvpQuWTTMGZvVwCqLQhoQm.get("User Principal Name")
            ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF = next((u for u in bEkbtmUlXxyLIFUgxZeyJVFdDdLuWOIk if u.get("User Principal Name") == krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm), {})
            xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ = next((lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa for lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa in hBsvUFSIcWsvpQuWTTMGZvVwCqLQhoQm if "Report Refresh Date" in lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa), None)
            RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb = hBsvUFSIcWsvpQuWTTMGZvVwCqLQhoQm.get(xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ, "Fecha no disponible")
            FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh.append({
                "Usuario Principal (User Principal Name)": krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm,
                "Nombre para mostrar (Display Name)": hBsvUFSIcWsvpQuWTTMGZvVwCqLQhoQm.get("Display Name"),
                "Productos asignados (Assigned Products)": hBsvUFSIcWsvpQuWTTMGZvVwCqLQhoQm.get("Assigned Products"),
                "Última actividad (Last Activity Date)": hBsvUFSIcWsvpQuWTTMGZvVwCqLQhoQm.get("Last Activity Date") or ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF.get("Last Activity Date") or "Sin actividad",
                "Correos recibidos (Receive Count)": hBsvUFSIcWsvpQuWTTMGZvVwCqLQhoQm.get("Receive Count"),
                "Correos enviados (Send Count)": hBsvUFSIcWsvpQuWTTMGZvVwCqLQhoQm.get("Send Count"),
                "Cantidad de elementos (Item Count)": ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF.get("Item Count"),
                "Almacenamiento usado (Storage Used)": FaLIRFbSWRoOpUbsdNxLJPKkFbKvGNNM(ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF.get("Storage Used (Byte)")),
                "Cuota para enviar prohibido (Prohibit Send Quota)": FaLIRFbSWRoOpUbsdNxLJPKkFbKvGNNM(ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF.get("Prohibit Send Quota (Byte)")),
                "¿Tiene archivo en línea? (Has Archive)": ShFmBYdmUvIZAJHkeJEukFccUrNIWEEF.get("Has Archive"),
                "Fecha de Informe (Report Refresh Date)": RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb,
            })
        return {"error": None, "datos": FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh}
    for BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu, yGrmlRDlOxCLsXiferoclBMkprOdnfmY in zip(GLJibTTSWvWfARmnLHOsLFdeQxasLhMZ, GsmdAiudjhqwBuUrEutGRPuSoJHgzYwO):
        if isinstance(yGrmlRDlOxCLsXiferoclBMkprOdnfmY, Exception):
            NinuaiRVRRKrHYAysgOpYbRIAqrSpWXp[BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu] = {"error": str(yGrmlRDlOxCLsXiferoclBMkprOdnfmY), "datos": None}
        elif BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu == "teams_actividad":
            FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh = []
            for djsjlXpfJjIJBvYSvLDfHeJIstoRKEso in yGrmlRDlOxCLsXiferoclBMkprOdnfmY:
                xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ = next((lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa for lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa in djsjlXpfJjIJBvYSvLDfHeJIstoRKEso if "Report Refresh Date" in lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa), None)
                RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb = djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get(xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ, "Fecha no disponible")
                FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh.append({
                    "Usuario (User Principal Name)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("User Principal Name", "N/A"),
                    "Llamadas Realizadas (Call Count)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Call Count", "0"),
                    "Reuniones (Meeting Count)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Meeting Count", "0"),
                    "Mensajes en Chats Privados (Private Chat Message Count)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Private Chat Message Count", "0"),
                    "Última actividad Teams (Last Activity Date)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Last Activity Date", "Sin actividad"),
                    "Fecha de Informe (Report Refresh Date)": RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb,
                })
            NinuaiRVRRKrHYAysgOpYbRIAqrSpWXp[BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu] = {"error": None, "datos": FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh}
        elif BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu == "sharepoint_uso":
            FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh = []
            for lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP in yGrmlRDlOxCLsXiferoclBMkprOdnfmY:
                xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ = next((lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa for lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa in lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP if "Report Refresh Date" in lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa), None)
                RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb = lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get(xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ, "N/A")
                FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh.append({
                    "Fecha de actualización del reporte": RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb,
                    "ID del sitio (Site Id)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Site Id", "N/A"),
                    "URL del sitio (Site URL)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Site URL", "N/A"),
                    "Nombre del propietario (Owner Display Name)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Owner Display Name", "N/A"),
                    "Correo del propietario (Owner Principal Name)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Owner Principal Name", "N/A"),
                    "¿Eliminado? (Is Deleted)": ("Sí" if lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Is Deleted") == "True" else "No"),
                    "Última actividad (Last Activity Date)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Last Activity Date", "Sin actividad"),
                    "Cantidad de archivos (File Count)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("File Count", "0"),
                    "Archivos activos (Active File Count)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Active File Count", "0"),
                    "Cantidad de visitas (Page View Count)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Page View Count", "0"),
                    "Páginas visitadas (Visited Page Count)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Visited Page Count", "0"),
                    "Almacenamiento usado (Storage Used GB)": FaLIRFbSWRoOpUbsdNxLJPKkFbKvGNNM(lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Storage Used (Byte)")),
                    "Almacenamiento asignado (Storage Allocated GB)": FaLIRFbSWRoOpUbsdNxLJPKkFbKvGNNM(lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Storage Allocated (Byte)")),
                    "Plantilla raíz (Root Web Template)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Root Web Template", "N/A"),
                    "Periodo del reporte (días)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("Report Period", "N/A"),
                })
            NinuaiRVRRKrHYAysgOpYbRIAqrSpWXp[BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu] = {"error": None, "datos": FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh}
        elif BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu == "sharepoint_actividad":
            FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh = []
            for djsjlXpfJjIJBvYSvLDfHeJIstoRKEso in yGrmlRDlOxCLsXiferoclBMkprOdnfmY:
                xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ = next((lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa for lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa in djsjlXpfJjIJBvYSvLDfHeJIstoRKEso if "Report Refresh Date" in lkTZifTJNIuTFbldSEPHIqNcIdhyvBsa), None)
                RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb = djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get(xVaHXOEpGuTMJfYuWzoYkJeajBXsKUiQ, "Fecha no disponible")
                FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh.append({
                    "Nombre de Usuario (User Principal Name)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("User Principal Name", "N/A"),
                    "Última Actividad (Last Activity Date)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Last Activity Date", "Sin actividad"),
                    "Archivos Vistos o Editados (Viewed Or Edited File Count)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Viewed Or Edited File Count", "0"),
                    "Archivos Sincronizados (Synced File Count)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Synced File Count", "0"),
                    "Archivos Compartidos Internamente (Shared Internally File Count)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Shared Internally File Count", "0"),
                    "Archivos Compartidos Externamente (Shared Externally File Count)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Shared Externally File Count", "0"),
                    "Páginas Visitadas (Visited Page Count)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Visited Page Count", "0"),
                    "Periodo del Informe (Report Period)": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.get("Report Period", "0"),
                    "Fecha de Informe (Report Refresh Date)": RMbBQrwLNbyQavPrRUhIQFBSdDyiJITb,
                })
            NinuaiRVRRKrHYAysgOpYbRIAqrSpWXp[BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu] = {"error": None, "datos": FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh}
        else:
            NinuaiRVRRKrHYAysgOpYbRIAqrSpWXp[BPLpfAcjoluxHFUrPbDIuxMzeyauKXZu] = {"error": None, "datos": yGrmlRDlOxCLsXiferoclBMkprOdnfmY}
    if len(GLJibTTSWvWfARmnLHOsLFdeQxasLhMZ) == 1:
        return NinuaiRVRRKrHYAysgOpYbRIAqrSpWXp[GLJibTTSWvWfARmnLHOsLFdeQxasLhMZ[0]]
    else:
        return NinuaiRVRRKrHYAysgOpYbRIAqrSpWXp
async def niMVyjGwXXGoBOFVETIWFMlLrFwhZCsD():
    try:
        TnaZVUzPTdzELnEdLgsGdSsdvvhgLdcm = await obtener_sitios_sharepoint()
        FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh = []
        for lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP in TnaZVUzPTdzELnEdLgsGdSsdvvhgLdcm:
            pfVQRWmSvKPziGtQjHNVuvfybByoursW = lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("id", "").split(",")
            LKeyJtvzzbdVqIqVmcBKfPImwqamnVic = pfVQRWmSvKPziGtQjHNVuvfybByoursW[1] if len(pfVQRWmSvKPziGtQjHNVuvfybByoursW) >= 2 else "N/A"
            FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh.append({
                "Fecha de creación": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("createdDateTime", "N/A"),
                "ID del sitio (Site Id)": LKeyJtvzzbdVqIqVmcBKfPImwqamnVic,
                "URL del sitio (Site URL)": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("webUrl", "N/A"),
                "Nombre del sitio": lKxuAfBBYtEEHCDhKSuSoeKPcCDHhYzP.get("displayName", "N/A"),
            })
        return {"error": None, "datos": FgdhypnZBIdtiIwScYRDrgoXSqXOqxQh}
    except Exception as NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy:
        return {"error": str(NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy), "datos": None}
def XVxKPGFKSymGlhWnUUHTLqUnhTXRoAAF():
    try:
        gZKIVkJsVZzWCZonBKaCQjGwIgFRUZoW = Licencia.query.order_by(Licencia.LicenciaPrincipal.desc(), Licencia.NombreLicencia.asc()).all()
        vmguZQqjpjnazXuvHhwIwuUMNhmjRzMD = [{"id": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.id, "LicenciaSkuId": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.LicenciaSkuId, "NombreLicencia": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.NombreLicencia, "LicenciaPrincipal": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.LicenciaPrincipal, "LicenciaDePago": IPohplcztfcTlFhPZBaDVBYzSDsNZXGt.LicenciaDePago} for IPohplcztfcTlFhPZBaDVBYzSDsNZXGt in gZKIVkJsVZzWCZonBKaCQjGwIgFRUZoW]
        return {"licencias": vmguZQqjpjnazXuvHhwIwuUMNhmjRzMD, "status": 200}
    except Exception as NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy:
        return {"error": str(NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy), "status": 500}
def kwtcdTJOrrqPnXndBlboJiEYvSMBAHRH(data):
    try:
        if not data.get("LicenciaSkuId"): return {"error": "El SKU ID es requerido", "status": 400}
        if not data.get("NombreLicencia"): return {"error": "El nombre comercial es requerido", "status": 400}
        if data.get("LicenciaPrincipal") and not data.get("LicenciaDePago"): return {"error": "Las licencias principales deben ser de pago", "status": 400}
        if Licencia.query.filter_by(LicenciaSkuId=data.get("LicenciaSkuId")).first(): return {"error": "La licencia ya existe", "status": 409}
        nVfWXLexLELLBKymzBuPQACweWubdoGg = Licencia(LicenciaSkuId=data["LicenciaSkuId"], NombreLicencia=data["NombreLicencia"], LicenciaPrincipal=bool(data.get("LicenciaPrincipal", False)), LicenciaDePago=bool(data.get("LicenciaDePago", False)))
        db.session.add(nVfWXLexLELLBKymzBuPQACweWubdoGg)
        db.session.commit()
        return {"message": "Licencia creada", "status": 201, "licencia": {"id": nVfWXLexLELLBKymzBuPQACweWubdoGg.id, "LicenciaSkuId": nVfWXLexLELLBKymzBuPQACweWubdoGg.LicenciaSkuId}}
    except Exception as NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy:
        db.session.rollback()
        return {"error": str(NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy), "status": 500}
def jGBTdbNUvGrcKdBJDpBlebEnUzvrBLUc(licencia_id, data):
    try:
        if not data.get("NombreLicencia"): return {"error": "El nombre comercial es requerido", "status": 400}
        if data.get("LicenciaPrincipal") and not data.get("LicenciaDePago"): return {"error": "Las licencias principales deben ser de pago", "status": 400}
        UyMcHgXMFXvckFNoEcBySePFBGlawNPJ = Licencia.query.filter_by(LicenciaSkuId=licencia_id).first()
        if not UyMcHgXMFXvckFNoEcBySePFBGlawNPJ: return {"error": "Licencia no encontrada", "status": 404}
        UyMcHgXMFXvckFNoEcBySePFBGlawNPJ.NombreLicencia = data["NombreLicencia"]
        UyMcHgXMFXvckFNoEcBySePFBGlawNPJ.LicenciaPrincipal = bool(data.get("LicenciaPrincipal", False))
        UyMcHgXMFXvckFNoEcBySePFBGlawNPJ.LicenciaDePago = bool(data.get("LicenciaDePago", False))
        db.session.commit()
        return {"message": "Licencia actualizada", "status": 200}
    except Exception as NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy:
        db.session.rollback()
        return {"error": str(NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy), "status": 500}
def oTaiILpfJnixcKnuFnxOlyYNdqOBlcOU(licencia_id):
    try:
        UyMcHgXMFXvckFNoEcBySePFBGlawNPJ = Licencia.query.filter_by(LicenciaSkuId=licencia_id).first()
        if not UyMcHgXMFXvckFNoEcBySePFBGlawNPJ: return {"error": "Licencia no encontrada", "status": 404}
        db.session.delete(UyMcHgXMFXvckFNoEcBySePFBGlawNPJ)
        db.session.commit()
        return {"message": "Licencia eliminada", "status": 200}
    except Exception as NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy:
        db.session.rollback()
        return {"error": str(NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy), "status": 500}
def EjdiUwOcnuoUMUEZtwakAsRIcloraMlb(user_id_sesion, correo_sesion):
    if not user_id_sesion or not correo_sesion:
        return {"error": "No hay usuario consultado en sesión", "status": 400}
    try:
        YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd = asyncio.run(eMoDGEBToAFtxgBFaOVPgFBsOmfEpFGh(correo_sesion))
        if user_id_sesion != YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("userId"):
            return {"error": "La identidad del usuario no coincide", "status": 403}
        RIbAFAqUzIXVPEsvYJfnuOGcOAazndKn = Usuario(
            djsjlXpfJjIJBvYSvLDfHeJIstoRKEso=correo_sesion,
            hCbGIyvgOLPeRWbPIhrHiKtiDdzPDWzJ=YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("nombreCompleto", "Desconocido"),
            oUjVFTywbfHKQxPCsTmZFYNeUKHLPWaH=YlWFeNOVmVAPSJimRxrzvHKfOUGEwXMd.get("userId"),
            okROKnvueOqonidfHalWVlZvQiPzYXgc='microsoft',
            xckdHCWaktmxrtTXBsjbigvqvWSvUDBW="Activo"
        )
        db.session.add(RIbAFAqUzIXVPEsvYJfnuOGcOAazndKn)
        db.session.commit()
        return {"success": "Acceso autorizado correctamente", "status": 200}
    except IntegrityError:
        db.session.rollback()
        return {"error": "El usuario ya ha sido autorizado previamente", "status": 409}
    except Exception as NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy:
        db.session.rollback()
        return {"error": f"Error al autorizar: {str(e)}", "status": 500}
def DoFKRkgfoWsRJNghBAkHnfQiQEWFUrre():
    try:
        lFgFMdzlRcWBEFhzkYTIzdyzbKkEVXCm = Usuario.query.filter_by(okROKnvueOqonidfHalWVlZvQiPzYXgc='microsoft').order_by(Usuario.fecha_creacion.desc()).all()
        return [
            {
                "fecha_autorizacion": pgZUeiswXHIPVnTnrumBSneEXGOlBQxZ.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": pgZUeiswXHIPVnTnrumBSneEXGOlBQxZ.hCbGIyvgOLPeRWbPIhrHiKtiDdzPDWzJ,
                "correo": pgZUeiswXHIPVnTnrumBSneEXGOlBQxZ.djsjlXpfJjIJBvYSvLDfHeJIstoRKEso,
                "estado": pgZUeiswXHIPVnTnrumBSneEXGOlBQxZ.xckdHCWaktmxrtTXBsjbigvqvWSvUDBW
            } for pgZUeiswXHIPVnTnrumBSneEXGOlBQxZ in lFgFMdzlRcWBEFhzkYTIzdyzbKkEVXCm
        ]
    except Exception as NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy:
        return {"error": str(NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy), "status": 500}
def IYXfsIYSnrBnMveUuMdNOoUncpYaOkpc(data):
    try:
        krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm = data.get("correo")
        if not krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm:
            return {"error": "Correo no proporcionado", "status": 400}
        djsjlXpfJjIJBvYSvLDfHeJIstoRKEso = Usuario.query.filter_by(djsjlXpfJjIJBvYSvLDfHeJIstoRKEso=krbIlIDgJAWmAPaFFYAdAdDfDfYyWnzm, okROKnvueOqonidfHalWVlZvQiPzYXgc='microsoft').first()
        if not djsjlXpfJjIJBvYSvLDfHeJIstoRKEso:
            return {"error": "Usuario no encontrado", "status": 404}
        djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.xckdHCWaktmxrtTXBsjbigvqvWSvUDBW = "Inactivo" if djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.xckdHCWaktmxrtTXBsjbigvqvWSvUDBW == "Activo" else "Activo"
        db.session.commit()
        return {"success": True, "nuevo_estado": djsjlXpfJjIJBvYSvLDfHeJIstoRKEso.xckdHCWaktmxrtTXBsjbigvqvWSvUDBW}
    except Exception as NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy:
        db.session.rollback()
        return {"error": str(NiGMXAsTZVAkzQWclWCJsjvUEGZSFocy), "status": 500}