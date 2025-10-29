import tkinter as tk
from tkinter import messagebox, filedialog


root = tk.Tk()
root.title("Ejercicio9Menu")
root.geometry("400x150")


menubar = tk.Menu(root)
root.config(menu=menubar)


menu_archivo = tk.Menu(menubar, tearoff=0)




def abrir_archivo():
    filedialog.askopenfilename(title="Abrir archivo")


menu_archivo.add_command(label="Abrir", command=abrir_archivo)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=menu_archivo)


menu_ayuda = tk.Menu(menubar, tearoff=0)


def acerca_de():
    messagebox.showinfo("Acerca de", "Ejercicio 9 - Menú\nDesarrollo de Interfaces 2025/26")


menu_ayuda.add_command(label="Acerca de", command=acerca_de)
menubar.add_cascade(label="Ayuda", menu=menu_ayuda)


root.mainloop()