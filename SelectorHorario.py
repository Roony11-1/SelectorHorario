import os
from CargadorCarrera import CargadorCarrera
from modelos.Carrera import Carrera

def limpiarPantalla():
    os.system("cls" if os.name == "nt" else "clear")

def mostrarMenu(carreraSeleccionada: Carrera):
    limpiarPantalla()
    print(f"""Hola, ¿qué deseas hacer?
1. Seleccionar carrera
2. Ver asignaturas (Carrera seleccionada: {carreraSeleccionada.getNombre()})
3. Salir
""")

def seleccionarCarrera(carreras: list) -> Carrera:
    limpiarPantalla()
    print("Lista de carreras disponibles:\n")

    for i, carrera in enumerate(carreras):
        print(f"{i + 1}. {carrera.getNombre()}")

    try:
        opcion = int(input("\nSelecciona una carrera (número): "))
        if 1 <= opcion <= len(carreras):
            return carreras[opcion - 1]
        else:
            print("Opción inválida.")
    except ValueError:
        print("Entrada no válida.")
    
    input("\nPresiona Enter para continuar...")
    return None

def mostrarAsignaturas(carrera: Carrera):
    limpiarPantalla()
    if carrera.getNombre() == "Ninguna":
        print("Debes seleccionar una carrera primero.")
    else:
        print(f"Asignaturas de la carrera {carrera.getNombre()}:\n")
        for asignatura in carrera.getAsignaturas():
            print(f"- {asignatura.getSigla()} {asignatura.getNombre()}")
    input("\nPresiona Enter para continuar...")

def main():
    carreras = CargadorCarrera.cargarCarreras()
    carreraSeleccionada = Carrera()
    carreraSeleccionada.setNombre("Ninguna")

    while True:
        mostrarMenu(carreraSeleccionada)
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            seleccion = seleccionarCarrera(carreras)
            if seleccion:
                carreraSeleccionada = seleccion
        elif opcion == "2":
            mostrarAsignaturas(carreraSeleccionada)
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
