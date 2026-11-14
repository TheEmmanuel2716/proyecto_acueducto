"""Pruebas de abuso: entradas hostiles o mal formadas que deben rechazarse.

Se agregaron en la semana 6 tras la revisión de seguridad (hallazgos H-02 y H-03).
"""
import pytest

from acueducto.tarifa import Tarifa, calcular_valor_factura


# --- H-02: la tarifa se valida al crearla -----------------------------------
@pytest.mark.parametrize(
    "campo", ["cargo_fijo", "limite_basico", "precio_basico", "precio_complementario"]
)
def test_tarifa_con_valor_negativo_se_rechaza(campo):
    with pytest.raises(ValueError):
        Tarifa(**{campo: -1})


@pytest.mark.parametrize(
    "campo", ["cargo_fijo", "limite_basico", "precio_basico", "precio_complementario"]
)
@pytest.mark.parametrize("valor", [1200.5, "1200", None, True])
def test_tarifa_con_valor_no_entero_se_rechaza(campo, valor):
    with pytest.raises(TypeError):
        Tarifa(**{campo: valor})


def test_precio_negativo_no_permite_facturar_menos_que_el_cargo_fijo():
    # Sin validación, un precio básico de -1000 daría una factura menor al cargo fijo.
    with pytest.raises(ValueError):
        calcular_valor_factura(20, Tarifa(precio_basico=-1000))


def test_tarifa_que_no_es_tarifa_se_rechaza_con_type_error():
    with pytest.raises(TypeError):
        calcular_valor_factura(10, {"cargo_fijo": 0})


# --- H-03: consumos de tipo inesperado --------------------------------------
@pytest.mark.parametrize("consumo", [True, False, "20", None, [20], 20.0])
def test_consumo_de_tipo_inesperado_se_rechaza_con_type_error(consumo):
    with pytest.raises(TypeError):
        calcular_valor_factura(consumo)


def test_consumo_enorme_se_calcula_exacto_sin_desbordarse():
    consumo = 10**18
    esperado = 8_500 + 20 * 1_200 + (consumo - 20) * 2_400
    assert calcular_valor_factura(consumo) == esperado
