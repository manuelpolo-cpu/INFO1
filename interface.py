import tkinter as tk

from test_graph import *
from graph import *
from tkinter import filedialog
from path import *


I = Graph()


def vacío():
    Plot(I)


def ejemplo():
    G = CreateGraph_1()
    Plot(G)


def inventado():
    H = CreateGraph_2()
    Plot(H)


def plot_file():
    filename = filedialog.askopenfilename(title = 'Seleccione el archivo', filetypes = [("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        FromFile(filename)

def input():
    texto = entry.get()
    if len(texto.split()) == 2:
        grafo_nombre, nodo_nombre = texto.split()
        if grafo_nombre == "G":
            PlotNode(G, nodo_nombre)
        elif grafo_nombre == "H":
            PlotNode(H, nodo_nombre)
        elif grafo_nombre == "I":
            PlotNode(I, nodo_nombre)
        else:
            print("No se encontró el grafo indicado.")
    else:
        print("Formato incorrecto. Usa: G A")


def add_node():
    texto = entry_2.get()
    if len(texto.split()) == 4:  # Comprobar si hay 4 partes: G, nombre, x, y
        grafo, nodo_nombre, nodo_x, nodo_y = texto.split()
        # Crear un objeto Node y luego pasarlo a AddNode
        nodo_x = float(nodo_x)  # Asegúrate de convertir las coordenadas a float
        nodo_y = float(nodo_y)
        nodo = Node(nodo_nombre, nodo_x, nodo_y)  # Crear el nodo correctamente
        if grafo == "G":
            AddNode(G, nodo)
            Plot(G)
        elif grafo == "H":
            AddNode(H, nodo)
            Plot(H)
        elif grafo == "I":
            AddNode(I, nodo)
            Plot(I)
        else:
            print("No se encontró el grafo indicado.")
        print("Nodo introducido correctamente")
    else:
        print("Formato incorrecto. Usa: G nombre x y")



def add_segment():
    texto = entry_3.get()  # Obtener el texto del campo de entrada
    if len(texto.split()) == 4:  # Comprobar que se tiene el formato correcto: G NodoA NodoB
        grafo, recorrido, origin_name, destination_name = texto.split()
        if grafo == "G":
            AddSegment(G, recorrido, origin_name, destination_name)
            Plot(G)  # Volver a graficar el grafo con el nuevo segmento
        elif grafo == "H":
            AddSegment(H, recorrido, origin_name, destination_name)
            Plot(H)  # Volver a graficar el grafo con el nuevo segmento
        elif grafo == "I":
            AddSegment(I, recorrido, origin_name, destination_name)
            Plot(I)
        else:
            print("No se encontró el grafo indicado.")
    else:
        print("Formato incorrecto. Usa: G NodoA NodoB")


def delete_node_from_gui():
    texto = entry_4.get()
    if len(texto.split()) == 2:
        grafo, nodo = texto.split()
        if grafo == "G":
            DeleteNode(G, nodo)
            Plot(G)
        elif grafo == "H":
            DeleteNode(H, nodo)
            Plot(H)
        elif grafo == "I":
            DeleteNode((I, nodo))
            Plot(I)
        else:
            print("Grafo no encontrado.")
    else:
        print("Formato incorrecto. ")


def find_path():
    texto = entry_5.get()
    if len(texto.split()) == 3:
        nombre_grafo, nombre_origen, nombre_destino = texto.split()
        if nombre_grafo == "G":
            grafo_seleccionado = G
        elif nombre_grafo == "H":
            grafo_seleccionado = H
        elif nombre_grafo == "I":
            grafo_seleccionado = I
        else:
            print("El nombre del grafo no es válido.")
            # Buscar los nodos dentro del grafo por nombre
        origen = next((n for n in grafo_seleccionado.nodes if n.name == nombre_origen), None)
        destino = next((n for n in grafo_seleccionado.nodes if n.name == nombre_destino), None)
        if origen and destino:
            # Buscar el camino más corto
            camino = FindShortestPath(grafo_seleccionado, origen, destino)
            if camino:
                # Si se encuentra un camino, graficarlo
                PlotPath(grafo_seleccionado, camino)
            else:
                print("No se encontró un camino.")
        else:
            print("Nodos no válidos.")
    else:
        print("Introduce tres elementos: el grafo, el nodo de origen y el nodo de destino.")


def alcanzable():
    texto = entry_6.get()
    if len(texto.split()) == 3:
        grafo, origen, destino = texto.split()
        if grafo == "G":
            grafo_alcance = G
        elif grafo == "H":
            grafo_alcance = H
        elif grafo_alcanzable == "I":
            grafo_alcance = I
        else:
            print("Grafo no encontrado")
        origen = next((n for n in grafo_alcance.nodes if n.name == origen), None)
        destino = next((n for n in grafo_alcance.nodes if n.name == destino), None)
        if origen and destino:
            resultado = Reachability(grafo_alcance, origen, destino)
            if resultado:
                print("El nodo es alcanzable.")
            else:
                print("El nodo no es alcanzable.")
        else:
            print("Nodos no válidos.")
    else:
        print("Formato no válido.")



def save_G():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        ToFile(G, filename)
        print("Grafo G guardado.")

def save_H():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        ToFile(H, filename)
        print("Grafo H guardado.")

def save_I():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        ToFile(I, filename)
        print("Grafo I guardado.")




### PROGRAMA PRINCIPAL ###
root = tk.Tk()
root.geometry("1500x850") # Tamaño inicial
root.title("INFO_PROJECT")
#la ventana principal tiene 4 filas y dos columnas
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 10)
root.rowconfigure(0, weight = 1)
root.rowconfigure(1, weight = 1)
root.rowconfigure(2, weight = 1)
root.rowconfigure(3, weight = 1)
root.rowconfigure(4, weight = 1)
root.rowconfigure(5, weight = 1)
root.rowconfigure(6, weight = 1)
root.rowconfigure(7, weight = 1)
root.rowconfigure(8, weight = 1)
root.rowconfigure(9, weight = 1)



#en la columna 0 fila 0 tenemos el frame para mostrar el gráfico de ejemplo
button_example_frame = tk.LabelFrame(root, text = 'Seleccionar grafo a mostrar')
button_example_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#este frame tiene una columna y una fila
button_example_frame.rowconfigure(0, weight = 1)
button_example_frame.rowconfigure(1, weight = 1)
button_example_frame.columnconfigure(0, weight = 1)

#defino el boton del frame
button1 = tk.Button(button_example_frame, text = 'GRAFO G', command = ejemplo)
button1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
button2 = tk.Button(button_example_frame, text = 'GRAFO H', command = inventado)
button2.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



#en la columna 0 fila 1 está el frame de selección de archivos
file_selector_frame = tk.LabelFrame(root, text = 'Selector')
file_selector_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#este frame tiene una columna y una fila
file_selector_frame.rowconfigure(0, weight = 1)
file_selector_frame.columnconfigure(0, weight = 1)

#defino el boton del frame
button3 = tk.Button(file_selector_frame, text = 'Seleccione un archivo', command = plot_file)
button3.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



#en la columna 0 fila 2 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame = tk.LabelFrame(root, text = 'Input')
input_frame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

input_frame.rowconfigure(0, weight = 1)
input_frame.rowconfigure(1, weight = 1)
input_frame.columnconfigure(0, weight = 1)

#colocamos el cuadro de tecto
entry = tk.Entry(input_frame)
entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#y el boton del input
button4 = tk.Button(input_frame, text = 'Mostrar vecinos', command = input)
button4.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



#en la columna 0 fila 3 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_2 = tk.LabelFrame(root, text = 'Input')
input_frame_2.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

input_frame_2.rowconfigure(0, weight = 1)
input_frame_2.rowconfigure(1, weight = 1)
input_frame_2.columnconfigure(0, weight = 1)

#colocamos el cuadro de tecto
entry_2 = tk.Entry(input_frame_2)
entry_2.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#y el boton del input
button5 = tk.Button(input_frame_2, text = 'Introduzca un nodo', command = add_node)
button5.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 4 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_3 = tk.LabelFrame(root, text = 'Input')
input_frame_3.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

input_frame_3.rowconfigure(0, weight = 1)
input_frame_3.rowconfigure(1, weight = 1)
input_frame_3.columnconfigure(0, weight = 1)

#colocamos el cuadro de tecto
entry_3 = tk.Entry(input_frame_3)
entry_3.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#y el boton del input
button6 = tk.Button(input_frame_3, text = 'Introduzca un segmento', command = add_segment)
button6.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



#en la columna 0 fila 5 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_4 = tk.LabelFrame(root, text = 'Input')
input_frame_4.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

input_frame_4.rowconfigure(0, weight = 1)
input_frame_4.rowconfigure(1, weight = 1)
input_frame_4.columnconfigure(0, weight = 1)

#colocamos el cuadro de tecto
entry_4 = tk.Entry(input_frame_4)
entry_4.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#y el boton del input
button7 = tk.Button(input_frame_4, text = 'Borre un nodo', command = delete_node_from_gui)
button7.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 6 está el frame de selección de archivos
grafo_vacío = tk.LabelFrame(root, text = 'Selector')
grafo_vacío.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#este frame tiene una columna y una fila
grafo_vacío.rowconfigure(0, weight = 1)
grafo_vacío.columnconfigure(0, weight = 1)
#defino el boton del frame
button8 = tk.Button(grafo_vacío, text = 'Dibujar un grafo vacío', command = vacío)
button8.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 7 tenemos el frame para mostrar el gráfico de ejemplo
button_save_frame = tk.LabelFrame(root, text = 'Seleccionar grafo a mostrar')
button_save_frame.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#este frame tiene una columna y una fila
button_save_frame.rowconfigure(0, weight = 1)
button_save_frame.rowconfigure(1, weight = 1)
button_save_frame.columnconfigure(0, weight = 1)

#defino el boton del frame
button9 = tk.Button(button_save_frame, text = 'SAVE G*', command = save_G)
button9.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
button10 = tk.Button(button_save_frame, text = 'SAVE H*', command = save_H)
button10.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
button11 = tk.Button(button_save_frame, text = 'SAVE I*', command = save_I)
button11.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



#en la columna 0 fila 8 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_5 = tk.LabelFrame(root, text = 'Input')
input_frame_5.grid(row = 7, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

input_frame_5.rowconfigure(0, weight = 1)
input_frame_5.rowconfigure(1, weight = 1)
input_frame_5.columnconfigure(0, weight = 1)

#colocamos el cuadro de tecto
entry_5 = tk.Entry(input_frame_5)
entry_5.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#y el boton del input
button12 = tk.Button(input_frame_5, text = 'Encuentre el camino mas corto', command = find_path)
button12.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 8 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_6 = tk.LabelFrame(root, text = 'Input')
input_frame_6.grid(row = 8, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

input_frame_6.rowconfigure(0, weight = 1)
input_frame_6.rowconfigure(1, weight = 1)
input_frame_6.columnconfigure(0, weight = 1)

#colocamos el cuadro de tecto
entry_6 = tk.Entry(input_frame_6)
entry_6.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#y el boton del input
button13= tk.Button(input_frame_6, text = '¿Es alcanzable?', command = alcanzable)
button13.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)





#en la columma 1 fila 0 de la ventana principal están los outputs
outputs_frame = tk.LabelFrame(root, text = 'Outputs')
outputs_frame.grid(row = 0, column = 1, rowspan = 3, padx = 5, pady = 5, sticky = "nsew")
outputs_frame.columnconfigure(0, weight = 1)
outputs_frame.rowconfigure(0, weight = 1)









root.mainloop()