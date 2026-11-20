# Conteo de FLOPs

## Resultados generales

| Operacion | FLOPs |
|---|---:|
| Eliminacion sin pivoteo | 1210 |
| Eliminacion con pivoteo | 1210 |
| Sustitucion regresiva | 156 |
| Total sin busqueda de pivote | 1366 |
| Total con divisiones de busqueda | 1443 |

## Sobrecosto del pivoteo

| Operacion | Cantidad |
|---|---:|
| Divisiones | 77 |
| Comparaciones | 66 |
| Intercambios | 8 |

Las comparaciones y los intercambios de filas se reportan por separado y no se incluyen en el total de FLOPs aritmeticos.

El calculo inicial de las escalas de fila no esta incluido en este conteo.

## FLOPs por etapa de eliminacion

| Paso | Sin pivoteo | Con pivoteo |
|---|---:|---:|
| 1 | 275 | 275 |
| 2 | 230 | 230 |
| 3 | 189 | 189 |
| 4 | 152 | 152 |
| 5 | 119 | 119 |
| 6 | 90 | 90 |
| 7 | 65 | 65 |
| 8 | 44 | 44 |
| 9 | 27 | 27 |
| 10 | 14 | 14 |
| 11 | 5 | 5 |
