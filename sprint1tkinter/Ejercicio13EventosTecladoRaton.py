import tkinter as tk

def dibujar_circulo(event):
    x, y = event.x, event.y
    radio = 20
    canvas.create_oval(x-radio, y-radio, x+radio, y+radio, fill="blue")

def limpiar_canvas(event):
    canvas.delete("all")

root = tk.Tk()
root.title("Ejercicio 13: Eventos de teclado y ratón")

canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack(padx=10, pady=10)

canvas.bind("<Button-1>", dibujar_circulo)
root.bind("c", limpiar_canvas)

root.mainloop()