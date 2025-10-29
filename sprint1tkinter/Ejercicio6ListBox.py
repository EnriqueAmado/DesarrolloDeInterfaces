import tkinter as tk


root = tk.Tk()
root.title("Ejercicio 6 - Listbox")
root.geometry("300x200")


label = tk.Label(root, text="Selecciona una fruta:")
label.pack(pady=5)


listbox = tk.Listbox(root, height=5)
frutas = ["Manzana", "Banana", "Naranja", "Pera", "Melocotón"]
for f in frutas:
    listbox.insert(tk.END, f)
    listbox.pack(pady=5)


label_sel = tk.Label(root, text="Fruta seleccionada: ")
label_sel.pack(pady=5)




def mostrar_seleccion():
    sel = listbox.curselection()
    if sel:
        fruta = listbox.get(sel[0])
        label_sel.config(text=f"Fruta seleccionada: {fruta}")
    else:
        label_sel.config(text="No has seleccionado ninguna fruta.")


boton = tk.Button(root, text="Mostrar fruta", command=mostrar_seleccion)
boton.pack(pady=5)


root.mainloop()