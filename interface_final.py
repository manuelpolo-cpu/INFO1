#importar todas las clases y funciones necesarias
from test_graph import *
from graph import *
from airSpace import *
from tkinter import filedialog
from path import *
#importar todas las librerias gráficas y numéricas
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import os
import tkinter.messagebox as messagebox
from tkinter import simpledialog


#inicializar todos los modos y variables globales
modo_seleccion = False
modo_anadir = False
modo_anadir_segmento = False
modo_eliminar = False
modo_encontrar_camino = False
modo_alcanzable = None
grafo_activo = None
nodos_activos = None
canvas = None
canvas_picture = None
toolbar_widget = None
origen_seleccionado = None
destino_seleccionado = None
graph_cat = None
graph_esp = None
graph_eur = None
shortest_path_global = None


#mostrar un grafo por pantalla dentro del contenedor
def show_plot(fig, G):
    global grafo_activo, nodos_activos, canvas_picture, canvas, toolbar_widget
    nodos_activos = grafo_activo.nodes
    if canvas_picture is not None:
        canvas_picture.grid_forget()
    canvas = FigureCanvasTkAgg(fig, master=outputs_frame)
    canvas.draw()
    canvas_picture = canvas.get_tk_widget()
    canvas_picture.config(width=600, height=400)
    canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
    canvas.mpl_connect('button_press_event', on_click)
    if toolbar_widget is not None:
        toolbar_widget.grid_forget()
    toolbar_frame = tk.Frame(outputs_frame)
    toolbar_frame.grid(row=11, column=0, padx=5, pady=2, sticky=tk.W)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
    toolbar_widget = toolbar

#activar el modo de encontrar el camino
def encontrar_camino():
    global modo_encontrar_camino
    if modo_encontrar_camino:
        modo_encontrar_camino = False
        print("Modo encontrar camino desactivado.")
    else:
        modo_encontrar_camino = True
        print("Modo encontrar camino activado. Haz clic para encontrar un camino.")

#activar el modo eliminar un nodo
def Delete_Node():
    global modo_eliminar
    if modo_eliminar:
        modo_eliminar = False
        print("Modo eliminar nodo desactivado.")
    else:
        modo_eliminar = True
        print("Modo eliminar nodo activado. Haz clic para eliminar un nodo.")

#activar el modo de selección de vecinos
def seleccionar_vecinos():
    global modo_seleccion
    if modo_seleccion:
        modo_seleccion = False
        print("Modo selección de vecinos desactivado.")
    else:
        modo_seleccion = True
        print("Modo selección de vecinos activado. Haz clic para mostrar los vecinos. ")

#activar el modo de añadir un nodo
def Add_Node():
    global modo_anadir
    if modo_anadir:
        modo_anadir = False
        print("Modo añadir nodo desactivado.")
    else:
        modo_anadir = True
        print("Modo añadir nodo activado. Haz clic para añadir un nodo.")

#activar el modo de añadir un segmento
def Add_Segment():
    global modo_anadir_segmento
    if modo_anadir_segmento:
        modo_anadir_segmento = False
        print("Modo añadir segmento desactivado.")
    else:
        modo_anadir_segmento = True
        print("Modo añadir segmento activado. Haz clic para añadir un segmento.")

#activar el modo de alcanzabilidad
def alcanzable():
    global modo_alcanzable
    if modo_alcanzable:
        modo_alcanzable = False
        print("Modo alcanzacble desactivado. ")
    else:
        modo_alcanzable = True
        print("Modo alcanzable activado. Haz clic para ver si son alcanzables. ")


def exportar():
    global shortest_path_global
    if shortest_path_global is None:
        messagebox.showwarning("Exportar ruta", "No hay camino para exportar.")
        return
    export_to_kml(shortest_path_global, "ruta_exportada.kml")
    messagebox.showinfo("Exportar ruta", "Archivo KML exportado con éxito.")


def calcular_tiempo():
    global shortest_path_global
    if shortest_path_global is None:
        messagebox.showwarning("Error", "Primero encuentra un camino entre dos nodos")
        return

    # Pedir al usuario la velocidad
    velocidad = simpledialog.askfloat("Velocidad","Introduce la velocidad (km/h):",
                                      minvalue=0.1)
    if velocidad is None:
        return

    # Calcular distancia total
    distancia_total = 0.0
    for i in range(len(shortest_path_global.nodes) - 1):
        nodo_actual = shortest_path_global.nodes[i]
        nodo_siguiente = shortest_path_global.nodes[i + 1]
        distancia_total += Distance(nodo_actual, nodo_siguiente)

    # Calcular tiempo (horas)
    tiempo_horas = distancia_total / velocidad

    # Convertir a horas, minutos, segundos
    horas = int(tiempo_horas)
    minutos = int((tiempo_horas - horas) * 60)
    segundos = int(((tiempo_horas - horas) * 60 - minutos) * 60)

    # Mostrar resultados
    mensaje = (f"Distancia total: {distancia_total:.2f} km\n"
               f"Velocidad: {velocidad} km/h\n"
               f"Tiempo estimado: {horas}h {minutos}m {segundos}s")

    messagebox.showinfo("Tiempo de recorrido", mensaje)
def camino():
    global shortest_path_global, grafo_activo, canvas_picture
    nodos_text = entry_nodos.get().strip()
    if not nodos_text:
        print("Introduce dos nodos separados por espacio, ej: A D")
        return
    nodos = nodos_text.split()
    if len(nodos) != 2:
        print("Introduce exactamente dos nodos separados por espacio")
        return
    origen_name, destino_name = nodos

    # Buscar nodos en el grafo por nombre (asumiendo que grafo_activo.nodes es iterable con atributo name)
    origen = next((n for n in grafo_activo.nodes if n.name == origen_name), None)
    destino = next((n for n in grafo_activo.nodes if n.name == destino_name), None)

    if origen is None or destino is None:
        print(f"Nodos no encontrados en el grafo: {origen_name}, {destino_name}")
        return

    # Encontrar camino más corto
    shortest_path = FindShortestPath(grafo_activo, origen, destino)

    if not shortest_path or not shortest_path.nodes:
        print("No se encontró camino entre los nodos indicados.")
        return

    # Plotear camino (adaptar a tu función y parámetros)
    plt.close('all')  # Cierra figuras previas

    if 'graph_cat' in globals() and grafo_activo == graph_cat:
        figsize = (15, 7)
        xticks = range(-1, 5, 1)
        yticks = np.arange(38, 42.5, 0.5)
    elif 'graph_esp' in globals() and grafo_activo == graph_esp:
        figsize = (17, 8)
        xticks = range(-9, 5, 1)
        yticks = np.arange(37, 43.5, 0.5)
    elif 'graph_eur' in globals() and grafo_activo == graph_eur:
        figsize = (17, 8)
        xticks = range(-6, 6, 1)
        yticks = np.arange(37.5, 50, 0.5)
    elif 'G' in globals() and grafo_activo == G:
        figsize = (8, 6)
        xticks = range(-5, 26, 5)
        yticks = range(-5, 26, 5)
    elif 'FF' in globals() and grafo_activo == FF:
        figsize = (8, 6)
        xticks = range(-5, 26, 5)
        yticks = range(-5, 26, 5)
    else:
        figsize = (8, 6)
        xticks = range(-5, 26, 5)
        yticks = range(-5, 26, 5)

    PlotPath(grafo_activo, shortest_path, figsize, xticks, yticks)

    # Mostrar en canvas tkinter (igual que tú haces)
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

    shortest_path_global = shortest_path


#inicializar todas las listas vacías que usaré posteriormente
nodos_seleccionados = []
nodos_segmento = []
def on_click(event):
    print("Click detectado")
    global modo_anadir, modo_seleccion, grafo_activo, canvas_picture, canvas, nodos_segmento, modo_anadir_segmento, modo_eliminar, origen_seleccionado, destino_seleccionado, nodos_seleccionados, shortest_path_global
    x_click, y_click = event.xdata, event.ydata

    if x_click is None or y_click is None:
        return
    if modo_anadir:
        nuevo_nombre = f"N{len(grafo_activo.nodes) + 1}"
        nuevo_nodo = Node(nuevo_nombre, x_click, y_click)
        if AddNode(grafo_activo, nuevo_nodo):
            if 'graph_cat' in globals() and grafo_activo == graph_cat:
                figsize = (15, 7)
                xticks = range(-1, 5, 1)
                yticks = np.arange(38, 42.5, 0.5)
            elif 'graph_esp' in globals() and grafo_activo == graph_esp:
                figsize = (17, 8)
                xticks = range(-9, 5, 1)
                yticks = np.arange(37, 43.5, 0.5)
            elif 'graph_eur' in globals() and grafo_activo == graph_eur:
                figsize = (17, 8)
                xticks = range(-6, 6, 1)
                yticks = np.arange(37.5, 50, 0.5)
            elif 'G' in globals() and grafo_activo == G:
                figsize = (8, 6)
                xticks = range(-5, 26, 5)
                yticks = range(-5, 26, 5)
            elif 'FF' in globals() and grafo_activo == FF:
                figsize = (8, 6)
                xticks = range(-5, 26, 5)
                yticks = range(-5, 26, 5)
            else:
                figsize = (8, 6)
                xticks = range(-5, 26, 5)
                yticks = range(-5, 26, 5)
            Plot(grafo_activo, figsize, xticks, yticks)
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

    if x_click is None or y_click is None:
        return
    elif modo_seleccion:
        threshold = 0.1
        for nodo in grafo_activo.nodes:
            dist = ((nodo.coordinate_x - x_click) ** 2 + (nodo.coordinate_y - y_click) ** 2) ** 0.5
            if dist <= threshold:
                modo_seleccion = False
                plt.close('all')
                if 'graph_cat' in globals() and grafo_activo == graph_cat:
                    figsize = (15, 7)
                    xticks = range(-1, 5, 1)
                    yticks = np.arange(38, 42.5, 0.5)
                elif 'graph_esp' in globals() and grafo_activo == graph_esp:
                    figsize = (17, 8)
                    xticks = range(-9, 5, 1)
                    yticks = np.arange(37, 43.5, 0.5)
                elif 'graph_eur' in globals() and grafo_activo == graph_eur:
                    figsize = (17, 8)
                    xticks = range(-6, 6, 1)
                    yticks = np.arange(37.5, 50, 0.5)
                elif 'G' in globals() and grafo_activo == G:
                    figsize = (8, 6)
                    xticks = range(-5, 26, 5)
                    yticks = range(-5, 26, 5)
                elif 'FF' in globals() and grafo_activo == FF:
                    figsize = (8, 6)
                    xticks = range(-5, 26, 5)
                    yticks = range(-5, 26, 5)
                else:
                    figsize = (8, 6)
                    xticks = range(-5, 26, 5)
                    yticks = range(-5, 26, 5)
                PlotNode(grafo_activo, nodo.name, figsize, xticks, yticks)
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

    if x_click is None or y_click is None:
        return
    elif modo_anadir_segmento:
        threshold = 0.1
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
            if 'graph_cat' in globals() and grafo_activo == graph_cat:
                figsize = (15, 7)
                xticks = range(-1, 5, 1)
                yticks = np.arange(38, 42.5, 0.5)
            elif 'graph_esp' in globals() and grafo_activo == graph_esp:
                figsize = (17, 8)
                xticks = range(-9, 5, 1)
                yticks = np.arange(37, 43.5, 0.5)
            elif 'graph_eur' in globals() and grafo_activo == graph_eur:
                figsize = (17, 8)
                xticks = range(-6, 6, 1)
                yticks = np.arange(37.5, 50, 0.5)
            elif 'G' in globals() and grafo_activo == G:
                figsize = (8, 6)
                xticks = range(-5, 26, 5)
                yticks = range(-5, 26, 5)
            elif 'FF' in globals() and grafo_activo == FF:
                figsize = (8, 6)
                xticks = range(-5, 26, 5)
                yticks = range(-5, 26, 5)
            else:
                figsize = (8, 6)
                xticks = range(-5, 26, 5)
                yticks = range(-5, 26, 5)
            Plot(grafo_activo, figsize, xticks, yticks)
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

    if x_click is None or y_click is None:
        return
    elif modo_eliminar:
        umbral = 0.1
        for node in grafo_activo.nodes:
            dx = node.coordinate_x - x_click
            dy = node.coordinate_y - y_click
            distancia = (dx ** 2 + dy ** 2) ** 0.5
            if distancia < umbral:
                DeleteNode(grafo_activo, node.name)
                plt.close('all')
                if 'graph_cat' in globals() and grafo_activo == graph_cat:
                    figsize = (15, 7)
                    xticks = range(-1, 5, 1)
                    yticks = np.arange(38, 42.5, 0.5)
                elif 'graph_esp' in globals() and grafo_activo == graph_esp:
                    figsize = (17, 8)
                    xticks = range(-9, 5, 1)
                    yticks = np.arange(37, 43.5, 0.5)
                elif 'graph_eur' in globals() and grafo_activo == graph_eur:
                    figsize = (17, 8)
                    xticks = range(-6, 6, 1)
                    yticks = np.arange(37.5, 50, 0.5)
                elif 'G' in globals() and grafo_activo == G:
                    figsize = (8, 6)
                    xticks = range(-5, 26, 5)
                    yticks = range(-5, 26, 5)
                elif 'FF' in globals() and grafo_activo == FF:
                    figsize = (8, 6)
                    xticks = range(-5, 26, 5)
                    yticks = range(-5, 26, 5)
                else:
                    figsize = (8, 6)
                    xticks = range(-5, 26, 5)
                    yticks = range(-5, 26, 5)
                Plot(grafo_activo, figsize, xticks, yticks)
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
                break

    if x_click is None or y_click is None:
        return
    elif modo_encontrar_camino:
        nodo_mas_cercano = None
        distancia_min = float('inf')
        umbral_distancia = 0.1  # Ajusta según escala de tu gráfico
        for nodo in grafo_activo.nodes:
            dx = nodo.coordinate_x - x_click
            dy = nodo.coordinate_y - y_click
            distancia = (dx ** 2 + dy ** 2) ** 0.5
            if distancia < distancia_min and distancia < umbral_distancia:
                distancia_min = distancia
                nodo_mas_cercano = nodo
        if nodo_mas_cercano is None:
            print("No se seleccionó ningún nodo cercano.")
            return
        if origen_seleccionado is None:
            origen_seleccionado = nodo_mas_cercano
            print(f"Origen seleccionado: {origen_seleccionado.name}")
        else:
            destino_seleccionado = nodo_mas_cercano
            print(f"Destino seleccionado: {destino_seleccionado.name}")
            shortest_path = FindShortestPath(grafo_activo, origen_seleccionado, destino_seleccionado)
            shortest_path_global = shortest_path
            plt.close('all')
            if 'graph_cat' in globals() and grafo_activo == graph_cat:
                figsize = (15, 7)
                xticks = range(-1, 5, 1)
                yticks = np.arange(38, 42.5, 0.5)
            elif 'graph_esp' in globals() and grafo_activo == graph_esp:
                figsize = (17, 8)
                xticks = range(-9, 5, 1)
                yticks = np.arange(37, 43.5, 0.5)
            elif 'graph_eur' in globals() and grafo_activo == graph_eur:
                figsize = (17, 8)
                xticks = range(-6, 6, 1)
                yticks = np.arange(37.5, 50, 0.5)
            elif 'G' in globals() and grafo_activo == G:
                figsize = (8, 6)
                xticks = range(-5, 26, 5)
                yticks = range(-5, 26, 5)
            elif 'FF' in globals() and grafo_activo == FF:
                figsize = (8, 6)
                xticks = range(-5, 26, 5)
                yticks = range(-5, 26, 5)
            else:
                figsize = (8, 6)
                xticks = range(-5, 26, 5)
                yticks = range(-5, 26, 5)
            PlotPath(grafo_activo, shortest_path, figsize, xticks, yticks)
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
            origen_seleccionado = None
            destino_seleccionado = None

    if x_click is None or y_click is None:
        return
    elif modo_alcanzable:
        threshold = 0.1
        for nodo in grafo_activo.nodes:
            x, y = nodo.coordinate_x, nodo.coordinate_y
            dist = ((x - x_click) ** 2 + (y - y_click) ** 2) ** 0.5
            if dist <= threshold:
                nodos_seleccionados.append(nodo)
                print(f"Nodo seleccionado: {nodo.name}")
                break
        if len(nodos_seleccionados) == 2:
            n1, n2 = nodos_seleccionados
            es_alcanzable = Reachability(grafo_activo, n1, n2)
            if es_alcanzable:
                print(f"El nodo {n2.name} es alcanzable desde {n1.name}")
            else:
                print(f"El nodo {n2.name} NO es alcanzable desde {n1.name}")
            nodos_seleccionados = []
        if 'graph_cat' in globals() and grafo_activo == graph_cat:
            figsize = (15, 7)
            xticks = range(-1, 5, 1)
            yticks = np.arange(38, 42.5, 0.5)
        elif 'graph_esp' in globals() and grafo_activo == graph_esp:
            figsize = (17, 8)
            xticks = range(-9, 5, 1)
            yticks = np.arange(37, 43.5, 0.5)
        elif 'graph_eur' in globals() and grafo_activo == graph_eur:
            figsize = (17, 8)
            xticks = range(-6, 6, 1)
            yticks = np.arange(37.5, 50, 0.5)
        elif 'G' in globals() and grafo_activo == G:
            figsize = (8, 6)
            xticks = range(-5, 26, 5)
            yticks = range(-5, 26, 5)
        elif 'FF' in globals() and grafo_activo == FF:
            figsize = (8, 6)
            xticks = range(-5, 26, 5)
            yticks = range(-5, 26, 5)
        else:
            figsize = (8, 6)
            xticks = range(-5, 26, 5)
            yticks = range(-5, 26, 5)
        Plot(grafo_activo, figsize, xticks, yticks)
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


#inicializar el grafo vacío y plotearlo por pantalla al llamar a la función con el botón
def vacío():
    global grafo_activo, GV
    GV = Graph()
    grafo_activo = GV
    figsize = (8,6)
    xticks = range(-5,26,5)
    yticks = range(-5,26,5)
    Plot(GV, figsize, xticks, yticks)
    Plot(GV)
    fig = plt.gcf()
    show_plot(fig, GV)

#inicializar el grafo de ejemplo y plotearlo por pantalla al llamar a la función por medio del botón
def ejemplo():
    global grafo_activo, G
    G = CreateGraph_1()
    grafo_activo = G
    figsize = (8,6)
    xticks = range(-5,26,5)
    yticks = range(-5,26,5)
    Plot(G, figsize, xticks, yticks)
    fig = plt.gcf()
    show_plot(fig, G)


#cargar el grafo de cataluña al llamar con el botón
def catalunya():
    global grafo_activo, graph_cat
    airspace_cat = LoadAirSpaceCat()
    graph_cat = AirSpaceToGraph(airspace_cat)
    grafo_activo = graph_cat
    figsize = (15, 7)
    xticks = range(-1, 5, 1)
    yticks = np.arange(38, 42.5, 0.5)
    Plot(graph_cat, figsize, xticks, yticks)
    fig = plt.gcf()
    show_plot(fig, graph_cat)

#cargar el grafo de españa al llamar al botón
def españa():
    global grafo_activo, graph_esp
    airspace_esp = LoadAirSpaceEsp()
    graph_esp = AirSpaceToGraph(airspace_esp)
    grafo_activo = graph_esp
    figsize = (17, 8)
    xticks = range(-9, 5, 1)
    yticks = np.arange(37, 43.5, 0.5)
    Plot(graph_esp, figsize, xticks, yticks)
    fig = plt.gcf()
    show_plot(fig, graph_esp)

#cargar el grafo de Europa al llamar con el botón
def europa():
    global grafo_activo, graph_eur
    airspace_eur = LoadAirSpaceEur()
    graph_eur = AirSpaceToGraph(airspace_eur)
    grafo_activo = graph_eur
    figsize = (17, 8)
    xticks = range(-6, 6, 1)
    yticks = np.arange(37.5, 50, 0.5)
    Plot(graph_eur, figsize, xticks, yticks)
    fig = plt.gcf()
    show_plot(fig, graph_esp)


#seleccionar el grafo activo y mandarlo a un archivo llamando a la función ToFile
def save_grafo_activo():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        ToFile(grafo_activo, filename)
        print(f"Grafo activo guardado en {filename}.")

#plotear un grafo que está en un archivo
def plot_file():
    global grafo_activo, canvas_picture, canvas, outputs_frame, FF
    filename = filedialog.askopenfilename(
        title='Seleccione el archivo',
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filename:
        return None
    grafo = FromFile(filename, grafo_existente=None)
    if grafo:
        grafo_activo = grafo  # Actualiza grafo activo
        plt.close('all')
        figsize = (8, 6)
        xticks = range(-5, 26, 5)
        yticks = range(-5, 26, 5)
        Plot(grafo_activo, figsize, xticks, yticks)
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
        return grafo_activo
    else:
        print("Error cargando el grafo.")
        return None


### PROGRAMA PRINCIPAL ###
root = tk.Tk()
root.geometry("1700x950") # Tamaño inicial
root.title("INFO_PROJECT")
#la ventana principal tiene once filas y dos columnas
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 15)
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
root.rowconfigure(10, weight = 1)
root.rowconfigure(11, weight = 1)
root.rowconfigure(12, weight = 1)
root.rowconfigure(13, weight = 1)


#en la columna 0 fila 0 tenemos el frame para mostrar el gráfico de ejemplo
button_example_frame = tk.LabelFrame(root, text = 'SHOW')
button_example_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#este frame tiene una columna y una fila
button_example_frame.rowconfigure(0, weight = 1)
button_example_frame.columnconfigure(0, weight = 1)
#defino el boton del frame
button1 = tk.Button(button_example_frame, text = 'Grafo G', command = ejemplo, bg = 'lightblue', fg = 'white')
button1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 1 está el frame de selección de archivos
file_selector_frame = tk.LabelFrame(root, text = 'SELECT_FILE')
file_selector_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#este frame tiene una columna y una fila
file_selector_frame.rowconfigure(0, weight = 1)
file_selector_frame.columnconfigure(0, weight = 1)
#defino el boton del frame
button3 = tk.Button(file_selector_frame, text = 'Seleccione un archivo', command = plot_file, bg = 'lightblue', fg = 'white')
button3.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 2 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame = tk.LabelFrame(root, text = 'NEIGHBORS')
input_frame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#este frame tiene una columna y una fila
input_frame.rowconfigure(0, weight = 1)
input_frame.columnconfigure(0, weight = 1)
#y el boton del frame
button4 = tk.Button(input_frame, text = 'Mostrar vecinos', command = seleccionar_vecinos, bg = 'lightblue', fg = 'white')
button4.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 3 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_2 = tk.LabelFrame(root, text = 'ADD_NODE')
input_frame_2.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#configuración del frame
input_frame_2.rowconfigure(0, weight = 1)
input_frame_2.columnconfigure(0, weight = 1)
#y el boton del frame
button5 = tk.Button(input_frame_2, text = 'Introduzca un nodo', command = Add_Node, bg = 'lightblue', fg = 'white')
button5.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 4 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_3 = tk.LabelFrame(root, text = 'ADD_SEGMENT')
input_frame_3.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#configuración del frame
input_frame_3.rowconfigure(0, weight = 1)
input_frame_3.columnconfigure(0, weight = 1)
#y el boton del frame
button6 = tk.Button(input_frame_3, text = 'Introduzca un segmento', command = Add_Segment, bg = 'lightblue', fg = 'white')
button6.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 5 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_4 = tk.LabelFrame(root, text = 'DELETE')
input_frame_4.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#configuración del frame
input_frame_4.rowconfigure(0, weight = 1)
input_frame_4.columnconfigure(0, weight = 1)
#y el boton del frame
button7 = tk.Button(input_frame_4, text = 'Borre un nodo', command = Delete_Node, bg = 'lightblue', fg = 'white')
button7.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 6 está el frame de selección de archivos
grafo_vacío = tk.LabelFrame(root, text = 'EMPTY')
grafo_vacío.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#este frame tiene una columna y una fila
grafo_vacío.rowconfigure(0, weight = 1)
grafo_vacío.columnconfigure(0, weight = 1)
#defino el boton del frame
button8 = tk.Button(grafo_vacío, text = 'Dibujar un grafo vacío', command = vacío, bg = 'lightblue', fg = 'white')
button8.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 7 tenemos el frame para mostrar el gráfico de ejemplo
button_save_frame = tk.LabelFrame(root, text = 'SAVE ON A FILE')
button_save_frame.grid(row = 7, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#este frame tiene una columna y una fila
button_save_frame.rowconfigure(0, weight = 1)
button_save_frame.columnconfigure(0, weight = 1)
#defino el boton del frame
button9 = tk.Button(button_save_frame, text = 'Guardar modificaciones', command = save_grafo_activo, bg = 'lightblue', fg = 'white')
button9.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 8 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_5 = tk.LabelFrame(root, text = 'PATH')
input_frame_5.grid(row = 8, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#configuración del frame
input_frame_5.rowconfigure(0, weight = 1)
input_frame_5.columnconfigure(0, weight = 1)
#y el boton del frame
button12 = tk.Button(input_frame_5, text = 'Encuentre el camino mas corto', command = encontrar_camino, bg = 'lightblue', fg = 'white')
button12.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 9 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_6 = tk.LabelFrame(root, text = 'REACHABILITY')
input_frame_6.grid(row = 9, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#configuración del frame
input_frame_6.rowconfigure(0, weight = 1)
input_frame_6.columnconfigure(0, weight = 1)
#y el boton del frame
button13= tk.Button(input_frame_6, text = '¿Es alcanzable?', command = alcanzable, bg = 'lightblue', fg = 'white')
button13.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 10 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_7 = tk.LabelFrame(root, text = 'AIRSPACE')
input_frame_7.grid(row = 10, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#configuración del frame
input_frame_7.columnconfigure(0, weight = 1)
input_frame_7.columnconfigure(1, weight = 1)
input_frame_7.rowconfigure(0, weight = 1)
input_frame_7.rowconfigure(1, weight = 1)
#boton del frame
button14= tk.Button(input_frame_7, text = 'CAT', command = catalunya, bg = 'lightblue', fg = 'white')
button14.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#boton del frame
button15= tk.Button(input_frame_7, text = 'ESP', command = españa, bg = 'lightblue', fg = 'white')
button15.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#boton del frame
button15= tk.Button(input_frame_7, text = 'EUR', command = europa, bg = 'lightblue', fg = 'white')
button15.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 9 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_6 = tk.LabelFrame(root, text = 'CAMIvNO_TEXTO')
input_frame_6.grid(row = 11, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#configuración del frame
input_frame_6.rowconfigure(0, weight = 1)
input_frame_6.rowconfigure(1, weight = 1)
input_frame_6.columnconfigure(0, weight = 1)
#entrada de texto
entry_nodos = tk.Entry(input_frame_6)
entry_nodos.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#y el boton del frame
button13= tk.Button(input_frame_6, text = 'Encontrar camino', command = camino, bg = 'lightblue', fg = 'white')
button13.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 9 está el input frame en el cual el usuario introduce un grafo y el nodo del que quiere los vecinos
input_frame_6 = tk.LabelFrame(root, text = 'EXPORT TO KML')
input_frame_6.grid(row = 12, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#configuración del frame
input_frame_6.rowconfigure(0, weight = 1)
input_frame_6.columnconfigure(0, weight = 1)
#y el boton del frame
button13= tk.Button(input_frame_6, text = 'Exportar', command = exportar, bg = 'lightblue', fg = 'white')
button13.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

# Frame para calcular tiempo de recorrido
input_frame_7 = tk.LabelFrame(root, text = 'TIEMPO DE RECORRIDO')
input_frame_7.grid(row = 13, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)
#configuración del frame
input_frame_7.rowconfigure(0, weight = 1)
input_frame_7.columnconfigure(0, weight = 1)
#y el boton del frame
button14= tk.Button(input_frame_7, text = 'Calcular tiempo', command = calcular_tiempo, bg = 'lightblue', fg = 'white')
button14.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



#en la columma 1 fila 0 de la ventana principal están los outputs
outputs_frame = tk.LabelFrame(root, text = 'Outputs')
outputs_frame.grid(row = 0, column = 1, rowspan = 13, padx = 5, pady = 5, sticky = "nsew")
outputs_frame.columnconfigure(0, weight = 1)
outputs_frame.rowconfigure(0, weight = 1)


root.mainloop()