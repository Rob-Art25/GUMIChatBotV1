from tkinter import *
from PIL import ImageTk, Image
from redPaTexto import generar_respuesta, preprocesar_texto, preguntas_procesadas


class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUMI ")
        self.root.geometry("800x600")

        self.root.resizable(0,0)

        # Ícono de la ventana
        root.iconbitmap("Chibi_GUMI02.ico")      

                            #Background
        self.fondo = ImageTk.PhotoImage(Image.open('GUMI_Background.jpeg'))
        self.imgLabel = Label(root, image = self.fondo)
        self.imgLabel.pack(fill=BOTH, expand=True)

        contenedor_widgets = Frame(root, bg="orange", bd=0,width=650, height=350) #Fondo blanco para que los widgets sean visibles
        contenedor_widgets.pack_propagate(False)  # Evitar que el contenedor se ajuste automáticamente a los widgets



        # Imagen al lado del cuadro de respuesta
        self.imagen = ImageTk.PhotoImage(Image.open('Chibi_GUMI.jpeg').resize((200, 200)))
        self.imgLabel = Label(contenedor_widgets, image = self.imagen)
        self.imgLabel.pack(side=LEFT, padx=15, expand=False)

        self.label = Label(contenedor_widgets, text="Escribe tu pregunta:", font=14, bd=0, bg="orange")
        self.label.pack(side=TOP, expand=False, pady=30)

        self.entry = Entry(contenedor_widgets, width=50)
        self.entry.pack(anchor="nw", expand=False)

        self.respuesta_text = Text(contenedor_widgets, height=5, width=32, font=18)
        self.respuesta_text.config(state=DISABLED)
        self.respuesta_text.pack(anchor="sw", pady=45, expand=False)

        self.button = Button(contenedor_widgets, text="Enviar", bg="lightgreen",command=self.enviar_pregunta)
        self.button.pack(side=BOTTOM, anchor="center", expand=False)

        self.exitButton = Button(contenedor_widgets, text="Salir", bg="red", command=self.salir_app)
        self.exitButton.pack(side=RIGHT, anchor="s", padx=50, expand=False)
        
        # Colocar el contenedor de widgets encima de la imagen de fondo
        contenedor_widgets.place(relx=0.5, rely=0.5, anchor="center")  # Centro del contenedor

    def enviar_pregunta(self):
        pregunta_usuario = self.entry.get()
        respuesta = self.obtener_respuesta(pregunta_usuario)
        self.mostrar_respuesta(respuesta)

    def obtener_respuesta(self, pregunta):
        pregunta_procesada = preprocesar_texto(pregunta)
        if pregunta_procesada not in preguntas_procesadas:
            return "Lo siento, no tengo respuesta para esa pregunta."
        else:
            return generar_respuesta(pregunta)

    def mostrar_respuesta(self, respuesta):
        self.respuesta_text.config(state=NORMAL)
        self.respuesta_text.delete(1.0, END)
        self.respuesta_text.insert(END, "GUMI: " + respuesta)
        self.respuesta_text.config(state=DISABLED)

        # Texto pa' voz
        import pygame

        pygame.init()
        pygame.mixer.init()

        if  "hola! :3" in respuesta:            
            pygame.mixer.music.load("Respuestas_Audio/GUMI Hola.wav")
            pygame.mixer.music.play()
        
        if  "16" in respuesta:            
            pygame.mixer.music.load("Respuestas_Audio/GUMI Edad.wav")
            pygame.mixer.music.play()
        
        if  "claaaro y muuuucho!" in respuesta:            
            pygame.mixer.music.load("Respuestas_Audio/GUMI Claro y Mucho.wav")
            pygame.mixer.music.play()

        if  "quisiera que si" in respuesta:            
            pygame.mixer.music.load("Respuestas_Audio/GUMI Quisiera Que Si.wav")
            pygame.mixer.music.play()
        
        if  "el sushi :3" in respuesta:            
            pygame.mixer.music.load("Respuestas_Audio/GUMI El Sushi.wav")
            pygame.mixer.music.play()
        
        if  "adiós! unu" in respuesta:            
            pygame.mixer.music.load("Respuestas_Audio/GUMI Adiós.wav")
            pygame.mixer.music.play()
        
        if  "gumi megpoid" in respuesta:            
            pygame.mixer.music.load("Respuestas_Audio/GUMI Nombre.wav")
            pygame.mixer.music.play()
    
    def salir_app(self):
        root.quit()



if __name__ == "__main__":
    root = Tk()
    app = ChatBotApp(root)
    root.mainloop()
