class AutomataFinito:
    # Constructor
    def __init__(self):
        self.estados = []
        self.simbolos = []
        self.estadoInicial = ""
        self.estadoFinal = []
        self.transiciones = {}

    # Funcion que simplifica el automata
    def simplifica(self):
        self.estados_extraños()
        self.actualiza_estados()
        self.estados_equivalentes()
        self.actualiza_estados()
        # No hay mucho que explicar :/

    # Funcion que encuentra y unifica estados equivalentes
    def estados_equivalentes(self):
        matriz = self.inicializa_matriz() # matriz = matriz Nyhill-Nerode vacia
        estados_equ = [] # lista vacia de estados equivalentes
        # Ciclo que marca equivalencia = 1 cuando en un par de estados del automata
        # uno es de aceptación y el otro no.
        for i in matriz:
            if i[0] in self.estadoFinal and i[1] not in self.estadoFinal:
                i[2] = 1
            elif i[1] in self.estadoFinal and i[0] not in self.estadoFinal:
                i[2] = 1
        # Ciclo que marca equivalencia = 1 cuando las transiciones de un par de estados
        # del automata fueron marcados con 1 anteriormente.
        for i in matriz:
            if i[2] == 0:
                aux_1 = self.transiciones.get(i[0]) # transiciones estado 1
                aux_2 = self.transiciones.get(i[1]) # transiciones estado 2
                for k in range(len(self.simbolos)):
                    aux_3 = aux_1.get(self.simbolos[k])
                    aux_4 = aux_2.get(self.simbolos[k])
                    if self.retorna_equivalencia(aux_3, aux_4, matriz) == 1:
                        i[2] = 1
        # Ciclo que busca los pares de estados con equivalencia = 0, son los estados que 
        # resultaron ser equivalentes siguiendo la teoría
        for i in matriz:
            if i[2] == 0:
                aux_5 = []
                aux_5.append(i[0])
                aux_5.append(i[1])
                if not estados_equ:
                    estados_equ.append(aux_5)
                else: 
                    for j in estados_equ:
                        # Condicion que verifica si dos conjuntos de estados equivalentes deben ser 
                        # unificados. ej:
                        # [A,B] [C,B] -> [A,B,C]
                        if any(k in j for k in aux_5):
                            estados_equ[estados_equ.index(j)] += aux_5
                            estados_equ[estados_equ.index(j)] = list(dict.fromkeys(j))
                        else:
                            if estados_equ.count(aux_5) == 0:   
                                estados_equ.append(aux_5)
        # Unifica los conjuntos de estados equivalentes
        self.unifica_estados(estados_equ)

    # Funcion que unifica los estados equivalentes
    def unifica_estados(self, lista_estados):
        for estado in lista_estados:
            tr_nuevas = {} # transiciones del nuevo estado
            new_estado = "" # estado nuevo
            # Almacena los nuevos estados
            for j in estado:
                    if self.estados.count(j) > 0:
                        self.estados.remove(j)
                    new_estado = new_estado + j
            new_estado = self.corrige_estado(new_estado)
            # Actualiza los values de las transiciones
            for i in self.transiciones:
                transiciones = self.transiciones.get(i)
                for key, value in transiciones.items():
                    for j in estado:
                        if value == j:
                            transiciones[key] = new_estado
            self.estados.append(new_estado)
            # Actualiza los keys de las transiciones
            tr_nuevas = self.transiciones.get(estado[0])
            self.transiciones[new_estado] = tr_nuevas
            # Elimina los estados antiguos
            for i in estado:
                if i in self.transiciones:
                    del self.transiciones[i]
                
    # Funcion que retorna el estado de equivalencia de dos estados
    def retorna_equivalencia(self, simbolo_a, simbolo_b, matriz):
        for i in matriz:
            if i[0] == simbolo_a and i[1] == simbolo_b:
                return i[2]
            elif i[1] == simbolo_a and i[0] == simbolo_b:
                return i[2]
            elif simbolo_a == simbolo_b:
                return 0
        return "Error"

    # Funcion que encuentra los estados extraños y los quita
    def estados_extraños(self):
        tr_nuevas = []
        terminado = False
        estado_p = self.estadoInicial
        tr_nuevas.append(estado_p)
        # Ciclo que evalúa la existencia de estados extraños
        while not terminado:
            lista = list(self.transiciones.get(estado_p).values())
            for i in range(len(self.simbolos)):
                estado_h = lista[i]
                if tr_nuevas.count(estado_h) == 0:
                    tr_nuevas.append(estado_h)
            if estado_p == tr_nuevas[len(tr_nuevas) - 1]:
                terminado = True
                break
            estado_p = tr_nuevas[tr_nuevas.index(estado_p) + 1]
        # Lista que agrupa los estados extraños del autómata
        estados_extraños = []
        for i in self.transiciones:
            if tr_nuevas.count(i) == 0:
                estados_extraños.append(i)
        # Ciclo que elimina los estados extraños del diccionario de transiciones
        for i in estados_extraños:
            del self.transiciones[i]
            if i in self.estadoFinal:
                self.estadoFinal.remove(i)
        self.estados = tr_nuevas

    # Funcion que inicializa la matriz de Nyhill-Nerode
    def inicializa_matriz(self):
        # Matriz del Teorema de Myhill-Nerode
        # Esta matriz es útil para minimizar un autómata finito
        matriz_mn = []
        for i in range(len(self.estados)):
            for j in range(len(self.estados)):
                if j != i and j < i:
                    aux = []
                    aux.append(self.estados[i])
                    aux.append(self.estados[j])
                    aux.append(0)
                    matriz_mn.append(aux)
        return matriz_mn

    # Funcion que convierte un AFND a un AFD
    def convierte_afnd(self):
        self.limpia_listas()
        terminado = False
        estado_p = self.estadoInicial
        tr_nuevas = {}
        lista_estados = []
        lista_estados.append(estado_p)
        while not terminado:
            tr_nuevas_p = {}
            if estado_p in self.transiciones:
                tr_estado_p = self.transiciones.get(estado_p)
                for i in self.simbolos:
                    transicion = tr_estado_p.get(i)
                    tr_nuevas_p[i] = transicion
                    if lista_estados.count(transicion) == 0 and transicion != '':
                        lista_estados.append(transicion)
            else:
                for j in self.simbolos:
                    estado_nuevo = ""
                    for i in estado_p:
                        estado_actual = self.transiciones.get(i)
                        estado_nuevo = estado_nuevo + estado_actual.get(j)
                    estado_nuevo = self.corrige_estado(estado_nuevo)
                    tr_nuevas_p[j] = estado_nuevo
                    if lista_estados.count(estado_nuevo) == 0 and estado_nuevo != '':
                        lista_estados.append(estado_nuevo)
            tr_nuevas[estado_p] = tr_nuevas_p
            if estado_p == lista_estados[len(lista_estados) - 1]:
                terminado = True
                break
            else:
                estado_p = lista_estados[lista_estados.index(estado_p) + 1]
        self.estados = lista_estados
        self.transiciones = tr_nuevas
        self.actualiza_estados()

    # Funcion que hace que las transiciones '[C,D]' de un AFND sean 'CD'
    def limpia_listas(self):
        for i in self.transiciones:
            estado_actual = self.transiciones.get(i)
            for j in self.simbolos:
                transicion = estado_actual.get(j)  
                if isinstance(transicion, list):
                    nuevo_estado = ""
                    for k in transicion:
                        nuevo_estado = nuevo_estado + k
                    nuevo_estado = self.corrige_estado(nuevo_estado)
                    self.transiciones[i][j] = nuevo_estado

    # Funcion que evita la existencia de estados anagramas o con caracteres repetidos
    def corrige_estado(self, estado):
        estado = sorted(estado)
        estado = "".join(dict.fromkeys(estado))
        return estado
     
    # Funcion que actualiza los estados de aceptacion y el inicial
    def actualiza_estados(self):
        final_aux = self.estadoFinal.copy()
        for i in self.estados:
            for j in final_aux:
                if i.count(j) > 0 and self.estadoFinal.count(i) == 0:
                    self.estadoFinal.append(i)
        final_aux = self.estadoFinal.copy()
        for j in final_aux:
            if self.estados.count(j) == 0:
                self.estadoFinal.remove(j)
        for i in self.estados:
            if self.estadoInicial in i:
                self.estadoInicial = i
        
    # Setters del Automata

    def set_estados(self, estados):
        self.estados = estados

    def set_simbolos(self, simbolos):
        self.simbolos = simbolos

    def set_inicial(self, estadoInicial):
        self.estadoInicial = estadoInicial

    def set_final(self, estadoFinal):
        self.estadoFinal = estadoFinal

    def set_transiciones(self, transiciones):
        self.transiciones = transiciones


        