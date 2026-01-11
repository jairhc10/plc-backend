"""
Constructor de respuestas HTTP estandarizadas
"""
from typing import Any, Optional
from flask import jsonify

class ResponseBuilder:
    """Construye respuestas JSON con formato consistente"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operación exitosa",
        meta: Optional[dict] = None
    ) -> tuple:
        """
        Construir respuesta exitosa
        
        Args:
            data: Datos de respuesta
            message: Mensaje descriptivo
            meta: Metadatos adicionales (paginación, totales, etc.)
            
        Returns:
            tuple: (response_json, status_code)
        """
        response = {
            "status": "success",
            "message": message
        }
        
        if data is not None:
            response["data"] = data
        
        if meta:
            response["meta"] = meta
        
        return jsonify(response), 200
    
    @staticmethod
    def error(
        message: str,
        status_code: int = 500,
        errors: Optional[dict] = None
    ) -> tuple:
        """
        Construir respuesta de error
        
        Args:
            message: Mensaje de error
            status_code: Código HTTP (400, 404, 500, etc.)
            errors: Detalles adicionales del error
            
        Returns:
            tuple: (response_json, status_code)
        """
        response = {
            "status": "error",
            "message": message
        }
        
        if errors:
            response["errors"] = errors
        
        return jsonify(response), status_code