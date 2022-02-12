from automataFinito import AutomataFinito as AF
from pythomata import SimpleDFA
from tkinter import *
from PIL import ImageTk, Image
import graphviz as gv
#import pydot

a = AF()
a.setEstados(['A', 'B', 'C'])
a.setSimbolos(['0', '1'])
a.setEstadoInicial('A')
a.setEstadoFinal(['C'])
transiciones = {
    'A': {
        '0': ['A', 'B'],'1': 'C'
    },
    'B': {
        '0': 'A','1': ['B', 'C']
    },
    'C': {
        '0': 'C','1': 'B'
    }}
a.setTransiciones(transiciones)
a.convierte_afnd()

print(set(a.estados))
for i in a.transiciones:
    print(i,' - ',a.transiciones.get(i))

b = SimpleDFA(set(a.estados), set(a.simbolos), a.estadoInicial, set(a.estadoFinal), a.transiciones)
graph = b.to_graphviz()
graph.render(directory='img') 


