"""
Convertidor de datos de SQL a tipos serializables en JSON
"""
from typing import Any, List
from datetime import datetime, date
from decimal import Decimal

class DataConverter:
    """Convierte tipos de datos de SQL a tipos compatibles con JSON"""
    
    @staticmethod
    def convert_value(value: Any) -> Any:
        """
        Convierte un valor individual a un tipo serializable
        
        Args:
            value: Valor a convertir
            
        Returns:
            Valor convertido y serializable
        """
        if value is None:
            return None
        
        # Fechas y horas
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        
        # Decimales y números
        if isinstance(value, Decimal):
            return float(value)
        
        # Bytes (binarios)
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8')
            except:
                return f"<binary data: {len(value)} bytes>"
        
        # UUID
        if hasattr(value, 'hex'):
            return str(value)
        
        return value
    
    @staticmethod
    def row_to_dict(row, columns: List[str]) -> dict:
        """
        Convierte una fila de resultados a diccionario
        
        Args:
            row: Fila de resultados SQL
            columns: Lista de nombres de columnas
            
        Returns:
            dict: Diccionario con los datos convertidos
        """
        result = {}
        for i, column in enumerate(columns):
            result[column] = DataConverter.convert_value(row[i])
        return result
    
    @staticmethod
    def rows_to_dict_list(rows, columns: List[str]) -> List[dict]:
        """
        Convierte múltiples filas a lista de diccionarios
        
        Args:
            rows: Filas de resultados SQL
            columns: Lista de nombres de columnas
            
        Returns:
            List[dict]: Lista de diccionarios
        """
        return [DataConverter.row_to_dict(row, columns) for row in rows]