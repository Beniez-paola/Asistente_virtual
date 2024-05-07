from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import speech_recognition as sr 
import pyttsx3
import wikipedia
import sys
import threading as tr
from pymongo import MongoClient
from tecnicohuman import VentanaNumeroCuenta

#nombre del asistente
name = 'Paloma'

# Diseño del GUI del asistente
main_window = Tk()
main_window.title("Asistente virtual")
    
main_window.geometry("900x500")
main_window.resizable(0,0)
main_window.configure(bg='#d2b48c')
    
label_title = Label(main_window, text="Soporte tecnico", bg='#d2b48c', fg="#000000",
                    font=('Verdana', 40, 'bold'))
label_title.pack(pady=10)
    
soporte_tecnico = ImageTk.PhotoImage(Image.open('soporte_tecnico.png'))
window_photo = Label(main_window, image=soporte_tecnico)
window_photo.pack(pady=5)

#Se establece la conexion de la base de datos con su colección 
client = MongoClient('mongodb://localhost:27017/')
db = client['speech_system']
requests_collection = db['user_requests']

# Aplicacion del patron Estrategia para manejar consultas complejas
class EscalateToHumanStrategy:
    def execute_query(self, query):
       if 'compleja' in query:
            # Realiza una consulta a la base de datos para verificar si hay una respuesta para esta consulta
            result = db.soporte_tecnico.find_one({"pregunta": query})
            if result:
                self.talk(result['respuesta'])
            else:
                pass # Escala a tecnico humano en la parte de abajo del programa
    
# Patron Singleton para el Procesador de Lenguaje Natural
class NaturalLanguageProcessor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Inicializa el procesador de lenguaje natural aquí
            cls._instance.recognizer = sr.Recognizer()
            cls._instance.engine = pyttsx3.init()
            # Configura la voz del asistente
            voices = cls._instance.engine.getProperty('voices')
            cls._instance.engine.setProperty('voice', voices[0].id)
            cls._instance.engine.setProperty('rate', 178)
            cls._instance.engine.setProperty('volume', 0.7)
            # Inicializa la estrategia por defecto
            cls._instance.strategy = EscalateToHumanStrategy()
        return cls._instance
    
    #Funcion de los procesos en general de lo que va a hacer el asistente
    def process_input(self):
        rec_audios = self.listen()

        rec = rec_audios['text']
        status = rec_audios['status']

        if status:
            if 'busca' in rec:
                order = rec.replace('busca', '')
                wikipedia.set_lang("es")
                info = wikipedia.summary(order, 1)
                self.talk(info)
            elif 'repite' in rec:
                last_request = self.get_last_request()
                if last_request:
                    self.talk(f"La última petición fue: {last_request}")
                else:
                    self.talk("No hay ninguna petición previa para repetir.")
            elif 'descansa' in rec:
                self.talk("¡Espero haberte ayudado! Hasta la próxima.")
                sys.exit()  # Sale del programa
            else:
                # Consulta en la base de datos MongoDB
                query = {"$or": [{"pregunta": {"$regex": rec, "$options": "i"}},
                                 {"tema": {"$regex": rec, "$options": "i"}},
                                 {"subtema": {"$regex": rec, "$options": "i"}},
                                 {"etiquetas": {"$in": [rec]}}]}
                result = db.soporte_tecnico.find_one(query)
                if result:
                    self.talk(result['respuesta'])
                else:
                    # Aquí puedes agregar el mensaje para enviar al usuario a soporte técnico
                    self.talk("Lo siento, no tengo una respuesta para esa pregunta. Tu solicitud será enviada a soporte técnico.")

            self.save_request(rec)
            
 # Esta funcion es para configurar como nos va a responder o hablar la asistente
    def listen(self):
        r = sr.Recognizer()
        status = False

        with sr.Microphone() as source:
            self.talk("Escuchando...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            rec = ""

            try:
                rec = r.recognize_google(audio, language='es-ES').lower()
                status = True
                if name in rec:
                    rec = rec.replace(f"{name} ", "")

            except:
                pass
        return {'text': rec, 'status': status}

   #Funcion que devuelve lo que le comentamos  
    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    # esta funcion almacenara la peticion que le pidamos a la asistente
    def save_request(self, request_text):
        requests_collection.insert_one({'request_text': request_text})
    # Aqui esta cuando se solicite repetir la consulta este la volvera a mencionar
    def get_last_request(self):
        last_request = requests_collection.find_one(sort=[('_id', -1)])
        if last_request:
           return last_request['request_text']
        else:
           return None
            
nlp_instance = NaturalLanguageProcessor()

#Parte del GUI
button_listen = Button(main_window, text="Escuchar", fg="black", bg="#f5f5dc",
            font=('Verdana', 30, 'bold'), command=nlp_instance.process_input)
button_listen.pack(side=BOTTOM, pady=40)
      
def say_hello():
    #Comentario de inicio del asistente
    nlp_instance.talk("Hola, mi nombre es Paloma. ¿En qué puedo ayudarte?".format(name))
    
#Lo transforma en hilos para que se ejecute al mismo tiempo del programa    
def hello_thread():
    t = tr.Thread(target=say_hello)
    t.start()

# Iniciar el hilo de escucha
hello_thread()
     
def mostrar_comandos():
    messagebox.showinfo("Ayuda","Paloma...busca\nPaloma..repite\nPara preguntar consultas no ocupa mencionar el nombre de Paloma\ndescansa..")
    
# Botón para solicitar información de usuario
def abrir_ventana_numero_cuenta():  # Define la función para abrir la ventana de solicitud de información del usuario
    ventana_cuenta = VentanaNumeroCuenta(main_window)
  
# Botón para mostrar comandos
button_help_comandos = Button(main_window, text="Comandos", command=mostrar_comandos, borderwidth=0, bg='#f5f5dc', fg='black', font=('Verdana', 7, 'bold'))
button_help_comandos.place(relx=1, rely=0.1, anchor='ne', x=-10, y=10, width=70, height=50)

# Botón para solicitar información de usuario
button_help_solicitar = Button(main_window, text="Tecnico humano", command=abrir_ventana_numero_cuenta, borderwidth=0, bg='#f5f5dc', fg='black', font=('Verdana', 7, 'bold'))
button_help_solicitar.place(relx=1, rely=0.3, anchor='ne', x=-10, y=10, width=150, height=50)

#Manda a llamar la ventana del asistente   
main_window.mainloop()
