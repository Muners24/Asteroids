from header import *
from Class.Disparo import *
from Class.Asteroide import *

class ATK(Exception):
    
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(mensaje)
        
class Nave:

    def __init__(self,x,y): 
        self.x = x
        self.y = y
        self.direccion = math.pi/2
        self.radio = NAVE_RAD
        self.front = Vector2(0,0)
        self.back_l = Vector2(0,0)
        self.back_r = Vector2(0,0)
        self.vel = Vector2(0,0)
        self.up_b = False
        self.left_b = False
        self.right_b = False
        self.down_b = False
        self.atk_b = False
        self.brake_b = False
        self.atk_c = 0
        self.vida = 4
        self.point = 0
        self.area = 0
        self.control = -1
        self.live_time = 0
        self.bonus = 0

    def posFront(self):
        v_unit = self.vectorUnitario(self.direccion)
        self.front.x = self.x + v_unit.x*self.radio*1.5
        self.front.y = self.y - v_unit.y*self.radio*1.5
    
    def posBackL(self):
        v_unit = self.vectorUnitario(self.direccion-(2*math.pi/3))
        self.back_l.x = self.x + v_unit.x*self.radio
        self.back_l.y = self.y - v_unit.y*self.radio
    
    def posBackR(self):
        v_unit = self.vectorUnitario(abs(self.direccion+(2*math.pi/3)))
        self.back_r.x = self.x + v_unit.x*self.radio
        self.back_r.y = self.y - v_unit.y*self.radio

    def vectorUnitario(self,direccion):
        return Vector2(math.cos(direccion),math.sin(direccion))
    
    def dir(self):
        mouse = Vector2(0,0)
        mouse.x, mouse.y = pygame.mouse.get_pos()
        triangulo = Vector2(0,0)
        triangulo.x = mouse.x - self.x
        triangulo.y = mouse.y - self.y
        
        
        self.direccion = math.atan2(triangulo.y, triangulo.x)
        self.direccion = abs(self.direccion)

        if triangulo.x > 0:
            if(triangulo.y > 0):
                self.direccion = 2*math.pi - self.direccion
        else:
            if(triangulo.y > 0):
                self.direccion = 2*math.pi - self.direccion
            else:
                self.direccion = self.direccion
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.up_b = keys[pygame.K_w]
        self.down_b = keys[pygame.K_s]
        self.left_b = keys[pygame.K_a]
        self.right_b = keys[pygame.K_d]
        self.brake_b = keys[pygame.K_SPACE]
        mouse = pygame.mouse.get_pressed()
        self.atk_b = mouse[0]
       
    def velocidad(self):
        if(self.control == 0):
            if self.up_b:
                if self.right_b:
                    self.vel.x = math.sin(math.pi/4) * NAVE_VEL
                    self.vel.y = -math.sin(math.pi/4) * NAVE_VEL
                elif self.left_b:
                    self.vel.x = -math.sin(math.pi/4) * NAVE_VEL
                    self.vel.y = -math.sin(math.pi/4) * NAVE_VEL
                else:
                    self.vel.x = 0
                    self.vel.y = -NAVE_VEL
            elif self.down_b:
                if self.right_b:
                    self.vel.x = math.sin(math.pi/4) * NAVE_VEL
                    self.vel.y = math.sin(math.pi/4) * NAVE_VEL
                elif self.left_b:
                    self.vel.x = -math.sin(math.pi/4) * NAVE_VEL
                    self.vel.y = math.sin(math.pi/4) * NAVE_VEL
                else:
                    self.vel.x = 0
                    self.vel.y = NAVE_VEL
            elif self.right_b:
                self.vel.x = NAVE_VEL
                self.vel.y = 0
            elif self.left_b:
                self.vel.x = -NAVE_VEL
                self.vel.y = 0
            else: 
                self.vel.x = 0
                self.vel.y = 0

        elif(self.control == 1):
            v_unit = self.vectorUnitario(self.direccion)
            if self.up_b:
                if math.sqrt(self.vel.x**2 + self.vel.x ** 2) <= NAVE_MAX_VEL:
                    self.vel.x = self.vel.x + v_unit.x*0.35
                    self.vel.y = self.vel.y + -v_unit.y*0.35 
            
            if(math.sqrt(self.vel.x**2 + self.vel.x ** 2) > 0):
                if(self.brake_b):
                    self.vel.x *= 0.95
                    self.vel.y *= 0.95
                else:
                    self.vel.x *= 0.996
                    self.vel.y *= 0.996
            else:
                self.vel.x = 0
                self.vel.y = 0

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
            
    def update(self):
        self.dir()
        self.vectorUnitario(self.direccion)
        self.input()
        self.velocidad()
        self.mov()
        self.bordes()
        self.posFront()
        self.posBackL()
        self.posBackR()
        self.calcularArea(self.x,self.y,self.back_l.x,self.back_l.y,self.back_r.x,self.back_r.y)
        if(self.bonus > 5000):
            self.vida += 1
            self.bonus = 0
        self.atk_c += 1
        self.live_time += 1
    
    def draw(self,window,navetxt,vida_tex):
        
        v_unit = self.vectorUnitario(self.direccion)
        
        navetxt_rotated = pygame.transform.rotate(navetxt, math.degrees(self.direccion-math.pi/2))
        navetxt_rect = navetxt_rotated.get_rect(center=(self.x+v_unit.x*14, self.y-v_unit.y*14))
        window.blit(navetxt_rotated, navetxt_rect.topleft)
        
        vida_tex = pygame.transform.scale(vida_tex,(40,40))
        vida_rec = vida_tex.get_rect()
        vida_rec.topleft=(20,20)
        window.blit(vida_tex,vida_rec)
        
        font = pygame.font.Font('fuentes/Minecraft.ttf', 45)
        text_surface = font.render(str(self.vida), True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (75, 20)
        window.blit(text_surface, text_rect)
        
        text_surface = font.render(str(self.point), True, (255, 255, 255))
        text_rect.topleft = (250, 20)
        window.blit(text_surface, text_rect)
          
    def disp(self):
        if(self.atk_b):
            if(self.atk_c > NAVE_ATKV):
                self.atk_c = 0
                return Disparo(self.front,self.direccion)
        raise ATK("atk en cd")
        
    def colision(self,asteroides,proyectiles):
        if(self.live_time > NAVE_INV_TIMER):
            for roca in asteroides:
                if (roca.colision(self.front.x,self.front.y)):
                        return True
                if (roca.colision(self.back_l.x,self.back_l.y)):
                        return True
                if (roca.colision(self.back_r.x,self.back_r.y)):
                        return True
                if (roca.colision(self.x,self.y)):
                        return True
            for disp in proyectiles:
                if(disp.timer > 10):
                    if(disp.colision(self.x,self.y,self.back_l.x,self.back_l.y,self.back_r.x,self.back_r.y,self.area)):
                        return True
        return False
            
    def respawn(self,x,y):
        self.vida -= 1
        self.x = x
        self.y = y
        self.live_time = 0
    
    def calcularArea(self,x1, y1, x2, y2, x3, y3):
        self.area = abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)