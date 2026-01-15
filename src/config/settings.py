#CONFIGURACION GENERAL
"""
Configuración general de la aplicación
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Settings:
    """Configuración centralizada de la aplicación"""
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Base de datos
    DB_SERVER = os.getenv('DB_SERVER')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    #AUTH
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'clave-jwt-secreta-cambiar-en-produccion')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=3)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    #SEGURIDAD
    SECRET_KEY =  os.getenv('SECRET_KEY', 'clave-secreta-cambiar')
    
    @classmethod
    def validate(cls):
        """Validar que las configuraciones obligatorias existan"""
        required = ['DB_SERVER', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(
                f"Faltan configuraciones obligatorias en .env: {', '.join(missing)}"
            )
        
        print("Configuración validada correctamente")

# Instancia global
settings = Settings()