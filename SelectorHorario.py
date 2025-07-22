import os
import copy
from CargadorCarrera import CargadorCarrera
from modelos.Carrera import Carrera

def limpiarPantalla():
    os.system("cls" if os.name == "nt" else "clear")

def mostrarMenu(carreraSeleccionada: Carrera, asignaturasSeleccionadas):
    limpiarPantalla()
    seleccionadas = ', '.join([a.getSigla() for a in asignaturasSeleccionadas]) if asignaturasSeleccionadas else "Ninguna"
    print(f"""Hola, ¿qué deseas hacer?
1. Seleccionar carrera
2. Ver asignaturas (Carrera seleccionada: {carreraSeleccionada.getNombre()})
3. Seleccionar asignaturas (Actualmente seleccionadas: {seleccionadas})
4. Ver horario
5. Ver datos
6. Salir
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
        for i, asignatura in enumerate(carrera.getAsignaturas()):
            print(f"{i + 1}. {asignatura.getSigla()} - {asignatura.getNombre()}")
    input("\nPresiona Enter para continuar...")

def horariosChocan(horariosExistentes, nuevosHorarios):
    # Compara todos los horarios existentes con los nuevos
    for horarioNuevo in nuevosHorarios:
        if horarioNuevo in horariosExistentes:
            return True
    return False

def seleccionarAsignaturas(carrera: Carrera):
    limpiarPantalla()
    asignaturasSeleccionadas = []
    horariosOcupados = []

    if carrera.getNombre() == "Ninguna":
        print("Debes seleccionar una carrera primero.")
        input("\nPresiona Enter para continuar...")
        return asignaturasSeleccionadas

    asignaturas = carrera.getAsignaturas()
    print("Selecciona las asignaturas (ingresa los números separados por coma, por ejemplo: 1,3,4):\n")
    for i, asignatura in enumerate(asignaturas):
        print(f"{i + 1}. {asignatura.getSigla()} - {asignatura.getNombre()}")

    entrada = input("\nSelecciona: ")
    try:
        indices = [int(i.strip()) - 1 for i in entrada.split(",")]

        for idx in indices:
            if 0 <= idx < len(asignaturas):
                asignaturaOriginal = asignaturas[idx]
                secciones = asignaturaOriginal.getSeccion()

                if not secciones:
                    print(f"La asignatura {asignaturaOriginal.getSigla()} no tiene secciones registradas.")
                    continue

                limpiarPantalla()
                print(f"\nSecciones disponibles para {asignaturaOriginal.getSigla()} - {asignaturaOriginal.getNombre()}:")

                for j, seccion in enumerate(secciones):
                    print(f"{j + 1}. Sección {seccion.getCodigo()} - Horarios: {', '.join(seccion.getHorario())} - Docente: {seccion.getDocente()}")

                seleccion = input("Selecciona una sección (número): ")
                try:
                    idx_seccion = int(seleccion.strip()) - 1
                    if 0 <= idx_seccion < len(secciones):
                        seccionElegida = secciones[idx_seccion]
                        if horariosChocan(horariosOcupados, seccionElegida.getHorario()):
                            print("¡La sección seleccionada tiene un tope horario con otra asignatura ya elegida!")
                            input("\nPresiona Enter para continuar...")
                            continue

                        # Crear copia de la asignatura con solo esta sección
                        asignaturaClonada = copy.deepcopy(asignaturaOriginal)
                        asignaturaClonada.setSeccion([seccionElegida])
                        asignaturasSeleccionadas.append(asignaturaClonada)

                        # Agregar los horarios de la sección elegida al registro
                        horariosOcupados.extend(seccionElegida.getHorario())
                    else:
                        print("Número de sección inválido.")
                except ValueError:
                    print("Entrada inválida. Se omite la asignatura.")
    except ValueError:
        print("Entrada no válida.")

    input("\nPresiona Enter para continuar...")
    return asignaturasSeleccionadas


def verHorario(asignaturasSeleccionadas):
    limpiarPantalla()
    if not asignaturasSeleccionadas:
        print("No has seleccionado asignaturas aún.")
    else:
        print("Horario generado a partir de las asignaturas seleccionadas:\n")
        for asignatura in asignaturasSeleccionadas:
            print(f"{asignatura.getSigla()} - {asignatura.getNombre()}")
            for seccion in asignatura.getSeccion():
                print(f"  Sección {seccion.getCodigo()} - Horarios: {', '.join(seccion.getHorario())} - Docente: {seccion.getDocente()}")
            print()
    input("Presiona Enter para continuar...")

def verDatos(listaCarrera):
    limpiarPantalla()

    for carrera in listaCarrera:
        carrera.imprimirCarrera()

    input("Presiona Enter para continuar...")

def main():
    carreras = CargadorCarrera.cargarCarreras()
    carreraSeleccionada = Carrera()
    carreraSeleccionada.setNombre("Ninguna")
    asignaturasSeleccionadas = []

    while True:
        mostrarMenu(carreraSeleccionada, asignaturasSeleccionadas)
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            seleccion = seleccionarCarrera(carreras)
            if seleccion:
                carreraSeleccionada = seleccion
                asignaturasSeleccionadas = []  # reset al cambiar carrera
        elif opcion == "2":
            mostrarAsignaturas(carreraSeleccionada)
        elif opcion == "3":
            asignaturasSeleccionadas = seleccionarAsignaturas(carreraSeleccionada)
        elif opcion == "4":
            verHorario(asignaturasSeleccionadas)
        elif opcion == "5":
            verDatos(carreras)
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
