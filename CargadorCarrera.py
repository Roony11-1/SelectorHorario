from modelos.Carrera import Carrera
from modelos.Asignatura import Asignatura
from modelos.Seccion import Seccion
import pandas as pd

class CargadorCarrera:
    @staticmethod
    def cargarDesdeExcel(rutaArchivo: str):
        df = pd.read_excel(rutaArchivo, sheet_name="Hoja1")
        listaCarreras = []

        for nombreCarrera in df['Carrera'].dropna().unique():
            carrera = Carrera()
            carrera.setNombre(nombreCarrera)

            listaAsignaturas = []
            listaSecciones = []
            dfCarrera = df[df['Carrera'] == carrera.getNombre()]

            for _, row in dfCarrera.iterrows():
                asignatura = Asignatura()
                asignatura.setNombre(row['Asignatura'])
                asignatura.setSigla(row['Sigla'])
                asignatura.setNivel(row['Nivel'])

                seccion = Seccion()
                seccion.setCodigo(row['Sección'])

                dfSeccion = dfCarrera[dfCarrera['Sección'] == seccion.getCodigo()]
                listaHorario = [row['Horario'] for _, row in dfSeccion.iterrows()]
                seccion.setHorario(list(set(listaHorario)))

                listaSecciones.append(seccion)
                listaAsignaturas.append(asignatura)

            listaSeccionesUnica = list(set(listaSecciones))
            listaAsignaturasUnicas = list(set(listaAsignaturas))

            for asignatura in listaAsignaturasUnicas:
                seccionesAsignatura = []
                for seccion in listaSeccionesUnica:
                    codigo = seccion.getCodigo()
                    if codigo is not None and codigo.startswith(asignatura.getSigla()):
                        seccionesAsignatura.append(seccion)
                asignatura.setSeccion(seccionesAsignatura)

            carrera.setAsignaturas(listaAsignaturasUnicas)
            listaCarreras.append(carrera)

        return listaCarreras
