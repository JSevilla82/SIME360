# ─────────────────────────────────────────────────────────────
# IMPORTACIÓN DE LIBRERÍAS Y VARIABLES DE ENTORNO
# ─────────────────────────────────────────────────────────────
import os
import sys
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────
# CARGA DE VARIABLES DE ENTORNO
# ─────────────────────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────────────────────
# DIRECTORIO BASE Y CREACIÓN DE CARPETA DE BASE DE DATOS
# ─────────────────────────────────────────────────────────────
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database")
os.makedirs(db_path, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# CLASE DE CONFIGURACIÓN PARA PRODUCCIÓN
# ─────────────────────────────────────────────────────────────
class ProductionConfig:
    
    # Claves secretas y entorno
    SECRET_KEY = os.environ["SECRET_KEY"]

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(db_path, 'sime.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Autenticación Microsoft (Azure AD)
    CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
    CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]
    TENANT_ID = os.environ["AZURE_TENANT_ID"]
    REDIRECT_PATH = "/callback"
    SCOPE = ["User.Read"]
    BASE_URL = os.environ["BASE_URL"]

    # Cookies de sesión
    SESSION_COOKIE_NAME = "sime360Session__Secure"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    PREFERRED_URL_SCHEME = "https"

    # Define el tiempo de vida del token CSRF en segundos (15 minutos)
    WTF_CSRF_TIME_LIMIT = 900
    
    # Asegura que la comprobación de 'referrer' sea estricta con HTTPS en producción
    WTF_CSRF_SSL_STRICT = True

# ─────────────────────────────────────────────────────────────
# SELECCIÓN DE CONFIGURACIÓN ACTIVA
# ─────────────────────────────────────────────────────────────
app_config = ProductionConfig()