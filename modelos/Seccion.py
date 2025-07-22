class Seccion:
    def __init__(self):
        self._codigo = None
        self._docente = None
        self._horarios = []

    def getCodigo(self):
        return self._codigo
    
    def setCodigo(self, codigo):
        self._codigo = codigo

    def getDocente(self):
        return self._docente
    
    def setDoccente(self, docente):
        self._docente = docente

    def getHorario(self):
        return self._horarios
    
    def setHorario(self, horarios):
        self._horarios = horarios

    def __eq__(self, other):
        if isinstance(other, Seccion):
            return self._codigo == other._codigo
        return False

    def __hash__(self):
        return hash(self._codigo)

    def imprimirSeccion(self):
        print(f"        Sección: {self._codigo} | Docente: {self._docente}")
        for horario in self._horarios:
            print(f"            Horario: [{horario}]")
        print("")

        