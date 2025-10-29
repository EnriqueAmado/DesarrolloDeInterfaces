from operaciones import suma, resta, multiplicacion, division

def main():
    print("=== Calculadora simple ===")
    while True:
        try:
            a = float(input("Introduce el primer número: "))
            b = float(input("Introduce el segundo número: "))
        except ValueError:
            print("Por favor introduce solo números.")
            continue

        print("\nOperaciones disponibles:")
        print("1. Suma")
        print("2. Resta")
        print("3. Multiplicación")
        print("4. División")

        opcion = input("Elige una opción (1-4): ")

        if opcion == "1":
            resultado = suma(a, b)
        elif opcion == "2":
            resultado = resta(a, b)
        elif opcion == "3":
            resultado = multiplicacion(a, b)
        elif opcion == "4":
            resultado = division(a, b)
        else:
            print("Opción no válida.")
            continue

        print(f"\n El resultado es: {resultado}")

        seguir = input("\n¿Quieres hacer otra operación? (s/n): ").lower()
        if seguir != "s":
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    main()