"""
Configuración principal de Flask
Factory pattern para crear la app
"""
from flask import Flask
from flask_cors import CORS
from config.settings import settings
from core.database.connection import db
from flask_jwt_extended import JWTManager
from api.middlewares.error_handle import register_error_handlers
from api.auth.auth_routes import auth_bp

# Importar blueprints
from features.tables.router import tables_bp
from features.reports.router import reportes_bp

def create_app() -> Flask:
    """
    Factory para crear y configurar la aplicación Flask
    
    Returns:
        Flask: Aplicación configurada y lista para usar
    """
    # Crear aplicación
    app = Flask(__name__)
    
    # Configurar CORS
    CORS(app, origins=settings.CORS_ORIGINS)
    
    #JWT
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    jwt = JWTManager(app)
    
    # Inicializar base de datos
    db.initialize(echo=settings.FLASK_DEBUG)
    
    # Registrar manejadores de error
    register_error_handlers(app)
    
    # Registrar blueprints (módulos)
    app.register_blueprint(tables_bp)
    
    app.register_blueprint(reportes_bp)
    
    #AUTH
    app.register_blueprint(auth_bp)
    
    # ==========================================
    # RUTAS RAÍZ
    # ==========================================
    
    @app.route('/')
    def home():
        """Ruta raíz - Información de la API"""
        return {
            "name": "Backend Flask - DB Automatización Hornos",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "health": "/health",
                "tables": {
                    "list": "/api/tables/",
                    "info": "/api/tables/{table_name}",
                    "data": "/api/tables/{table_name}/data"
                }
            }
        }
    
    @app.route('/health')
    def health():
        """Health check - Verificar estado de la app y BD"""
        db_status = db.test_connection()
        
        return {
            "status": "healthy" if db_status["success"] else "unhealthy",
            "database": db_status,
            "flask": {
                "debug": settings.FLASK_DEBUG,
                "environment": settings.FLASK_ENV
            }
        }
    
    return app