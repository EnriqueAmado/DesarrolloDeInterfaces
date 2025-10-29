import tkinter as tk


root = tk.Tk()
root.title("Ejercicio 4 - Checkbutton")
root.geometry("350x160")


var_leer = tk.IntVar()
var_deporte = tk.IntVar()
var_musica = tk.IntVar()


label_estado = tk.Label(root, text="Aficiones seleccionadas: ")
label_estado.pack(pady=5)




def actualizar():
    seleccion = []
    if var_leer.get():
        seleccion.append("Leer")
    if var_deporte.get():
        seleccion.append("Deporte")
    if var_musica.get():
        seleccion.append("Música")
    if seleccion:
        label_estado.config(text="Aficiones seleccionadas: " + ", ".join(seleccion))
    else:
        label_estado.config(text="Aficiones seleccionadas: Ninguna")


cb1 = tk.Checkbutton(root, text="Leer", variable=var_leer, command=actualizar)
cb1.pack(anchor='w')
cb2 = tk.Checkbutton(root, text="Deporte", variable=var_deporte, command=actualizar)
cb2.pack(anchor='w')
cb3 = tk.Checkbutton(root, text="Música", variable=var_musica, command=actualizar)
cb3.pack(anchor='w')


root.mainloop()