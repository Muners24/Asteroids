
from header import *
from Class.Nave import Nave, ATK
from Class.Disparo import Disparo
from Class.Asteroide import Asteroide
import sys
import threading
import re

pygame.init()

letras = [chr(i) for i in range(32, 32+90)]
end = False
start = False
timer_asteroides = 60
actual_timer_asteroid = ASTEROID_MAX_TIMER
window = pygame.display.set_mode(WINDOW_SIZE)
record = []
presionado = False
i = 0

pygame.display.set_caption("Asteroids")

nave = Nave(SPAWNX,SPAWNY)
proyectiles = []
asteroides = []
navetxt = pygame.image.load("texture//NAVEP.png").convert_alpha()
wasd = pygame.image.load("texture//wasd.png").convert_alpha()
w_space = pygame.image.load("texture//w_space.png").convert_alpha()
corazon = pygame.image.load("texture//corazon.png").convert_alpha()

pygame.mixer.init()

def generarAsteroide(lado,nave_pos,radio):
    global timer_asteroides
    global actual_timer_asteroid
    timer_asteroides += 1  

    if (radio == ASTEROID_RAD0):
        if (timer_asteroides > actual_timer_asteroid):
            timer_asteroides = 0
            actual_timer_asteroid += 1
            if actual_timer_asteroid > ASTEROID_MAX_TIMER:
                actual_timer_asteroid = ASTEROID_MIN_TIMER 
                if (nave.point != 0):
                    actual_timer_asteroid -= math.log(nave.point/3)+nave.point/7500
                
            pos = Vector2(0,0)
            if (lado == LEFT):
                pos.x = 0 - ASTEROID_RAD0
                pos.y = randint(0,HEIGHT)   
                
            if (lado == RIGHT):
                pos.x = WIDTH + ASTEROID_RAD0
                pos.y = randint(0,HEIGHT)
                
            if (lado == UP):
                pos.x = randint(0,WIDTH)
                pos.y = 0 - HEIGHT
                
            if (lado == DOWN):
                pos.x = randint(0,WIDTH)
                pos.y = HEIGHT + ASTEROID_RAD0
            
            triangulo = Vector2(0,0)
            triangulo.x = nave_pos.x - pos.x
            triangulo.y = nave_pos.x - pos.y
            
            direccion = math.atan2(triangulo.y, triangulo.x)
            direccion = abs(direccion)

            if triangulo.x > 0:
                if(triangulo.y > 0):
                    direccion = 2*math.pi - direccion
            else:
                if(triangulo.y > 0):
                    direccion = 2*math.pi - direccion
                else:
                    direccion = direccion
            
            direccion += math.radians(randint(0,15)) if randint(0,1) else -math.radians(randint(0,15))
            return Asteroide(pos,direccion,radio)
        else:
            raise ATK("asteroide en cd")
    else:
        return Asteroide(nave_pos,math.radians(randint(0,359)),radio)

def befStart():
    global start
    global NAVE_VEL
    x,y = pygame.mouse.get_pos()
    pygame.draw.rect(window,(85,85,85),(WIDTH/2-300,50,600,300))
    if(50 < y < 300):
        if(WIDTH/2-300 < x < WIDTH/2):
            pygame.draw.rect(window,(190,190,190),(WIDTH/2-300,50,300,300))
            keys = pygame.mouse.get_pressed()
            if(keys[0]):
                start = True
                nave.control = 0
                NAVE_VEL += 2
            
        if(WIDTH/2 < x < WIDTH/2+300):
            pygame.draw.rect(window,(190,190,190),(WIDTH/2,50,300,300))
            keys = pygame.mouse.get_pressed()
            if(keys[0]):
                start = True
                nave.control = 1
    
    rect = wasd.get_rect()
    rect.topleft=(WIDTH/2-300,50)
    window.blit(wasd, rect)
    rect = w_space.get_rect()
    rect.topleft=(WIDTH/2,50)
    window.blit(w_space, rect)
    
    drawText("Normal",WIDTH/2-150,70,(0,0,0))
    drawText("Dificil",WIDTH/2+150,70,(0,0,0))
                
def update():
    nave.update()
    if (nave.colision(asteroides,proyectiles)):
        nave.respawn(SPAWNX,SPAWNY)
        sonido("danio")
    try:
        proyectiles.append(nave.disp())
        sonido("laser")

    except ATK:
        pass
        
    try:
        asteroides.append(generarAsteroide(randint(0,3),Vector2(nave.x,nave.y),ASTEROID_RAD0))
    except ATK:
        pass
                
    for asteroide in asteroides:
        if(not asteroide.should_del):
            if (asteroide.colisionDisp(proyectiles)):
                try:
                    if (asteroide.radio == ASTEROID_RAD0):
                        temp = generarAsteroide(0,Vector2(asteroide.x,asteroide.y),ASTEROID_RAD1)
                        asteroides.append(temp)
                        asteroides.append(Asteroide(Vector2(temp.x,temp.y),temp.direccion+math.pi,temp.radio))
                        nave.point += 5
                        nave.bonus += 5
                        sonido("expmax")
                    elif (asteroide.radio == ASTEROID_RAD1):
                        temp = generarAsteroide(0,Vector2(asteroide.x,asteroide.y),ASTEROID_RAD2)
                        asteroides.append(temp)
                        asteroides.append(Asteroide(Vector2(temp.x,temp.y),temp.direccion+math.pi,temp.radio))
                        nave.point += 10
                        nave.bonus += 10
                        sonido("expmed")
                    elif (asteroide.radio == ASTEROID_RAD2):
                        nave.point += 30
                        nave.bonus += 30
                        sonido("expmin")
                    asteroide.should_del = True
                    
                except ATK:
                    pass
            asteroide.draw(window)
            asteroide.update()

        else:
            asteroides.remove(asteroide)
            
    for disp in proyectiles:
        if disp.timer > DISP_TTL:
            proyectiles.remove(disp)
        else:
            disp.update()
            disp.draw(window)

def onEnd():
    global end

    dif = ""
    if(nave.control == 0):
        dif = "Dificultad Normal"
    elif(nave.control == 1):
        dif = "Dificultad Dificil"
        
    drawText("Record",WIDTH/2,50,WHITE)
    drawText(dif,WIDTH/2,100,WHITE)
    drawText(str(nave.point),WIDTH/2,150,WHITE)
    input()

def drawText(text,x,y,color):
    font = pygame.font.Font('fuentes/Minecraft.ttf', 45)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x-text_rect.width/2, y)
    
    window.blit(text_surface, text_rect)

def input():
    global record
    global presionado
    global end
    global start
    
    dif = ""
    if(nave.control == 1):
        dif = "records/dificil.txt"
    elif (nave.control == 0):
        dif = "records/normal.txt"
            
    if not presionado:
        for char in letras:
            keys = pygame.key.get_pressed()
            if keys[pygame.key.key_code(char)]:
                record.append(char.upper())
                break
            
            elif keys[pygame.K_BACKSPACE]:
                if(len(record)!= 0):
                    record.pop()
                    break
            
 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        end = False
        start = False
        text = ""
        for char in record:
            text += char
            
        with open(dif,"a") as file:
            if(text == ""):
                text = "NAVE"
            file.write(text + ": " + str(nave.point) + "\n" )
        nave.point = 0
        record.clear()
    presionado = False
    
    for key in keys:
        presionado = presionado or key
               
    drawInput(record,WIDTH/2,250)
    
    with open(dif,"r") as file:
        y = 400
        for line in file:
            line = line[:-1]
            drawText(line,WIDTH/2,y,WHITE)
            y += 50
    
def drawInput(list_char,x,y):
    text = ""
    for char in list_char:
        text += char
        
    global i
    i += 1
    font = pygame.font.Font('fuentes/Minecraft.ttf', 45)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x-text_rect.width/2-15, y)
    window.blit(text_surface, text_rect)
    
    final_x = text_rect.x+text_rect.width
    if(30 > i ):
        text_surface = font.render("_", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (final_x, y)
        window.blit(text_surface, text_rect)
    else:
        if(i > 50):
            i = 0
     
def sonido(nombre):
    def reproducir():
        pygame.mixer.init()
        sonido = pygame.mixer.Sound("audio//"+nombre+".wav")
        if(nombre == "danio"):
            sonido.set_volume(1.2)
        elif(nombre == "laser"):
            sonido.set_volume(0.5)
        sonido.play()
    
    hilo_audio = threading.Thread(target=reproducir)
    hilo_audio.daemon = True
    hilo_audio.start()
    
while True:
    window.fill((0,0,0))
    pygame.time.delay(16)
    if nave.vida == -1:
        end = True
        nave.vida = 4
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break
    if(not end):
        nave.draw(window,navetxt,corazon)
        if(start):
            update()
        else:
            befStart()
    else:
        onEnd()
          
    pygame.display.update()
    

