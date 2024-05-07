from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pymongo import MongoClient

# Ventana principal
main_login = Tk()
main_login.title("Inicio de sesión")

# Fondo de la ventana
imagen_fondo = Image.open("soporte_tecnico.png").resize((400, 300))
fondo_login = ImageTk.PhotoImage(imagen_fondo)
fondo_label = Label(main_login, image=fondo_login)
fondo_label.pack()

# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
db = client["speech_system"]
usuarios = db["usuarios"]

# Función para abrir la ventana de registro
def abrir_registro():
    main_login.withdraw()
    import registro  # Import registro inside the function
    registro.realizar_registro()
    
def login():
    correo = correo_entry.get()
    contrasena = contrasena_entry.get()

    usuario = usuarios.find_one({"correo_electronico": correo})

    if not usuario:
        messagebox.showerror("Error", "Usuario no encontrado")
    elif usuario["contrasena"] != contrasena:
        messagebox.showerror("Error", "Contraseña incorrecta")
    else:
        messagebox.showinfo("Inicio de sesión", "Bienvenido " + usuario["nombre"])
        pass

# Etiquetas y campos de entrada
correo_label = Label(main_login, text="Correo electrónico")
correo_entry = Entry(main_login)

contrasena_label = Label(main_login, text="Contraseña")
contrasena_entry = Entry(main_login, show="*")

# Botón de inicio de sesión
login_boton = Button(main_login, text="Iniciar sesión", command=login)

# Posicionamiento de widgets
correo_label.place(x=100, y=100)
correo_entry.place(x=100, y=125)

contrasena_label.place(x=100, y=150)
contrasena_entry.place(x=100, y=175)

login_boton.place(x=100, y=200)

main_login.mainloop()







