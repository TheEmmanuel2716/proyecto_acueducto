"""Pruebas de HU-04: límites entre escalones y consumo cero.

Valores ilustrativos de la tarifa (P-01): cargo fijo $8.500; básico hasta
20 m³ a $1.200; complementario a $2.400.
"""
import pytest

from acueducto.tarifa import Tarifa, calcular_valor_factura


# --- Casos normales ---------------------------------------------------------
def test_consumo_de_25_m3_da_44500():
    assert calcular_valor_factura(25) == 44_500  # 8.500 + 20*1.200 + 5*2.400


def test_consumo_de_18_m3_dentro_del_basico_da_30100():
    assert calcular_valor_factura(18) == 30_100  # factura n.º 3 de HU-03


# --- Casos límite -----------------------------------------------------------
def test_consumo_cero_cobra_solo_el_cargo_fijo():
    assert calcular_valor_factura(0) == 8_500


def test_consumo_igual_al_limite_basico_da_32500():
    assert calcular_valor_factura(20) == 32_500


def test_consumo_un_metro_sobre_el_limite_da_34900():
    assert calcular_valor_factura(21) == 34_900


# --- Casos de error ---------------------------------------------------------
def test_consumo_negativo_se_rechaza_con_value_error():
    with pytest.raises(ValueError):
        calcular_valor_factura(-1)


def test_limite_cambiado_por_error_a_15_hace_que_20_m3_de_38500():
    # HU-04, escenario 2: con el límite en 15 el valor ya no es $32.500.
    tarifa_equivocada = Tarifa(limite_basico=15)
    assert calcular_valor_factura(20, tarifa_equivocada) == 38_500
    assert calcular_valor_factura(20, tarifa_equivocada) != 32_500


def test_consumo_decimal_se_rechaza_con_type_error():
    with pytest.raises(TypeError):
        calcular_valor_factura(20.5)
