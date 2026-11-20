import numpy as np

def eliminacion_gaussiana_sin_pivoteo(A, b, contador=None):
    A = A.copy().astype(float)
    b = b.copy().astype(float)
    n = len(b)

    for k in range(n - 1):
        pivote = A[k, k]
        paso = k + 1
        for i in range(k + 1, n):
            # Calcular multiplicador
            if contador is not None:
                m = contador.dividir(A[i, k], pivote, paso)
            else:
                m = A[i, k] / pivote
            # Actualizar matriz
            for j in range(k + 1, n):
                if contador is not None:
                    producto = contador.multiplicar(
                        m, A[k, j], paso
                    )
                    A[i, j] = contador.restar(
                        A[i, j], producto, paso
                    )
                else:
                    A[i, j] = A[i, j] - m * A[k, j]
            # Actualizar vector b
            if contador is not None:
                producto = contador.multiplicar(
                    m, b[k], paso
                )
                b[i] = contador.restar(
                    b[i], producto, paso
                )
            else:
                b[i] = b[i] - m * b[k]
            A[i, k] = 0
    return A, b


def eliminacion_gaussiana_con_pivoteo(A, b, contador=None):
    A = A.copy().astype(float)
    b = b.copy().astype(float)
    n = len(b)

    escalas = np.max(np.abs(A), axis=1)

    for k in range(n - 1):
        paso = k + 1
        # Seleccionar fila pivote
        ratios = np.abs(A[k:, k]) / escalas[k:]
        fila_pivote = k + np.argmax(ratios)
        if contador is not None:
            contador.registrar_pivoteo(
                divisiones=n-k,
                comparaciones=n-k-1
            )
        # Intercambiar filas
        if fila_pivote != k:
            if contador is not None:
                contador.registrar_pivoteo(intercambios=1)
            A[[k, fila_pivote]] = A[[fila_pivote, k]]
            b[[k, fila_pivote]] = b[[fila_pivote, k]]
            escalas[[k, fila_pivote]] = escalas[[fila_pivote, k]]
        pivote = A[k, k]
        for i in range(k + 1, n):
            if contador is not None:
                m = contador.dividir(A[i, k], pivote, paso)
            else:
                m = A[i, k] / pivote
            for j in range(k + 1, n):
                if contador is not None:
                    producto = contador.multiplicar(
                        m, A[k, j], paso
                    )
                    A[i, j] = contador.restar(
                        A[i, j], producto, paso
                    )
                else:
                    A[i, j] = A[i, j] - m * A[k, j]
            if contador is not None:
                producto = contador.multiplicar(
                    m, b[k], paso
                )
                b[i] = contador.restar(
                    b[i], producto, paso
                )
            else:
                b[i] = b[i] - m * b[k]
            A[i, k] = 0
    return A, b

def sustitucion_regresiva(A, b, contador=None):
    n = len(b)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            if contador is not None:
                producto = contador.multiplicar(
                    A[i, j], x[j], "Sustitucion"
                )
                suma = contador.sumar(
                    suma, producto, "Sustitucion"
                )
            else:
                suma += A[i, j] * x[j]
        if contador is not None:
            diferencia = contador.restar(
                b[i], suma, "Sustitucion"
            )
            x[i] = contador.dividir(
                diferencia, A[i, i], "Sustitucion"
            )
        else:
            x[i] = (b[i] - suma) / A[i, i]
    return x
