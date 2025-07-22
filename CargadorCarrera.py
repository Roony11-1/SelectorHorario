from modelos.Carrera import Carrera
from modelos.Asignatura import Asignatura
from modelos.Seccion import Seccion
import pandas as pd

class CargadorCarrera:
    @staticmethod
    def cargarCarreras():
        df = pd.read_excel("PADRE-ALONSO-DE-OVALLE.xlsx", sheet_name="Hoja1")
        listaCarreras = []

        for nombreCarrera in df['Carrera'].dropna().unique():
            carrera = Carrera()
            carrera.setNombre(nombreCarrera)

            listaAsignaturas = []
            listaSecciones = []
            dfCarrera = df[df['Carrera'] == carrera.getNombre()]  # 👈 importante

            for _, row in dfCarrera.iterrows():
                asignatura = Asignatura()
                asignatura.setNombre(row['Asignatura'])
                asignatura.setSigla(row['Sigla'])
                asignatura.setNivel(row['Nivel'])

                # Creamos las secciones
                seccion = Seccion()
                seccion.setCodigo(row['Sección'])

                # Cargamos los horarios
                dfSeccion = dfCarrera[dfCarrera['Sección'] == seccion.getCodigo()]
                listaHorario = []
                
                for _, row in dfSeccion.iterrows():
                    listaHorario.append(row['Horario'])
                    seccion.setDoccente(row['Docente'])

                seccion.setHorario(list(set(listaHorario)))
                listaSecciones.append(seccion)
                listaAsignaturas.append(asignatura)

            # Eliminar duplicados
            listaSeccionesUnica = list(set(listaSecciones))
            listaAsignaturasUnicas = list(set(listaAsignaturas))

            # Asociar secciones a asignaturas
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
