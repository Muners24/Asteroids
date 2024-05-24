from header import *

class Asteroide:
    
    def __init__(self,pos,direccion,radio):
        self.x = pos.x
        self.y = pos.y
        self.vel = Vector2(0,0)
        self.direccion = direccion
        self.should_del = False
        self.radio = radio
        self.time = 0
        if (radio != ASTEROID_RAD0):
            self.vel.y = math.sin(direccion) * (ASTEROID_V*1.5) * -1
            self.vel.x = math.cos(direccion) * (ASTEROID_V*1.5)
        else:
            self.vel.y = math.sin(direccion) * ASTEROID_V * -1
            self.vel.x = math.cos(direccion) * ASTEROID_V
    
    def mov(self):
        if(math.sqrt(self.vel.x**2+self.vel.y**2) != ASTEROID_V):
            if(math.sqrt(self.vel.x**2+self.vel.y**2) > ASTEROID_V):
                self.vel.x *= 0.994
                self.vel.y *= 0.994
            else:
                self.vel.y = math.sin(self.direccion) * ASTEROID_V * -1
                self.vel.x = math.cos(self.direccion) * ASTEROID_V
        self.x += self.vel.x
        self.y += self.vel.y
    
    def colisionDisp(self,proyectiles):
        for disp in proyectiles:
            if (self.colision(disp.x,disp.y)):
                return True
        return False
    
    def colision(self,x,y):
        triangulo = Vector2(0,0)
        triangulo.x = abs(x - self.x)
        triangulo.y = abs(y - self.y)
            
        distancia = math.sqrt(triangulo.x**2+ triangulo.y**2)
            
        if(distancia < self.radio):
            return True
        return False
    
    def outScreen(self):
        if(self.y < -10-self.radio):
            self.y = HEIGHT+10+self.radio
            return True
        if(self.y > HEIGHT+10+self.radio):
            self.y = -10-self.radio
            return True
        if(self.x < -10-self.radio):    
            self.x = WIDTH+10+self.radio
            return True
        if(self.x > WIDTH+10+self.radio):
            self.x = -10-self.radio
            return True
        return False
    
    def update(self):
        self.mov()
        self.outScreen()
        self.time += 1
        if(self.time > ASTEROID_TTL):
            self.should_del = True
        
    def draw(self,window):
        pygame.draw.circle(window,WHITE,(self.x,self.y),self.radio)
        
    
        