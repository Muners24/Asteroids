from header import *

class Disparo:
    
    def __init__(self,pos,direccion):
        self.vel = Vector2(0,0)
        self.timer = 0
        self.x = pos.x
        self.y = pos.y
        self.direccion = direccion
        self.should_del = False
        self.vel.y = math.sin(direccion) * DISP_VEL * -1
        self.vel.x = math.cos(direccion) * DISP_VEL
        
    def mov(self):
        self.x += self.vel.x
        self.y += self.vel.y
    
    def bordes(self):
        if(self.y < 0):
            self.y = HEIGHT
        if(self.y > HEIGHT):
            self.y = 0
        if(self.x < 0):    
            self.x = WIDTH
        if(self.x > WIDTH):
            self.x = 0
    
    def draw(self,window):
        pygame.draw.circle(window,WHITE,(self.x,self.y),DISP_RAD)
        
    def update(self):
        self.mov()
        self.bordes()
        self.timer += 1
        
    def colision(self,x1, y1, x2, y2, x3, y3,area):
        A1 = self.area(self.x, self.y, x2, y2, x3, y3)
        A2 = self.area(x1, y1, self.x, self.y, x3, y3)
        A3 = self.area(x1, y1, x2, y2, self.x, self.y)
        return int(area) == int(A1 + A2 + A3)
    
    def area(self,x1, y1, x2, y2, x3, y3):
        return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)
    
