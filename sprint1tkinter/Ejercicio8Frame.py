import tkinter as tk


root = tk.Tk()
root.title("Ejercicio8Frame")
root.geometry("400x200")


frame_top = tk.Frame(root, bd=2, relief=tk.SUNKEN, pady=10)
frame_top.pack(fill='x')
frame_bottom = tk.Frame(root, pady=10)
frame_bottom.pack(fill='x')


lbl1 = tk.Label(frame_top, text="Etiqueta 1")
lbl1.grid(row=0, column=0, padx=5)


lbl2 = tk.Label(frame_top, text="Etiqueta 2")
lbl2.grid(row=0, column=1, padx=5)


entrada = tk.Entry(frame_top)
entrada.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky='we')


label_mostrar = tk.Label(frame_bottom, text="Aquí se mostrará el contenido")
label_mostrar.pack(pady=5)




def mostrar():
    label_mostrar.config(text=entrada.get())




def borrar():
    entrada.delete(0, tk.END)
    label_mostrar.config(text="")


bot_mostrar = tk.Button(frame_bottom, text="Mostrar", command=mostrar)
bot_mostrar.pack(side=tk.LEFT, padx=20)
bot_borrar = tk.Button(frame_bottom, text="Borrar", command=borrar)
bot_borrar.pack(side=tk.RIGHT, padx=20)


root.mainloop()