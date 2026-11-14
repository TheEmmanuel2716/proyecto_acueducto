# Bitácora de uso de IA

Proyecto: Documentar y proteger con pruebas el cálculo de tarifa de un sistema heredado de facturación de agua
Estudiante: Emmanuel Steven González Muñoz
Funcionalidad: HU-04 Pruebas de límites entre escalones y consumo cero
Asistente usado: Claude (Anthropic), en modo chat

Contexto: el proyecto es académico y el cliente, el acueducto y el programa heredado son ficticios. Como no existe un código heredado real, escribí con el asistente una función que lo representa, a partir del contrato de HU-04. En mi propuesta dije que no usaría IA para escribir código nuevo en el MVP; aquí la usé para la implementación solo porque la tarea de la semana 5 lo pide, y solo para esta función de apoyo.

## Entradas

### Entrada 1

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** Le di al asistente el contrato de HU-04 (límite de 20 m³, cargo fijo de $8.500, básico a $1.200 y complementario a $2.400) y le pedí casos de prueba. Propuso: 25 m³, 18 m³, 0, 20, 21, consumo negativo, límite cambiado a 15 y consumo decimal.
- **Decisión:** Aceptada con cambios
- **Por qué:** El escenario 2 de HU-04 (alguien cambia el límite a 15) no se puede probar modificando el código dentro de una prueba. Lo convertí en una prueba de sensibilidad que le pasa `Tarifa(limite_basico=15)` y comprueba que 20 m³ da $38.500 y no $32.500. El caso de 18 m³ lo tomé de la factura n.º 3 de HU-03 ($30.100).
- **Verificación:** Calculé a mano cada valor esperado (por ejemplo 8.500 + 20·1.200 + 5·2.400 = 44.500). Con el esqueleto sin implementar, las 8 pruebas fallaron con `NotImplementedError`, así que estaban en rojo antes del código.
- **Commit relacionado:** f6a1399 «Pruebas de HU-04: límites entre escalones y consumo cero (en rojo)»

### Entrada 2

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** Al definir la firma de la función evalué con el asistente usar `Decimal` para los valores en pesos.
- **Decisión:** Rechazada
- **Por qué:** La tarifa y las facturas de mi documento de requisitos son pesos enteros. Con `int` la comparación es exacta, que es lo que pide RNF-01 («ni un peso de diferencia»). El redondeo sigue pendiente en P-04, así que `Decimal` agregaría complejidad sin una necesidad confirmada.
- **Verificación:** Las pruebas comparan con `==` sobre enteros y pasan; las sumas de los ejemplos del README dan exacto.
- **Commit relacionado:** c06eb63 «Implementación de calcular_valor_factura: 8 pruebas en verde»

### Entrada 3

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** Para el caso de error, el asistente sugirió que un consumo negativo lance `ValueError` y un consumo decimal lance `TypeError`.
- **Decisión:** Aceptada
- **Por qué:** El cliente simulado dijo que un consumo negativo «no puede ser» (error de digitación), pero qué debe hacer el programa quedó en la pregunta pendiente P-02, y los decimales en P-03. Lo adopto como supuesto provisional y lo dejé escrito en el README para cambiarlo si el cliente responde otra cosa.
- **Verificación:** Pruebas `test_consumo_negativo_se_rechaza_con_value_error` y `test_consumo_decimal_se_rechaza_con_type_error`; el supuesto y las preguntas P-02 y P-03 están en el README.
- **Commit relacionado:** c06eb63

### Entrada 4

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** «Implementa `calcular_valor_factura` para que pasen estas pruebas», con el contrato y las pruebas como contexto. El asistente devolvió una función con validación, un `if` para el consumo dentro del básico y la fórmula completa para el exceso.
- **Decisión:** Aceptada
- **Por qué:** Cumple el contrato, usa solo la librería estándar (`dataclasses`) y no me obligó a tocar las pruebas. Leí el código línea por línea: la validación va primero, el `<=` hace que 20 m³ se cobre todo como básico y el exceso se cobra al precio complementario.
- **Verificación:** `pytest` → 8 passed. Antes, con el esqueleto, eran 8 failed.
- **Commit relacionado:** c06eb63

### Entrada 5

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** Con las pruebas en verde le pedí un refactor. El asistente propuso extraer `_validar_consumo` y `_dividir_consumo`, reemplazar el `if` con dos fórmulas por una sola expresión con `min` y `max`, y documentar cada campo de `Tarifa`.
- **Decisión:** Aceptada
- **Por qué:** La función era larga y tenía dos fórmulas casi iguales (duplicación). Ahora hay una sola expresión y cada campo de la tarifa tiene su significado escrito, lo que ayuda a HU-02 (cambiar un rango usando solo la ficha).
- **Verificación:** No modifiqué nada en `tests/` (`git diff` sobre esa carpeta salió vacío). `pytest` → 8 passed después del refactor.
- **Commit relacionado:** 57d4cae «Refactor: extrae _validar_consumo y _dividir_consumo…»

## Entradas de la semana 6

### Entrada 6

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Le pedí al asistente una segunda revisión de `tarifa.py` y las pruebas con los criterios de la semana, una tabla de hallazgos con línea y severidad, y que separara problemas seguros de sospechas. [Pega aquí el prompt exacto que usaste.]
- **Decisión:** Aceptada con cambios
- **Por qué:** De seis hallazgos, dos eran reales (`Tarifa` sin validar y falta de pruebas de tipos inesperados) y cuatro eran falsos positivos (desbordamiento con consumos enormes, `bool` aceptado, S101 en pruebas y `__init__.py` vacío).
- **Verificación:** Para cada uno escribí una prueba o ejecuté el código: 22 pruebas nuevas fallaron antes de corregir; el consumo de `10**18` da el valor exacto; `True` ya se rechazaba. Todo está en la sección 3 de `revision_seguridad.md`.
- **Commit relacionado:** 96dbede

### Entrada 7

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** El asistente propuso validar los cuatro campos de `Tarifa` en `__post_init__` (enteros ≥ 0) y exigir que `tarifa` sea un objeto `Tarifa`.
- **Decisión:** Aceptada
- **Por qué:** Un precio negativo hacía que la factura saliera menor que el cargo fijo (cobrar de menos o de más sin aviso), y RNF-01 pide exactitud. No cambia el comportamiento con tarifas válidas.
- **Verificación:** Escribí las pruebas de abuso primero (22 en rojo), apliqué la corrección y pasaron 37. `git diff` sobre `tests/test_tarifa.py` salió vacío: no modifiqué ninguna prueba existente. `ruff check --select E,F,B,S .` sin avisos.
- **Commit relacionado:** 96dbede «H-02/H-03»

### Entrada 8

- **Fecha:** 2026-11-14
- **Prompt o sugerencia:** Pedí un borrador de docstrings y del README con las ocho secciones. No usé un agente de código esta semana: todo fue en chat y apliqué los cambios yo mismo.
- **Decisión:** Aceptada con cambios
- **Por qué:** Corregí el borrador para que cada docstring coincida con el código (por ejemplo, que `TypeError` incluya booleanos y tarifas que no son `Tarifa`) y quité del README afirmaciones sin comprobar.
- **Verificación:** Comparé cada docstring con el código línea por línea y probé en una carpeta limpia `pip install -r requirements-dev.txt`, el comando de ejecución, `pytest` (37 passed), ruff y pip-audit.
- **Commit relacionado:** 266a179 y e7d0e8c

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 3 |
| Aceptadas con cambios | 1 |
| Rechazadas | 1 |

## Errores que atraparon las pruebas

El código del asistente pasó las 8 pruebas en la primera ejecución, así que mis pruebas no atraparon un defecto en la implementación. Para comprobar que sí protegen, introduje yo mismo dos errores y ejecuté `pytest` (después los revertí con `git checkout`):

1. **Límite del básico de 20 a 21.** Fallaron 2 pruebas: `test_consumo_de_25_m3_da_44500` (obtuvo 43.300 en vez de 44.500) y `test_consumo_un_metro_sobre_el_limite_da_34900`. Las de 0 y 20 m³ siguieron pasando, porque en esos consumos el valor no cambia. Por eso HU-04 pide probar también 21 m³.
2. **Reparto con `min(consumo, límite - 1)`.** Fallaron 4 pruebas (25, 20 y 21 m³, y la del límite en 15).

También me pasó algo útil: en la primera mutación `pytest` mostró «8 passed», y al revertir los cambios mostró fallos que no correspondían. Era bytecode obsoleto en `__pycache__`. Borré la caché, volví a correr y el resultado fue el correcto. Aprendí a no creer un resultado que no coincide con lo que acabo de cambiar.

## Reflexión final (5 a 8 líneas)

El asistente me ayudó más con la lista de casos de prueba y con las ideas para el refactor, porque me ahorró lo repetitivo.
Lo que más me costó fue decidir el caso de error: el cliente solo dijo que un consumo negativo «no puede ser», y lo dejé como supuesto provisional en P-02 en vez de presentarlo como un hecho.
Mis pruebas no encontraron un fallo en el código generado, pero sí detectaron los dos errores que introduje a propósito, y vi que probar 21 m³ es lo que revela un límite mal puesto.
También aprendí a desconfiar de un resultado verde o rojo cuando no estoy seguro de que mi cambio se aplicó.
En mi propuesta dije que no usaría IA para escribir código nuevo, y aquí la usé solo porque la tarea lo pide, para una función que representa a la heredada.
En el MVP real la voy a usar para explicar la función y proponer pruebas de caracterización, y voy a revisar cada resultado contra el valor exacto de las facturas.
En la próxima funcionalidad escribiré las pruebas contra el código existente y le pediré al asistente que me explique cada decisión antes de aceptarla.
