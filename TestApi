# ---------------------------------------------------------------------------
# 1. IMPORTACIONES Y CONFIGURACIÓN
# ---------------------------------------------------------------------------
import os
import time
import io
import csv
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

load_dotenv()

token_cache = {}


# ---------------------------------------------------------------------------
# 2. AUTENTICACIÓN
# ---------------------------------------------------------------------------
async def obtener_token() -> str:
    current_time = time.time()

    if "access_token" in token_cache and token_cache.get("expires_on", 0) > current_time:
        return token_cache["access_token"]

    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        raise HTTPException(
            status_code=500,
            detail="Faltan credenciales de servidor para la autenticación.",
        )

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(token_url, data=payload, headers=headers, timeout=30.0)
            response.raise_for_status()

        token_data = response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=500, detail="La respuesta no contenía access_token.")

        expires_in = token_data.get("expires_in", 3600)
        token_cache["access_token"] = access_token
        token_cache["expires_on"] = current_time + expires_in - 300
        return access_token

    except httpx.HTTPStatusError as http_err:
        raise HTTPException(
            status_code=http_err.response.status_code,
            detail=f"Error de autenticación con Microsoft: {http_err.response.text}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado en el servidor: {e}")


# ---------------------------------------------------------------------------
# 3. LÓGICA DE NEGOCIO
# ---------------------------------------------------------------------------
GRAPH_API_USERS_ENDPOINT = (
    "https://graph.microsoft.com/v1.0/users?"
    "$filter=userType eq 'Member'"
    "&$top=999"
    "&$select=id,displayName,mail,userPrincipalName,assignedLicenses,"
    "jobTitle,officeLocation,accountEnabled,createdDateTime"
)
GRAPH_API_USERS_ACTIVITY_ENDPOINT = (
    "https://graph.microsoft.com/v1.0/users?"
    "$filter=userType eq 'Member'"
    "&$top=999"
    "&$select=id,signInActivity"
)
GRAPH_API_USUARIO_POR_CORREO_ENDPOINT = (
    "https://graph.microsoft.com/v1.0/users/{correo}?"
    "$select=id,displayName,mail,userPrincipalName,assignedLicenses,"
    "jobTitle,officeLocation,accountEnabled,createdDateTime,department"
)
GRAPH_API_MANAGER_USUARIO_ENDPOINT = "https://graph.microsoft.com/v1.0/users/{correo}/manager"
GRAPH_API_SITES_SEARCH_ENDPOINT = "https://graph.microsoft.com/v1.0/sites?search=*"
GRAPH_API_LICENSES_ENDPOINT = "https://graph.microsoft.com/v1.0/subscribedSkus"

BASE_REPORT_ENDPOINTS = {
    "outlook_actividad": "https://graph.microsoft.com/v1.0/reports/getEmailActivityUserDetail(period='{}')",
    "buzon_uso": "https://graph.microsoft.com/v1.0/reports/getMailboxUsageDetail(period='{}')",
    "onedrive_actividad": "https://graph.microsoft.com/v1.0/reports/getOneDriveActivityUserDetail(period='{}')",
    "onedrive_uso": "https://graph.microsoft.com/v1.0/reports/getOneDriveUsageAccountDetail(period='{}')",
    "sharepoint_actividad": "https://graph.microsoft.com/v1.0/reports/getSharePointActivityUserDetail(period='{}')",
    "sharepoint_uso": "https://graph.microsoft.com/v1.0/reports/getSharePointSiteUsageDetail(period='{}')",
    "teams_actividad": "https://graph.microsoft.com/v1.0/reports/getTeamsUserActivityUserDetail(period='{}')",
    "teams_dispositivos": "https://graph.microsoft.com/v1.0/reports/getTeamsDeviceUsageUserDetail(period='{}')",
}


class UserNotFoundError(Exception):
    pass


async def obtener_datos_graph(endpoint: str, client: httpx.AsyncClient | None = None) -> dict:
    token = await obtener_token()
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    async def _request(c: httpx.AsyncClient) -> dict:
        resp = await c.get(endpoint, headers=headers, timeout=30.0)
        resp.raise_for_status()
        return resp.json()

    if client is not None:
        return await _request(client)

    async with httpx.AsyncClient(verify=False) as new_client:
        return await _request(new_client)


async def obtener_paginas_completas(endpoint: str) -> list[dict]:
    all_items: list[dict] = []
    next_url = endpoint

    async with httpx.AsyncClient(verify=False) as client:
        while next_url:
            try:
                response = await obtener_datos_graph(next_url, client)
                if "value" in response:
                    all_items.extend(response["value"])
                next_url = response.get("@odata.nextLink")
            except Exception:
                break

    return all_items


async def obtener_usuarios_miembros() -> list[dict]:
    return await obtener_paginas_completas(GRAPH_API_USERS_ENDPOINT)


async def obtener_usuarios_con_actividad() -> list[dict]:
    return await obtener_paginas_completas(GRAPH_API_USERS_ACTIVITY_ENDPOINT)


async def obtener_licencias_disponibles() -> list[dict]:
    response = await obtener_datos_graph(GRAPH_API_LICENSES_ENDPOINT)
    return response.get("value", [])


async def obtener_informe_actividad(servicio: str, dias: int):
    url = BASE_REPORT_ENDPOINTS.get(servicio)
    if not url:
        raise ValueError("Servicio no válido")

    token = await obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(
            url.format(f"D{dias}"),
            headers=headers,
            timeout=60.0,
            follow_redirects=True,
        )
        resp.raise_for_status()

    csv_text = resp.text
    try:
        csv_reader = csv.DictReader(io.StringIO(csv_text))
        return [row for row in csv_reader]
    except Exception:
        return {"message": "Informe recibido pero no se pudo procesar el CSV.", "content": csv_text}


async def obtener_sitios_sharepoint() -> list[dict]:
    return await obtener_paginas_completas(GRAPH_API_SITES_SEARCH_ENDPOINT)


async def obtener_usuario_por_correo(correo: str) -> dict:
    endpoint_usuario = GRAPH_API_USUARIO_POR_CORREO_ENDPOINT.format(correo=correo)

    try:
        usuario = await obtener_datos_graph(endpoint_usuario)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise UserNotFoundError(f"Usuario con correo {correo} no encontrado.")
        raise

    endpoint_manager = GRAPH_API_MANAGER_USUARIO_ENDPOINT.format(correo=correo)
    try:
        jefe = await obtener_datos_graph(endpoint_manager)
        usuario["manager"] = jefe
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            usuario["manager"] = None
        else:
            usuario["manager"] = {"error": str(e)}

    return usuario


# ---------------------------------------------------------------------------
# 4. DEFINICIÓN DE LA API
# ---------------------------------------------------------------------------
app = FastAPI(
    title="API de Consultas a Microsoft Graph",
    description="Una API para centralizar y exponer consultas comunes a la API de Microsoft Graph.",
    version="1.1.0",
)


class ServicioInforme(str, Enum):
    outlook_actividad = "outlook_actividad"
    buzon_uso = "buzon_uso"
    onedrive_actividad = "onedrive_actividad"
    onedrive_uso = "onedrive_uso"
    sharepoint_actividad = "sharepoint_actividad"
    sharepoint_uso = "sharepoint_uso"
    teams_actividad = "teams_actividad"
    teams_dispositivos = "teams_dispositivos"


@app.get("/", tags=["General"])
async def root():
    return {"message": "Bienvenido a la API de Microsoft Graph. Visita /docs para ver los endpoints disponibles."}


@app.get("/usuarios/miembros", tags=["Usuarios"])
async def get_usuarios_miembros():
    try:
        usuarios = await obtener_usuarios_miembros()
        return JSONResponse(content=usuarios)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/usuarios/actividad", tags=["Usuarios"])
async def get_usuarios_actividad():
    try:
        actividad_usuarios = await obtener_usuarios_con_actividad()
        return JSONResponse(content=actividad_usuarios)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/usuarios/por-correo/{correo}", tags=["Usuarios"])
async def get_usuario_por_correo(correo: str):
    try:
        usuario = await obtener_usuario_por_correo(correo)
        return JSONResponse(content=usuario)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/licencias", tags=["Licencias y Facturación"])
async def get_licencias_disponibles():
    try:
        licencias = await obtener_licencias_disponibles()
        return JSONResponse(content=licencias)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sharepoint/sitios", tags=["SharePoint"])
async def get_sitios_sharepoint():
    try:
        sitios = await obtener_sitios_sharepoint()
        return JSONResponse(content=sitios)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/informes/{servicio_informe}", tags=["Informes"])
async def get_informe_actividad(
    servicio_informe: ServicioInforme,
    dias: int = Query(7, ge=1, le=180, description="Período del informe en días (1, 7, 30, 90, 180)"),
):
    try:
        informe = await obtener_informe_actividad(servicio_informe.value, dias)
        return JSONResponse(content=informe)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# 5. EJECUCIÓN DE LA API
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
