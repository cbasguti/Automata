from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from pythomata import SimpleDFA
from automataFinito import AutomataFinito
import sys, os

config_name = 'myapp.cfg'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, config_name)

lista_estados = []
estado_inicial = ""
lista_aceptacion = []
lista_simbolos = []
transiciones = {}
entries = []
checks = []
auto_plugin = None



menu_inicio = Tk()
ventana_estados = Tk()
ventana_e_inicial = Tk()
ventana_e_final = Tk()

## VENTANA PARA ESTADOS Y SIMBOLOS
def comenzar():
    menu_inicio.destroy()
    estados_label_1.pack()
    estados.pack()
    estados_ing.pack()
    simbolos_label_1.pack()
    simbolos.pack()
    simbolos_ing.pack()
    boton_continuar_1.pack()
    boton_mostrar.pack()
    ventana_estados.eval('tk::PlaceWindow . center')
    ventana_estados.mainloop()

## VENTANA PARA ESTADO INICIAL Y ESTADOS DE ACEPTACION
def continuar_1():
    global lista_estados 
    global lista_simbolos
    global checks
    lista_estados = list(estados.get().split(','))
    lista_simbolos = list(simbolos.get().split(','))
    ventana_estados.destroy()
    e_inicial_label.pack()
    variable.set(lista_estados[0])
    e_inicial_menu = OptionMenu(ventana_e_inicial, variable, *lista_estados)  
    e_inicial_menu.pack()
    e_aceptacion_label.pack()
    for estado in lista_estados:
        new_estado = ttk.Checkbutton(ventana_e_inicial, text=estado)
        new_estado.state(['!alternate'])
        checks.append(new_estado)
        new_estado.pack()
    boton_continuar_2.pack()
    ventana_e_inicial.eval('tk::PlaceWindow . center')
    ventana_e_inicial.mainloop()

## VENTANA CON LA TABLA DE TRANSICIONES
def continuar_2():
    global lista_estados
    global lista_aceptacion
    global lista_simbolos
    global checks
    global estado_inicial
    for check in checks:
        if 'selected' in str(check.state()):
            lista_aceptacion.append(check.cget("text"))
    estado_inicial = variable.get()
    resumen_1 = Label(ventana_e_final, text="Los estados del automata son: " + str(lista_estados) +"\nLos simbolos de entrada son: " + str(lista_simbolos) + "\nEl estado inicial es: " + estado_inicial + "\nLos estados de aceptacion son: " + str(lista_aceptacion) + "\n\nAhora, por favor llene la tabla de transiciones usando los estados.\n(si desea ingresar un AFND, separe los estados por comas ','):\n", anchor="e", justify=LEFT)
    resumen_1.grid(columnspan=len(lista_simbolos) + 2)
    crea_tabla_tr(ventana_e_final)
    boton_continuar_3.grid(column=1, columnspan=2)
    ventana_e_inicial.destroy()
    ventana_e_final.eval('tk::PlaceWindow . center')
    ventana_e_final.mainloop()

def continuar_3():
    global transiciones
    global lista_estados
    global lista_simbolos
    global entries
    afnd = False
    for tr in range(len(entries)):
        tr_nuevas = {}
        estado = lista_estados[tr]
        obj = entries[tr]
        for tk in range(len(obj)):
            simbolo = lista_simbolos[tk]
            if obj[tk].get().count(',') > 0:
                tr_nuevas[simbolo] = list(obj[tk].get().split(','))
                afnd = True
            else:
                tr_nuevas[simbolo] = obj[tk].get()
        transiciones[estado] = tr_nuevas
    label_estados.grid(columnspan=len(lista_simbolos) + 2)
    label_final.grid(columnspan=len(lista_simbolos) + 2)
    iniciar_programa(ventana_e_final, afnd)
    ventana_e_final.eval('tk::PlaceWindow . center')
    boton_continuar_3["state"] = "disabled"

def iniciar_programa(root, afnd):
    global lista_estados
    global lista_aceptacion
    global lista_simbolos
    global estado_inicial
    global transiciones
    global auto_plugin
    automata = AutomataFinito()
    automata.set_estados(lista_estados)
    automata.set_inicial(estado_inicial)
    automata.set_final(lista_aceptacion)
    automata.set_simbolos(lista_simbolos)
    automata.set_transiciones(transiciones)
    if afnd:
        automata.convierte_afnd()
    else:
        automata.simplifica()
    auto_plugin = SimpleDFA(
        set(automata.estados), 
        set(automata.simbolos), 
        automata.estadoInicial, 
        set(automata.estadoFinal), 
        automata.transiciones)
    muestra_resultado(root, automata)
    fila = root.grid_size()
    fila = fila[1] + 2
    boton_muestra_d.grid(row=fila, column=1, columnspan=len(lista_simbolos))
    label_secuencia.grid(row=fila+1, column=0, columnspan=len(lista_simbolos) + 2)
    secuencia.grid(row=fila+2, column=0,columnspan=len(lista_simbolos) + 2)
    label_acepta.grid(row=fila+3, column=1, columnspan=len(lista_simbolos))
    boton_acepta_s.grid(row=fila+4, column=1, columnspan=len(lista_simbolos))
    transiciones = {}

def muestra_resultado(root, automata):
    if label_estados.winfo_exists():
        label_estados.config(text = "Los NUEVOS estados del automata son: " + str(automata.estados), anchor="e", justify=LEFT)
    if label_final.winfo_exists():
        label_final.config(text = "Los NUEVOS estados de aceptacion son: " + str(automata.estadoFinal) + "\nLas NUEVAS transiciones son:", anchor="e", justify=LEFT)
    for row in range(len(automata.estados) + 1):
        fila = label_final.grid_info()['row'] + 2
        fila += row
        for column in range(len(automata.simbolos) + 2):
            if row > 0 and column > 0 and column < (len(automata.simbolos) + 1):
                tr_resultado = Label(root, width=5, text=automata.transiciones.get(automata.estados[row - 1]).get(automata.simbolos[column - 1]))
                tr_resultado.grid(row=fila, column=column)
            if column == len(automata.simbolos) + 1:
                if row != 0:
                    if automata.estadoFinal.count(automata.estados[row - 1]) != 0:
                        label_x = Label(root, text="1")
                    else:
                        label_x = Label(root, text="0")
                    label_x.grid(row=fila, column=column)
            elif row == 0 and column == 0:
                c = True
            else:
                if row == 0:
                    label_x = Label(root, text=automata.simbolos[column - 1])
                    label_x.grid(row=fila, column=column)
                elif column == 0:
                    label_x = Label(root, text=automata.estados[row - 1])
                    label_x.grid(row=fila, column=column)
                
def muestra_estados():
    lista_estados = estados.get().split(',')
    if estados_ing.winfo_exists():
        estados_ing.config(text = lista_estados) 
    lista_simbolos = simbolos.get().split(',')
    if simbolos_ing.winfo_exists():
        simbolos_ing.config(text = lista_simbolos) 
    
def muestra_diagrama():
    global lista_simbolos
    global auto_plugin
    graph = auto_plugin.to_graphviz()
    graph.render(directory='')     
    graph.view()      

def acepta_secuencia():
    global auto_plugin
    texto_secuencia = str(secuencia.get())
    if auto_plugin.accepts(texto_secuencia):
        label_acepta.config(text="Acepta secuencia")
    else: 
        label_acepta.config(text="Rechaza secuencia")

def crea_tabla_tr(root):
    global lista_estados
    global lista_simbolos
    global lista_aceptacion
    global entries
    for row in range(len(lista_estados) + 1):
        cols = []
        for column in range(len(lista_simbolos) + 2):
            if column == len(lista_simbolos) + 1:
                if row != 0:
                    if lista_aceptacion.count(lista_estados[row - 1]) != 0:
                        label_x = Label(root, text="1")
                    else:
                        label_x = Label(root, text="0")
                    label_x.grid(row=row + 1, column=column)
            elif row == 0 and column == 0:
                c = True
            else:
                if row == 0:
                    label_x = Label(root, text=lista_simbolos[column - 1])
                    label_x.grid(row=row + 1, column=column)
                elif column == 0:
                    label_x = Label(root, text=lista_estados[row - 1])
                    label_x.grid(row=row + 1, column=column)
                else:
                    tr_nueva = Entry(root, width=5)
                    cols.append(tr_nueva)
                    tr_nueva.grid(row=row + 1, column=column)
        if cols:
            entries.append(cols)



estados_label_1 = Label(ventana_estados, text="Por favor, ingrese los estados de su automata sin espacios y separados por comas ',':")
estados_ing = Label(ventana_estados, text = "Aqui se mostraran los estados ingresados")
simbolos_label_1 = Label(ventana_estados, text="Por favor, ingrese los simbolos de su automata sin espacios y separados por comas ',':")
simbolos_ing = Label(ventana_estados, text = "Aqui se mostraran los simbolos ingresados")
e_inicial_label = Label(ventana_e_inicial, text="Por favor seleccion un estado inicial de los ingresados anteriormente:")
e_aceptacion_label = Label(ventana_e_inicial, text="A continuacion, seleccione los estados de aceptacion:")
label_estados = Label(ventana_e_final, text="")
label_final = Label(ventana_e_final, text="")
label_secuencia = Label(ventana_e_final, text="Ingrese una secuencia de Simbolos para verificar si es aceptada:")
label_acepta = Label(ventana_e_final, text="No se ha ingresado secuencia")

variable = StringVar(ventana_e_inicial)

estados = Entry(ventana_estados, width=50)
simbolos = Entry(ventana_estados, width=50)
secuencia = Entry(ventana_e_final, width=50)

boton_mostrar = Button(ventana_estados, text="MOSTRAR", command=muestra_estados)
boton_continuar_1 = Button(ventana_estados, text="CONTINUAR", command=continuar_1)
boton_continuar_2 = Button(ventana_e_inicial, text="CONTINUAR", command=continuar_2)
boton_continuar_3 = Button(ventana_e_final, text="CONVERTIR / SIMPLIFICAR", command=continuar_3)
boton_acepta_s = Button(ventana_e_final, text="INGRESAR", command=acepta_secuencia)
boton_muestra_d = Button(ventana_e_final, text="MUESTRA DIAGRAMA", command=muestra_diagrama)

ventana_estados.withdraw()
ventana_e_inicial.withdraw()
ventana_e_final.withdraw()



# Importing a image
img = ImageTk.PhotoImage(Image.open("Automata.png"))
panel = Label(menu_inicio, image = img)
panel.pack(side = "top", fill = "both", expand = "yes")

# Creatinng a Label Widget
myLabel1 = Label(menu_inicio, text="¡Bienvenido al programa Automata!")
myLabel2 = Label(menu_inicio, text="Este programa le permite al usuario ingresar AFD y AFND para su posterior simplificación y verificación de secuencias")
# Shoving it onto the screen
myLabel1.pack()
myLabel2.pack()
# Boton para iniciar
myButton = Button(menu_inicio, text="Comenzar", command=comenzar)
myButton.pack()

menu_inicio.eval('tk::PlaceWindow . center')
menu_inicio.mainloop()
