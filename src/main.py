import os
import numpy as np
import csv
from mpmath import mp
from gauss import eliminacion_gaussiana_sin_pivoteo
from gauss import eliminacion_gaussiana_con_pivoteo
from gauss import sustitucion_regresiva
from conteo import ContadorFlops
from verificacion import calcular_residuo, norma_infinito
from verificacion import calcular_residuo_extendido
from gauss import factorizacion_lu_pivoteo_escalado
from gauss import resolver_con_lu
from verificacion import refinamiento_iterativo
from verificacion import calcular_condicion
from verificacion import error_hacia_atras
from verificacion import solucion_alta_precision

def cargar_datos():
    ruta_archivo_actual = os.path.abspath(__file__)
    carpeta_src = os.path.dirname(ruta_archivo_actual)
    carpeta_proyecto = os.path.dirname(carpeta_src)
    ruta_csv_a = os.path.join(carpeta_proyecto, "datos", "matriz_a.csv")
    ruta_csv_b = os.path.join(carpeta_proyecto, "datos", "vector_b.csv")
    mat_a = np.genfromtxt(
        ruta_csv_a, delimiter=",", skip_header=1,
        usecols=range(1, 13), dtype=float
    )
    vec_b = np.genfromtxt(
        ruta_csv_b, delimiter=",", skip_header=1,
        usecols=1, dtype=float
    )
    if mat_a.shape != (12, 12):
        raise ValueError(
            "La matriz A debe tener dimensiones 12x12"
        )
    if vec_b.shape != (12,):
        raise ValueError(
            "El vector b debe contener 12 elementos"
        )  
        
    if not np.all(np.isfinite(mat_a)):
        raise ValueError("La matriz A contiene valores no validos")

    if not np.all(np.isfinite(vec_b)):
        raise ValueError("El vector b contiene valores no validos")
    
    return mat_a, vec_b


def calcular_error_relativo(x, x_referencia):
    with mp.workdps(80):
        norma_referencia = max(
            abs(valor) for valor in x_referencia
        )

        error = max(
            abs(mp.mpf(float(x[i])) - x_referencia[i])
            for i in range(len(x))
        )

        if norma_referencia == 0:
            return error

        return error / norma_referencia


def calcular_cifras_significativas(aproximacion, referencia):
    with mp.workdps(80):
        aproximacion = mp.mpf(float(aproximacion))

        if referencia == 0:
            return abs(aproximacion), 0

        error = abs(aproximacion - referencia) / abs(referencia)

        if error == 0:
            return error, 16

        digitos = max(
            0,
            int(mp.floor(-mp.log10(2 * error)))
        )

        return error, min(digitos, 16)


if __name__ == "__main__":
    np.set_printoptions(linewidth=200, suppress=False)

    mat_a, vec_b = cargar_datos()

    contador = ContadorFlops()

    # Eliminacion sin pivoteo
    A_sin, b_sin, multiplicador_sin, crecimiento_sin = (
        eliminacion_gaussiana_sin_pivoteo(
            mat_a, vec_b, contador
        )
    )

    print("\nMULTIPLICADOR MAXIMO SIN PIVOTEO:")
    print(multiplicador_sin)

    print("\nFACTOR DE CRECIMIENTO SIN PIVOTEO:")
    print(crecimiento_sin)

    total = sum(
        sum(operaciones.values())
        for operaciones in contador.conteo.values()
    )

    print("\nTotal eliminacion:", total, "FLOPs")

    # Resolver el sistema sin pivoteo
    x_sin = sustitucion_regresiva(A_sin, b_sin)

    print("\nSOLUCION SIN PIVOTEO:")
    print(x_sin)

    # Eliminacion con pivoteo
    contador_pivoteo = ContadorFlops()

    traza_pivoteo = []

    A_piv, b_piv, multiplicador_con, crecimiento_con = (
        eliminacion_gaussiana_con_pivoteo(
            mat_a, vec_b, contador_pivoteo, traza=traza_pivoteo
        )
    )

    print("\nMULTIPLICADOR MAXIMO CON PIVOTEO:")
    print(multiplicador_con)

    print("\nFACTOR DE CRECIMIENTO CON PIVOTEO:")
    print(crecimiento_con)

    print("\nCONTEO CON PIVOTEO")
    contador_pivoteo.mostrar_conteo()


    total_eliminacion = sum(
        sum(operaciones.values())
        for operaciones in contador_pivoteo.conteo.values()
    )

    print(
        "\nTotal eliminacion con pivoteo:",
        total_eliminacion,
        "FLOPs"
    )

    x = sustitucion_regresiva(
        A_piv, b_piv, contador_pivoteo
    )

    print("\nSOLUCION DEL SISTEMA:")
    print(x)

    print("\nCOMPARACION DE SOLUCIONES:")

    for i in range(len(x)):
        print(
            f"x{i+1}: "
            f"sin pivoteo = {x_sin[i]:.16e} | "
            f"con pivoteo = {x[i]:.16e}"
        )

    diferencia_soluciones = np.max(np.abs(x_sin - x))

    print("\nDIFERENCIA MAXIMA ENTRE SOLUCIONES:")
    print(diferencia_soluciones)

    # Solucion de referencia con 80 digitos
    carpeta_src = os.path.dirname(os.path.abspath(__file__))
    carpeta_proyecto = os.path.dirname(carpeta_src)

    ruta_a = os.path.join(
        carpeta_proyecto, "datos", "matriz_a.csv"
    )
    ruta_b = os.path.join(
        carpeta_proyecto, "datos", "vector_b.csv"
    )

    x_referencia = solucion_alta_precision(ruta_a, ruta_b)

    print("\nSOLUCION DE REFERENCIA EN ALTA PRECISION:")
    for i in range(len(x_referencia)):
        print(f"x{i+1} = {mp.nstr(x_referencia[i], 25)}")

    # Comparar ambas soluciones con la referencia
    error_sin = calcular_error_relativo(x_sin, x_referencia)
    error_con = calcular_error_relativo(x, x_referencia)

    print("\nERROR RELATIVO SIN PIVOTEO:")
    print(mp.nstr(error_sin, 16))

    print("\nERROR RELATIVO CON PIVOTEO:")
    print(mp.nstr(error_con, 16))
    
    
    print("\nCIFRAS SIGNIFICATIVAS POR INCOGNITA:")

    for i in range(len(x)):
        error_individual, digitos = calcular_cifras_significativas(
            x[i], x_referencia[i]
        )

        print(
            f"x{i+1}: "
            f"error = {mp.nstr(error_individual, 6)} | "
            f"digitos = {digitos}"
        )


    print("\nCONTEO DE SUSTITUCION REGRESIVA")
    print(contador_pivoteo.conteo["Sustitucion"])

    total_sustitucion = sum(
        contador_pivoteo.conteo["Sustitucion"].values()
    )

    print(
        "\nTotal sustitucion:",
        total_sustitucion,
        "FLOPs"
    )

    contador_pivoteo.mostrar_pivoteo()

    total_pivoteo = sum(
        sum(operaciones.values())
        for operaciones in contador_pivoteo.conteo.values()
    )
    total_con_pivoteo = (
        total_pivoteo
        + contador_pivoteo.costo_pivoteo["divisiones"]
    )
    print(
        "\nTOTAL SIN BUSQUEDA DE PIVOTE:",
        total_pivoteo,
        "FLOPs"
    )
    print(
        "\nTOTAL CON DIVISIONES DE BUSQUEDA:",
        total_con_pivoteo,
        "FLOPs"
    )

    residuo = calcular_residuo(mat_a, vec_b, x)
    norma_residuo = norma_infinito(residuo)

    print("\nRESIDUO:")
    print(residuo)

    print("\nNORMA INFINITO DEL RESIDUO:")
    print(norma_residuo)

    # Residuo con precision extendida
    residuo_ext = calcular_residuo_extendido(
        mat_a, vec_b, x
    )

    norma_ext = max(abs(valor) for valor in residuo_ext)

    print("\nRESIDUO EN PRECISION EXTENDIDA:")
    print(residuo_ext)

    print("\nNORMA INFINITO EXTENDIDA:")
    print(norma_ext)

    P, L, U = factorizacion_lu_pivoteo_escalado(mat_a)

    error_lu = np.max(np.abs(P @ mat_a - L @ U))

    print("\nVERIFICACION FACTORIZACION LU:")
    print("Maximo error absoluto PA-LU:", error_lu)

    # Resolver utilizando LU
    x_lu = resolver_con_lu(P, L, U, vec_b)

    print("\nSOLUCION MEDIANTE LU:")
    print(x_lu)

    diferencia = np.max(np.abs(x - x_lu))

    print("\nDIFERENCIA ENTRE GAUSS Y LU:")
    print(diferencia)

    x_refinada, historial = refinamiento_iterativo(
        mat_a, vec_b, x, P, L, U, max_iter=5
    )

    print("\nREFINAMIENTO ITERATIVO:")

    for registro in historial:
        print(
            "Iteracion:", registro["iteracion"],
            "| Residuo:", registro["norma_residuo"],
            "| Correccion:", registro["norma_correccion"]
        )

    print("\nSOLUCION REFINADA:")
    print(x_refinada)
    
    error_refinado = calcular_error_relativo(x_refinada, x_referencia)

    print("\nERROR RELATIVO DE LA SOLUCION REFINADA:")
    print(mp.nstr(error_refinado, 16))
    
    # Solucion de control mediante NumPy
    x_numpy = np.linalg.solve(mat_a, vec_b)

    diferencia_numpy = np.max(
        np.abs(x_refinada - x_numpy)
    )

    error_numpy = calcular_error_relativo(x_numpy, x_referencia)

    print("\nSOLUCION NUMPY:")
    print(x_numpy)

    print("\nDIFERENCIA MAXIMA REFINAMIENTO VS NUMPY:")
    print(diferencia_numpy)

    print("\nERROR RELATIVO NUMPY:")
    print(mp.nstr(error_numpy, 16))

    print("\nDIFERENCIA RESPECTO A SOLUCION INICIAL:")
    print(np.max(np.abs(x_refinada - x)))

    residuo_final = calcular_residuo_extendido(
        mat_a, vec_b, x_refinada
    )

    norma_final = max(abs(valor) for valor in residuo_final)

    print("\nNORMA DEL RESIDUO FINAL REFINADO:")
    print(norma_final)

    print("\nREDUCCION DEL RESIDUO:")

    if norma_final != 0:
        reduccion = float(norma_ext / norma_final)
    elif norma_ext == 0:
        reduccion = 1.0
    else:
        reduccion = float("inf")

    print(reduccion)

    condicion = calcular_condicion(mat_a)

    print("\nNUMERO DE CONDICION:")
    print(condicion)

    print("\nDIGITOS POTENCIALMENTE PERDIDOS:")
    print(np.log10(condicion))

    error_atras = error_hacia_atras(
        mat_a, vec_b, x_refinada, norma_final
    )

    print("\nERROR HACIA ATRAS RELATIVO:")
    print(error_atras)

    producto_condicion_error = condicion * error_atras

    if producto_condicion_error < 1:
        cota_error_adelante = (
            producto_condicion_error /
            (1 - producto_condicion_error)
        )
    else:
        cota_error_adelante = float("inf")

    print("\nCOTA RELATIVA DE ERROR HACIA ADELANTE:")
    print(cota_error_adelante)


    # Generar reporte de conteo de FLOPs
    carpeta_src = os.path.dirname(os.path.abspath(__file__))
    carpeta_proyecto = os.path.dirname(carpeta_src)
    carpeta_resultados = os.path.join(
        carpeta_proyecto, "resultados"
    )
    os.makedirs(carpeta_resultados, exist_ok=True)
    ruta_reporte = os.path.join(
        carpeta_resultados, "conteo_flops.md"
    )

    with open(ruta_reporte, "w", encoding="utf-8") as archivo:
        archivo.write("# Conteo de FLOPs\n\n")
        archivo.write("## Resultados generales\n\n")
        archivo.write("| Operacion | FLOPs |\n")
        archivo.write("|---|---:|\n")
        archivo.write(
            f"| Eliminacion sin pivoteo | {total} |\n"
        )
        archivo.write(
            f"| Eliminacion con pivoteo | {total_eliminacion} |\n"
        )
        archivo.write(
            f"| Sustitucion regresiva | {total_sustitucion} |\n"
        )
        archivo.write(
            f"| Total sin busqueda de pivote | {total_pivoteo} |\n"
        )
        archivo.write(
            f"| Total con divisiones de busqueda | {total_con_pivoteo} |\n\n"
        )
        archivo.write("## Sobrecosto del pivoteo\n\n")
        archivo.write("| Operacion | Cantidad |\n")
        archivo.write("|---|---:|\n")
        for nombre, cantidad in contador_pivoteo.costo_pivoteo.items():
            archivo.write(
                f"| {nombre.capitalize()} | {cantidad} |\n"
            )
        archivo.write("\n")
        archivo.write(
            "Las comparaciones y los intercambios de filas "
            "se reportan por separado y no se incluyen "
            "en el total de FLOPs aritmeticos.\n\n"
        )
        archivo.write(
            "El calculo inicial de las escalas de fila "
            "no esta incluido en este conteo.\n\n"
        )
        
        archivo.write(
        "El conteo corresponde a las operaciones aritmeticas "
        "registradas durante la eliminacion y sustitucion. "
        "No representa el costo computacional total del programa.\n\n"
        )
        
        archivo.write("## FLOPs por etapa de eliminacion\n\n")
        archivo.write(
            "| Paso | Sin pivoteo Mult./Div. | Sin pivoteo Sumas/Restas | "
            "Sin pivoteo Total | Con pivoteo Mult./Div. | "
            "Con pivoteo Sumas/Restas | Con pivoteo Total |\n"
        )
        archivo.write("|---|---:|---:|---:|---:|---:|---:|\n")
        desglose_sin = contador.obtener_desglose()
        desglose_con = contador_pivoteo.obtener_desglose()
        total_mult_div_sin = 0
        total_sum_rest_sin = 0
        total_mult_div_con = 0
        total_sum_rest_con = 0
        for paso in range(1, len(vec_b)):
            sin = desglose_sin[paso]
            con = desglose_con[paso]
            total_mult_div_sin += sin["mult_div"]
            total_sum_rest_sin += sin["sum_rest"]
            total_mult_div_con += con["mult_div"]
            total_sum_rest_con += con["sum_rest"]
            archivo.write(
                f"| {paso} "
                f"| {sin['mult_div']} | {sin['sum_rest']} | {sin['total']} "
                f"| {con['mult_div']} | {con['sum_rest']} | {con['total']} |\n"
            )
        archivo.write(
            f"| **Total** "
            f"| **{total_mult_div_sin}** | **{total_sum_rest_sin}** "
            f"| **{total_mult_div_sin + total_sum_rest_sin}** "
            f"| **{total_mult_div_con}** | **{total_sum_rest_con}** "
            f"| **{total_mult_div_con + total_sum_rest_con}** |\n"
        )

    print("\nReporte generado:", ruta_reporte)

    # Guardar soluciones y cifras significativas
    ruta_solucion = os.path.join(
        carpeta_resultados, "solucion.csv"
    )

    with open(ruta_solucion, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        escritor.writerow([
            "incognita",
            "sin_pivoteo",
            "con_pivoteo",
            "refinada",
            "referencia",
            "error_relativo_con_pivoteo",
            "digitos_significativos_con_pivoteo"
        ])

        for i in range(len(x)):
            referencia = x_referencia[i]

            error_individual, digitos = calcular_cifras_significativas(
                x[i], referencia
            )

            escritor.writerow([
                f"x{i+1}",
                f"{x_sin[i]:.16e}",
                f"{x[i]:.16e}",
                f"{x_refinada[i]:.16e}",
                mp.nstr(referencia, 25),
                mp.nstr(error_individual, 16),
                digitos
            ])

    print("\nArchivo generado:", ruta_solucion)
    
    
    # Guardar resultados de verificacion numerica
    ruta_residuo = os.path.join(
        carpeta_resultados, "residuo.txt"
    )

    with open(ruta_residuo, "w", encoding="utf-8") as archivo:
        archivo.write("VERIFICACION NUMERICA DEL SISTEMA\n")
        archivo.write("=" * 40 + "\n\n")

        archivo.write("RESIDUO INICIAL\n")
        archivo.write(f"Norma infinito: {norma_residuo:.16e}\n\n")

        archivo.write("RESIDUO EN PRECISION EXTENDIDA\n")
        archivo.write(f"Norma infinito: {norma_ext:.16e}\n\n")

        archivo.write("REFINAMIENTO ITERATIVO\n")

        for registro in historial:
            archivo.write(
                f"Iteracion {registro['iteracion']}: "
                f"residuo = {registro['norma_residuo']:.16e}, "
                f"correccion = {registro['norma_correccion']:.16e}\n"
            )

        archivo.write("\nRESULTADO FINAL\n")
        archivo.write(f"Residuo refinado: {norma_final:.16e}\n")
        archivo.write(f"Reduccion del residuo: {reduccion:.6f}\n")
        archivo.write(
            f"Error relativo refinado: "
            f"{mp.nstr(error_refinado, 16)}\n\n"
        )

        archivo.write("CONDICIONAMIENTO\n")
        archivo.write(f"Numero de condicion infinito: {condicion:.16e}\n")
        archivo.write(f"Error hacia atras: {error_atras:.16e}\n")
        archivo.write(
            f"Cota de error hacia adelante: "
            f"{cota_error_adelante:.16e}\n\n"
        )

        archivo.write("COMPARACION CON NUMPY\n")
        archivo.write(
            f"Diferencia maxima: {diferencia_numpy:.16e}\n"
        )
        archivo.write(
            f"Error relativo NumPy: "
            f"{mp.nstr(error_numpy, 16)}\n"
        )

    print("\nArchivo generado:", ruta_residuo)
    
    
    # Generar traza de eliminacion con pivoteo
    ruta_traza = os.path.join(
        carpeta_resultados, "traza_eliminacion.txt"
    )

    with open(ruta_traza, "w", encoding="utf-8") as archivo:
        archivo.write("TRAZA DE ELIMINACION GAUSSIANA\n")
        archivo.write("Metodo: pivoteo parcial escalado\n")
        archivo.write("=" * 50 + "\n\n")

        for registro in traza_pivoteo:
            archivo.write(
                f"PASO {registro['paso']}\n"
            )

            archivo.write(
                f"Fila pivote seleccionada: "
                f"{registro['fila_pivote']}\n"
            )

            archivo.write(
                f"Intercambio de filas: "
                f"{'Si' if registro['intercambio'] else 'No'}\n"
            )

            archivo.write(
                f"Valor del pivote: "
                f"{registro['pivote']:.16e}\n\n"
            )

            archivo.write("Matriz resultante:\n")
            archivo.write(
                np.array2string(
                    registro["matriz"],
                    precision=16,
                    suppress_small=False,
                    threshold=np.inf,
                    max_line_width=200
                )
            )

            archivo.write("\n\nVector resultante:\n")
            archivo.write(
                np.array2string(
                    registro["vector"],
                    precision=16,
                    suppress_small=False,
                    threshold=np.inf,
                    max_line_width=200
                )
            )

            archivo.write("\n\n" + "-" * 50 + "\n\n")

    print("\nArchivo generado:", ruta_traza)

