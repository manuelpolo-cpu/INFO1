import tkinter as tk

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

#en la columna 0 fila 2 de la ventana principal está el select file pero no se si ha de ser un selector
outputs_frame = tk.LabelFrame(root, text = "Outputs")
outputs_frame.grid(row = 0, column = 1, rowspan = 3, padx = 5, pady = 5, sticky = "nsew")

root.mainloop()