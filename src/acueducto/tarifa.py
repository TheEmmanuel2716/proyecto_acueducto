"""Cálculo del valor de la factura de agua."""
from dataclasses import dataclass, fields


def _validar_entero_no_negativo(nombre: str, valor: object) -> None:
    """Comprueba que un valor sea un entero mayor o igual que cero.

    Args:
        nombre: nombre del dato, para el mensaje de error.
        valor: dato a comprobar.

    Raises:
        TypeError: si ``valor`` no es ``int`` (los decimales y los booleanos
            se rechazan).
        ValueError: si ``valor`` es negativo.
    """
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise TypeError(f"{nombre} debe ser un número entero")
    if valor < 0:
        raise ValueError(f"{nombre} no puede ser negativo")


@dataclass(frozen=True)
class Tarifa:
    """Rangos y precios de la tarifa, en pesos.

    Los valores por defecto son ilustrativos (P-01). Todos los campos deben ser
    enteros mayores o iguales que cero; se valida al crear el objeto.

    Attributes:
        cargo_fijo: pesos que se cobran siempre, incluso con consumo cero.
        limite_basico: m³ que se cobran a precio básico.
        precio_basico: pesos por m³ hasta el límite.
        precio_complementario: pesos por m³ por encima del límite.

    Raises:
        TypeError: si algún campo no es entero.
        ValueError: si algún campo es negativo.
    """

    cargo_fijo: int = 8500
    limite_basico: int = 20
    precio_basico: int = 1200
    precio_complementario: int = 2400

    def __post_init__(self) -> None:
        for campo in fields(self):
            _validar_entero_no_negativo(campo.name, getattr(self, campo.name))


TARIFA_ILUSTRATIVA = Tarifa()


def _dividir_consumo(consumo_m3: int, limite_basico: int) -> tuple[int, int]:
    """Reparte el consumo entre el tramo básico y el complementario.

    Args:
        consumo_m3: consumo total en m³.
        limite_basico: m³ que se cobran a precio básico.

    Returns:
        Una tupla ``(m3_basicos, m3_complementarios)``. Un consumo igual al
        límite se cobra completo como básico.
    """
    m3_basicos = min(consumo_m3, limite_basico)
    m3_complementarios = max(0, consumo_m3 - limite_basico)
    return m3_basicos, m3_complementarios


def calcular_valor_factura(
    consumo_m3: int, tarifa: Tarifa = TARIFA_ILUSTRATIVA
) -> int:
    """Calcula el valor de la factura de agua en pesos.

    Fórmula: ``cargo_fijo + básicos * precio_basico + complementarios *
    precio_complementario``. Con consumo cero se cobra solo el cargo fijo.

    Args:
        consumo_m3: consumo del periodo en m³; entero mayor o igual que cero.
        tarifa: tarifa a aplicar; por defecto la tarifa ilustrativa (P-01).

    Returns:
        Valor de la factura en pesos, como entero (sin decimales ni redondeo).

    Raises:
        TypeError: si ``consumo_m3`` no es ``int`` (decimales y booleanos se
            rechazan) o si ``tarifa`` no es un objeto ``Tarifa``.
        ValueError: si ``consumo_m3`` es negativo.
    """
    _validar_entero_no_negativo("consumo_m3", consumo_m3)
    if not isinstance(tarifa, Tarifa):
        raise TypeError("La tarifa debe ser un objeto Tarifa")
    m3_basicos, m3_complementarios = _dividir_consumo(
        consumo_m3, tarifa.limite_basico
    )
    return (
        tarifa.cargo_fijo
        + m3_basicos * tarifa.precio_basico
        + m3_complementarios * tarifa.precio_complementario
    )
