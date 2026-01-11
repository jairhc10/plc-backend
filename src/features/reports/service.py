from typing import Optional, List, Dict, Any
from datetime import date
from .repository import ReporteHornosRepository

class ReporteHornosService:
    def __init__(self, repository: ReporteHornosRepository):
        self.repository = repository
    
    def generar_reporte(
        self,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None,
        numero_ot: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Genera el reporte de hornos con validación
        """
        # Convertir strings a dates si es necesario
        fecha_desde_obj = date.fromisoformat(fecha_desde) if fecha_desde else None
        fecha_hasta_obj = date.fromisoformat(fecha_hasta) if fecha_hasta else None
        
        # Obtener datos
        datos = self.repository.obtener_reporte_hornos(
            fecha_desde=fecha_desde_obj,
            fecha_hasta=fecha_hasta_obj,
            numero_ot=numero_ot
        )
        
        return {
            "success": True,
            "total": len(datos),
            "data": datos
        }