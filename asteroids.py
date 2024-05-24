
from header import *
from Class.Nave import Nave, ATK
from Class.Disparo import Disparo
from Class.Asteroide import Asteroide

timer_asteroides = 60
actual_timer_asteroid = ASTEROID_MAX_TIMER

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
        
pygame.init()

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Asteroids")

navetxt = pygame.image.load("texture//NAVEP.png").convert_alpha()

nave = Nave(SPAWNX,SPAWNY)
proyectiles = []
asteroides = []

# Bucle principal del juego

while True:
    window.fill((0,0,0))
    pygame.time.delay(16)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            break
    
    nave.update()
    nave.draw(window,navetxt)
    if (nave.colision(asteroides,proyectiles)):
        nave.respawn(SPAWNX,SPAWNY)
        
    try:
        proyectiles.append(nave.disp())
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
                        nave.point += 15
                    elif (asteroide.radio == ASTEROID_RAD1):
                        temp = generarAsteroide(0,Vector2(asteroide.x,asteroide.y),ASTEROID_RAD2)
                        asteroides.append(temp)
                        asteroides.append(Asteroide(Vector2(temp.x,temp.y),temp.direccion+math.pi,temp.radio))
                        nave.point += 30
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
            
    
    
    pygame.display.update()
    

