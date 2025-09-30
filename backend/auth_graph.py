import os
import requests
from dotenv import load_dotenv
load_dotenv()
def xYDxZUHFiRqKVpDvgPnJVVQyCMXACjux():
    oTsgAwPGeIuQgEOKSVQAFMaOzwbDuGYQ = os.getenv("AZURE_TENANT_ID")
    HRSDRAeSYVHeEtBqNYDyFPitrRKAkdxQ = os.getenv("AZURE_CLIENT_ID")
    nVHHzfeBZacOVUYsxYKxdQMyDAnmlZKi = os.getenv("AZURE_CLIENT_SECRET")
    if not all([oTsgAwPGeIuQgEOKSVQAFMaOzwbDuGYQ, HRSDRAeSYVHeEtBqNYDyFPitrRKAkdxQ, nVHHzfeBZacOVUYsxYKxdQMyDAnmlZKi]):
        return None
    SadxfGpkofDENAfiCKSTBQpDKmtiVkAk = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    IFuOXwXTZVWNBQbrWBLNgKFbhthBisDA = {
        'client_id': HRSDRAeSYVHeEtBqNYDyFPitrRKAkdxQ,
        'client_secret': nVHHzfeBZacOVUYsxYKxdQMyDAnmlZKi,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    }
    SjhzhjVZiXwbovWzsugsXmscGuRbLVkq = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        NUlPWmVuBigHZqvbDdxElymZVzoNNUce = requests.post(SadxfGpkofDENAfiCKSTBQpDKmtiVkAk, data=IFuOXwXTZVWNBQbrWBLNgKFbhthBisDA, SjhzhjVZiXwbovWzsugsXmscGuRbLVkq=SjhzhjVZiXwbovWzsugsXmscGuRbLVkq, verify=False)
        NUlPWmVuBigHZqvbDdxElymZVzoNNUce.raise_for_status() 
        gfcoLijwXODlrKsJeXxoPpOLRFsLXKjU = NUlPWmVuBigHZqvbDdxElymZVzoNNUce.json()
        return gfcoLijwXODlrKsJeXxoPpOLRFsLXKjU.get("access_token")
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP obteniendo el token: {http_err} - {response.text}")
    except Exception as oHgZmFxabIvkzLKcEkAnysDIsyyXdsyD:
        print(f"Ocurrió un error inesperado al obtener el token: {e}")
    return None