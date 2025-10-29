import tkinter as tk
from tkinter import scrolledtext


root = tk.Tk()
root.title("Ejercicio10Scrollbar")
root.geometry("500x300")


frame = tk.Frame(root)
frame.pack(fill='both', expand=True)


scroll = tk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)


texto = tk.Text(frame, wrap='word', yscrollcommand=scroll.set)
texto.pack(side=tk.LEFT, fill='both', expand=True)


scroll.config(command=texto.yview)


# Rellenar con texto de prueba (varios párrafos)
for i in range(1, 21):
    texto.insert(tk.END, f"Párrafo {i}: Este es un texto de ejemplo para probar la barra de desplazamiento.\n\n")


root.mainloop()