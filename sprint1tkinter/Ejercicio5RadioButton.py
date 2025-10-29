import tkinter as tk


root = tk.Tk()
root.title("Ejercicio 5 - Radiobutton")
root.geometry("300x160")


var_color = tk.StringVar(value="white")




def cambiar_color():
    root.config(bg=var_color.get())


label = tk.Label(root, text="Elige tu color favorito:")
label.pack(pady=5)


rb1 = tk.Radiobutton(root, text="Rojo", variable=var_color, value="red", command=cambiar_color)
rb1.pack(anchor='w')
rb2 = tk.Radiobutton(root, text="Verde", variable=var_color, value="green", command=cambiar_color)
rb2.pack(anchor='w')
rb3 = tk.Radiobutton(root, text="Azul", variable=var_color, value="blue", command=cambiar_color)
rb3.pack(anchor='w')


root.mainloop()