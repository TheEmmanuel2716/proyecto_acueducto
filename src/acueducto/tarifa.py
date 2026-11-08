"""Cálculo del valor de la factura de agua (esqueleto: aún sin implementar)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Tarifa:
    cargo_fijo: int = 8500
    limite_basico: int = 20
    precio_basico: int = 1200
    precio_complementario: int = 2400


TARIFA_ILUSTRATIVA = Tarifa()


def calcular_valor_factura(consumo_m3: int, tarifa: Tarifa = TARIFA_ILUSTRATIVA) -> int:
    raise NotImplementedError
