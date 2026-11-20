import numpy as np

def eliminacion_gaussiana_sin_pivoteo(A, b, contador=None):
    A = A.copy().astype(float)
    b = b.copy().astype(float)
    n = len(b)

    multiplicador_maximo = 0.0

    # Valor maximo de la matriz original
    maximo_inicial = np.max(np.abs(A))
    maximo_proceso = maximo_inicial

    for k in range(n - 1):
        pivote = A[k, k]
        paso = k + 1
        for i in range(k + 1, n):
            # Calcular multiplicador
            if contador is not None:
                m = contador.dividir(A[i, k], pivote, paso)
            else:
                m = A[i, k] / pivote
            # Registrar multiplicador maximo
            multiplicador_maximo = max(
                multiplicador_maximo, abs(m)
            )
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
        # Registrar el maximo despues de cada etapa
        maximo_proceso = max(
            maximo_proceso,
            np.max(np.abs(A))
        )
    factor_crecimiento = maximo_proceso / maximo_inicial
    return A, b, multiplicador_maximo, factor_crecimiento


def eliminacion_gaussiana_con_pivoteo(A, b, contador=None, traza=None):
    A = A.copy().astype(float)
    b = b.copy().astype(float)
    n = len(b)

    escalas = np.max(np.abs(A), axis=1)

    multiplicador_maximo = 0.0
    maximo_inicial = np.max(np.abs(A))
    maximo_proceso = maximo_inicial

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
        # Registrar seleccion del pivote
        if traza is not None:
            traza.append({
                "paso": paso,
                "fila_pivote": int(fila_pivote + 1),
                "intercambio": bool(fila_pivote != k)
            })
        # Intercambiar filas
        if fila_pivote != k:
            if contador is not None:
                contador.registrar_pivoteo(intercambios=1)
            A[[k, fila_pivote]] = A[[fila_pivote, k]]
            b[[k, fila_pivote]] = b[[fila_pivote, k]]
            escalas[[k, fila_pivote]] = escalas[[fila_pivote, k]]
        pivote = A[k, k]
        for i in range(k + 1, n):
            # Calcular multiplicador
            if contador is not None:
                m = contador.dividir(A[i, k], pivote, paso)
            else:
                m = A[i, k] / pivote
            # Registrar multiplicador maximo
            multiplicador_maximo = max(
                multiplicador_maximo, abs(m)
            )
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
        # Registrar el maximo al finalizar cada etapa
        maximo_proceso = max(
            maximo_proceso,
            np.max(np.abs(A))
        )
        # Guardar estado del sistema al finalizar la etapa
        if traza is not None:
            traza[-1]["pivote"] = float(pivote)
            traza[-1]["matriz"] = A.copy()
            traza[-1]["vector"] = b.copy()
    # Calcular factor de crecimiento
    factor_crecimiento = maximo_proceso / maximo_inicial
    return A, b, multiplicador_maximo, factor_crecimiento

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

def factorizacion_lu_pivoteo_escalado(A):
    A = A.copy().astype(float)
    n = A.shape[0]

    L = np.eye(n)
    U = A.copy()
    P = np.eye(n)

    escalas = np.max(np.abs(A), axis=1)

    for k in range(n - 1):
        ratios = np.abs(U[k:, k]) / escalas[k:]
        fila_pivote = k + np.argmax(ratios)
        if fila_pivote != k:
            U[[k, fila_pivote]] = U[[fila_pivote, k]]
            P[[k, fila_pivote]] = P[[fila_pivote, k]]
            escalas[[k, fila_pivote]] = escalas[[fila_pivote, k]]
            if k > 0:
                L[[k, fila_pivote], :k] = L[[fila_pivote, k], :k]
        pivote = U[k, k]
        if pivote == 0:
            raise ValueError("Pivote nulo: no se puede continuar")
        for i in range(k + 1, n):
            m = U[i, k] / pivote
            L[i, k] = m
            for j in range(k + 1, n):
                U[i, j] -= m * U[k, j]
            U[i, k] = 0
    if U[n - 1, n - 1] == 0:
        raise ValueError("La matriz es singular")
    return P, L, U

def sustitucion_progresiva(L, b):
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        suma = 0
        for j in range(i):
            suma += L[i, j] * y[j]
        y[i] = (b[i] - suma) / L[i, i]
    return y

def resolver_con_lu(P, L, U, b):
    b_permutado = P @ b
    y = sustitucion_progresiva(L, b_permutado)
    x = sustitucion_regresiva(U, y)
    return x
