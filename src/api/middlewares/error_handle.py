"""
Manejador global de errores HTTP
"""
from flask import Flask
from core.exceptions.custom_exceptions import AppException
from shared.responses.response_builder import ResponseBuilder

def register_error_handlers(app: Flask):
    """Registrar manejadores de error en la app"""
    
    @app.errorhandler(AppException)
    def handle_app_exception(error: AppException):
        """Manejar excepciones personalizadas de la app"""
        return ResponseBuilder.error(error.message, error.status_code)
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Manejar error 404 - Ruta no encontrada"""
        return ResponseBuilder.error("Endpoint no encontrado", 404)
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Manejar error 500 - Error interno del servidor"""
        return ResponseBuilder.error("Error interno del servidor", 500)