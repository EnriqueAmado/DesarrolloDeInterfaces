import tkinter as tk


root = tk.Tk()
root.title("Ejercicio 3 - Entry")
root.geometry("350x140")


label_instr = tk.Label(root, text="Escribe tu nombre:")
label_instr.pack(pady=5)


entrada = tk.Entry(root)
entrada.pack(pady=5)


label_saludo = tk.Label(root, text="")
label_saludo.pack(pady=5)




def saludar():
    nombre = entrada.get().strip()
    if nombre:
        label_saludo.config(text=f"Hola, {nombre}!")
    else:
        label_saludo.config(text="Por favor, introduce tu nombre.")


boton = tk.Button(root, text="Saludar", command=saludar)
boton.pack(pady=5)


root.mainloop()