"""
Validadores de datos y seguridad SQL
"""
import re
from core.exceptions.custom_exceptions import ValidationException

class SQLValidator:
    """Validaciones de seguridad para SQL"""
    
    # Palabras peligrosas en SQL (para evitar inyección)
    DANGEROUS_KEYWORDS = [
        'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE',
        'INSERT', 'UPDATE', 'EXEC', 'EXECUTE', 'GRANT',
        'REVOKE', 'SHUTDOWN', 'BACKUP', 'RESTORE'
    ]
    
    @staticmethod
    def validate_table_name(table_name: str) -> str:
        """
        Valida que el nombre de tabla sea seguro
        
        Args:
            table_name: Nombre de la tabla
            
        Returns:
            str: Nombre validado
            
        Raises:
            ValidationException: Si el nombre no es válido
        """
        if not table_name:
            raise ValidationException("El nombre de tabla no puede estar vacío")
        
        # Solo permitir letras, números y guiones bajos
        if not re.match(r'^[a-zA-Z0-9_]+$', table_name):
            raise ValidationException(
                "El nombre de tabla solo puede contener letras, números y guiones bajos"
            )
        
        return table_name