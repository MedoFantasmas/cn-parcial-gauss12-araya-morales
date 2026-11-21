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

El conteo corresponde a las operaciones aritmeticas registradas durante la eliminacion y sustitucion. No representa el costo computacional total del programa.

## FLOPs por etapa de eliminacion

| Paso | Sin pivoteo Mult./Div. | Sin pivoteo Sumas/Restas | Sin pivoteo Total | Con pivoteo Mult./Div. | Con pivoteo Sumas/Restas | Con pivoteo Total |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 143 | 132 | 275 | 143 | 132 | 275 |
| 2 | 120 | 110 | 230 | 120 | 110 | 230 |
| 3 | 99 | 90 | 189 | 99 | 90 | 189 |
| 4 | 80 | 72 | 152 | 80 | 72 | 152 |
| 5 | 63 | 56 | 119 | 63 | 56 | 119 |
| 6 | 48 | 42 | 90 | 48 | 42 | 90 |
| 7 | 35 | 30 | 65 | 35 | 30 | 65 |
| 8 | 24 | 20 | 44 | 24 | 20 | 44 |
| 9 | 15 | 12 | 27 | 15 | 12 | 27 |
| 10 | 8 | 6 | 14 | 8 | 6 | 14 |
| 11 | 3 | 2 | 5 | 3 | 2 | 5 |
| **Total** | **638** | **572** | **1210** | **638** | **572** | **1210** |
