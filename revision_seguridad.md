# Informe de revisión de código y seguridad

Proyecto: Cálculo de tarifa de agua, acueducto veredal «Aguas Claras» (proyecto académico)
Estudiante: Emmanuel Steven González Muñoz
Fecha: 2026-11-14
Commit revisado: af0f1bd

## 1. Herramientas y criterios

- **Linter:** ruff 0.17.5 con las reglas E, F, B, S. Configuración en `pyproject.toml`.
  Resultado inicial: 9 avisos (2 E501, 7 S101). Resultado final: sin avisos.
- **Auditoría de dependencias:** pip-audit 2.9.0 sobre `requirements-dev.txt`. Resultado: sin vulnerabilidades conocidas.
- **Lista de revisión:** la de la semana 6 (corrección y pruebas, diseño y legibilidad, seguridad).
- **Revisión con IA:** Claude (Anthropic) con el prompt de revisión de la semana (ver sección 3 y entrada 6 de la bitácora).

### Puntos de seguridad revisados

| Punto | ¿Aplica? | Resultado |
|---|---|---|
| Inyección (consultas con parámetros) | No: el proyecto no tiene base de datos, SQL, shell, `eval` ni entrada de texto que se interprete | Sin hallazgos |
| Secretos (código, historial, .gitignore, .env.example) | Sí | Sin claves en el código ni en el historial (`git log --all -p` revisado). `.env` ya estaba en `.gitignore`; faltaba `.env.example` (H-04). Datos personales (RNF-04): el repo no tiene CSV de facturas, así que hay 0 nombres y 0 cédulas |
| Contraseñas (scrypt, bcrypt o argon2 con sal) | No: el proyecto no guarda contraseñas ni usuarios | Sin hallazgos |
| Control de acceso (rol verificado y prueba de abuso) | No: no hay roles ni operaciones restringidas. Se aplicó el equivalente a entradas hostiles: pruebas de abuso sobre `Tarifa` y el consumo | Ver H-02 y H-03 |
| Dependencias (existen, necesarias, versión fijada, pip-audit) | Sí, solo de desarrollo | `pytest`, `ruff` y `pip-audit` existen, son necesarias y están fijadas en `requirements-dev.txt`; pip-audit sin vulnerabilidades |

## 2. Tabla de hallazgos

Las líneas corresponden al commit revisado (af0f1bd).

| Id | Archivo y línea | Problema | Categoría (OWASP o tipo) | Severidad | Corrección | Commit |
|---|---|---|---|---|---|---|
| H-00 | (raíz) | No había linter ni versiones fijadas | A06 Componentes vulnerables / calidad | Media | `pyproject.toml` con ruff (E,F,B,S) y `requirements-dev.txt` fijado | bad9b88 |
| H-01 | tarifa.py:7 y :34 | Líneas de más de 88 caracteres (E501) | Estilo | Baja | Se reparten en varias líneas | 5296976 |
| H-02 | tarifa.py:5-12 (`Tarifa`) y :33 | `Tarifa` aceptaba precios o límites negativos y valores no enteros; `calcular_valor_factura` aceptaba cualquier objeto como tarifa. Con `precio_basico=-1000` la factura salía menor que el cargo fijo | A04 Diseño inseguro / validación de entrada | Media | `__post_init__` valida enteros ≥ 0; la función exige un objeto `Tarifa`; 4 familias de pruebas de abuso | 96dbede |
| H-03 | README.md y tests/ | El README decía que un booleano se rechaza con `TypeError`, pero ninguna prueba lo comprobaba | Pruebas insuficientes | Baja | Pruebas nuevas de consumos `True`, `False`, `"20"`, `None`, `[20]`, `20.0` y de un consumo enorme | 96dbede |
| H-04 | (raíz) | Faltaba `.env.example`; `.gitignore` sin `.venv/` ni `.ruff_cache/` | A05 Configuración / secretos | Baja | Se agrega `.env.example` y se amplía `.gitignore` | bfdb7cd |
| H-05 | tarifa.py:18-23 | Validación de enteros repetida (la del consumo) y docstrings sin errores ni argumentos | Mantenibilidad | Baja | Una sola `_validar_entero_no_negativo`; docstrings completos | 266a179 |

**Severidad:** alta (permite acceder o cambiar datos sin permiso, o expone secretos), media (error probable o riesgo con condiciones), baja (estilo o mantenibilidad).

### Avisos del linter no corregidos

| Regla | Archivo y línea | Por qué se mantiene |
|---|---|---|
| S101 | `tests/**` (7 avisos iniciales) | `assert` es la forma normal de comprobar en pytest. Se ignora solo en `tests/**` desde `pyproject.toml`; en `src/` sigue activa |

## 3. Revisión con IA

**Prompt usado:**

> Revisa este proyecto de Python (cálculo de tarifa del acueducto) con la lista de revisión de la semana 6. Analiza calidad, seguridad y pruebas, y entrega una tabla con hallazgos ordenados por archivo, línea y severidad. Separa claramente: (1) problemas seguros y (2) sospechas o falsos positivos. Considera validación de entrada, tipos no esperados (`bool`, `None`, texto, listas, decimales), desbordamiento entero, abuso de entrada, dependencias, secretos, uso de `assert`, archivos vacíos y requisitos de seguridad. Si encuentras un problema, indica la categoría (OWASP o tipo), la severidad alta/media/baja y la forma de verificarlo. Haz que la revisión sea práctica: incluye al menos un caso que verifiques ejecutando el código o con pruebas, y escribe la conclusión en lenguaje claro para una entrega académica.

Enlace: entrada 6 de `bitacora_ia.md`.

| Hallazgo de la IA | ¿Real o falso positivo? | Cómo lo verifiqué |
|---|---|---|
| `Tarifa` y el parámetro `tarifa` no se validan (seguro) | Real (H-02) | Escribí las pruebas primero: 22 fallaron. Con el código corregido, pasan |
| Consumo muy grande podría desbordar o causar denegación de servicio (sospecha) | Falso positivo | Los enteros de Python no se desbordan; la prueba con `10**18` da el valor exacto |
| `True` se acepta como entero porque `bool` es subclase de `int` (sospecha) | Falso positivo | `_validar_consumo` ya lo rechazaba; lo comprobé con pruebas nuevas (H-03) |
| S101 en las pruebas (linter) | Falso positivo | `assert` es la forma de pytest; se ignora solo en `tests/**` |
| Faltan pruebas de tipos inesperados (`"20"`, `None`, lista) (seguro) | Real (H-03) | Las pruebas nuevas pasan; antes no existía ninguna |
| `src/acueducto/__init__.py` está vacío (baja) | Falso positivo | Es normal: marca la carpeta como paquete |

**Lo que la IA no encontró:** El repositorio faltaba `.env.example` y no había una regla para `.venv/` y `.ruff_cache/` en `.gitignore`; lo verifiqué revisando el árbol del proyecto y el contenido del archivo de exclusiones, y ese hallazgo quedó registrado como H-04. También confirmé de forma directa que el README hablaba de una validación para tipos inesperados sin que hubiera pruebas que la respaldaran, lo cual quedó cubierto en H-03.

## 4. Pendientes

| Pendiente | Por qué no se corrigió todavía | Plan |
|---|---|---|
| Preguntas P-01 a P-04 (valores reales de la tarifa, consumo negativo, decimales, redondeo) | Dependen del cliente simulado | Ajustar `Tarifa` y las pruebas cuando haya respuesta |
| Facturas históricas en CSV y script `revisar_anonimizacion.py` (HU-03, HU-05, RNF-04) del diseño de la semana 4 | Todavía no están en el repositorio; el incremento actual solo cubre la función y sus límites | Al agregarlos: el script debe rechazar cualquier columna distinta de código, consumo y valor, con prueba de abuso (fila con nombre o cédula); revisar el historial antes de subir el CSV |
| Licencia del proyecto | No he decidido cuál usar | Elegirla antes del MVP y actualizar el README |
| Integración continua (ruff, pytest y pip-audit en cada push) | Fuera del alcance de esta semana | Agregar un flujo de GitHub Actions en la semana 7 |

**Claves expuestas:** Ninguna.
