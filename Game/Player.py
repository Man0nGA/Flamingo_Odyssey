import pygame, math, Animation
from Music import MusicHandler
# from tile_map import TileMap


def scale_mouse_pos(screen_size):
    mousepos = list(pygame.mouse.get_pos())
    ratio_x = (screen_size[0] - 1) / 380
    ratio_y = (screen_size[1] - 1) / 220
    return mousepos[0] / ratio_x, mousepos[1] / ratio_y


class Player():
    def __init__(self, surface:pygame.Surface, pos, mass: float = 1.0, gravity: float = 9.81, friction: float = 1.1 , winx: int=0, winy: int=0):
        self.pos = pos

        self.gravity = gravity*10
        self.friction = friction

        self.mass = mass
        self.speed = 0
        self.velocity = [0, 0]
        self.angle = 0
        self.size = (14, 30)

        self.dist = 0
        self.slope = None

        self.v_init = 0
        self.a_init = 0
        self.t = 0
        self.elapsed_time = 0.01

        self.win=False

        self.imgrect = pygame.Surface(self.size)
        self.imgrect.fill((255,0,0))

        self.img=Animation.Animation("flamantidle",0,150)
        self.fd=Animation.Animation("flamantdown")
        self.fu=Animation.Animation("flamantup")
        self.fdl=Animation.Animation("backdown")
        self.ful=Animation.Animation("backup")
        self.imgl=Animation.Animation("backidle")
        self.LMO=True


        self.rect = self.img.get_rect()
        self.rect.center = (surface.get_size()[0]/2, surface.get_size()[1]/2)

        self.clicked = False  # not using for now, might remove

        self.winx=winx
        self.winy=winy

        self.music = MusicHandler()


    def draw(self, surface:pygame.Surface):
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        if self.velocity[0]<0:
            surface.blit(self.imgl.getframe(), [self.rect.topleft[0], self.rect.topleft[1]-5])
        else:
            surface.blit(self.img.getframe(), [self.rect.topleft[0], self.rect.topleft[1]-5])        

    def showArrow(self, mousepos: tuple, surface: pygame.Surface):
        ssize = surface.get_size()

        mpos = ((ssize[0]/2 + (mousepos[0]-ssize[0]/2)/2), (ssize[1]/2 + (mousepos[1]-ssize[1]/2)/2))
        self.dist = math.sqrt((mpos[0]-190)**2+(mpos[1]-110)**2)

        if self.LMO == True :
            self.music.tirer.play()
            self.LMO = False

        if self.dist >= 15 :
            self.dist = 15
        self.speed = self.dist/20
        self.velocity = [self.speed * (mpos[0]-190), self.speed * (mpos[1]-110)]

        pygame.draw.line(surface, (255, 255, 255), (190, 110), mpos)

        self.slope = (mpos[1] - 110) / (mpos[0] - 190)
        self.angle = math.atan(self.slope)
        if self.slope < 0:
            self.angle += math.pi
        self.angle = math.degrees(self.angle)
        # TODO: If above or under 110 add/subtract to angle
        if mpos[1] < 110:
            self.angle = 180 - self.angle
        else:
            self.angle = 360 - self.angle

        tipsize = math.log(math.sqrt((110 - mpos[1])**2 + (190 - mpos[0])**2))*2

        # left side
        newangle = math.atan2(110 - mpos[1], 190 - mpos[0])
        newangle += math.radians(45)
        x = mpos[0] + tipsize*math.cos(newangle)
        y = mpos[1] + tipsize*math.sin(newangle)
        pygame.draw.line(surface, (255,255,255), mpos, (x, y))

        # right side
        newangle = math.atan2(110 - mpos[1], 190 - mpos[0])
        newangle += math.radians(-45)
        x = mpos[0] + tipsize*math.cos(newangle)
        y = mpos[1] + tipsize*math.sin(newangle)
        pygame.draw.line(surface, (255,255,255), mpos, (x, y))

        self.t = 0
    
    def movement(self, surface: pygame.surface, screen, map):

        if self.mouseaction[0]:
            self.showArrow(scale_mouse_pos(pygame.display.get_window_size()), surface)

        elif self.clicked or 0 == 1:


            run = True
            self.music.lache.play()
            while run:
                
                
                self.velocity[1] += self.gravity * self.elapsed_time
                x = self.velocity[0] * self.elapsed_time
                y = self.velocity[1] * self.elapsed_time
    
                # x collisions
                self.pos[0] += x
                map.calcCollidables(self.pos)
                collisions = map.collides(self.rect, surface)


                if collisions:
                    
                    for c in collisions:
                        if c[2] == "kill":
                            self.isOverLimit(map, surface, screen, 1)
                            return
                    
                    # right collision
                    if min(collisions, key=lambda r: r[0].bottom)[1][0] > self.pos[0] + 19:
                        collision = min(collisions, key=lambda r: r[0].bottom)
                        self.pos[0] = collision[1][0]
                        self.pos[0] -= 20
                        self.velocity[0] /= -3
                        if self.dist >= 15 :
                            self.music.mur.play()

                    # left collision
                    else:
                        collision = min(collisions, key=lambda r: r[0].bottom)
                        self.pos[0] = collision[1][0]
                        self.pos[0] -= 17
                        self.velocity[0] /= -3
                        if self.dist >= 15 :
                            self.music.mur.play()

                # y collisions
                self.pos[1] += y
                map.calcCollidables(self.pos)
                collisions = map.collides(self.rect, surface)

                if collisions:
                    
                    for c in collisions:
                        if c[2] == "kill":
                            self.isOverLimit(map, surface, screen, 1)
                            return

                    if 0.5 > self.velocity[0] > -0.5 or 0.5 > self.velocity[1] > -0.5:
                        run = False

                    # bottom collision
                    if min(collisions, key=lambda r: r[0].bottom)[1][1] > self.pos[1] + 10:
                        collision = min(collisions, key=lambda r: r[0].bottom)
                        self.pos[1] = collision[1][1]
                        self.pos[1] -= 12
                        self.velocity[1] /= -3
                        self.velocity[0] /= self.friction

                    # up collision
                    else:
                        collision = min(collisions, key=lambda r: r[0].bottom)
                        self.pos[1] = collision[1][1]
                        self.pos[1] -= 9 
                        self.velocity[1] /= -3
                        if self.dist >= 15 :
                            self.music.mur.play()

                map.draw_map(surface, self.pos)
                self.waypoints_handler(map, surface)

                if self.velocity[1]>10:
                    self.LMO = True
                    if self.velocity[0]>0:
                        surface.blit(self.fd.getframe(), [self.rect.topleft[0], self.rect.topleft[1]-5])
                        self.fu.counter = 0
                        self.fu.frame = 0
                        
                    else:
                        surface.blit(self.fdl.getframe(), [self.rect.topleft[0], self.rect.topleft[1]-5])
                        self.ful.counter = 0
                        self.ful.frame = 0

                elif self.velocity[1]<10:
                    if self.velocity[0]>0:
                        surface.blit(self.fu.getframe(), [self.rect.topleft[0], self.rect.topleft[1]-5])
                        self.fdl.counter = 0
                        self.fdl.frame = 0
                    else:
                        surface.blit(self.ful.getframe(), [self.rect.topleft[0], self.rect.topleft[1]-5])
                        self.fdl.counter = 0
                        self.fdl.frame = 0

                self.t += self.elapsed_time
                screen.blit(pygame.transform.scale(surface, pygame.display.get_window_size()), (0, 0))
                pygame.display.update()

                self.isOverLimit(map, surface, screen)

    def isOverLimit(self, map, surface: pygame.Surface, screen: pygame.display, bypass = 0):
        if map.isOverLimit(self) or bypass:

            self.velocity = [0, 0]
            self.music.death_sound.play()
            for i in range(0, 400, 10):
                self.draw(surface)
                pygame.draw.circle(surface, (0, 0, 0), (190, 110), i)
                screen.blit(pygame.transform.scale(surface, pygame.display.get_window_size()), (0, 0))
                pygame.display.update()
                pygame.time.wait(12)
            
            self.pos = map.basecamerapos.copy()
            self.music.respawn.play()
            for i in range(400, 0, -10):
                surface.fill((0, 0, 0))
                map.draw_map(surface, self.pos)
                self.waypoints_handler(map, surface)
                self.draw(surface)
                pygame.draw.circle(surface, (0, 0, 0), (190, 110), i)
                screen.blit(pygame.transform.scale(surface, pygame.display.get_window_size()), (0, 0))
                pygame.display.update()
                pygame.time.wait(10)


    def mouse_handler(self):
        self.mouseaction = pygame.mouse.get_pressed()

    def click_handler(self):   # not using for now, might remove
        if self.mouseaction[0]:
            self.clicked = True
        else:
            self.clicked = False

    def waypoints_handler(self, map, surface):
        x = (self.winx - self.pos[0]) * 10
        y = (self.winy - self.pos[1]) * 10
        map.showWaypoint(surface, [x, y])

    def winning(self):
        winzone = pygame.Rect((self.winx - self.pos[0]) * 10, (self.winy - self.pos[1]) * 10, 40, 40)
        if winzone.colliderect(self.rect):
            self.music.win.play()
            self.win=True
            return 1


    def update(self, surface: pygame.Surface, map, screen: pygame.display):
        self.mouse_handler()

        self.draw(surface)

        self.waypoints_handler(map, surface)

        self.movement(surface, screen, map)

        self.click_handler()

        self.isOverLimit(map, surface, screen, 0)

        self.winning()