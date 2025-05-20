import tkinter as tk

from fontTools.misc.cython import returns
from test_graph import *
from graph import *
from tkinter import filedialog
from path import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt


modo_seleccion = False
modo_anadir = False
modo_anadir_segmento = False
grafo_activo = None
nodos_activos = None
canvas = None
canvas_picture = None



grafos_cargados = {}




def show_plot(fig, G):
    global grafo_activo, nodos_activos, canvas_picture, canvas
    grafo_activo = G
    nodos_activos = G.nodes
    if canvas_picture is not None:
        canvas_picture.grid_forget()
    canvas = FigureCanvasTkAgg(fig, master=outputs_frame)
    canvas.draw()
    canvas_picture = canvas.get_tk_widget()
    canvas_picture.config(width=600, height=400)
    canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.E+tk.W+tk.S)
    canvas.mpl_connect('button_press_event', on_click)






def seleccionar_vecinos():
    global modo_seleccion
    modo_seleccion = True
    print("Modo selección activado: haz clic en un nodo")


def Add_Node():
    global modo_anadir
    if modo_anadir:
        modo_anadir = False
        print("Modo añadir nodo desactivado.")
    else:
        modo_anadir = True
        print("Modo añadir nodo activado. Haz clic para añadir un nodo.")


def Add_Segment():
    global modo_anadir_segmento
    if modo_anadir_segmento:
        modo_anadir_segmento = False
        print("Modo añadir segmento desactivado.")
    else:
        modo_anadir_segmento = True
        print("Modo añadir segmento activado. Haz clic para añadir un segmento.")



nodos_segmento = []
def on_click(event):
    global modo_anadir, modo_seleccion, grafo_activo, canvas_picture, canvas, nodos_segmento, modo_anadir_segmento
    x_click, y_click = event.xdata, event.ydata
    if x_click is None or y_click is None:
        return
    if modo_anadir:
        nuevo_nombre = f"N{len(grafo_activo.nodes) + 1}"
        nuevo_nodo = Node(nuevo_nombre, x_click, y_click)
        if AddNode(grafo_activo, nuevo_nodo):
            Plot(grafo_activo)
            print(f"Nodo añadido: {nuevo_nombre} en ({x_click:.2f}, {y_click:.2f})")
        else:
            print(f"Error: El nodo {nuevo_nombre} ya existe.")
        fig = plt.gcf()
        new_canvas = FigureCanvasTkAgg(fig, master=outputs_frame)
        new_canvas.mpl_connect('button_press_event', on_click)
        new_canvas.draw()
        if canvas_picture is not None:
            canvas_picture.grid_forget()
        canvas_picture = new_canvas.get_tk_widget()
        canvas_picture.config(width=600, height=400)
        canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
        canvas = new_canvas


    if modo_seleccion:
        threshold = 1
        for nodo in grafo_activo.nodes:
            dist = ((nodo.coordinate_x - x_click)**2 + (nodo.coordinate_y - y_click)**2)**0.5
            if dist <= threshold:
                modo_seleccion = False
                plt.close('all')
                PlotNode(grafo_activo, nodo.name)
                fig = plt.gcf()
                new_canvas = FigureCanvasTkAgg(fig, master=outputs_frame)
                new_canvas.draw()
                if canvas_picture is not None:
                    canvas_picture.grid_forget()
                canvas_picture = new_canvas.get_tk_widget()
                canvas_picture.config(width=600, height=400)
                canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
                canvas = new_canvas
                break


    if not modo_anadir_segmento:
        return

    if x_click is None or y_click is None:
        return

    if modo_anadir_segmento:
        threshold = 1
        for nodo in grafo_activo.nodes:
            x, y = nodo.coordinate_x, nodo.coordinate_y
            dist = ((x - x_click) ** 2 + (y - y_click) ** 2) ** 0.5
            if dist <= threshold:
                nodos_segmento.append(nodo.name)
                print(f"Nodo seleccionado: {nodo.name}")
                break

        if len(nodos_segmento) == 2:
            name_origin = nodos_segmento[0]
            name_dest = nodos_segmento[1]
            name_segment = f"{name_origin}-{name_dest}"
            AddSegment(grafo_activo, name_segment, name_origin, name_dest)
            print(f"Segmento añadido: {name_segment}")
            nodos_segmento = []
            plt.close('all')
            Plot(grafo_activo)
            fig = plt.gcf()
            new_canvas = FigureCanvasTkAgg(fig, master=outputs_frame)
            new_canvas.mpl_connect('button_press_event', on_click)
            new_canvas.draw()
            if canvas_picture is not None:
                canvas_picture.grid_forget()
            canvas_picture = new_canvas.get_tk_widget()
            canvas_picture.config(width=600, height=400)
            canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
            canvas = new_canvas






def vacío():
    GV = Graph()
    Plot(GV)
    fig = plt.gcf()
    show_plot(fig, GV)


def ejemplo():
    G = CreateGraph_1()
    Plot(G)
    fig = plt.gcf()
    show_plot(fig, G)


def inventado():
    H = CreateGraph_2()
    Plot(H)
    fig = plt.gcf()
    show_plot(fig, H)




def plot_file():
    filename = filedialog.askopenfilename(title='Seleccione el archivo', filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    base_name = os.path.basename(filename)
    if base_name == 'FF.txt':
        grafo = FromFile(filename, grafo_existente=grafos_cargados.get("FF"))
        if grafo:  # Si el grafo fue cargado correctamente
            grafos_cargados["FF"] = grafo
        return grafo
    elif base_name == 'G.txt':
        grafo = FromFile(filename, grafo_existente=grafos_cargados.get("G"))
        if grafo:
            grafos_cargados["G"] = grafo
        return grafo
    elif base_name == 'H.txt':
        grafo = FromFile(filename, grafo_existente=grafos_cargados.get("H"))
        if grafo:
            grafos_cargados["H"] = grafo
        return grafo
    elif base_name == 'GV.txt':
        grafo = FromFile(filename, grafo_existente=grafos_cargados.get("GV"))
        if grafo:
            grafos_cargados["GV"] = grafo
        return grafo






def delete_node_from_gui():
    texto = entry_4.get()
    if len(texto.split()) == 2:
        grafo, nodo = texto.split()
        if grafo == "G":
            DeleteNode(G, nodo)
            Plot(G, (10,8), range(-5, 26, 5), range(-5, 26, 5))
        elif grafo == "H":
            DeleteNode(H, nodo)
            Plot(H, (10,8), range(-5, 26, 5), range(-5, 26, 5))
        elif grafo == "GV":
            DeleteNode(GV, nodo)
            Plot(I, (10,8), range(-5, 26, 5), range(-5, 26, 5))
        elif grafo_nombre in grafos_cargados:
            DeleteNode(grafos_cargados[grafo_nombre], nodo)
            Plot(grafos_cargados[grafo_nombre], (10,8), range(-5, 26, 5), range(-5, 26, 5))
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
        elif nombre_grafo == "GV":
            grafo_seleccionado = GV
        elif nombre_grafo in grafos_cargados:
            grafo_seleccionado = grafos_cargados[nombre_grafo]
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
        elif grafo_alcanzable == "GV":
            grafo_alcance = GV
        elif grafo_alcanzable in grafos_cargados:
            grafo_alcance = grafos_cargados[grafo_alcanzable]
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

def save_GV():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        ToFile(GV, filename)
        print("Grafo GV guardado.")

def save_FF ():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        ToFile(FF, filename)
        print("Grafo FF guardado.")




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
input_frame.columnconfigure(0, weight = 1)


#y el boton del input
button4 = tk.Button(input_frame, text = 'Mostrar vecinos', command = seleccionar_vecinos)
button4.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



#en la columna 0 fila 3 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_2 = tk.LabelFrame(root, text = 'Input')
input_frame_2.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

input_frame_2.rowconfigure(0, weight = 1)
input_frame_2.columnconfigure(0, weight = 1)


#y el boton del input
button5 = tk.Button(input_frame_2, text = 'Introduzca un nodo', command = Add_Node)
button5.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 4 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_3 = tk.LabelFrame(root, text = 'Input')
input_frame_3.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

input_frame_3.rowconfigure(0, weight = 1)
input_frame_3.columnconfigure(0, weight = 1)

#y el boton del input
button6 = tk.Button(input_frame_3, text = 'Introduzca un segmento', command = Add_Segment)
button6.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



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
button_save_frame.columnconfigure(1, weight = 1)

#defino el boton del frame
button9 = tk.Button(button_save_frame, text = 'SAVE G*', command = save_G)
button9.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
button10 = tk.Button(button_save_frame, text = 'SAVE H*', command = save_H)
button10.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
button11 = tk.Button(button_save_frame, text = 'SAVE GV', command = save_GV)
button11.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
button111 = tk.Button(button_save_frame, text = 'SAVE FF*', command = save_FF)
button111.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



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
outputs_frame.grid(row = 0, column = 1, rowspan = 9, padx = 5, pady = 5, sticky = "nsew")
outputs_frame.columnconfigure(0, weight = 1)
outputs_frame.rowconfigure(0, weight = 1)









root.mainloop()