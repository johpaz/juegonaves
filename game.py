import pygame
import random
import math
import sys
import os

#inicializar pygame
pygame.init()


#establece el tamaño de la pantalla

screen_with = 800 
screen_heigth= 600
screen = pygame.display.set_mode((screen_with,screen_heigth))
#Funcion para obtener la rita de los recursos

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path,relative_path) 
    
#Cargar imagen de fondo
asset_background = resource_path('assets/images/background.png')
background = pygame.image.load(asset_background)
    

#Cargar icono de ventana
asset_icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)

#Cargar sonido de fondo
asset_sound = resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer_music.load(asset_sound)

#Cargar imagen del jugador
assest_playering = resource_path('assets/images/space-invaders.png')
playering= pygame.image.load(assest_playering)

#Cargar imagen de bala
assest_bulletimg = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(assest_bulletimg)

#Cargar fuente para texto de game over
assest_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(assest_over_font, 60)

#Cargar fuente para texto de puntaje
assest_font = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(assest_font,32)


# Establecer titulo de ventana
pygame.display.set_caption("Heroe Galactico")

#Establecer icono de ventana
pygame.display.set_icon(icon)

#Reproducir sonido de fondp en loop
pygame.mixer.music.play(-1)

#Crear reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

#Pocicion inicial del juegador
playerX = 370
playerY = 470
playerx_change = 0
playery_change = 0

#lista para almacenar posicionrs de los enemigos
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

#Se inicializa la variables para guardar las posiciones de los enemigos

for i in range(no_of_enemies):
    #Se carga la imagen del enemigo1 
    enemy1 = resource_path('assets/images/enemy1.png')
    enemyimg.append(pygame.image.load(enemy1))
    #Se carga la imagen del enemigo1 
    enemy2 = resource_path('assets/images/enemy2.png')
    enemyimg.append(pygame.image.load(enemy2))
        
    #Se asigna una posicion aleatoria en X e Y para el enemigo
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))

    #Se establece la velocidad del movimiento del enemigo en X e Y
    enemyX_change.append(5)
    enemyY_change.append(20)

    #Se inicializa las variables para guardar la posicion de la bala
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    #Se inicializa la puntuacion en 0
    score = 0

    #Funcion mostrar la puntuacion en la pantalla
    def show_score():
        score_value = font.render("SCORE "+ str(score),True,(255,255,255))
        screen.blit(score_value,(10,10)) 
        
    #Funcion para dibujar al jugador en la pantalla
    def player(x,y):
        screen.blit(playering,(x,y))

    #Funcion dibujar al enemigo en pantall
    def enemy(x,y, i):
        screen.blit(enemyimg[i], (x, y))
        
    #Funcion para disparar la bala
    def fire_bullet(x,y):
        global bullet_state

        bullet_state = "fire"
        screen.blit(bulletimg,(x+16, y+10))

    #Funcion para comprobar la colision de la bala con el enemigo
    def isCollision(enemyX,enemmyY,bulletX,bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX,2)) +
                             (math.pow(enemmyY-bulletY,2))) 
        if distance < 27:
            return True
        else: 
            return False
            

    #Funcion para mostrar el texto de game over en pantalla
    def game_over_text():
        over_text = over_font.render("PERDISTE", True,(255,255,255))
        text_rect = over_text.get_rect(
            center=(int(screen_with/2), int(screen_heigth/2)))
        screen.blit(over_text,text_rect)

    #Funcion principal(bucle) del juego
    def gameloop():

    #Declarar variables globales
        global score
        global playerX
        global playerx_change
        global bulletX
        global bulletY
        global collision
        global bullet_state

        in_game = True
        while in_game:
            #Maneja eventos,actualiza y renderiza el juego
            #limpia la pantalla
            screen.fill((0,0,0))
            screen.blit(background,(0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                    pygame.quit()
                    sys.exit

                if event.type == pygame.KEYDOWN:
                    #maneja los movimientos del juegador y el disparo
                    if event.key == pygame.K_LEFT: 
                        playerx_change = -5

                    if event.key == pygame.K_RIGHT:
                        playerx_change = 5        
                            
                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                            
                if event.type == pygame.KEYUP:
                    playerx_change = 0

            #Aqui se esta actualizando la posicion del juegador
            playerX += playerx_change

            if playerX <= 0:
                playerX= 0    
            elif playerX >= 736:
                 playerX = 736

            #Bucle que se ejecuta para cada enemigo
            for i in range(no_of_enemies):
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                       enemyY[j] = 2000
                    game_over_text()
                    
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i]= 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                     enemyX_change[i] = -5
                     enemyY[i] += enemyY_change[i]
        
                #Aqui se compueba si ha habido una colision entre un enemigo y la bala

                collision = isCollision(enemyX[i], enemyY[i],bulletX, bulletY)
                if collision:
                    bulletY = 454
                    bullet_state = "ready"
                    score += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                enemy(enemyX[i],enemyY[i],i)
                    
                if bulletY < 0:
                    bulletY = 454
                    bullet_state = "ready"
                if bullet_state == "fire":
                    fire_bullet(bulletX,bulletY)
                    bulletY -= bulletY_change

            player(playerX,playerY)
            show_score()
            pygame.display.update()
            clock.tick(120)

        pygame.quit()
        sys.exit()

gameloop()           
