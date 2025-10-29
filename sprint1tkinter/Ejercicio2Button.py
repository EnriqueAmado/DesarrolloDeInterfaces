import tkinter as tk


root = tk.Tk()
root.title("Ejercicio2Button")
root.geometry("300x120")


label = tk.Label(root, text="Pulsa un botón")
label.pack(pady=10)




def mostrar_mensaje():
    label.config(text="Has pulsado el botón!")


bot_mostrar = tk.Button(root, text="Mostrar", command=mostrar_mensaje)
bot_mostrar.pack(side=tk.LEFT, padx=20, pady=10)


bot_salir = tk.Button(root, text="Salir", command=root.quit)
bot_salir.pack(side=tk.RIGHT, padx=20, pady=10)


root.mainloop()