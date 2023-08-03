
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Parámetros del juego
WIDTH, HEIGHT = 640, 480
PADDLE_HEIGHT = 60
BALL_RADIUS = 10
LR = 0.001  # Tasa de aprendizaje
EPISODES = 10000  # Número de episodios de entrenamiento
STEPS_PER_EPISODE = 500  # Número de pasos por episodio

# Función para generar el conjunto de datos de entrenamiento
def generate_training_data():
    training_data = []
    for episode in range(EPISODES):
        paddle1_pos = (HEIGHT - PADDLE_HEIGHT) // 2
        ball_pos = [WIDTH // 2, HEIGHT // 2]
        ball_vel = [5, 5]
        episode_data = []
        for step in range(STEPS_PER_EPISODE):
            input_data = np.array([paddle1_pos, ball_pos[0], ball_pos[1]])
            action = 0 if paddle1_pos <= ball_pos[1] else 1  # Acción para la red neuronal (0: Mover hacia arriba, 1: Mover hacia abajo)
            episode_data.append((input_data, action))
            # Movimiento de la paleta controlada por la IA (red neuronal)
            if paddle1_pos <= ball_pos[1]:
                paddle1_pos += 5
            else:
                paddle1_pos -= 5
            # Movimiento de la pelota
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]
            # Colisiones con las paredes
            if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - BALL_RADIUS:
                ball_vel[1] = -ball_vel[1]
        training_data.extend(episode_data)
    return training_data

# Generar el conjunto de datos de entrenamiento
training_data = generate_training_data()

# Preparar los datos de entrenamiento
inputs = np.array([data[0] for data in training_data])
actions = np.array([data[1] for data in training_data])

# Construir el modelo de red neuronal
model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(3,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compilar el modelo
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LR),
              loss='binary_crossentropy',
              metrics=['accuracy'])
#model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LR),
#              loss='sparse_categorical_crossentropy',  # O 'categorical_crossentropy' si las acciones están codificadas de manera one-hot
#              metrics=['accuracy'])

# Entrenar el modelo
model.fit(inputs, actions, epochs=10, batch_size=32)

# Guardar el modelo entrenado
model.save('pong_model.h5')