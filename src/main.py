# punto de entrada único que reproduce todo
import numpy as np
import os
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

def cargar_datos():
    ruta_archivo_actual = os.path.abspath(__file__)
    carpeta_src = os.path.dirname(ruta_archivo_actual)
    carpeta_proyecto = os.path.dirname(carpeta_src)
    ruta_csv_a = os.path.join(carpeta_proyecto, "datos", "matriz_a.csv")
    ruta_csv_b = os.path.join(carpeta_proyecto, "datos", "vector_b.csv")

    mat_a = np.genfromtxt(ruta_csv_a, delimiter=",", skip_header=1, usecols=range(1, 13), dtype=float)

    vec_b = np.genfromtxt(ruta_csv_b, delimiter=",", skip_header=1, usecols=1, dtype=float)

    return mat_a, vec_b


if __name__ == "__main__":

    np.set_printoptions(linewidth=200, suppress=False)

    mat_a, vec_b = cargar_datos()


    contador = ContadorFlops()

    A_sin, b_sin = eliminacion_gaussiana_sin_pivoteo(
        mat_a, vec_b, contador
    )

    print("\nCONTEO DE ELIMINACION SIN PIVOTEO")
    contador.mostrar_conteo()

    total = sum(
        sum(operaciones.values())
        for operaciones in contador.conteo.values()
    )

    print("\nTotal eliminacion:", total, "FLOPs")

    contador_pivoteo = ContadorFlops()

    A_piv, b_piv = eliminacion_gaussiana_con_pivoteo(
        mat_a, vec_b, contador_pivoteo
    )

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
        reduccion = float(
            historial[0]["norma_residuo"] / norma_final
        )
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

    print("\nCOTA DE ERROR HACIA ADELANTE:")
    print(condicion * error_atras)


    #GENERAR REPORTE DE CONTEO DE FLOPS
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
        archivo.write("## FLOPs por etapa de eliminacion\n\n")
        archivo.write(
            "| Paso | Sin pivoteo | Con pivoteo |\n"
        )
        archivo.write("|---|---:|---:|\n")
        for paso in range(1, len(vec_b)):
            sin = sum(contador.conteo[paso].values())
            con = sum(contador_pivoteo.conteo[paso].values())
            archivo.write(
                f"| {paso} | {sin} | {con} |\n"
            )

    print("\nReporte generado:", ruta_reporte)