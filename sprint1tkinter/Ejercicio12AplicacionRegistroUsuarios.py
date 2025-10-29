import tkinter as tk
from tkinter import messagebox

def añadir_usuario():
    nombre = entry_nombre.get()
    edad = scale_edad.get()
    genero = genero_var.get()
    if nombre == "":
        messagebox.showwarning("Error", "El nombre no puede estar vacío")
        return
    lista_usuarios.insert(tk.END, f"{nombre} - {edad} años - {genero}")
    entry_nombre.delete(0, tk.END)

def eliminar_usuario():
    seleccionado = lista_usuarios.curselection()
    if seleccionado:
        lista_usuarios.delete(seleccionado)

def salir():
    root.destroy()

def guardar_lista():
    messagebox.showinfo("Guardar Lista", "Función de guardar lista")

def cargar_lista():
    messagebox.showinfo("Cargar Lista", "Función de cargar lista")

root = tk.Tk()
root.title("Ejercicio 12: Registro de Usuarios")

# Nombre
tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

# Edad
tk.Label(root, text="Edad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
scale_edad = tk.Scale(root, from_=0, to=100, orient="horizontal")
scale_edad.grid(row=1, column=1, padx=5, pady=5)

# Género
genero_var = tk.StringVar(value="Masculino")
tk.Label(root, text="Género:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
tk.Radiobutton(root, text="Masculino", variable=genero_var, value="Masculino").grid(row=2, column=1, sticky="w")
tk.Radiobutton(root, text="Femenino", variable=genero_var, value="Femenino").grid(row=3, column=1, sticky="w")
tk.Radiobutton(root, text="Otro", variable=genero_var, value="Otro").grid(row=4, column=1, sticky="w")

# Botones
tk.Button(root, text="Añadir", command=añadir_usuario).grid(row=5, column=0, padx=5, pady=10)
tk.Button(root, text="Eliminar", command=eliminar_usuario).grid(row=5, column=1, padx=5, pady=10)
tk.Button(root, text="Salir", command=salir).grid(row=5, column=2, padx=5, pady=10)

# Listbox con scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=6, column=3, sticky="ns")
lista_usuarios = tk.Listbox(root, yscrollcommand=scrollbar.set, width=40)
lista_usuarios.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
scrollbar.config(command=lista_usuarios.yview)

# Menú
menu = tk.Menu(root)
root.config(menu=menu)
archivo_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Archivo", menu=archivo_menu)
archivo_menu.add_command(label="Guardar Lista", command=guardar_lista)
archivo_menu.add_command(label="Cargar Lista", command=cargar_lista)

root.mainloop()