"""
SERVICIO DE AUTH USANDO TABLA USUARIOS
"""
from flask_jwt_extended import create_access_token
from core.database.connection import db
from sqlalchemy import text

class AuthService:
    @staticmethod
    def login(usuario, clave):
        try:
            query = text("""
            SELECT ID_USUARIO, NOMBRE_USUARIO, USUARIO, CLAVE, DNI, ESTADO
            FROM TBL_USUARIO
            WHERE USUARIO = :usuario AND CLAVE = :clave AND ESTADO = 1
            """)
            
            # Usar el context manager de tu DatabaseConnection
            with db.get_connection() as conn:
                result = conn.execute(query, {
                    'usuario': usuario,
                    'clave': clave
                }).fetchone()
            
            if not result:
                return {
                    "error": "Usuario o Contraseña incorrectas"
                }, 401
            
            # Convertir resultado a diccionario
            user_data = {
                'ID_USUARIO': result[0],
                'NOMBRE_USUARIO': result[1],
                'USUARIO': result[2],
                'CLAVE': result[3],
                'DNI': result[4],
                'ESTADO': result[5]
            }
            
            access_token = create_access_token(
                identity=user_data['ID_USUARIO'],
                additional_claims={
                    "nombre": user_data['NOMBRE_USUARIO'],
                    "usuario": user_data["USUARIO"]
                }
            )
            
            return {
                "success": True,
                "message": "Login Exitoso",
                "token": access_token,
                "user": {
                    "id": user_data['ID_USUARIO'],
                    "nombre": user_data['NOMBRE_USUARIO'],
                    "usuario": user_data['USUARIO'],
                    "dni": user_data['DNI']
                }
            }, 200
            
        except Exception as e:
            return {
                "error": f"Error en autenticación: {str(e)}"
            }, 500
    
    @staticmethod
    def verificar_token(user_id):
        try:
            query = text("""
            SELECT ID_USUARIO, NOMBRE_USUARIO, USUARIO, DNI
            FROM TBL_USUARIO
            WHERE ID_USUARIO = :user_id AND ESTADO = 1
            """)
            
            with db.get_connection() as conn:
                result = conn.execute(query, {'user_id': user_id}).fetchone()
            
            if not result:
                return False, None
            
            # Convertir a diccionario
            user_data = {
                'ID_USUARIO': result[0],
                'NOMBRE_USUARIO': result[1],
                'USUARIO': result[2],
                'DNI': result[3]
            }
            
            return True, user_data
            
        except Exception:
            return False, None

# INSTANCIA GLOBAL
auth_service = AuthService()