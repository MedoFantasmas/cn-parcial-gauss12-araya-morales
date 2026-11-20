# punto de entrada único que reproduce todo
import numpy as np
import os
from gauss import eliminacion_gaussiana_sin_pivoteo
from gauss import eliminacion_gaussiana_con_pivoteo
from gauss import sustitucion_regresiva

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

    #mat_a_gauss, vect_b_gauss = eliminacion_gaussiana_sin_pivoteo(mat_a, vec_b)

    mat_a_pivoteo, vec_b_pivoteo = eliminacion_gaussiana_con_pivoteo(mat_a, vec_b)



    print(mat_a_pivoteo)
    print("")
    print(vec_b_pivoteo)

    x = sustitucion_regresiva(mat_a_pivoteo, vec_b_pivoteo)

    print("\nSolucion:")
    print(x)