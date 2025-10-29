import tkinter as tk

def actualizar_valor(valor):
    etiqueta.config(text=f"Valor seleccionado: {valor}")

root = tk.Tk()
root.title("Ejercicio 11: Scale")

scale = tk.Scale(root, from_=0, to=100, orient="horizontal", command=actualizar_valor)
scale.pack(padx=20, pady=20)

etiqueta = tk.Label(root, text="Valor seleccionado: 0")
etiqueta.pack(padx=20, pady=10)

root.mainloop()