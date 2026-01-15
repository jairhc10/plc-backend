from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth_service import auth_service


auth_bp = Blueprint('auth', __name__, url_prefix = '/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'USUARIO' not in data or 'CLAVE' not in data:
        return jsonify({
            "error": "Se requiere usuario y clave"
        }), 400
    return auth_service.login(data['USUARIO'], data['CLAVE'])

@auth_bp.route('/verificar', methods=['GET'])
@jwt_required()
def verificar():
    user_id = get_jwt_identity()
    valido, user_data =  auth_service.verificar_token(user_id)
    if not valido:
        return jsonify({
            "error": "Token invalido o usuario no existe"
        }), 401
    return jsonify({
        "success": True,
        "message": "Token válido",
        "user": user_data
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
     return jsonify({
        "success": True,
        "message": "Sesión cerrada"
    }), 200