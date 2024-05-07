# Importar los módulos necesarios
from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient

# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
db = client["speech_system"]
tecnicos_collection = db["tecnico_humano"]

class VentanaNumeroCuenta:
    def __init__(self, parent):
        self.parent = parent
        self.ventana = Toplevel(parent)
        self.ventana.title("Ingrese su información")
        
        self.label_nombre = Label(self.ventana, text="Nombre completo:")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=5)
        self.entry_nombre = Entry(self.ventana)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=5)
        
        self.label_cuenta = Label(self.ventana, text="Número de cuenta:")
        self.label_cuenta.grid(row=1, column=0, padx=10, pady=5)
        self.entry_cuenta = Entry(self.ventana)
        self.entry_cuenta.grid(row=1, column=1, padx=10, pady=5)
        
        self.label_telefono = Label(self.ventana, text="Número de teléfono:")
        self.label_telefono.grid(row=2, column=0, padx=10, pady=5)
        self.entry_telefono = Entry(self.ventana)
        self.entry_telefono.grid(row=2, column=1, padx=10, pady=5)
        
        self.boton_enviar = Button(self.ventana, text="Enviar", command=self.enviar_info)
        self.boton_enviar.grid(row=3, columnspan=2, padx=10, pady=10)
    
    def enviar_info(self):
        nombre = self.entry_nombre.get()
        cuenta = self.entry_cuenta.get()
        telefono = self.entry_telefono.get()
        
        if nombre and cuenta and telefono:
            # Muestra los datos del técnico humano y del usuario
            tecnico = tecnicos_collection.find_one()
            mensaje = f"Te pondremos en contacto con {tecnico['nombre']} al número {tecnico['numero_telefono']}.\n"
            mensaje += f"Tu nombre completo es: {nombre}\n"
            mensaje += f"Tu número de cuenta es: {cuenta}\n"
            mensaje += f"Tu número de teléfono es: {telefono}"
            messagebox.showinfo("Información de contacto", mensaje)
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")


