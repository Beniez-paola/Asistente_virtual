from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pymongo import MongoClient
import datetime

# Funcion de lo que hace el registro 
def registro():
    nombre = nombre_entry.get()
    correo = correo_entry.get()
    contrasena = contrasena_entry.get()
    rol = rol_var.get()

    # Verificar si el correo ya está registrado
    if usuarios.find_one({"correo_electronico": correo}):
        messagebox.showerror("Error", "Correo electrónico ya registrado")
        return

    # Insertar usuario en la base de datos
    usuarios.insert_one({
        "nombre": nombre,
        "correo_electronico": correo,
        "contrasena": contrasena,
        "rol": rol,
        "fecha_creacion": datetime.datetime.now()
    })

    messagebox.showinfo("Registro", "Usuario registrado correctamente")

    # Cerrar la ventana de registro y volver a la de login
    main_registro.destroy()
    from login import login
    login()
    
# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
db = client["speech_system"]
usuarios = db["usuarios"]

# Crear ventana
main_registro = Tk()
main_registro.title("Registro")

# Etiquetas y campos de entrada
nombre_label = Label(main_registro, text="Nombre:")
nombre_entry = Entry(main_registro)

correo_label = Label(main_registro, text="Correo electrónico:")
correo_entry = Entry(main_registro)

contrasena_label = Label(main_registro, text="Contraseña:")
contrasena_entry = Entry(main_registro, show="*")

rol_label = Label(main_registro, text="Rol:")
rol_var = StringVar()
rol_var.set("usuario")
rol_option_menu = OptionMenu(main_registro, rol_var, "usuario", "administrador")

# Botón de registro
registro_button = Button(main_registro, text="Registrar", command=registro)

# Posicionamiento de widgets
nombre_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

correo_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
correo_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

contrasena_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
contrasena_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

rol_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
rol_option_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

registro_button.grid(row=4, columnspan=2, padx=10, pady=10)

main_registro.mainloop()  



