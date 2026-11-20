# Informe Lab 3: Eliminación gaussiana con mínimo costo operacional y máxima exactitud de mantisa

## 1. Identificación:
**Estudiantes:** Felipe Araya Díaz y Mariana Morales Muñoz  
**Asignatura:** Computación Numérica  
**Fecha de entrega:** 21-11-2026  
**Enlace al repositorio:** https://github.com/MedoFantasmas/cn-parcial-gauss12-araya-morales


## 2. Planteamiento
------> el sistema, sus escalas de fila y qué lo hace costoso de resolver. <----------

## 3. Estrategia de eliminación

------> el orden de pasos elegido y por qué no excede el mínimo teórico; cómo se reutilizan los multiplicadores. <----------

## 4. Conteo de operaciones

------> tabla paso a paso (11 pasos) con multiplicaciones/divisiones y sumas/restas; total; comparación con la cota; convención declarada. <----------

| i | Operación |
| ---- | ----- |
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
| 6 |
| 7 |
| 8 |
| 9 |
| 10 |
| 11 |

## 5. Análisis de mantisa y pivoteo

------> multiplicadores máximos, factor de crecimiento, bits perdidos, comparación de las dos corridas. Debe aparecer el argumento de por qué el pivote a(1,1) es inaceptable. <----------

## 6. Condicionamiento

------> estimación de κ(A), cota κ·ε y conclusión sobre cuántos dígitos son recuperables, incluida la discusión de por qué la cota resulta pesimista aquí. <----------


## 7. Resultados

------> tabla de las 12 incógnitas con sus dígitos reportados y los dígitos afirmados como correctos. <----------

| xi | Dígito reportado | Dígito correcto |
| ---- | ----- | ---- |
| x1 |  |  |
| x2 |  |  |
| x3 |  |  |
| x4 |  |  |
| x5 |  |  |
| x6 |  |  |
| x7 |  |  |
| x8 |  |  |
| x9 |  |  |
| x10 |  |  |
| x11 |  |  |
| x12 |  |  |

## 8. Verificación

------> residuo en precisión extendida, norma infinito, refinamiento iterativo, control con biblioteca. <----------


## 9. Conclusiones

------> el compromiso costo/exactitud que se eligió y por qué; qué haría distinto con n = 1000. <----------



## 10. Reprucibilidad

------> versión de Python, de las librerías, comando ejecutado. <----------

