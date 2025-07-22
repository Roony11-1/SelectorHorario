import os
from CargadorCarrera import CargadorCarrera

def main():
    carreras = CargadorCarrera.cargarDesdeExcel("PADRE-ALONSO-DE-OVALLE.xlsx")
    os.system("cls" if os.name == "nt" else "clear")

    print(f"Cantidad de carreras registradas: {len(carreras)}")

    for carrera in carreras:
        carrera.imprimirCarrera()

if __name__ == "__main__":
    main()
