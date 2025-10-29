import tkinter as tk

from tkinter import messagebox

def dibujar():
    try:
        # Obtener los valores de los Entry
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        x2 = int(entry_x2.get())
        y2 = int(entry_y2.get())

        # Limpiar el canvas antes de dibujar algo nuevo
        canvas.delete("all")

        # Dibujar un rectángulo y un círculo
        canvas.create_rectangle(x1, y1, x2, y2, outline='black', width=2)
        canvas.create_oval(x1, y1, x2, y2, outline='blue', width=2)

    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce solo números válidos.")

root = tk.Tk()
root.title("Ejercicio7Canvas")

tk.Label(root, text="x1:").grid(row=0, column=0, padx=5, pady=5)
entry_x1 = tk.Entry(root)
entry_x1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="y1:").grid(row=1, column=0, padx=5, pady=5)
entry_y1 = tk.Entry(root)
entry_y1.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="x2:").grid(row=2, column=0, padx=5, pady=5)
entry_x2 = tk.Entry(root)
entry_x2.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="y2:").grid(row=3, column=0, padx=5, pady=5)
entry_y2 = tk.Entry(root)
entry_y2.grid(row=3, column=1, padx=5, pady=5)

boton_dibujar = tk.Button(root, text="Dibujar", command=dibujar)
boton_dibujar.grid(row=4, column=0, columnspan=2, pady=10)

canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
