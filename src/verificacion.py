import numpy as np
import csv

from mpmath import mp
from decimal import Decimal, localcontext
from gauss import resolver_con_lu

def calcular_residuo(A, b, x):
    residuo = b - A @ x
    return residuo


def calcular_residuo_extendido(A, b, x):
    with localcontext() as ctx:
        ctx.prec = 50
        residuo = []
        for i in range(len(b)):
            suma = Decimal(0)
            for j in range(len(x)):
                a_ij = Decimal.from_float(float(A[i, j]))
                x_j = Decimal.from_float(float(x[j]))
                suma += a_ij * x_j
            b_i = Decimal.from_float(float(b[i]))
            residuo.append(b_i - suma)
        return residuo


def norma_infinito(vector):
    return np.max(np.abs(vector))


def refinamiento_iterativo(A, b, x_inicial, P, L, U, max_iter=5):
    x = np.array(x_inicial, dtype=float, copy=True)
    historial = []
    for iteracion in range(1, max_iter + 1):
        # Calcular residuo en precision extendida
        residuo_ext = calcular_residuo_extendido(A, b, x)
        norma_residuo = max(
            abs(valor) for valor in residuo_ext
        )
        # Convertir residuo a doble precision
        residuo_float = np.array(
            [float(valor) for valor in residuo_ext],
            dtype=float
        )
        # Resolver A * delta = residuo
        delta = resolver_con_lu(P, L, U, residuo_float)
        x_nueva = x + delta
        norma_delta = np.max(np.abs(delta))
        historial.append({
            "iteracion": iteracion,
            "norma_residuo": norma_residuo,
            "norma_correccion": norma_delta
        })
        # Detener si la correccion no modifica la solucion
        if np.array_equal(x_nueva, x):
            print(
                f"\nRefinamiento detenido en iteracion {iteracion}: "
                "la solucion ya no cambia en doble precision."
            )
            break
        x = x_nueva
    return x, historial


def calcular_condicion(A):
    return np.linalg.cond(A, p=np.inf)


def error_hacia_atras(A, b, x, norma_residuo):
    norma_A = np.linalg.norm(A, ord=np.inf)
    norma_x = np.linalg.norm(x, ord=np.inf)
    norma_b = np.linalg.norm(b, ord=np.inf)
    denominador = norma_A * norma_x + norma_b
    if denominador == 0:
        return 0.0 if norma_residuo == 0 else np.inf
    return float(norma_residuo) / denominador


def solucion_alta_precision(ruta_a, ruta_b):
    with mp.workdps(80):
        # Leer matriz A conservando los decimales originales
        with open(ruta_a, "r", encoding="utf-8-sig") as archivo:
            lector = csv.reader(archivo)
            next(lector)
            datos_a = [
                [mp.mpf(valor.strip()) for valor in fila[1:13]]
                for fila in lector
                if fila
            ]
        # Leer vector b conservando los decimales originales
        with open(ruta_b, "r", encoding="utf-8-sig") as archivo:
            lector = csv.reader(archivo)
            next(lector)
            datos_b = [
                mp.mpf(fila[1].strip())
                for fila in lector
                if fila
            ]
        A = mp.matrix(datos_a)
        b = mp.matrix(datos_b)
        # Resolver con precision extendida
        x_referencia = mp.lu_solve(A, b)
        return x_referencia
