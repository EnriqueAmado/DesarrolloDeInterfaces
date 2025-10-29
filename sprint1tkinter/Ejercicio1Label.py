import tkinter as tk


root = tk.Tk()
root.title("Ejercicio1Label")
root.geometry("350x150")


label_saludo = tk.Label(root, text ="Bienvenido al ejercicio 1")
label_saludo.pack(pady=5)


label_nombre = tk.Label(root, text ="Tu Nombre Apellido")
label_nombre.pack(pady=5)


label_cambio = tk.Label(root, text="Texto original")
label_cambio.pack(pady=5)




def cambiar_texto():
    label_cambio.config(text="Texto cambiado al pulsar el botón")


boton = tk.Button(root, text="Cambiar texto", command=cambiar_texto)
boton.pack(pady=5)


root.mainloop()