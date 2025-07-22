class Asignatura:
    def __init__(self):
        self._sigla = None
        self._nombre = None
        self._nivel = None
        self._plan = None
        self._seccion = []

    def getNombre(self):
        return self._nombre
    
    def setNombre(self, nombre):
        self._nombre = nombre

    def getSigla(self):
        return self._sigla
    
    def setSigla(self, sigla):
        self._sigla = sigla
    
    def getNivel(self):
        return self._nivel

    def setNivel(self, nivel):
        self._nivel = nivel

    def getPlan(self):
        return self._plan
    
    def setPlan(self, plan):
        self._plan = plan

    def getSeccion(self):
        return self._seccion
    
    def setSeccion(self, seccion):
        self._seccion = seccion

    def __eq__(self, other):
        if isinstance(other, Asignatura):
            return self._nombre == other._nombre
        return False

    def __hash__(self):
        return hash(self._nombre)
    
    def imprimirAsignatura(self):
        secciones = self.getSeccion() or []
        
        print(f"-- Asignatura: {self.getNombre()} | Sigla: {self.getSigla()} | Nivel: {self.getNivel()} | Cantidad de secciones: {len(secciones)}")

        for seccion in secciones:
            seccion.imprimirSeccion()
        

