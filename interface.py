import tkinter as tk

from Scripts.graph import AddNode
from test_graph import CreateGraph_1
from graph import *
from tkinter import filedialog



current_graph = [
    {'name': 'Node A', 'neighbors': ['Node B', 'Node C']},
    {'name': 'Node B', 'neighbors': ['Node A', 'Node D']},
    {'name': 'Node C', 'neighbors': ['Node A']},
    {'name': 'Node D', 'neighbors': ['Node B']}
]

def update_node_listbox():
    """Actualiza la lista de nodos en el Listbox."""
    node_listbox.delete(0, tk.END)  # Eliminar todos los nodos actuales
    for node in current_graph:
        node_listbox.insert(tk.END, node['name'])  # Insertar cada nodo en el Listbox

def on_select_node(event):
    """Acción cuando se selecciona un nodo."""
    try:
        selected_node_name = node_listbox.get(node_listbox.curselection())
        selected_node = next((n for n in current_graph if n['name'] == selected_node_name), None)
        if selected_node:
            show_neighbors(selected_node)
    except IndexError:
        pass  # En caso de que no haya selección, no hace nada

def show_neighbors(node):
    """Muestra los vecinos de un nodo."""
    neighbors_list = node['neighbors']
    neighbors_text.set(f"Vecinos de {node['name']}: {', '.join(neighbors_list)}")




def step_3():
    G = CreateGraph_1()
    Plot(G)

def inventado():
    G = CreateGraph_2()
    Plot(G)

def load_and_plot_file():
    filename = filedialog.askopenfilename(
        title="Selecciona el archivo de grafo",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if filename:
        g = graph_from_file(filename)
        Plot(g)

root = tk.Tk()
root.geometry("800x600")
root.title("STEP4")

#configuración visual principal que consta de dos columnas y 4 filas
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 10)
root.rowconfigure(0, weight = 1)
root.rowconfigure(1, weight = 1)
root.rowconfigure(2, weight = 1)
root.rowconfigure(3, weight = 1)
root.rowconfigure(4,weight = 1)


#en la coluumna 0 fila 0 tenemos el frame para el ejemplo del paso 3
button_example_frame = tk.LabelFrame(root, text = "Example graph from step 3")
button_example_frame.grid(row=0, column= 0, padx=5, pady=5, sticky = tk.N + tk.E + tk.W + tk.S)

#este frame tiene una columna y una fila
button_example_frame.rowconfigure(0, weight = 1)
button_example_frame.columnconfigure(0, weight = 1)

#defino los botones del frame
button1 = tk.Button(button_example_frame, text = "Mostrar gráfico STEP 3", command = step_3)
button1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 1 de la ventana principal tenemos el frame para el gráfico inventado
button_invented_frame = tk.LabelFrame(root, text = "Ejemplo inventado from step 3")
button_invented_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#este frame tiene una columna y una fila
button_invented_frame.rowconfigure(0, weight = 1)
button_invented_frame.columnconfigure(0,weight = 1)

#defino los botones del frame:
button2 = tk.Button(button_invented_frame, text = "Mostrar gráfico inventado", command = inventado)
button2.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 2 de la ventana principal tenemos el frame para seleccionar file
button_selection_frame = tk.LabelFrame(root, text = "Selección de archivos")
button_selection_frame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#este frame tiene 2 filas y dos columnas
button_selection_frame.rowconfigure(2, weight = 1)
button_selection_frame.columnconfigure(2,weight = 1)

#defino el boton del frame para seleccionar el archivo:
button3 = tk.Button(button_selection_frame, text = "Seleccione el archivo", command = load_and_plot_file)
button3.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)



#en la columna 0 fila 1 de la ventana principal tenemos el frame para el gráfico inventado
button_nodeselection_frame = tk.LabelFrame(root, text = "Seleccione un nodo para mostrar sus vecinos")
button_nodeselection_frame.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#este frame tiene una columna y una fila
button_nodeselection_frame.rowconfigure(2, weight = 1)
button_nodeselection_frame.columnconfigure(2,weight = 1)

node_listbox = tk.Listbox(button_nodeselection_frame)
node_listbox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

# Añadir la función de selección de nodo
node_listbox.bind('<<ListboxSelect>>', on_select_node)

# Etiqueta para mostrar los vecinos
neighbors_text = tk.StringVar()
neighbors_label = tk.Label(root, textvariable=neighbors_text)
neighbors_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

# Actualizar la lista de nodos al cargar la ventana
update_node_listbox()


#En la columna 0 fila 4 está el input frame
input_frame = tk.LabelFrame(root,text = "Input")
input_frame.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

input_frame.rowconfigure(0,weight = 1)
input_frame.rowconfigure(1,weight = 1)
input_frame.columnconfigure(0,weight = 1)

entry = tk.Entry(input_frame)
entry.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

button11 = tk.Button(input_frame, text = "Input", command = AddNode)
button11.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 2 de la ventana principal está el select file que son cuatro botones
outputs_frame = tk.LabelFrame(root, text = "Outputs")
outputs_frame.grid(row = 0, column = 1, rowspan = 3, padx = 5, pady = 5, sticky = "nsew")


root.mainloop()