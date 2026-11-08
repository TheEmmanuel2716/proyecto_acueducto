# Cálculo de tarifa de agua: acueducto veredal «Aguas Claras» (cliente ficticio)

Proyecto del Seminario IA Aplicada al Ciclo de Vida del Software.
Estudiante: Emmanuel Steven González Muñoz.

## Funcionalidad de la semana 5

> **Nota sobre el alcance.** Este es un proyecto académico: el acueducto «Aguas Claras», el
> administrador y el programa heredado son ficticios, y el cliente fue simulado (ver documento
> de requisitos de la semana 3). Como el código heredado no existe, la función de esta semana
> se implementó a partir del contrato y hace el papel de la función heredada de cálculo de
> tarifa. Los valores de la tarifa son ilustrativos (P-01).

### Historia de usuario
**HU-04 (Must).** Como administrador del acueducto, quiero pruebas sobre los límites entre
escalones y sobre el consumo cero, para que un error de un solo metro cúbico no cobre de más
a las familias. Necesidad de origen: N-04.

**Criterios de aceptación**
- *Escenario 1.* Dado que el límite del básico es 20 m³ y el cargo fijo $8.500, cuando se
  ejecutan las pruebas con 0, 20 y 21 m³, entonces la función devuelve $8.500, $32.500 y $34.900.
- *Escenario 2 (error).* Dado que alguien cambia por error el límite del básico de 20 a 15 m³,
  cuando se ejecutan las pruebas, entonces la prueba de 20 m³ falla con esperado $32.500 y
  obtenido $38.500.

### Contrato de la función

```python
def calcular_valor_factura(consumo_m3: int, tarifa: Tarifa = TARIFA_ILUSTRATIVA) -> int
```

- **Recibe:** `consumo_m3`, entero ≥ 0 (metros cúbicos); `tarifa`, objeto `Tarifa` con
  `cargo_fijo`, `limite_basico`, `precio_basico` y `precio_complementario` (por defecto
  8.500 / 20 / 1.200 / 2.400, valores **ilustrativos**, pendiente P-01).
- **Devuelve:** valor de la factura en pesos, entero (sin decimales ni redondeo).
- **Fórmula:** `cargo_fijo + min(consumo, límite)·precio_básico + max(0, consumo − límite)·precio_complementario`.
- **Supuestos:** el consumo exactamente igual al límite se cobra todo como básico; el consumo
  cero cobra solo el cargo fijo (dicho por el cliente).
- **Casos límite:** 0 m³, 20 m³ (límite) y 21 m³ (primer metro complementario).
- **Errores:** consumo negativo → `ValueError`; consumo no entero (decimal o booleano) →
  `TypeError`.
- **Supuestos provisionales (preguntas pendientes):** el rechazo del consumo negativo
  depende de **P-02** (el cliente solo dijo «no puede ser»); rechazar decimales depende de
  **P-03**. Se cambiarán si el cliente responde otra cosa.

**Ejemplos**

| Entrada (`consumo_m3`) | Salida |
|---|---|
| `0`  | `8500` |
| `20` | `32500` |
| `21` | `34900` |
| `25` | `44500` (8.500 + 20·1.200 + 5·2.400) |
| `-1` | `ValueError` |

### Cómo ejecutar las pruebas

```bash
pip install pytest
pytest
```

(`pytest.ini` ya configura la ruta `src`; no hay pasos manuales adicionales.)

### Estructura

```
src/acueducto/tarifa.py   # implementación
tests/test_tarifa.py      # pruebas
bitacora_ia.md            # bitácora de uso de IA
```
