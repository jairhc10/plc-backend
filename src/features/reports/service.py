from typing import Optional, Dict, Any
from datetime import date
import math
from .repository import ReporteHornosRepository

class ReporteHornosService:
    def __init__(self, repository: ReporteHornosRepository):
        self.repository = repository

    def generar_reporte(
        self,
        fecha_desde: Optional[str] = None,
        fecha_hasta: Optional[str] = None,
        numero_ot: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None
    ) -> Dict[str, Any]:
        # Convertir strings a dates si es necesario
        fecha_desde_obj = date.fromisoformat(fecha_desde) if fecha_desde else None
        fecha_hasta_obj = date.fromisoformat(fecha_hasta) if fecha_hasta else None

        # Normalizar numero_ot
        if numero_ot is not None:
            numero_ot = numero_ot.strip()
            if numero_ot == "":
                numero_ot = None

        # Si viene page/size => paginado
        if page is not None or size is not None:
            page = int(page or 1)
            size = int(size or 10)

            data, total = self.repository.obtener_reporte_hornos_paginado(
                fecha_desde=fecha_desde_obj,
                fecha_hasta=fecha_hasta_obj,
                numero_ot=numero_ot,
                page=page,
                size=size
            )

            pages = max(1, math.ceil(total / max(1, size)))

            return {
                "success": True,
                "data": data,
                "page": page,
                "size": size,
                "total": total,
                "pages": pages
            }

        # Si NO viene page/size => modo antiguo (para Excel u otros)
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
