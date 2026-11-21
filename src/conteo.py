
class ContadorFlops:

    def __init__(self):
        self.conteo = {}
        self.costo_pivoteo = {
            "divisiones": 0,
            "comparaciones": 0,
            "intercambios": 0
        }

    def registrar(self, paso, operacion):
        if paso not in self.conteo:
            self.conteo[paso] = {
                "multiplicaciones": 0,
                "divisiones": 0,
                "sumas": 0,
                "restas": 0
            }

        self.conteo[paso][operacion] += 1

    def multiplicar(self, a, b, paso):
        self.registrar(paso, "multiplicaciones")
        return a * b

    def dividir(self, a, b, paso):
        self.registrar(paso, "divisiones")
        return a / b

    def sumar(self, a, b, paso):
        self.registrar(paso, "sumas")
        return a + b

    def restar(self, a, b, paso):
        self.registrar(paso, "restas")
        return a - b
    
    
    def obtener_desglose(self):
        desglose = {}

        for paso, operaciones in self.conteo.items():
            mult_div = (
                operaciones["multiplicaciones"]
                + operaciones["divisiones"]
            )

            sum_rest = (
                operaciones["sumas"]
                + operaciones["restas"]
            )

            desglose[paso] = {
                "mult_div": mult_div,
                "sum_rest": sum_rest,
                "total": mult_div + sum_rest
            }

        return desglose

    def mostrar_conteo(self):
        for paso, operaciones in self.conteo.items():
            print(f"\nPaso {paso}")

            total = 0

            for nombre, cantidad in operaciones.items():
                print(f"{nombre}: {cantidad}")
                total += cantidad

            print(f"Total: {total} FLOPs")

    def registrar_pivoteo(self, divisiones=0, comparaciones=0,
                    intercambios=0):
        self.costo_pivoteo["divisiones"] += divisiones
        self.costo_pivoteo["comparaciones"] += comparaciones
        self.costo_pivoteo["intercambios"] += intercambios

    def mostrar_pivoteo(self):
        print("\nSOBRECOSTO DEL PIVOTEO")

        for nombre, cantidad in self.costo_pivoteo.items():
            print(f"{nombre}: {cantidad}")
    
if __name__ == "__main__":

    contador = ContadorFlops()

    m = contador.dividir(6, 3, 1)

    a22 = contador.restar(
        5,
        contador.multiplicar(m, 2, 1),
        1
    )

    b2 = contador.restar(
        16,
        contador.multiplicar(m, 7, 1),
        1
    )

    print("Multiplicador:", m)
    print("Nuevo a22:", a22)
    print("Nuevo b2:", b2)

    contador.mostrar_conteo()
    
    print("\nDESGLOSE DE OPERACIONES")
    print(contador.obtener_desglose())
