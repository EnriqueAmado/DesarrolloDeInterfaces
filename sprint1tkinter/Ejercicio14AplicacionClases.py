import tkinter as tk
from tkinter import messagebox

class RegistroApp:
    def __init__(self, root):
        self.root = root
        root.title("Ejercicio 14: Registro de Usuarios con Clases")

        # Nombre
        tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Edad
        tk.Label(root, text="Edad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.scale_edad = tk.Scale(root, from_=0, to=100, orient="horizontal")
        self.scale_edad.grid(row=1, column=1, padx=5, pady=5)

        # Género
        self.genero_var = tk.StringVar(value="Masculino")
        tk.Label(root, text="Género:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Radiobutton(root, text="Masculino", variable=self.genero_var, value="Masculino").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(root, text="Femenino", variable=self.genero_var, value="Femenino").grid(row=3, column=1, sticky="w")
        tk.Radiobutton(root, text="Otro", variable=self.genero_var, value="Otro").grid(row=4, column=1, sticky="w")

        # Botones
        tk.Button(root, text="Añadir", command=self.añadir_usuario).grid(row=5, column=0, padx=5, pady=10)
        tk.Button(root, text="Eliminar", command=self.eliminar_usuario).grid(row=5, column=1, padx=5, pady=10)
        tk.Button(root, text="Salir", command=self.salir).grid(row=5, column=2, padx=5, pady=10)

        # Listbox con scrollbar
        self.scrollbar = tk.Scrollbar(root)
        self.scrollbar.grid(row=6, column=3, sticky="ns")
        self.lista_usuarios = tk.Listbox(root, yscrollcommand=self.scrollbar.set, width=40)
        self.lista_usuarios.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        self.scrollbar.config(command=self.lista_usuarios.yview)

    def añadir_usuario(self):
        nombre = self.entry_nombre.get()
        edad = self.scale_edad.get()
        genero = self.genero_var.get()
        if nombre == "":
            messagebox.showwarning("Error", "El nombre no puede estar vacío")
            return
        self.lista_usuarios.insert(tk.END, f"{nombre} - {edad} años - {genero}")
        self.entry_nombre.delete(0, tk.END)

    def eliminar_usuario(self):
        seleccionado = self.lista_usuarios.curselection()
        if seleccionado:
            self.lista_usuarios.delete(seleccionado)

    def salir(self):
        self.root.destroy()

# Crear la instancia
root = tk.Tk()
app = RegistroApp(root)
root.mainloop()