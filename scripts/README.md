# Procesamiento de los registros publicados

La fuente de las puntuaciones es `evidencias/pruebas_usuarios/resultados/registros_evaluacion.csv`. El procesamiento exige los 30 registros de P1–P3, versiones `A_original` y `B_rediseno`, y momentos M1–M5. Rechaza claves duplicadas, combinaciones ausentes, campos vacíos, columnas incompatibles y valores que no sean enteros de −3 a +3. El cero es una puntuación válida.

Las rutas se resuelven desde la ubicación de los scripts. Los comandos siguientes se ejecutan desde la raíz del repositorio.

## Validar y calcular

La validación y el resumen utilizan únicamente la biblioteca estándar de Python:

```bash
python3 scripts/procesar_resultados.py --validar
python3 scripts/procesar_resultados.py
```

El segundo comando actualiza `curva_emocional/resumen_resultados.csv`. No modifica el CSV de entrada. Las medias se calculan con los registros íntegros y se redondean a seis decimales al escribir el resumen.

## Regenerar los gráficos

Dependencias de Python:

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/generar_curva_y_matriz.py --sin-matriz
```

Se generan seis gráficos emocionales, el resumen, la figura de contraste y `contrastes.csv`, conservando los nombres publicados. Las bandas de la comparación son mínimos y máximos, no intervalos de confianza. `generar_contrastes.py` usa los siete pares HEX documentados; su resultado no certifica la accesibilidad completa de la interfaz.

Para revisar los resultados en otra carpeta:

```bash
python3 scripts/generar_curva_y_matriz.py --sin-matriz --salida /ruta/de/revision
```

## Actualizar también la matriz

El generador de Excel requiere **Node.js con `@oai/artifact-tool` disponible**. Esta dependencia es independiente de `pip` y no se instala mediante `requirements.txt`. Se puede comprobar sin escribir archivos:

```bash
node scripts/generar_matriz.mjs --comprobar
```

El módulo se busca mediante la resolución habitual de Node.js. Si está en un directorio de módulos externo, se puede indicar con `IHC_NODE_MODULES`. El entorno de ejecución integrado también admite `CODEX_PRIMARY_RUNTIME_NODE` y `CODEX_PRIMARY_RUNTIME_NODE_MODULES`. Si el motor no está disponible, el comando completo termina antes de reemplazar resultados; `--sin-matriz` permite actualizar los gráficos por separado.

```bash
python3 scripts/generar_curva_y_matriz.py
```

El flujo valida la entrada, genera los resultados en una carpeta temporal y los copia a sus rutas finales cuando todos los generadores terminan. La matriz existente se utiliza como base para conservar las hojas `Verificación` y `Heurísticas`. Se actualizan `Matriz UX` y `Datos de evaluación`.

- `Datos de evaluación` conserva las ocho columnas de los 30 registros y añade una validación por fila, las medias por momento y por código, y la media global.
- `Matriz UX` enlaza sus medias y diferencias con esos cálculos y muestra las emociones anotadas en el registro.
- Las fórmulas distinguen cero de una celda vacía. Si hay registros inválidos o duplicados, las medias quedan sin resultado válido en lugar de mostrar un promedio parcial.
- Para actualizar el conjunto, editar primero el CSV y ejecutar el flujo. Las ediciones manuales dentro de Excel no se escriben de vuelta al CSV.
- El conjunto corresponde a la versión evaluada. Las correcciones posteriores se consultan en `rediseño/correcciones_pendientes.md`.

La opción `--qa-dir /ruta/de/revision` comprueba cambios de entrada, vacío y duplicación, restaura los valores originales y guarda vistas de las hojas para revisión. `--salida /ruta/de/revision` permite generar la matriz y las figuras fuera de sus rutas publicadas.

## Informe entregado

Estos comandos no generan Word ni PDF ni modifican `informe/informe_final.pdf`. `generar_informe_apes.py` conserva el nombre del punto de entrada anterior y termina con un mensaje explicativo: la plantilla APES que requería no forma parte del repositorio y ese flujo ya no se utiliza.
