import numpy as np

def eliminacion_gaussiana_sin_pivoteo(A, b):
    A = A.copy().astype(float)
    b = b.copy().astype(float)
    n = len(b)

    for k in range(n - 1):
        pivote = A[k, k]
        for i in range(k + 1, n):
            m = A[i, k] / pivote
            for j in range(k + 1, n):
                A[i, j] = A[i, j] - m * A[k, j]
            b[i] = b[i] - m * b[k]
            A[i, k] = 0
    return A, b

def eliminacion_gaussiana_con_pivoteo(A, b):
    A = A.copy().astype(float)
    b = b.copy().astype(float)
    n = len(b)

    escalas = np.max(np.abs(A), axis=1) # Escalas de cada fila

    for k in range(n - 1):
        ratios = np.abs(A[k:, k]) / escalas[k:] # Buscar la mejor fila pivote
        fila_pivote = k + np.argmax(ratios)

        if fila_pivote != k: # Intercambiar filas si es necesario
            A[[k, fila_pivote]] = A[[fila_pivote, k]]
            b[[k, fila_pivote]] = b[[fila_pivote, k]]
            escalas[[k, fila_pivote]] = escalas[[fila_pivote, k]]

        pivote = A[k, k] #PROCEDIMIENTO NORMAL
        for i in range(k + 1, n):
            m = A[i, k] / pivote
            for j in range(k + 1, n):
                A[i, j] = A[i, j] - m * A[k, j]
            b[i] = b[i] - m * b[k]
            A[i, k] = 0
    return A, b

def sustitucion_regresiva(A, b): # RECIBE MATRIZ A TRIANGULADA
    n = len(b)
    x = np.zeros(n)

    for i in range(n - 1, -1, -1):
        suma = 0

        for j in range(i + 1, n):
            suma += A[i, j] * x[j]

        x[i] = (b[i] - suma) / A[i, i]

    return x
