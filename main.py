
# Aqui se ejecuta todos los archivos
import registro
import login
import gui2

if __name__ == "__main__":
    # Realizar registro
    registro.realizar_registro()
    
    # Iniciar sesión
    login.main_login.mainloop()

    # Ejecutar el asistente virtual
    gui2.main_window.mainloop()




