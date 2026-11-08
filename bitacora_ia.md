# Bitácora de uso de IA

Proyecto: Documentar y proteger con pruebas el cálculo de tarifa de un sistema heredado de facturación de agua
Estudiante: Emmanuel Steven González Muñoz
Funcionalidad: HU-04 Pruebas de límites entre escalones y consumo cero
Asistente usado: Claude (Anthropic), en modo chat

## Entradas

### Entrada 1

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** Con el contrato de HU-04 (límite 20 m³, cargo fijo $8.500, $1.200 y $2.400), el asistente propuso una lista de casos de prueba: 25 m³, 18 m³, 0, 20, 21, consumo negativo, límite cambiado a 15 y consumo decimal.
- **Decisión:** Aceptada con cambios
- **Por qué:** El escenario 2 de HU-04 («alguien cambia el límite a 15») no se puede probar modificando el código dentro de una prueba. Lo convertí en una prueba de sensibilidad que pasa `Tarifa(limite_basico=15)` y comprueba que 20 m³ da $38.500 y no $32.500. El 18 m³ lo tomé de la factura n.º 3 de HU-03 (valor $30.100).
- **Verificación:** Calculé a mano cada valor esperado (por ejemplo 8.500 + 20·1.200 + 5·2.400 = 44.500). Las 8 pruebas fallaron al principio con `NotImplementedError`, lo que confirma que estaban en rojo antes del código.
- **Commit relacionado:** f6a1399 «Pruebas de HU-04: límites entre escalones y consumo cero (en rojo)»

### Entrada 2

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** Alternativa considerada al definir la firma: usar `Decimal` para los valores en pesos.
- **Decisión:** Rechazada
- **Por qué:** La tarifa y las facturas del documento de requisitos son pesos enteros. Con `int` la comparación es exacta, que es lo que exige RNF-01 («ni un peso de diferencia»). El redondeo de decimales sigue pendiente en P-04, así que `Decimal` agregaría complejidad sin una necesidad confirmada.
- **Verificación:** Las pruebas comparan con `==` sobre enteros y pasan; las sumas de los ejemplos del README dan exacto.
- **Commit relacionado:** c06eb63 «Implementación de calcular_valor_factura: 8 pruebas en verde»

### Entrada 3

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** Para el caso de error de la historia, el asistente sugirió que un consumo negativo lance `ValueError` y un consumo decimal lance `TypeError`.
- **Decisión:** Aceptada
- **Por qué:** El cliente dijo que un consumo negativo «no puede ser» (error de digitación), pero qué debe hacer el programa está en la pregunta pendiente P-02, y los decimales en P-03. Lo adopto como supuesto provisional y lo dejo escrito en el README para cambiarlo si el cliente responde otra cosa.
- **Verificación:** Pruebas `test_consumo_negativo_se_rechaza_con_value_error` y `test_consumo_decimal_se_rechaza_con_type_error`; el README documenta el supuesto y las preguntas P-02 y P-03.
- **Commit relacionado:** c06eb63

### Entrada 4

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** «Implementa `calcular_valor_factura` para que pasen estas pruebas», con el contrato y las pruebas como contexto. El asistente devolvió una función con validación, un `if` para el caso dentro del básico y la fórmula completa para el exceso.
- **Decisión:** Aceptada
- **Por qué:** Cumple el contrato, usa solo la librería estándar (`dataclasses`) y no cambia las pruebas. Leí cada línea: la validación va primero, el `<=` hace que 20 m³ se cobre todo como básico y el exceso se cobra al complementario.
- **Verificación:** `pytest` → 8 passed. Antes, con el esqueleto, eran 8 failed.
- **Commit relacionado:** c06eb63

### Entrada 5

- **Fecha:** 2026-11-08
- **Prompt o sugerencia:** Pedí un refactor con las pruebas en verde. El asistente propuso extraer `_validar_consumo` y `_dividir_consumo`, reemplazar la rama con `if` por una sola fórmula con `min`/`max` y documentar cada campo de `Tarifa`.
- **Decisión:** Aceptada
- **Por qué:** La función era larga y tenía dos fórmulas casi iguales (duplicación). Con `min`/`max` hay una sola expresión y cada campo de la tarifa tiene su significado escrito, lo que ayuda a HU-02 (cambiar un rango con una ficha).
- **Verificación:** No toqué `tests/` (`git diff` sobre esa carpeta vacío). `pytest` → 8 passed después del refactor.
- **Commit relacionado:** 57d4cae «Refactor: extrae _validar_consumo y _dividir_consumo…»

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 3 |
| Aceptadas con cambios | 1 |
| Rechazadas | 1 |

## Errores que atraparon las pruebas

El código que generó el asistente pasó las 8 pruebas desde la primera ejecución, así que las pruebas no atraparon un defecto en la implementación. Para comprobar que protegen de verdad, introduje a propósito dos errores en el código y ejecuté `pytest` (los revertí después con `git checkout`):

1. **Límite del básico de 20 a 21.** Fallaron 2 pruebas: `test_consumo_de_25_m3_da_44500` (obtenido 43.300 en lugar de 44.500) y `test_consumo_un_metro_sobre_el_limite_da_34900`. Las de 0 y 20 m³ siguieron pasando, porque en 0 y en 20 el resultado no cambia; las de 21 y 25 m³ sí detectan el error. Esto confirma por qué HU-04 pide probar 21 m³ y no solo 20.
2. **Reparto con `min(consumo, límite - 1)`.** Fallaron 4 pruebas (25, 20, 21 m³ y la del límite en 15).

En la primera mutación `pytest` mostró «8 passed», probablemente por la caché de bytecode al cambiar el archivo dentro del mismo segundo. Repetí la ejecución y falló como debía. Lección: desconfiar de un «todo pasa» justo después de un cambio y volver a correr.

## Reflexión final (5 a 8 líneas)

El asistente me ayudó más al proponer la lista de casos y al sugerir el refactor, porque me ahorró tiempo en lo repetitivo. Lo difícil fue decidir los casos de error: el cliente solo dijo que un consumo negativo «no puede ser», así que lo dejé como supuesto provisional (P-02) y no como un hecho. Las pruebas no atraparon un fallo del código generado, pero sí detectaron los dos errores que introduje a propósito, y vi que probar 21 m³ es lo que revela un límite mal puesto. También aprendí a desconfiar de un resultado verde cuando no estoy seguro de que mi cambio se aplicó. En la próxima funcionalidad escribiré las pruebas de caracterización contra la función heredada real, no contra una reimplementación, y pediré al asistente que me explique cada decisión antes de aceptarla.
