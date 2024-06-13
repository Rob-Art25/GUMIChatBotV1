import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from nltk.corpus import stopwords
import numpy as np

print("Tensorflow Version:", tf.__version__)

# Preguntas y Respuestas
preguntas = ["Hola", "Te Quieren?", "Me Quieres?", "Adiós", 
             "comida favorita?", "cómo te llamas?", "cuántos años tienes?"]

respuestas = ["Hola! :3", "Quisiera que si", "Claaaro y Muuuucho!", "Adiós! unu", 
              "El Sushi :3", "Gumi Megpoid", "16"]

# Preprocesamiento de texto
stop_words = set(stopwords.words('spanish'))

def preprocesar_texto(texto):
    # Convertir a minúsculas
    texto = texto.lower() if isinstance(texto, str) else texto
    return texto

preguntas_procesadas = [preprocesar_texto(pregunta) for pregunta in preguntas]
respuestas_procesadas = [preprocesar_texto(respuesta) for respuesta in respuestas]

# Tokenización y Padding
tokenizer = Tokenizer(filters='')
tokenizer.fit_on_texts(preguntas_procesadas + respuestas_procesadas)

preguntas_secuencia = tokenizer.texts_to_sequences(preguntas_procesadas)
respuestas_secuencia = tokenizer.texts_to_sequences(respuestas_procesadas)

# Ajustar la longitud de las secuencias de preguntas y respuestas
max_len_preguntas = max(len(seq) for seq in preguntas_secuencia)
max_len_respuestas = max_len_preguntas

preguntas_padded = pad_sequences(preguntas_secuencia, maxlen=max_len_preguntas, padding='post')
respuestas_padded = pad_sequences(respuestas_secuencia, maxlen=max_len_respuestas, padding='post')

# Definición del Modelo
model = Sequential()
model.add(Embedding(len(tokenizer.word_index) + 1, 128, input_length=max_len_preguntas))
model.add(LSTM(256, return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(256, return_sequences=True))
model.add(Dense(len(tokenizer.word_index) + 1, activation='softmax'))

# Compilación del Modelo
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics=['accuracy']
)

# Entrenamiento del Modelo
print("Entrenando el modelo...")
model.fit(preguntas_padded, respuestas_padded, epochs=500, verbose=False) # Base son 500 epocas, probaar con más...
print("Modelo entrenado!")

# Función para generar respuesta
def generar_respuesta(pregunta):
    pregunta_secuencia = tokenizer.texts_to_sequences([pregunta])
    pregunta_padded = pad_sequences(pregunta_secuencia, maxlen=max_len_preguntas, padding='post')
    respuesta_padded = model.predict(pregunta_padded)

    # Obtener las palabras más probables
    palabras_indices = np.argmax(respuesta_padded, axis=-1)
    respuesta = []
    for indice in palabras_indices[0]:
        palabra = tokenizer.index_word.get(indice, ' ')
        """if palabra == 'end' or palabra is None:
            break
        """
        respuesta.append(palabra)

    return ' '.join(respuesta)


"""# Interacción con el usuario
print("¡Hola! Soy GUMI. Puedes escribir 'salir' en cualquier momento para terminar la conversación.")
while True:
    pregunta_usuario = input("En qué te puedo ayudar?: ")
    if pregunta_usuario.lower() == 'salir':
        print("GUMI: ¡Hasta luego! ^u^")
        break
    if preprocesar_texto(pregunta_usuario) not in preguntas_procesadas:
        print("GUMI: Lo siento, no tengo respuesta para esa pregunta.")
    else:
        respuesta = generar_respuesta(pregunta_usuario)
        print("GUMI:", respuesta)
"""