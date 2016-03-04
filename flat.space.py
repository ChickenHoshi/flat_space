helpText = ['press MOUSE LEFT to move',
'press LEFT CONTROL or MOUSE RIGHT to shoot',
'press SPACE to brake',
'press V to toggle visibility',
'press 1 - 5 for shooting styles',
'press P to spawn aliens',
False]


import pygame, sys, math, random, time

from pygame.locals import*

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
#set up window
windowX = 1080
windowY = 720
DISPLAYSURF = pygame.display.set_mode((windowX,windowY))
pygame.display.set_caption('Flat_Space 0.1a')
font = pygame.font.SysFont('consolas',20)
fonth = pygame.font.SysFont('consolas',10)

#set up colors

BLACK = ( 0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255,255,255)
shots = []
explosions = []
aliens = []
class explosion_parker:
     def __init__(self, pos,speed = 10, rad = 5):
          self.x = pos[0]+random.randint(-5,5)
          self.y = pos[1]+random.randint(-5,5)
          self.rad = rad
          self.color = 255
          self.speed = speed
          self.big = self.rad/50 #i cant think of a good name
          
          

     def draw(self,time):
          #if time % (FPS/5) == 0:
          pygame.draw.circle(DISPLAYSURF,(self.color,self.color,self.color),(self.x,self.y),int(self.rad*2),1)
          
          pygame.draw.circle(DISPLAYSURF,(self.color,self.color,self.color),(self.x,self.y),int(self.rad))
          
          
     def update(self, time):
          self.rad += self.big
          if self.color >= self.speed:
               self.color -= self.speed

class shot_carrot:
     def __init__(self, pos, angle,ship):
          self.range = 200
          self.length = 10
          self. speed = 20
          self.x = pos[0]
          self.y = pos[1]
          self.angle = math.radians(angle)
          self.movex = math.cos(self.angle) * self.speed
          self.movey = -math.sin(self.angle) * self.speed
          self.damage = 5
          ship.fuel -= 10
          #print(angle, self.angle, self.movex, self.movey)
     def update(self):
          self.x += self.movex
          self.y += self.movey
     def draw(self):
          self.eX = self.x - self.length * math.cos(self.angle)
          self.eY = self.y + self.length * math.sin(self.angle)
          pygame.draw.line(DISPLAYSURF, green(100), (int(self.x),int(self.y)), (int(self.eX),int(self.eY)),5)
          pygame.draw.line(DISPLAYSURF, WHITE, (int(self.x),int(self.y)), (int(self.eX),int(self.eY)),1)
          
          
class alien_FRD:
     def __init__(self,pos,radius = 15):
          self.healthMax = 200
          self.health = 10*radius
          self.x = pos[0]
          self.y = pos[1]
          self.movex = self.movex = random.uniform(-1,1)
          self.movey = self.movey = random.uniform(-1,1)
          self.speedx = self.movex
          self.speedy = self.movey
          self.rad = radius
          self.edges = int(self.rad/3)
          self.pList = []
          self.color = (random.randint(50,255),random.randint(50,255),random.randint(50,255))
          for i in range(self.edges):
                    self.pList.append([self.x + random.randint(-self.rad,self.rad),\
                                  self.y + random.randint(-self.rad,self.rad)])
          
     def draw(self,time):
          
          if time % 10 == 0:
               self.pList = []
               for i in range(self.edges):
                    self.pList.append([self.x + random.randint(-self.rad,self.rad),\
                                  self.y + random.randint(-self.rad,self.rad)])
          pygame.draw.circle(DISPLAYSURF,green(50),(int(self.x),int(self.y)),self.rad,3)
          pygame.draw.polygon(DISPLAYSURF, self.color, self.pList)
          pygame.draw.circle(DISPLAYSURF,green(255),(int(self.x),int(self.y)),int(self.rad/5),int(self.rad/10))

          self.hbX = self.health/self.healthMax/2*self.rad
          self.hbY = self.y - self.rad
          
          pygame.draw.line(DISPLAYSURF, green(255),(self.x - self.hbX, self.hbY),(self.x + self.hbX, self.hbY))

     def update(self, time):
          if time % (FPS*5) == 0:
               self.movex = random.uniform(-1,1)
               self.movey = random.uniform(-1,1)
               self.speedx += self.movex
               self.speedy += self.movey
               if abs(self.speedx) > 1: self.speedx = math.copysign(1,self.speedx)
               if abs(self.speedy) > 1: self.speedy = math.copysign(1,self.speedy)
               #print(self.speedx,self.speedy)
          if self.movex != 0 or self.movey != 0:
               self.x += self.speedx
               self.y += self.speedy
          if self.x < -self.rad*2: self.x = windowX + self.rad*2
          if self.x > windowX + self.rad*2 : self.x = -self.rad*2
          if self.y < -self.rad*2: self.y = windowY + self.rad*2
          if self.y > windowY + self.rad*2 : self.y = -self.rad*2

          for shot in range(len(shots)):
               if self.x - self.rad <shots[shot].x <self.x + self.rad and \
                  self.y - self.rad <shots[shot].y <self.y + self.rad:
                    self.health -= shots[shot].damage
                    addExplosion((int(shots[shot].x), int(shots[shot].y)))
                    deleteShots(shot)
                    break

class ship_macbeth:
     def __init__(self,pos):
          self.unlimitedVisib = False
          self.x = pos[0]
          self.y = pos[1]
          self.rad = 5
          self.visib = 200
          self.speedx = 0
          self.speedy = 0
          self.accel = 0.1
          self.fuelMax = 1000000
          self.fuel = 1000000
          self.fuel_regen = 1
          self.stopSpeed = .5
          self.angle0 = 0
          
          

     def draw(self):
          self.mposX, self.mposY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
          self.angle0 = findAngle(self.mposX, self.mposY,(self.x,self.y))
          self.angle = math.radians(self.angle0)
          self.angle2 = math.radians(self.angle0+120)
          self.angle3 = math.radians(self.angle0-120)
          self.p1 = (math.cos(self.angle) * self.rad*2 + int(self.x),\
                     -math.sin(self.angle) * self.rad*2 + int(self.y))
          self.p2 = (math.cos(self.angle2) * self.rad + int(self.x),\
                     -math.sin(self.angle2) * self.rad + int(self.y))
          self.p3 = (math.cos(self.angle3) * self.rad + int(self.x),\
                     -math.sin(self.angle3) * self.rad + int(self.y))
##          pygame.draw.circle(DISPLAYSURF,green(50),(int(self.x),int(self.y)),self.visib)
          pygame.draw.lines(DISPLAYSURF,green(200),True,(self.p1,self.p2,self.p3))
          
          #fuel bar
          self.fbX = self.fuel/self.fuelMax/2*self.rad*4
          self.fbY = self.y - self.rad*2
          
          pygame.draw.line(DISPLAYSURF, green(255),(self.x - self.fbX, self.fbY),(self.x + self.fbX, self.fbY))
     def move(self):
          if self.speedx != 0 : self.x += self.speedx
          if self.speedy != 0 : self.y += self.speedy  
          
          if self.x < -self.rad*2 - self.visib: self.x = windowX + self.rad*2 + self.visib
          if self.x > windowX + self.rad*2 + self.visib: self.x = -self.rad*2 - self.visib
          if self.y < -self.rad*2 - self.visib: self.y = windowY + self.rad*2 + self.visib
          if self.y > windowY + self.rad*2 + self.visib: self.y = -self.rad*2 - self.visib


     def stop(self):
          if self.fuel > 0 and (self.speedx != 0 or self.speedy != 0):
               self.speedx += math.copysign(self.stopSpeed, self.speedx)*-1
               self.speedy += math.copysign(self.stopSpeed, self.speedy)*-1
               if -self.stopSpeed<= self.speedx <= self.stopSpeed: self.speedx = 0
               if -self.stopSpeed<= self.speedy <= self.stopSpeed: self.speedy = 0
          
               self.fuel -= self.stopSpeed*4
          
     def setDest(self,dest):
          if self.fuel > 0:
               if self.x < dest[0]: self.speedx += self.accel
               if self.x > dest[0]: self.speedx -= self.accel
               if self.y < dest[1]: self.speedy += self.accel
               if self.y > dest[1]: self.speedy -= self.accel
               self.fuel -= self.accel*4
     def fuelRegen(self):
          if self.fuel < self.fuelMax: self.fuel += self.fuel_regen
          
shootingStyles = [0,1,1,False,0,0]
def addShot(pos, ship,time):
     if (pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.mouse.get_pressed()[2])and ship.fuel > 0:
          for i in range(shootingStyles[0],shootingStyles[1]):
               for j in range(shootingStyles[2]):
                    shots.append(shot_carrot(pos,ship.angle0 + i*5+ j*shootingStyles[4] + shootingStyles[5], ship))
          
          

def update_draw_Shots ():
     for shot in shots:
          shot.update()
          shot.draw()

def green(n):
     green = n
     if n > 255: green = 255
     if n < 0: green = 0
     return (0,green,0)

def findAngle(x,y,pos):
     opp, adj = -(pos[1] - y), (pos[0] - x)
     if adj == 0: adj = -1
     deg = math.degrees(math.atan(opp/adj))
     if x < pos[0]:
          deg += 180
     return deg

def deleteShots(hit = -1):
     delList = []
     for shot in range(len(shots)):
          if -windowX > shots[shot].x or shots[shot].x > windowX*2 or \
             -windowY > shots[shot].y or shots[shot].y > windowY*2 :
               delList.append(shot)
     if hit != -1: delList.append(hit)
     adjust = 0
     for shot in delList:
          shots.pop(shot - adjust)
          adjust += 1


def addExplosion(pos):
     #if pygame.key.get_pressed()[pygame.K_LSHIFT]:
     explosions.append(explosion_parker(pos))

def update_draw_Explosions (time):
     for explosion in explosions:
          explosion.update(time)
          explosion.draw(time)

def deleteExplosion():
     delList = []
     for explosion in range(len(explosions)):
          if explosions[explosion].color <= explosions[explosion].speed:
               delList.append(explosion)
     adjust = 0
     for explosion in delList:
          explosions.pop(explosion - adjust)
          adjust += 1

def addAliens(time):
     if time % 10 == 0 and pygame.key.get_pressed()[pygame.K_p]:
          aliens.append(alien_FRD((random.randint(0,windowX),random.randint(0,windowY))))
          if random.randint(0,10) == 0:
               aliens.append(alien_FRD( (random.randint(0,windowX),random.randint(0,windowY)) , 50))
def aliens_update_draw(time,player):
     for ayy in aliens:
          ayy.update(time)
          if player.unlimitedVisib == False:
               if math.hypot(player.x - ayy.x, player.y- ayy.y) <= player.visib  :
                    ayy.draw(time)
          else:
               ayy.draw(time)

def deleteAliens():
     delList = []
     for ayy in range(len(aliens)):
          if aliens[ayy].health <= 0:
               delList.append(ayy)
     adjust = 0
     for ayy in delList:
          explosions.append(explosion_parker((int(aliens[ayy- adjust].x),int(aliens[ayy- adjust].y)),\
                                             int(aliens[ayy- adjust].rad/3),int(aliens[ayy- adjust].rad/3*2)))
          aliens.pop(ayy - adjust)
          adjust += 1
          score[0] += 1
               
m = ship_macbeth((900,200))
#n = ship_macbeth((22,560))
helpS1 = fonth.render(helpText[0],1,(0,255,0))
helpS2 = fonth.render(helpText[1],1,(0,255,0))
helpS3 = fonth.render(helpText[2],1,(0,255,0))
helpS4 = fonth.render(helpText[3],1,(0,255,0))
helpS5 = fonth.render(helpText[4],1,(0,255,0))
helpS6 = fonth.render(helpText[5],1,(0,255,0))

time = 0
score = [0]
while True: ##main game loop
     if time < 1200: time += 1
     else: time = 0
     if time % FPS == 0:
          #print(len(shots), len(explosions), len(aliens), )
          pass
     deleteShots()
     deleteExplosion()
     deleteAliens()
     #get mouse position
     mposX, mposY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
     addAliens(time)
     
     if pygame.mouse.get_pressed()[0]:
          m.setDest((mposX, mposY))
##     if pygame.mouse.get_pressed()[2]:
##          n.setDest((mposX, mposY))
          
     if pygame.key.get_pressed()[pygame.K_SPACE]:
          m.stop()
##          n.stop()
     m.move()
##     n.move()
     m.fuelRegen()
##     n.fuelRegen()

     scoreS = font.render('kills: '+str(score[0])+' -- H: help',1,(0,255,0))
     
     if shootingStyles[3] == True:
          shootingStyles[5] = time
     
     if time%5 == 0:
          #addExplosion((mposX,mposY))
          addShot((m.x,m.y),m,time)
##          addShot((n.x,n.y),n)
     #print(m.x, m.y)
     #print(angle)
     DISPLAYSURF.fill(BLACK)
     pygame.draw.circle(DISPLAYSURF,green(25),(int(m.x),int(m.y)),m.visib)
     update_draw_Explosions (time)
     aliens_update_draw(time, m)
     m.draw()
##     n.draw()
     
     update_draw_Shots()
     DISPLAYSURF.blit(scoreS,(0,0))
     if helpText[6]:
          DISPLAYSURF.blit(helpS1,(0,25))
          DISPLAYSURF.blit(helpS2,(0,36))
          DISPLAYSURF.blit(helpS3,(0,47))
          DISPLAYSURF.blit(helpS4,(0,58))
          DISPLAYSURF.blit(helpS5,(0,69))
          DISPLAYSURF.blit(helpS6,(0,80))
     
     #pygame.draw.circle(DISPLAYSURF,WHITE,(900,200),5)
     for event in pygame.event.get():
##          if event.type == MOUSEBUTTONDOWN and event.button == 1:
##               m.setDest((mposX, mposY))
##               n.setDest((mposX, mposY))
          if event.type == KEYDOWN:
               if event.key == K_1:
                    shootingStyles = [0,1,1,False,0,0]
               if event.key == K_2:
                    shootingStyles = [-2,3,1,False,0,0]
               if event.key == K_3:
                    shootingStyles = [-2,3,2,False,180,0]
               if event.key == K_4:
                    shootingStyles = [-2,3,4,False,90,0]
               if event.key == K_5:
                    shootingStyles = [-2,3,4,True,90,0]
               if event.key == K_h:
                    if helpText[6]: helpText[6] = False
                    else: helpText[6] = True
               if event.key == K_v:
                    if m.unlimitedVisib: m.unlimitedVisib = False
                    else: m.unlimitedVisib = True
                         
          if event.type == QUIT:
               pygame.quit()
               sys.exit()
     pygame.display.update()
     fpsClock.tick(FPS)
