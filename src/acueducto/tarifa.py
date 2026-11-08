"""Cálculo del valor de la factura de agua."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Tarifa:
    cargo_fijo: int = 8500
    limite_basico: int = 20
    precio_basico: int = 1200
    precio_complementario: int = 2400


TARIFA_ILUSTRATIVA = Tarifa()


def calcular_valor_factura(consumo_m3: int, tarifa: Tarifa = TARIFA_ILUSTRATIVA) -> int:
    if not isinstance(consumo_m3, int) or isinstance(consumo_m3, bool):
        raise TypeError("El consumo debe ser un número entero de m³")
    if consumo_m3 < 0:
        raise ValueError("El consumo no puede ser negativo")

    if consumo_m3 <= tarifa.limite_basico:
        return tarifa.cargo_fijo + consumo_m3 * tarifa.precio_basico

    exceso = consumo_m3 - tarifa.limite_basico
    return (
        tarifa.cargo_fijo
        + tarifa.limite_basico * tarifa.precio_basico
        + exceso * tarifa.precio_complementario
    )
