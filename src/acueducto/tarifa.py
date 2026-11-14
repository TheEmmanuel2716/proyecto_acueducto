"""Cálculo del valor de la factura de agua."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Tarifa:
    """Rangos y precios de la tarifa, en pesos.

    Los valores por defecto son ilustrativos (P-01).
    """

    cargo_fijo: int = 8500
    limite_basico: int = 20  # m³ que se cobran a precio básico
    precio_basico: int = 1200  # pesos por m³ hasta el límite
    precio_complementario: int = 2400  # pesos por m³ por encima del límite


TARIFA_ILUSTRATIVA = Tarifa()


def _validar_consumo(consumo_m3: int) -> None:
    """Rechaza consumos que no son enteros (TypeError) o son negativos (ValueError)."""
    if not isinstance(consumo_m3, int) or isinstance(consumo_m3, bool):
        raise TypeError("El consumo debe ser un número entero de m³")
    if consumo_m3 < 0:
        raise ValueError("El consumo no puede ser negativo")


def _dividir_consumo(consumo_m3: int, limite_basico: int) -> tuple[int, int]:
    """Reparte el consumo en (m³ básicos, m³ complementarios)."""
    m3_basicos = min(consumo_m3, limite_basico)
    m3_complementarios = max(0, consumo_m3 - limite_basico)
    return m3_basicos, m3_complementarios


def calcular_valor_factura(
    consumo_m3: int, tarifa: Tarifa = TARIFA_ILUSTRATIVA
) -> int:
    """Devuelve la factura en pesos: cargo fijo + básico + complementario."""
    _validar_consumo(consumo_m3)
    m3_basicos, m3_complementarios = _dividir_consumo(
        consumo_m3, tarifa.limite_basico
    )
    return (
        tarifa.cargo_fijo
        + m3_basicos * tarifa.precio_basico
        + m3_complementarios * tarifa.precio_complementario
    )
