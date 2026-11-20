import numpy as np

from decimal import Decimal, localcontext

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

def calcular_residuo(A, b, x):
    residuo = b - A @ x
    return residuo

def norma_infinito(vector):
    return np.max(np.abs(vector))

def calcular_residuo_extendido(A, b, x):
    A_ext = np.asarray(A, dtype=np.longdouble)
    b_ext = np.asarray(b, dtype=np.longdouble)
    x_ext = np.asarray(x, dtype=np.longdouble)

    residuo = b_ext - A_ext @ x_ext

    return residuo


def refinamiento_iterativo(A, b, x_inicial, P, L, U, max_iter=5):
    from gauss import resolver_con_lu

    x = np.array(x_inicial, dtype=float, copy=True)
    historial = []

    for iteracion in range(1, max_iter + 1):
        # Residuo calculado con Decimal
        residuo_ext = calcular_residuo_extendido(A, b, x)
        norma_residuo = max(abs(valor) for valor in residuo_ext)
        # Resolver A * delta = residuo usando LU existente
        residuo_float = np.array(
            [float(valor) for valor in residuo_ext],
            dtype=float
        )
        delta = resolver_con_lu(P, L, U, residuo_float)
        x_nueva = x + delta
        norma_delta = np.max(np.abs(delta))
        historial.append({
            "iteracion": iteracion,
            "norma_residuo": norma_residuo,
            "norma_correccion": norma_delta
        })
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