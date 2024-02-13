import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import alfabeto as letras;
import re


texto = ''
while(True): # Bucle que se rompe hasta que el usuario ingrese un mensaje válido
    texto = input('Ingrese un mensaje\n').lower() # Input para tomar el mensaje
    if re.match(r'^[a-zA-Z\s]+$', texto): # Expresion regular para verificar que solo sean letras u espacios
        if len(texto) > 30: # Verificar máximo 30 caracteres
            print('Por favor ingrese un mensaje de máximo 30 caracteres!')
        else:
            break    
    else:
        print('Por favor ingrese un mensaje válido! Solo letras del alfabeto inglés [A-Z]')
    
    

mensaje = [np.array(letras.alfabeto_conway[i]) for i in texto] # Generar un array de matrices a partir del mensaje ingresado por el usuario
matriz_inicial = np.concatenate(mensaje, axis=1) # Concatenar las matrices horizontalmente 


# Función para aplicar las reglas del Juego de la Vida en un paso
def aplicar_reglas(tablero):
    # Crear una matriz llamada "vecindario" del mismo tamaño que el tablero, inicializada con ceros.
    vecindario = np.zeros_like(tablero)

    # Bucle para recorrer todas las celdas del tablero, excepto los bordes.
    for i in range(1, tablero.shape[0] - 1):
        for j in range(1, tablero.shape[1] - 1):
            # Calcular la suma de los valores de las celdas vecinas y restar el valor de la propia celda, es decir calcula la cantidad de vecinos de una celula
            vecindario[i, j] = np.sum(tablero[i-1:i+2, j-1:j+2]) - tablero[i, j]


    tablero_nuevo = tablero.copy()

    # Cada variable es una matriz booleana que almacena un True o False si se cumplen las condiciones
    celulas_que_mueren_por_soledad = (tablero == 1) & (vecindario < 2)
    # Se modifica el valor de la celda en las posiciones donde este un True en la matriz anteriormente evaluada en un nuevo tablero que no modifica el original para poder seguir evaluando cada regla
    tablero_nuevo[celulas_que_mueren_por_soledad] = 0

    celulas_que_permanecen_vivas = (tablero == 1) & ((vecindario == 2) | (vecindario == 3))
    tablero_nuevo[celulas_que_permanecen_vivas] = 1

    celulas_que_mueren_por_sobrepoblacion = (tablero == 1) & (vecindario > 3)
    tablero_nuevo[celulas_que_mueren_por_sobrepoblacion] = 0

    celulas_que_nacen = (tablero == 0) & (vecindario == 3)
    tablero_nuevo[celulas_que_nacen] = 1

    return tablero_nuevo


# Función para animar el juego
def animar_juego(frames):
    # fig contiende la figura de matplotlib y ax los ejes donde se trazan los datos 
    fig, ax = plt.subplots()

    # se llama en cada en cada iteración de la animación para actualizar los ejes con el próximo frame
    def update(frame):
        # limpia los ejes (elimina y controla la visibilidad de la "figura") en cada actualizacion para mostrar cada frame
        ax.clear() 
        ax.set_xticks([])
        ax.set_yticks([])
        # Muestra cada frame o matriz usando el mapa de colores (blanco = 0 , negro = 1)
        ax.imshow(frame, cmap='binary') 

    # Maneja la animacion con la biblioteca de matplotlib recibe por parametro el espacio que se actualiza
    # la funcion que se llama en cada iteracion de la animacion
    # la secuencia de frames 
    # intervalo de tiempo
    # repeticion de la animacion
    # tecnica que solo cambia lo necesario del frame anterior en lugar de redibujar
    animacion = animation.FuncAnimation(fig, update, frames=frames, interval=1500, repeat=True)
    # Llama la ventana de la animacion
    plt.show()


# Almacenar los frames
frames = [matriz_inicial.copy()]
# Número de generaciones
generaciones = 1

# Crear una copia de la matriz inicial 
tablero_actual = matriz_inicial.copy()
# Evalua las reglas en cada frame y los almacena
for _ in range(generaciones): 
    tablero_actual = aplicar_reglas(tablero_actual)
    frames.append(tablero_actual.copy())

# Animar el juego

animar_juego(frames)