import tkinter as tk

from select import select

root = tk.Tk()
root.geometry("800x400")
root.title("STEP4")

#configuración visual principal que consta de dos columnas y 4 filas
root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 10)
root.rowconfigure(0, weight = 1)
root.rowconfigure(1, weight = 1)
root.rowconfigure(2, weight = 1)
root.rowconfigure(3, weight = 1)


#en la coluumna 0 fila 0 tenemos el frame para el ejemplo del paso 3
button_example_frame = tk.LabelFrame(root, text = "Example graph from step 3")
button_example_frame.grid(row=0, column= 0, padx=5, pady=5, sticky = tk.N + tk.E + tk.W + tk.S)

#este frame tiene una columna y una fila
button_example_frame.rowconfigure(0, weight = 1)
button_example_frame.columnconfigure(0, weight = 1)

#defino los botones del frame
button1 = tk.Button(button_example_frame, text = "Mostrar gráfico STEP 3", command = None)
button1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 1 de la ventana principal tenemos el frame para el gráfico inventado
button_invented_frame = tk.LabelFrame(root, text = "Ejemplo inventado from step 3")
button_invented_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#este frame tiene una columna y una fila
button_invented_frame.rowconfigure(0, weight = 1)
button_invented_frame.columnconfigure(0,weight = 1)

#defino los botones del frame:
button2 = tk.Button(button_invented_frame, text = "Mostrar gráfico inventado", command = None)
button2.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 2 de la ventana principal tenemos el frame para seleccionar file
button_selection_frame = tk.LabelFrame(root, text = "Seleccione los archivos")
button_selection_frame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#este frame tiene 2 filas y dos columnas
button_selection_frame.rowconfigure(2, weight = 1)
button_selection_frame.columnconfigure(2,weight = 1)

#defino los botones del frame:
button3 = tk.Button(button_selection_frame, text = "FILE 1", comand = None)
button3.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

button4 = tk.Button(button_selection_frame, text = "FILE 2", comand = None)
button4.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

button5 = tk.Button(button_selection_frame, text = "FILE 3", comand = None)
button5.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

button6 = tk.Button(button_selection_frame, text = "FILE 4", comand = None)
button6.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 1 de la ventana principal tenemos el frame para el gráfico inventado
button_nodeselection_frame = tk.LabelFrame(root, text = "Ejemplo inventado from step 3")
button_nodeselection_frame.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

#este frame tiene una columna y una fila
button_nodeselection_frame.rowconfigure(2, weight = 1)
button_nodeselection_frame.columnconfigure(2,weight = 1)

#defino los botones del frame:
button7 = tk.Button(button_nodeselection_frame, text = "NODE A", command = None)
button7.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

button8 = tk.Button(button_nodeselection_frame, text = "NODE B", command = None)
button8.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

button9 = tk.Button(button_nodeselection_frame, text = "NODE C", command = None)
button9.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)

button10 = tk.Button(button_nodeselection_frame, text = "NODE D", command = None)
button10.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tk.N + tk.E + tk.W + tk.S)


#en la columna 0 fila 2 de la ventana principal está el select file que son cuatro botones
outputs_frame = tk.LabelFrame(root, text = "Outputs")
outputs_frame.grid(row = 0, column = 1, rowspan = 3, padx = 5, pady = 5, sticky = "nsew")

root.mainloop()