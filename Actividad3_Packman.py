from random import choice
from turtle import *
from freegames import floor, vector

#En esta sección se Inicializa el marcador, camino y vectores de Fantasmas y Pacman
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
#Lista nueva que representa el mapa, 0= pared, 1=camino
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

#Funcion que dibuja los cuadrados o mosaicos del camino, usada para diseñar el mapa a partir de ciertas coordenadas
def square(x, y):
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill() 

    for count in range(4): #Cada iteración del ciclo for dibuja una línea del cuadrado
        path.forward(20)
        path.left(90)

    path.end_fill()

#Funcion que regresa el desplazamiento del punto en el mapa
def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

#Esta función es fundamental para que el juego funcione ya que verifica que todas las posiciones sean validas
def valid(point):
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

#Funcion que dibuja el mundo (tablero) haciendo uso de la lista de tiles de antes, colorea el mapa y hace uso de path para los caminos
def world():
    "Draw world using path."
    bgcolor('black') #Colorea de negro todo el fondo de la venta 
    path.color('blue') #Define el camino de color azul

    for index in range(len(tiles)): #Ciclo for que recorre cada cuadrito o mosaico previamente definido en la lista tiles
        tile = tiles[index] 

        if tile == 1: #Los mosaicos definidos con 1 en la lista tiles se colorean como camino
            #A partir del índice del mosaico definimos x, y
            x = (index % 20) * 20 - 200  
            y = 180 - (index // 20) * 20
            square(x, y) #Se llama a la función square para dibujar y pintar el mosaico de color azul
            #Se mueve path al centro del mosaico para dibujar el punto blanco que representa la comida
            path.up() 
            path.goto(x + 10, y + 10) 
            path.dot(2, 'white') 

#Funcion que hace que se mueva el personaje principal (Pacman) y genera los movimientos de los bots (fantasmas)
def move():
    "Move pacman and all ghosts."

    #Ciclo for que hace que los fantasmas avancen 2 posiciones por cada 1 que avanza Pacman;
    #si en lugar de range (2) se pone range (3), los fantasmas avanzarán 3 veces más rápido que Pacman y así sucesivamente
    for i in range (2): 
        writer.undo() #Se borra el marcador
        writer.write(state['score']) #Se vuelve a dibujar el marcador con el score actualizado

        clear() #Se borran los dibujos anteriores de los personajes

        if i == 0: #Solo la primera vez que se ejecuta el ciclo for Pacman cambia de posición
            if valid(pacman + aim):
                pacman.move(aim)

            index = offset(pacman)

            if tiles[index] == 1: #Si hay comida en la posición de pacman:
                tiles[index] = 2 #Se le asigna al mosaico el valor 2
                state['score'] += 1 #Aumenta 1 punto el marcador
                x = (index % 20) * 20 - 200 
                y = 180 - (index // 20) * 20
                square(x, y) #Se llama a la función square para que coloree el mosaico de azul y ya no aparezca el punto de la comida

        up()
        goto(pacman.x + 10, pacman.y + 10)
        dot(20, 'yellow') #Dibuja a pacman como un punto amarillo en su pocición establecida

        for point, course in ghosts: 
            if valid(point + course):
                point.move(course)
            else:
                options = [
                    vector(5, 0),
                    vector(-5, 0),
                    vector(0, 5),
                    vector(0, -5),
                ]
                plan = choice(options)
                course.x = plan.x
                course.y = plan.y

            up()
            goto(point.x + 10, point.y + 10)
            dot(20, 'red')

        update()

        for point, course in ghosts:
            if abs(pacman - point) < 20: #Si Pacman choca con un fantasma el juego se detiene.
                return

    ontimer(move, 100) #La función move se repite cada 0.1 segundos

#Esta funcion verifica que el pacman pueda cambiar de dirección en su posición actual del mapa
def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        #Mueve en direccion X
        aim.x = x
        #Mueve en direccion Y
        aim.y = y

#Da el tamaño de la ventana del usuario, entre otros.
setup(420, 420, 370, 0)
hideturtle()
tracer(False)

#Inicializa el marcador con su posición y color
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()

#Asigna los comandos de movimiento del pacman 
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

#Se inicializa el juego y el aim
world()
move()
done()