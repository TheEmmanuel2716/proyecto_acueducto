# Cálculo de tarifa de agua: acueducto veredal «Aguas Claras»

## 1. Qué es

Biblioteca en Python que calcula el valor de la factura de agua de un acueducto
veredal: un cargo fijo más el consumo, con dos escalones de precio (básico hasta un
límite y complementario por encima).

> **Alcance.** Es un proyecto académico del Seminario IA Aplicada al Ciclo de Vida del
> Software. El acueducto «Aguas Claras», el administrador y el programa heredado son
> ficticios y el cliente fue simulado (documento de requisitos de la semana 3). Como el
> código heredado no existe, la función se implementó a partir del contrato y hace el
> papel de la función heredada. Los valores de la tarifa son **ilustrativos** (P-01).

**Historia de usuario HU-04 (Must).** Como administrador, quiero pruebas sobre los
límites entre escalones y sobre el consumo cero, para que un error de un metro cúbico no
cobre de más a las familias.

### Contrato de la función

```python
def calcular_valor_factura(consumo_m3: int, tarifa: Tarifa = TARIFA_ILUSTRATIVA) -> int
```

- **Recibe:** `consumo_m3`, entero ≥ 0; `tarifa`, objeto `Tarifa` con `cargo_fijo`,
  `limite_basico`, `precio_basico` y `precio_complementario` (por defecto
  8.500 / 20 / 1.200 / 2.400). Todos los campos de `Tarifa` deben ser enteros ≥ 0.
- **Devuelve:** valor de la factura en pesos, entero (sin decimales ni redondeo).
- **Fórmula:** `cargo_fijo + min(consumo, límite)·precio_básico + max(0, consumo − límite)·precio_complementario`.
- **Errores:** consumo o campo de tarifa negativo → `ValueError`; valor no entero
  (decimal, booleano, texto, `None`) o tarifa que no es `Tarifa` → `TypeError`.
- **Supuestos provisionales:** rechazar consumos negativos depende de **P-02** y rechazar
  decimales de **P-03**; se cambiarán si el cliente responde otra cosa.

| Entrada (`consumo_m3`) | Salida |
|---|---|
| `0`  | `8500` |
| `20` | `32500` |
| `21` | `34900` |
| `25` | `44500` (8.500 + 20·1.200 + 5·2.400) |
| `-1` | `ValueError` |

## 2. Requisitos

- Python 3.10 o superior.
- Dependencias **solo de desarrollo** (pruebas y linter), con versión fijada en
  `requirements-dev.txt`: `pytest`, `ruff` y `pip-audit`. El código no usa librerías
  externas.

## 3. Instalación

```bash
git clone https://github.com/TheEmmanuel2716/proyecto_acueducto.git
cd proyecto_acueducto
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

No se necesitan secretos. `.env.example` explica cómo manejarlos si se agregan.

## 4. Ejecución

El proyecto es una biblioteca sin interfaz. Para usarla desde la raíz del repositorio:

```bash
PYTHONPATH=src python -c "from acueducto.tarifa import calcular_valor_factura as f; print(f(25))"
```

Resultado esperado: `44500`. En Windows (PowerShell): `$env:PYTHONPATH="src"` antes del comando.

## 5. Pruebas

```bash
pytest                                   # 37 pruebas
ruff check --select E,F,B,S .            # linter; configuración en pyproject.toml
pip-audit -r requirements-dev.txt        # vulnerabilidades en dependencias
```

Las pruebas de `tests/test_tarifa_abuso.py` comprueban que se rechazan tarifas con
precios negativos o de tipo incorrecto y consumos de tipo inesperado.

## 6. Estructura

```
src/acueducto/tarifa.py        # Tarifa y calcular_valor_factura
tests/test_tarifa.py           # pruebas de HU-04 (semana 5)
tests/test_tarifa_abuso.py     # pruebas de abuso (semana 6)
pyproject.toml                 # configuración de ruff
requirements-dev.txt           # dependencias de desarrollo con versión fijada
pytest.ini                     # ruta src para pytest
.env.example                   # plantilla de variables de entorno (vacía)
revision_seguridad.md          # informe de revisión de código y seguridad
bitacora_ia.md                 # bitácora de uso de IA
```

## 7. Uso de IA

Se usó Claude (Anthropic) para proponer casos de prueba, implementar la función a partir
del contrato, sugerir el refactor y hacer una segunda revisión de código y seguridad.
Cada sugerencia se verificó ejecutando las pruebas y el linter y se registró en
`bitacora_ia.md`. Los hallazgos de la revisión con IA y su verificación están en
`revision_seguridad.md`.

## 8. Autor y licencia

Emmanuel Steven González Muñoz. Proyecto académico, sin licencia de uso abierto: todos
los derechos reservados al autor mientras no se elija otra.
