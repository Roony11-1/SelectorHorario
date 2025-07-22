import os
import copy
from CargadorCarrera import CargadorCarrera
from modelos.Carrera import Carrera

from openpyxl import Workbook
from openpyxl.styles import Alignment

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
6. Exportar horario a Excel
7. Salir
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

def horariosChocan(horariosOcupados, nuevosHorarios):
    for nuevo in nuevosHorarios:
        for ocupado in horariosOcupados:
            if nuevo == ocupado["horario"]:
                return ocupado  # Retorna la info de la asignatura y sección que choca
    return None


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
        print(f"{i + 1}. Sigla: [{asignatura.getSigla()}] - Nombre: [{asignatura.getNombre()}] - Plan: [{asignatura.getPlan()}]")

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

                seleccion_valida = False
                while not seleccion_valida:
                    limpiarPantalla()
                    print(f"\nSecciones disponibles para {asignaturaOriginal.getSigla()} - {asignaturaOriginal.getNombre()}:")

                    for j, seccion in enumerate(secciones):
                        print(f"{j + 1}. Sección {seccion.getCodigo()} - Docente: {seccion.getDocente()}")
                        for horario in seccion.getHorario():
                            print(horario)

                    seleccion = input("Selecciona una sección (número, o 0 para cancelar): ")
                    try:
                        idx_seccion = int(seleccion.strip()) - 1

                        if idx_seccion == -1:
                            print("Selección de sección cancelada.")
                            break

                        if 0 <= idx_seccion < len(secciones):
                            seccionElegida = secciones[idx_seccion]
                            conflicto = horariosChocan(horariosOcupados, seccionElegida.getHorario())

                            if conflicto:
                                print("\n¡La sección seleccionada tiene un tope horario!")
                                print(f"Conflicto con: [{conflicto['sigla']}] - [{conflicto['nombre']}] Sección: [{conflicto['seccion']}]")
                                print(f"Horario en conflicto: [{conflicto['horario']}]\n")
                                print("Intenta con otra sección o ingresa 0 para omitir esta asignatura.\n")
                                input("Presiona Enter para continuar...")
                            else:
                                asignaturaClonada = copy.deepcopy(asignaturaOriginal)
                                asignaturaClonada.setSeccion([seccionElegida])
                                asignaturasSeleccionadas.append(asignaturaClonada)

                                for horario in seccionElegida.getHorario():
                                    horariosOcupados.append({
                                        "horario": horario,
                                        "sigla": asignaturaOriginal.getSigla(),
                                        "nombre": asignaturaOriginal.getNombre(),
                                        "seccion": seccionElegida.getCodigo()
                                    })
                                seleccion_valida = True
                        else:
                            print("Número de sección inválido.")
                            input("Presiona Enter para continuar...")
                    except ValueError:
                        print("Entrada inválida.")
                        input("Presiona Enter para continuar...")
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
            print(f"Sigla: [{asignatura.getSigla()}] - Nombre: [{asignatura.getNombre()}] - Plan: [{asignatura.getPlan()}]")
            for seccion in asignatura.getSeccion():
                print(f"Sección: [{seccion.getCodigo()}] - Docente: [{seccion.getDocente()}]")
                for horario in seccion.getHorario():
                    print(horario)
            print()
    input("Presiona Enter para continuar...")

def generarExcelHorario(asignaturasSeleccionadas):
    if not asignaturasSeleccionadas:
        print("No hay asignaturas seleccionadas para generar el horario.")
        input("Presiona Enter para continuar...")
        return

    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    bloques = ["08:15-09:45", "10:00-11:30", "11:45-13:15", "14:30-16:00", "16:15-17:45", "18:00-19:30", "19:45-21:15"]
    
    # Diccionario que usaremos para llenar la tabla
    horario = {bloque: {dia: "" for dia in dias_semana} for bloque in bloques}

    for asignatura in asignaturasSeleccionadas:
        for seccion in asignatura.getSeccion():
            for hora in seccion.getHorario():
                try:
                    dia, bloque = hora.split(" ")
                    if bloque in horario and dia in horario[bloque]:
                        contenido = f"{asignatura.getSigla()} ({seccion.getCodigo()})"
                        if horario[bloque][dia]:
                            horario[bloque][dia] += " / " + contenido
                        else:
                            horario[bloque][dia] = contenido
                except ValueError:
                    continue  # Formato de horario no esperado

    # Crear archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Horario"

    # Escribir encabezados
    ws.cell(row=1, column=1, value="Bloque / Día")
    for col, dia in enumerate(dias_semana, start=2):
        ws.cell(row=1, column=col, value=dia)

    # Escribir contenido
    for row, bloque in enumerate(bloques, start=2):
        ws.cell(row=row, column=1, value=bloque)
        for col, dia in enumerate(dias_semana, start=2):
            celda = ws.cell(row=row, column=col, value=horario[bloque][dia])
            celda.alignment = Alignment(wrap_text=True, vertical="top")

    archivo_nombre = "horario_generado.xlsx"
    wb.save(archivo_nombre)
    print(f"\nHorario guardado exitosamente en '{archivo_nombre}'.")
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
            generarExcelHorario(asignaturasSeleccionadas)
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
