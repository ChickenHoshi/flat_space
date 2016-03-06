'''new stuff:
    more organized: superclasses and subclasses
    new alien that shoots
    zoomed view + follow
    alien drops + collection
    targetting missile
    pause'''

helpText = ['press MOUSE LEFT to move',
          'press LEFT CONTROL or MOUSE RIGHT to shoot',
          'press SPACE to brake',
          'press V to toggle visibility',
          'press 1 - 5 for shooting styles',
          'press P to spawn aliens',
          'press C to collect drops',
          'press Z to toggle views',
          'press M while mouseover an alien for missile',
          'press 0 to pause',
          False]


import pygame, sys, math, random, time

from pygame.locals import*

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
#set up window
windowX = 1080
windowY = 720
surface = pygame.display.set_mode((windowX,windowY))
DISPLAYSURF = pygame.Surface((400,400))
pygame.display.set_caption('Flat_Space 0.2a')
font = pygame.font.SysFont('consolas',20)
fonth = pygame.font.SysFont('consolas',10)

#set up colors

BLACK = ( 0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255,255,255)
shots = []
explosions = []
aliens = []
materials = []

class Entity:
     def __init__(self,pos):
          self.x = pos[0]
          self.y = pos[1]

class material_snappite(Entity):
     def __init__(self, pos):
          Entity.__init__(self, pos)
          self.rad = int(5)
          self.collectionDist = 1000
          self.rotateSpeed = 2
          self.x2 = self.x
          self.y2 = self.y
          self.speed = [random.choice([-0.01,0.01]),
                        random.choice([-0.01,0.01])]
          
          self.randx = random.randint(-self.rad*2,self.rad*2)
          self.randy = random.randint(-self.rad*2,self.rad*2)
          self.angle = random.randint(0,360)
           
          self.pList= [[self.x + self.randx + math.cos(math.radians(self.angle))*self.rad, \
                              self.y + math.sin(math.radians(self.angle))*self.rad+ self.randy],
                             [self.x + self.randx, self.y+ self.randy],
                             [self.x + self.randx+ math.cos(math.radians(self.angle + 150))*self.rad,
                              self.y + math.sin(math.radians(self.angle + 150))*self.rad+ self.randy],
                              [self.x + self.randx+ math.cos(math.radians(self.angle + 210))*self.rad,
                              self.y + math.sin(math.radians(self.angle + 210))*self.rad+ self.randy],
                              [self.x + self.randx, self.y + self.randy],
                              ]
          
          
     def draw(self):
          pygame.draw.polygon(DISPLAYSURF,green(157),self.pList,1)
          
     def update(self, time, player):
          self.x2 += self.speed[0]
          self.y2 += self.speed[1]
          
          if math.hypot(self.x - player.x , self.y - player.y) <= self.collectionDist and\
             pygame.key.get_pressed()[pygame.K_c]:
               self.x2 += math.copysign(5,player.x - self.x)
               self.y2 += math.copysign(5,player.y - self.y)
               
          self.x = int(self.x2)
          self.y = int(self.y2)
          self.pList= [[self.x + self.randx + math.cos(math.radians(self.angle))*self.rad, \
                    self.y + math.sin(math.radians(self.angle))*self.rad+ self.randy],
                   [self.x + self.randx, self.y+ self.randy],
                   [self.x + self.randx+ math.cos(math.radians(self.angle + 150))*self.rad,
                    self.y + math.sin(math.radians(self.angle + 150))*self.rad+ self.randy],
                    [self.x + self.randx+ math.cos(math.radians(self.angle + 210))*self.rad,
                    self.y + math.sin(math.radians(self.angle + 210))*self.rad+ self.randy],
                    [self.x + self.randx, self.y + self.randy],
                    ]
               
               
          
class explosion_parker(Entity):
     def __init__(self, pos,speed = 10, rad = 5):
          Entity.__init__(self, pos)
          self.x += random.randint(-5,5)
          self.y += random.randint(-5,5)
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
class Shot(Entity):
     def __init__(self, pos, angle,ship, alien = False):
          Entity.__init__(self, pos)
          self.alien = ship
          self.recoil = 5
          self.range = 200
          self.length = 10
          self. speed = 20

          self.angle = math.radians(angle)
          self.movex = math.cos(self.angle) * self.speed
          self.movey = -math.sin(self.angle) * self.speed
          self.damage = 5
          
          ship.fuel -= 1
     def update(self):
          self.x += self.movex
          self.y += self.movey
     def draw(self, width = 1):
          self.eX = self.x - self.length * math.cos(self.angle)
          self.eY = self.y + self.length * math.sin(self.angle)
          pygame.draw.line(DISPLAYSURF, green(100), (int(self.x),int(self.y)), (int(self.eX),int(self.eY)),5)
          pygame.draw.line(DISPLAYSURF, WHITE, (int(self.x),int(self.y)), (int(self.eX),int(self.eY)),width)
          
class shot_carrot(Shot):
     def __init__(self, pos, angle,ship, alien = False):
          Shot.__init__(self, pos, angle,ship, alien = False)
     def update(self):
          super(shot_carrot,self).update()
     def draw(self):
          super(shot_carrot,self).draw()

          
class shot_broccoli(Shot):
     def __init__(self, pos, ship,target , alien = False, angle = -1):
          Shot.__init__(self, pos, angle,ship, alien = False)
          self.target = target
          self.alien = ship
          self.length = 20
          self.speed = 2
          self.recoil = 1
          self.angle = math.radians(findAngle(target.x,target.y,(self.x,self.y)))
          self.damage = 50
          ship.fuel -= 1
     def update(self):
          if self.speed < 100: self.speed += 0.1
          if self.target != False:
               self.angle = math.radians(findAngle(self.target.x,self.target.y,(self.x,self.y)))
          self.movex = math.cos(self.angle) * self.speed
          self.movey = -math.sin(self.angle) * self.speed
          super(shot_broccoli,self).update()
     def draw(self):
          super(shot_broccoli,self).draw(width = 5)
          
class Alien(Entity):
     def __init__(self,pos,radius = 15):
          Entity.__init__(self, pos)
          self.healthMax = 10*radius
          self.health = 10*radius
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
          self.hbX = self.health/self.healthMax/2*self.rad
          self.hbY = self.y - self.rad
          
          pygame.draw.line(DISPLAYSURF, green(255),(self.x - self.hbX, self.hbY),(self.x + self.hbX, self.hbY))

     def update(self, time, player):
          if time % (FPS*5) == 0:
               self.movex = random.uniform(-1,1)
               self.movey = random.uniform(-1,1)
               self.speedx += self.movex
               self.speedy += self.movey
               if abs(self.speedx) > 1: self.speedx = math.copysign(1,self.speedx)
               if abs(self.speedy) > 1: self.speedy = math.copysign(1,self.speedy)
              
          if self.movex != 0 or self.movey != 0:
               self.x += self.speedx
               self.y += self.speedy
          if self.x < -self.rad*2: self.x = windowX + self.rad*2
          if self.x > windowX + self.rad*2 : self.x = -self.rad*2
          if self.y < -self.rad*2: self.y = windowY + self.rad*2
          if self.y > windowY + self.rad*2 : self.y = -self.rad*2

          for shot in range(len(shots)):
               if self.x - self.rad <shots[shot].x <self.x + self.rad and \
                  self.y - self.rad <shots[shot].y <self.y + self.rad and not shots[shot].alien == self:
                    self.a = shots[shot].recoil * math.cos(shots[shot].angle)
                    self.b = shots[shot].recoil * math.sin(shots[shot].angle)
                    self.speedx += self.a / 20
                    self.speedy -= self.b / 20
                    self.x += self.a 
                    self.y -= self.b 
                    self.health -= shots[shot].damage
                    addExplosion((int(shots[shot].x), int(shots[shot].y)))
                    deleteShots(shot)
                    break
               
class alien_STVN(Alien):
     def __init__(self,pos,radius = 25):
          Alien.__init__(self,pos,radius = 25)
          self.angle = 270
          self.fuel = 100
          self.wings = []
          self.pList = []
          self.shootRange = 1000
     def draw(self,time):
          self.wings = [[int(self.x + self.rad*math.cos(math.radians(self.angle - 120))),
                         int(self.y - self.rad*math.sin(math.radians(self.angle - 120)))],
                        [int(self.x + self.rad/2*math.cos(math.radians(self.angle - 150))),
                         int(self.y - self.rad/2*math.sin(math.radians(self.angle - 150)))],
                        [int(self.x ), int(self.y )],
                        [int(self.x + self.rad/2*math.cos(math.radians(self.angle + 150))),
                         int(self.y - self.rad/2*math.sin(math.radians(self.angle + 150)))],
                        [int(self.x + self.rad*math.cos(math.radians(self.angle + 120))),
                         int(self.y - self.rad*math.sin(math.radians(self.angle + 120)))],
                        [int(self.x + self.rad/2*math.cos(math.radians(self.angle + 100))),
                         int(self.y - self.rad/2*math.sin(math.radians(self.angle + 100)))],
                        [int(self.x), int(self.y)],
                        [int(self.x + self.rad/2*math.cos(math.radians(self.angle - 100))),
                         int(self.y - self.rad/2*math.sin(math.radians(self.angle - 100)))]]
          if time % 10 == 0:
               self.pList = []
               for i in range(self.edges):
                    self.pList.append([self.x + self.rad/2*math.cos(math.radians(self.angle ))+ random.randint(int(-self.rad*1/4),int(self.rad*1/4)),\
                                  self.y - self.rad/2*math.sin(math.radians(self.angle ))+ random.randint(int(-self.rad*1/4),int(self.rad*1/4))])
          pygame.draw.circle(DISPLAYSURF,green(50),(int(self.x),int(self.y)),self.rad,1)
          pygame.draw.polygon(DISPLAYSURF, self.color, self.pList)
          pygame.draw.polygon(DISPLAYSURF, self.color, self.wings)
          
          super(alien_STVN,self).draw(time)
     def update(self, time, player):
          ##shoot
          
          if math.hypot(player.x - self.x, player.y - self.y) <= self.shootRange and time%(30+random.randint(-2,2)) == 0:
               self.angle = findAngle(player.x, player.y,(self.x, self.y))
               shots.append(shot_carrot((self.x, self.y),self.angle, self,alien = True))
          
          super(alien_STVN,self).update(time, player)

class alien_FRD(Alien):
     def __init__(self,pos,radius = 15):
          Alien.__init__(self, pos)
          
     def draw(self,time):
          
          if time % 10 == 0:
               self.pList = []
               for i in range(self.edges):
                    self.pList.append([self.x + random.randint(-self.rad,self.rad),\
                                  self.y + random.randint(-self.rad,self.rad)])
          pygame.draw.circle(DISPLAYSURF,green(50),(int(self.x),int(self.y)),self.rad,3)
          pygame.draw.polygon(DISPLAYSURF, self.color, self.pList)
          pygame.draw.circle(DISPLAYSURF,green(255),(int(self.x),int(self.y)),int(self.rad/5),int(self.rad/10))

          super(alien_FRD,self).draw(time)
          
     def update(self, time, player):
          super(alien_FRD,self).update(time, player)

class ship_macbeth(Entity):
     def __init__(self,pos):
          Entity.__init__(self, pos)
          self.cargo = {}
          self.unlimitedVisib = True
          self.rad = 15
          self.visib = 200
          self.speedx = 0
          self.speedy = 0
          self.accel = 0.1
          self.fuelMax = 1000
          self.fuel = 1000
          self.fuel_regen = 1
          self.stopSpeed = .5
          self.angle0 = 0
          self.speedLimit = 10000
          
          

     def draw(self):
          self.mposX, self.mposY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
          self.angle0 = findAngle(self.mposX, self.mposY,(self.x,self.y))
          if not fullView[0]:
               self.angle0 = findAngle(self.mposX, self.mposY,(windowX/2, windowY/2))
          
          self.angle = math.radians(self.angle0)
          self.angle2 = math.radians(self.angle0+120)
          self.angle3 = math.radians(self.angle0-120)
          self.p1 = (math.cos(self.angle) * self.rad*2 + int(self.x),\
                     -math.sin(self.angle) * self.rad*2 + int(self.y))
          self.p2 = (math.cos(self.angle2) * self.rad + int(self.x),\
                     -math.sin(self.angle2) * self.rad + int(self.y))
          self.p3 = (math.cos(self.angle3) * self.rad + int(self.x),\
                     -math.sin(self.angle3) * self.rad + int(self.y))
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
          if self.fuel > 0  :
               if self.x < dest[0] and not self.speedx > self.speedLimit: self.speedx += self.accel
               if self.x > dest[0] and not self.speedx < -self.speedLimit: self.speedx -= self.accel
               if self.y < dest[1] and not self.speedy > self.speedLimit: self.speedy += self.accel
               if self.y > dest[1] and not self.speedy < -self.speedLimit: self.speedy -= self.accel
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
          aliens.append(alien_STVN((random.randint(0,windowX),random.randint(0,windowY))))
          if random.randint(0,10) == 0:
               aliens.append(alien_FRD( (random.randint(0,windowX),random.randint(0,windowY)) , 50))
def aliens_update_draw(time,player):
     for ayy in aliens:
          ayy.update(time, player)
          if player.unlimitedVisib == False:
               if math.hypot(player.x - ayy.x, player.y- ayy.y) <= player.visib  :
                    ayy.draw(time)
          else:
               ayy.draw(time)

def deleteAliens():
     delList = []
     delList2 = []
     for ayy in range(len(aliens)):
          if aliens[ayy].health <= 0:
               delList.append(ayy)
     adjust = 0
     for ayy in delList:
          explosions.append(explosion_parker((int(aliens[ayy- adjust].x),int(aliens[ayy- adjust].y)),\
                                             int(aliens[ayy- adjust].rad/3),int(aliens[ayy- adjust].rad/3*2)))
          for i in range(int(aliens[ayy - adjust].rad/5)):
               addMaterials((aliens[ayy- adjust].x,aliens[ayy- adjust].y))
          for shot in range(len(shots)):
               if isinstance(shots[shot], shot_broccoli):
                    shots[shot].target = False
          aliens.pop(ayy - adjust)
          adjust += 1
          score[0] += 1
          

def addMaterials(pos):
     materials.append(material_snappite(pos))

def update_draw_Materials (time, player):
     for material in materials:
          material.update(time, player)
          material.draw()

def deleteMaterials(player):
     delList = []
     for material in range(len(materials)):
          if math.hypot(materials[material].x - player.x, materials[material].y - player.y) <= 5:
               delList.append(material)
     adjust = 0
     for material in delList:
          try:
               player.cargo['Snappite'] += 1
          except KeyError:
               player.cargo['Snappite'] = 1
          materials.pop(material - adjust)
          adjust += 1









               
m = ship_macbeth((900,200))
helps = []
for i in range(len(helpText)-1):
     helps.append(fonth.render(helpText[i],1,(0,255,0)))
fullView = [True]
time = 0
score = [0]
paused = False
while True: ##main game loop
     if paused == False:
          if time < 12000: time += 1
          else: time = 0
          if time % FPS == 0:
               pass
          deleteShots()
          deleteExplosion()
          deleteAliens()
          deleteMaterials(m)
          mposX, mposY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
          addAliens(time)
          
          if pygame.mouse.get_pressed()[0]:
               m.setDest((mposX, mposY))
          if pygame.key.get_pressed()[pygame.K_SPACE]:
               m.stop()
          m.move()
          m.fuelRegen()

          scoreS = font.render('kills: '+str(score[0])+' -- H: help',1,(0,255,0))
          
          if shootingStyles[3] == True:
               shootingStyles[5] = time
          
          if time%5 == 0:
               addShot((m.x,m.y),m,time)
          DISPLAYSURF.fill(BLACK)
          pygame.draw.circle(DISPLAYSURF,green(25),(int(m.x),int(m.y)),m.visib)
          update_draw_Explosions (time)
          update_draw_Materials (time, m)
          aliens_update_draw(time, m)
          m.draw()
          
          update_draw_Shots()
          
     if not fullView[0]:
          surface.fill(BLACK)
          
          DISP = pygame.transform.scale(DISPLAYSURF,(2400,2400))
          surface.blit(DISP,(-int(m.x*2 - windowX/2),-int(m.y*2 - windowY/2)))
     else:
          DISPLAYSURF = pygame.transform.scale(DISPLAYSURF,(1200,1200))
          surface.blit(DISPLAYSURF,(0,0))
          
     if helpText[6]:
          for i in range(len(helps)):
                 surface.blit(helps[i],(0,25 + i*11))
     surface.blit(scoreS,(0,0))
     for event in pygame.event.get():
          if event.type == MOUSEBUTTONDOWN:
               pass
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
               if event.key == K_z:
                    if fullView[0]: fullView[0] = False
                    else: fullView[0] = True
               if event.key == K_v:
                    if m.unlimitedVisib: m.unlimitedVisib = False
                    else: m.unlimitedVisib = True
               if event.key == K_m:
                    for ayy in aliens:
                         if math.hypot(mposX - ayy.x, mposY - ayy.y) <= ayy.rad :
                                    shots.append(shot_broccoli((m.x, m.y),m,ayy))
               if event.key == K_0:
                    if paused: paused = False
                    else: paused = True
               
                         
          if event.type == QUIT:
               pygame.quit()
               sys.exit()
     pygame.display.update()
     fpsClock.tick(FPS)
