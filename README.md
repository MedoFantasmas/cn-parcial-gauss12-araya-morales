# El pivote (cn-parcial-gauss12-araya-morales)

Resolución de sistema lineal denso de 12 incógnitas haciendo uso de eliminación gaussiana, buscando equilibrar un mínimo costo operacional con una máxima exactitud de mantisa.

### Autores: Felipe Araya - Mariana Morales
### Asignatura: Computación Numérica

## Requisitos
* Python ver. 3.14.3
* numpy 1.26.4
* mpmath 1.4.1
Instalar haciendo uso del comando: pip install -r requirements.txt

## Ejecución
Basta con ejecutar python src/main.py. Ejecutar resulta en la generación de los archivos en la carpeta /resultados:
* conteo_flops.md
* solucion.csv
* residuo.txt
* traza_eliminacion.txt

## Estructura de carpetas
La estructura de las carpetas se encuentra de la siguiente forma:

cn-parcial-gauss12-araya-morales/\
├── datos/\
│   ├── matriz_a.csv\
│   └── vector_b.csv\
├── resultados/\
│   ├── conteo_flops.md\
│   ├── residuo.txt\
│   ├── solucion.csv\
│   └── traza_eliminacion.txt\
├── src/\
│   ├── conteo.py\
│   ├── gauss.py\
│   ├── main.py\
│   └── verificacion.py\
├── informe.md\
├── README.md\
├── requirements.txt\
├── .gitignore\
└── .gitattributes

## Resumen del resultado

Solución del sistema de 12 incógnitas mediante eliminación gaussiana con pivoteo parcial escalado y refinamiento iterativo.

| Incógnita | Valor (10 dígitos) |
|---|---:|
| x1 | 0.7384915627 |
| x2 | -1.205937417 |
| x3 | 0.0043871952 |
| x4 | -0.0917264538 |
| x5 | 2.846109372 |
| x6 | -0.0062815409 |
| x7 | 1.473820592 |
| x8 | -0.0384927164 |
| x9 | 0.9152648037 |
| x10 | -2.607139485 |
| x11 | 0.0518736294 |
| x12 | -1.084937163 |

**Total de operaciones:** 1443 FLOPs (incluyendo las divisiones de búsqueda de pivote).

**Norma infinito del residuo final refinado:** (1.6227 \times 10^{-10}).

## Informe

[Aquí puede consultar el informe del laboratorio](informe.md).

## Licencia y uso académico

Este proyecto fue desarrollado con fines académicos para la asignatura Computación Numérica. Su código y documentación se presentan como material de estudio y evaluación del laboratorio. No se establece una licencia de software para su redistribución o uso comercial.
