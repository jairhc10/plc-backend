#CONFIGURACION DE LA DB
"""
Configuración de la cadena de conexión a SQL Server
"""
import urllib.parse
from config.settings import settings

def get_database_url() -> str:
    """
    Construir la URL de conexión a SQL Server
    
    Returns:
        str: Cadena de conexión SQLAlchemy
    """
    params = urllib.parse.quote_plus(
        f"DRIVER={{{settings.DB_DRIVER}}};"
        f"SERVER={settings.DB_SERVER};"
        f"DATABASE={settings.DB_NAME};"
        f"UID={settings.DB_USER};"
        f"PWD={settings.DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    
    database_url = f"mssql+pyodbc:///?odbc_connect={params}"
    
    print(f"Conectando a: {settings.DB_SERVER}/{settings.DB_NAME}")
    
    return database_url