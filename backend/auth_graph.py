import os
import requests
from dotenv import load_dotenv

load_dotenv()

def obtener_token():
    
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        return None

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    try:
        response = requests.post(token_url, data=payload, headers=headers, verify=False)
        response.raise_for_status() 
        
        token_data = response.json()
        return token_data.get("access_token")
        
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP obteniendo el token: {http_err} - {response.text}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al obtener el token: {e}")
    
    return None