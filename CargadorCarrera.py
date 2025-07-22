from modelos.Carrera import Carrera
from modelos.Asignatura import Asignatura
from modelos.Seccion import Seccion
import pandas as pd

class CargadorCarrera:
    @staticmethod
    def cargarCarreras():
        df = pd.read_excel("PADRE-ALONSO-DE-OVALLE.xlsx", sheet_name="Hoja1")
        listaCarreras = []

        # Agrupar por nombre de carrera
        for nombreCarrera in df['Carrera'].dropna().unique():
            carrera = Carrera()
            carrera.setNombre(nombreCarrera)
            listaAsignaturas = []

            # Filtrar por la carrera actual
            dfCarrera = df[df['Carrera'] == nombreCarrera]

            # Agrupar por sigla para no repetir asignaturas
            for siglaAsignatura in dfCarrera['Sigla'].dropna().unique():
                dfAsignatura = dfCarrera[dfCarrera['Sigla'] == siglaAsignatura]

                # Crear asignatura
                asignatura = Asignatura()
                asignatura.setSigla(siglaAsignatura)
                asignatura.setNombre(dfAsignatura.iloc[0]['Asignatura'])
                asignatura.setNivel(dfAsignatura.iloc[0]['Nivel'])
                asignatura.setPlan(dfAsignatura.iloc[0]['Plan'])

                secciones = []
                for codSeccion in dfAsignatura['Sección'].dropna().unique():
                    dfSeccion = dfAsignatura[dfAsignatura['Sección'] == codSeccion]
                    
                    seccion = Seccion()
                    seccion.setCodigo(codSeccion)
                    seccion.setDoccente(dfSeccion.iloc[0]['Docente'])
                    seccion.setHorario(dfSeccion['Horario'].dropna().unique().tolist())
                    
                    secciones.append(seccion)

                asignatura.setSeccion(secciones)
                listaAsignaturas.append(asignatura)

            carrera.setAsignaturas(listaAsignaturas)
            listaCarreras.append(carrera)

        return listaCarreras
