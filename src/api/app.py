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
from features.tables.router import tables_bp
from features.reports.router import reportes_bp
import socket

def create_app() -> Flask:
    """
    Factory para crear y configurar la aplicación Flask
    
    Returns:
        Flask: Aplicación configurada y lista para usar
    """
    app = Flask(__name__)
    
    # Configurar CORS
    CORS(app, origins=settings.CORS_ORIGINS)
    
    # JWT
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    jwt = JWTManager(app)
    
    # Inicializar base de datos
    db.initialize(echo=settings.FLASK_DEBUG)
    
    # Registrar manejadores de error
    register_error_handlers(app)
    
    # Registrar blueprints (módulos)
    app.register_blueprint(tables_bp)
    app.register_blueprint(reportes_bp)
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
            "status": "running"
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
    
    @app.route('/test-db')
    def test_db():
        """Probar consulta real a la base de datos"""
        from sqlalchemy import text
        try:
            with db.get_connection() as conn:
                # Probar consulta a tabla de usuarios
                result = conn.execute(text("SELECT COUNT(*) as total FROM TBL_USUARIO")).fetchone()
                total_usuarios = result[0]
                
                # Probar consulta específica del login
                result_user = conn.execute(text("""
                    SELECT ID_USUARIO, NOMBRE_USUARIO, USUARIO 
                    FROM TBL_USUARIO 
                    WHERE USUARIO = 'JSO' AND ESTADO = 1
                """)).fetchone()
                
                return {
                    "success": True,
                    "message": "Conexión a BD exitosa",
                    "total_usuarios": total_usuarios,
                    "usuario_jso_existe": result_user is not None,
                    "datos_usuario": {
                        "id": result_user[0] if result_user else None,
                        "nombre": result_user[1] if result_user else None,
                        "usuario": result_user[2] if result_user else None
                    } if result_user else None
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error al conectar a la base de datos"
            }, 500
    
    return app

# ==========================================
# ⭐ ESTO DEBE ESTAR FUERA DE create_app()
# ==========================================
# if __name__ == '__main__':
#     app = create_app()
    
#     hostname = socket.gethostname()
#     local_ip = socket.gethostbyname(hostname)
    
#     print("\n" + "="*70)
#     print("🔥 BACKEND FLASK - SISTEMA MODEPSA")
#     print("="*70)
#     print(f"🌐 Local:    http://localhost:5000")
#     print(f"🌐 Red:      http://{local_ip}:5000")
#     print(f"🔍 Health:   http://{local_ip}:5000/health")
#     print(f"🧪 Test DB:  http://{local_ip}:5000/test-db")
#     print("="*70)
#     print("✅ Presiona Ctrl+C para detener\n")
    
#     app.run(
#         host='0.0.0.0',
#         port=5000,
#         debug=True,
#         threaded=True
#     )