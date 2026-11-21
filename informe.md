# Informe Lab 3: Eliminación gaussiana con mínimo costo operacional y máxima exactitud de mantisa

## 1. Identificación:
**Estudiantes:** Felipe Araya Díaz y Mariana Morales Muñoz\
**Asignatura:** Computación Numérica\
**Fecha de entrega:** 20-11-2026\
**Enlace al repositorio:** https://github.com/MedoFantasmas/cn-parcial-gauss12-araya-morales


## 2. Planteamiento

El problema consiste en resolver un sistema de ecuaciones lineales de la forma (Ax=b), donde (A) es una matriz densa de (12\times12), (b) es el vector de términos independientes y (x) contiene las 12 incógnitas.

La principal dificultad del sistema está en la gran diferencia de magnitud entre los coeficientes de la matriz (A), cuyos valores van aproximadamente desde (10^{-8}) hasta (10^{6}). Esta variación puede afectar la estabilidad numérica de la eliminación gaussiana, especialmente cuando se utilizan elementos de magnitud muy pequeña como pivotes.

Por eso, se comparan dos procedimientos: eliminación gaussiana sin pivoteo y eliminación gaussiana con pivoteo parcial escalado. El objetivo es evaluar cómo influye la selección del pivote tanto en el costo operacional como en la precisión de la solución obtenida. Haciendo uso de asistentes de IA (chatGPT) para planear código con mayor facilidad.


## 3. Estrategia de eliminación

Se implementan dos variantes de eliminación gaussiana para resolver el sistema: sin pivoteo y con pivoteo parcial. Ambas realizan 11 etapas de eliminación, en las que se anulan los 66 elementos ubicados debajo de la diagonal principal, transformando la matriz en una matriz triangular superior.

En la variante sin pivoteo, se utiliza directamente el elemento diagonal de cada paso como pivote. Para cada fila inferior se calcula el multiplicador m_{ik}=a_{ik}/a_{kk}, que se reutiliza durante toda la actualización de esa fila. Luego se actualizan los elementos restantes de la matriz y el término correspondiente del vector \(b\). Finalmente, el elemento que se desea eliminar se establece en cero.

En la segunda variante se utiliza pivoteo parcial escalado. Se selecciona la fila con la razón más alta y se intercambia con la fila actual si es necesario. Estos intercambios también se aplican al vector (b) y a las escalas de las filas. Una vez seleccionado el pivote, se realiza el mismo procedimiento de eliminación que en la primera variante.

En ambos métodos, los multiplicadores se calculan una sola vez por fila y se reutilizan para actualizar la matriz y el vector de términos independientes.

Finalmente, sobre las matrices triangulares obtenidas se aplica sustitución regresiva para calcular las incógnitas, comenzando por la última ecuación y avanzando hacia la primera.


## 4. Conteo de operaciones

Para contabilizar el costo operacional, se consideró cada multiplicación, división, suma y resta como una operación de punto flotante (FLOP). El conteo contempla tanto la eliminación como la sustitución regresiva.

Como se mencionó anteriormente, en cada etapa se calcula una sola vez el multiplicador de cada fila y se reutiliza durante la actualización. La tabla presenta el número de operaciones aritméticas realizadas en cada una de las 11 etapas:

| Paso | Mult./Div. | Sumas/Restas | Total |
|---|---|---|---|
| 1 | 143 | 132 | 275 |
| 2 | 120 | 110 | 230 |
| 3 | 99 | 90 | 189 |
| 4 | 80 | 72 | 152 |
| 5 | 63 | 56 | 119 |
| 6 | 48 | 42 | 90 |
| 7 | 35 | 30 | 65 |
| 8 | 24 | 20 | 44 |
| 9 | 15 | 12 | 27 |
| 10 | 8 | 6 | 14 |
| 11 | 3 | 2 | 5 |
| Total | 638 | 572 | 1210 |

El conteo de la sustitución regresiva corresponde a 156 FLOPs. Por lo tanto, el costo aritmético total de la eliminación y sustitución es: 1210 + 156 = **1366 FLOPs**

Este resultado es igual para ambas estrategias de pivoteo, ya que los intercambios de filas no modifican la cantidad de elementos que deben actualizarse.

En el caso del pivoteo parcial escalado, se agregan operaciones para seleccionar los pivotes:

| Operación adicional | Cantidad |
|---|---:|
| Divisiones para calcular los cocientes | 77 |
| Comparaciones | 66 |
| Intercambios de filas | 8 |

Al incluir las 77 divisiones utilizadas en la búsqueda de pivotes, el total contabilizado sube a 1443 operaciones. Las comparaciones y los intercambios se informan por separado, ya que no se consideran FLOPs.

Cabe señalar que este conteo no incluye el cálculo inicial de las escalas de las filas y representa únicamente las operaciones registradas durante la eliminación y sustitución, no el costo computacional completo del programa.

## 5. Análisis de mantisa y pivoteo

La comparación entre ambas estrategias muestra una diferencia importante en la estabilidad numérica del procedimiento.

| Indicador | Sin pivoteo | Pivoteo parcial escalado |
|---|---:|---:|
| Multiplicador máximo | 2.7526 * 10^13 | 2.4656 * 10^9 |
| Factor de crecimiento | 2641.2243 | 1.7832 |
| Intercambios de filas | 0 | 8 |

En la primera etapa sin pivoteo se utiliza como pivote el elemento a_11 = 1.3407e-8. Este valor es extremadamente pequeño en comparación con otros elementos de la primera columna, por lo que al dividir entre él se generan multiplicadores de gran magnitud.

El problema se vuelve especialmente evidente al alcanzar un multiplicador máximo del orden de 10^13. Estos valores pueden amplificar los errores de redondeo durante las operaciones posteriores y perjudicar la precisión de la solución.

Con el pivoteo parcial escalado, el multiplicador máximo disminuye considerablemente y el factor de crecimiento pasa de aproximadamente 2641.22 a 1.78. Esto indica que el intercambio de filas permite controlar mejor el crecimiento de los elementos durante la eliminación.

Como referencia de escala, el logaritmo en base 2 de los multiplicadores máximos es aproximadamente 44.65 bits para el método sin pivoteo y 31.20 bits para el método con pivoteo. Estos valores permiten comparar la magnitud de los multiplicadores, pero no representan una medición exacta de los bits de mantisa perdidos.

Por eso, utilizar directamente a_11 como pivote resulta inadecuado para este sistema. El pivoteo parcial escalado ofrece un comportamiento numérico más estable sin aumentar la cantidad de operaciones principales de eliminación.

## 6. Condicionamiento

El condicionamiento permite estudiar cuánto puede cambiar la solución de un sistema ante pequeñas perturbaciones en sus datos.

Para este problema se calculó el número de condición utilizando la norma infinito: k(A)=5.3678e13

Este valor indica que el sistema está muy mal condicionado. En términos generales, un número de condición elevado significa que pequeños errores en los datos o en los cálculos pueden producir variaciones importantes en la solución.

Considerando la precisión de máquina de doble precisión: epsilon =(aprox) 2.2204e-16

se obtiene: k(A) * epsilon = approx= 1.1919e-2

Esta estimación es una cota de referencia pesimista, que sugiere que el sistema puede ser sensible a errores numéricos. Sin embargo, no representa necesariamente el error que tendrá la solución obtenida.

En nuestra ejecución, el error relativo hacia atrás de la solución refinada fue aproximadamente (7.6244e-18). Al combinarlo con el número de condición se obtuvo una cota de error relativo hacia adelante de aproximadamente (4.0943e-4).


## 7. Resultados

Para evaluar la precisión de las soluciones, se comparó el resultado obtenido mediante pivoteo parcial escalado con una solución de referencia calculada utilizando mayor precisión numérica.


| Incógnita | Dígitos obtenidos | Dígitos significativos según el criterio |
|---|---:|---:|
| \(x_1\) | 12 | 12 |
| \(x_2\) | 11 | 11 |
| \(x_3\) | 9 | 9 |
| \(x_4\) | 11 | 11 |
| \(x_5\) | 12 | 12 |
| \(x_6\) | 9 | 9 |
| \(x_7\) | 12 | 12 |
| \(x_8\) | 11 | 11 |
| \(x_9\) | 12 | 12 |
| \(x_{10}\) | 12 | 12 |
| \(x_{11}\) | 11 | 11 |
| \(x_{12}\) | 12 | 12 |

Los resultados muestran que el método con pivoteo parcial escalado obtiene entre 9 y 12 dígitos significativos para las incógnitas. Las variables \(x_3\) y \(x_6\) presentan la menor precisión, mientras que las demás alcanzan entre 11 y 12 dígitos.

Por lo tanto, el método permite recuperar una cantidad considerable de cifras significativas a pesar del mal condicionamiento del sistema.

## 8. Verificación

Para comprobar la calidad de la solución se calculó el residuo del sistema:

\[
r=b-Ax
\]

Se utilizó la norma infinito del residuo para medir la mayor magnitud entre sus componentes.

La verificación en precisión extendida entregó inicialmente:
|r\| =7.6304e-10


Posteriormente, se aplicó refinamiento iterativo utilizando una factorización LU con pivoteo escalado para calcular las correcciones de la solución.

| Iteración | Norma del residuo | Norma de la corrección |
|---:|---:|---:|
| 1 | 7.6304e-10 | 5.0901e-13 |
| 2 | 1.6227e-10 | 1.8377e-16 |

Luego de dos iteraciones, el residuo disminuyó aproximadamente 4.70 veces, alcanzando:
r_refinado = 1.6227e-10

El error relativo de la solución refinada respecto de la referencia de alta precisión fue aproximadamente 5.6837e-14.

Finalmente, se comparó el resultado con la solución obtenida mediante `numpy.linalg.solve`. La diferencia máxima entre ambas soluciones fue aproximadamente 5.6333e-13, lo que sirve como comprobación adicional de los resultados.

## 9. Conclusiones

La comparación realizada demuestra que el pivoteo parcial escalado es fundamental para resolver este sistema de manera estable. Aunque ambos métodos presentan el mismo costo principal de eliminación y sustitución, el método sin pivoteo genera multiplicadores excesivamente grandes y un factor de crecimiento elevado.

En cambio, el pivoteo escalado reduce considerablemente estos valores y permite obtener entre 9 y 12 dígitos significativos en las incógnitas. Además, el refinamiento iterativo disminuye el residuo y mejora la precisión de la solución.

Por lo tanto, se considera que el pequeño costo adicional asociado a la búsqueda e intercambio de pivotes está justificado por la mejora en estabilidad numérica y exactitud.

Si el sistema tuviera dimensiones mucho mayores, por ejemplo 1000 x 1000, sería necesario considerar algoritmos más eficientes en memoria y tiempo de ejecución, además de aprovechar bibliotecas optimizadas para operaciones matriciales.

## 10. Reproducibilidad

El proyecto fue desarrollado en Python y utiliza las bibliotecas NumPy y mpmath para realizar los cálculos numéricos y las verificaciones de precisión.

**Entorno de ejecución comprobado:**
- Python 3.13.5
- NumPy 1.26.4
- mpmath 1.4.1

Para instalar las dependencias, se debe ejecutar desde la carpeta raíz del proyecto:

```bash
pip install -r requirements.txt
```

Luego, para ejecutar el programa completo:

```bash
python src/main.py
```

El programa carga los datos desde la carpeta `datos/`, ejecuta los métodos de eliminación gaussiana, calcula las soluciones, realiza las verificaciones y genera los archivos de resultados en la carpeta `resultados/`.


**Uso de herramientas de inteligencia artificial:** se utilizó asistencia de inteligencia artificial como apoyo para revisar, explicar y documentar partes del desarrollo. La implementación, ejecución y revisión de los resultados fueron realizadas por los integrantes del equipo.
