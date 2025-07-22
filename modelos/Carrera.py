class Carrera:
    def __init__(self):
        self._nombre = None
        self._asignaturas = []

    def getNombre(self):
        return self._nombre
    
    def setNombre(self, nombre):
        self._nombre = nombre
    
    def getAsignaturas(self):
        return self._asignaturas
    
    def setAsignaturas(self, asignaturas):
        self._asignaturas = asignaturas

    def imprimirCarrera(self):
        print(f"Nombre carrera: {self.getNombre()} | Cantidad de asignaturas: {len(self.getAsignaturas())}")
        
        for asignatura in self.getAsignaturas():
            asignatura.imprimirAsignatura()
        
        print(f"")