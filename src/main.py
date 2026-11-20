# punto de entrada único que reproduce todo
import numpy as np
import os
from gauss import eliminacion_gaussiana_sin_pivoteo
from gauss import eliminacion_gaussiana_con_pivoteo
from gauss import sustitucion_regresiva
from conteo import ContadorFlops

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
    np.set_printoptions(linewidth=200, suppress=False) # ESTO HACE QUE CADA FILA SE IMPRIMA EN UNA SOLA LINEA EN LA TERMINAL

    mat_a, vec_b = cargar_datos()
    
    # Prueba del contador sin pivoteo
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



    # Conteo con pivoteo parcial escalado
    contador_pivoteo = ContadorFlops()

    A_piv, b_piv = eliminacion_gaussiana_con_pivoteo(
        mat_a, vec_b, contador_pivoteo
    )

    
    # Conteo de eliminacion con pivoteo
    print("\nCONTEO CON PIVOTEO")
    contador_pivoteo.mostrar_conteo()

    total_eliminacion = sum(
        sum(operaciones.values())
        for operaciones in contador_pivoteo.conteo.values()
    )

    print("\nTotal eliminacion con pivoteo:",
          total_eliminacion, "FLOPs")

    # Sustitucion regresiva
    x = sustitucion_regresiva(A_piv, b_piv, contador_pivoteo)

    print("\nSOLUCION DEL SISTEMA:")
    print(x)

    # Conteo de sustitucion regresiva
    print("\nCONTEO DE SUSTITUCION REGRESIVA")
    print(contador_pivoteo.conteo["Sustitucion"])

    total_sustitucion = sum(
        contador_pivoteo.conteo["Sustitucion"].values()
    )

    print("\nTotal sustitucion:", total_sustitucion, "FLOPs")

    # Sobrecosto del pivoteo
    contador_pivoteo.mostrar_pivoteo()

    # Total de operaciones aritmeticas
    total_pivoteo = sum(
        sum(operaciones.values())
        for operaciones in contador_pivoteo.conteo.values()
    )

    print("\nTOTAL SIN BUSQUEDA DE PIVOTE:",
          total_pivoteo, "FLOPs")

    print("\nTOTAL CON DIVISIONES DE BUSQUEDA:",
          total_pivoteo
          + contador_pivoteo.costo_pivoteo["divisiones"],
          "FLOPs")
    
    
    # Guardar resultados del conteo en Markdown
    carpeta_src = os.path.dirname(os.path.abspath(__file__))
    carpeta_proyecto = os.path.dirname(carpeta_src)

    carpeta_resultados = os.path.join(carpeta_proyecto, "resultados")
    os.makedirs(carpeta_resultados, exist_ok=True)

    ruta_reporte = os.path.join(
        carpeta_resultados, "conteo_flops.md"
    )

    total_con_pivoteo = (
        total_pivoteo
        + contador_pivoteo.costo_pivoteo["divisiones"]
    )

    with open(ruta_reporte, "w", encoding="utf-8") as archivo:
        archivo.write("# Conteo de FLOPs\n\n")

        archivo.write("## Resultados generales\n\n")
        archivo.write("| Operacion | FLOPs |\n")
        archivo.write("|---|---:|\n")
        archivo.write(f"| Eliminacion sin pivoteo | {total} |\n")
        archivo.write(f"| Eliminacion con pivoteo | {total_eliminacion} |\n")
        archivo.write(f"| Sustitucion regresiva | {total_sustitucion} |\n")
        archivo.write(f"| Total sin busqueda de pivote | {total_pivoteo} |\n")
        archivo.write(f"| Total con divisiones de busqueda | {total_con_pivoteo} |\n\n")

        archivo.write("## Sobrecosto del pivoteo\n\n")
        archivo.write("| Operacion | Cantidad |\n")
        archivo.write("|---|---:|\n")

        for nombre, cantidad in contador_pivoteo.costo_pivoteo.items():
            archivo.write(f"| {nombre.capitalize()} | {cantidad} |\n")

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
        archivo.write("| Paso | Sin pivoteo | Con pivoteo |\n")
        archivo.write("|---|---:|---:|\n")

        for paso in range(1, len(vec_b)):
            sin = sum(contador.conteo[paso].values())
            con = sum(contador_pivoteo.conteo[paso].values())

            archivo.write(f"| {paso} | {sin} | {con} |\n")

    print("\nReporte generado:", ruta_reporte)
    