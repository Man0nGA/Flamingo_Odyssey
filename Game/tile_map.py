import pygame, json, os, Animation
from Player import scale_mouse_pos

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

class TileMap():

    def __init__(self, tile_size, tiles_file, image_file):

        self.running = True

        self.tile_size = tile_size
        self.nbr_x_tiles = 380/self.tile_size
        self.nbr_y_tiles = 220/self.tile_size

        self.tiles = {".".join(f.split(".")[:-1]):pygame.image.load(tiles_file+f) for f in os.listdir(tiles_file)}
        self.images = {".".join(f.split(".")[:-1]):pygame.image.load(image_file+f) for f in os.listdir(image_file) if f != "Mini"}

        [print("Loaded TILE:", tile) for tile in self.tiles]
        [print("Loaded IMAGE:", img) for img in self.images]

        self.tile_map = {}
        self.animated_objects = {}
        self.all_layers = {}
        self.collidables = []
        self.current_layer = None

        self.basecamerapos = [0,0]

        self.loaded_map = None

        self.missingtexture = pygame.Surface((10,10))
        self.missingtexture.fill((255,0,255))
        blacksurf = pygame.Surface((5,5))
        blacksurf.fill((0,0,0))
        self.missingtexture.blit(blacksurf,(0,0))
        self.missingtexture.blit(blacksurf,(5,5))

        self.waypointicon = pygame.Surface((7,7))
        self.waypointicon.fill((255,255,0))
        # self.waypointrec = self.waypointicon.get_rect()

        self.maplimits = [None, None, None] # left, bottom, right

        # devtools
        self.showcollisions = False
        self.showcenter = False
        self.font = pygame.font.Font("PixelFont.ttf", 10)
        self.showinfo = False

    def load_map(self, path):
        with open(path, 'r') as f:
            json_data = json.load(f)
        
        self.tile_map = json_data['map']
        self.all_layers = json_data['all_layers']
        self.basecamerapos = json_data["camera_pos"]
        self.maplimits = json_data["map_limits"]
        self.loaded_map = path

        self.animated_objects = json_data['animated_objects']
        for layer in self.animated_objects:
            for tile in self.animated_objects[layer]:
                self.animated_objects[layer][tile]["class"] = Animation.Animation(self.animated_objects[layer][tile]["type"], self.animated_objects[layer][tile]["startingFrame"], self.animated_objects[layer][tile]["delay"])

        print("Loaded MAP:", path)
        print()

    def draw_map(self, display:pygame.Surface, playerpos):
        playerpos = [round(playerpos[0], 3), round(playerpos[1], 3)]
        self.collidables = []
        for layer in sorted([int(layr) for layr in self.all_layers]):
            for tile in self.tile_map[str(layer)].values():

                if self.all_layers[str(layer)]["layerspeed"] < 1:
                    addedlayerspeedx = + (tile["pos"][0] / 2 * self.tile_size)
                    addedlayerspeedy = + (tile["pos"][1] / 2 * self.tile_size)
                elif self.all_layers[str(layer)]["layerspeed"] == 1:
                    addedlayerspeedx = 0
                    addedlayerspeedy = 0
                else:
                    addedlayerspeedx = - (tile["pos"][0] / 2 * self.tile_size)
                    addedlayerspeedy = - (tile["pos"][1] / 2 * self.tile_size)

                if self.all_layers[str(layer)]["layerspeed"] == 0:
                    x = tile["pos"][0] * self.tile_size
                    y = tile["pos"][1] * self.tile_size
                else:
                    x = (tile["pos"][0] - playerpos[0]) * self.tile_size * self.all_layers[str(layer)]["layerspeed"] + addedlayerspeedx
                    y = (tile["pos"][1] - playerpos[1]) * self.tile_size * self.all_layers[str(layer)]["layerspeed"] + addedlayerspeedy
                    
                    
                if -380 <= x <= 380 and -220 <= y <= 220:
                    
                    if tile["type"] in self.tiles:
                        toblit = self.tiles[tile["type"]]
                    elif tile["type"] in self.images:
                        toblit = self.images[tile["type"]]
                    else:
                        toblit = self.missingtexture

                    if self.current_layer == None or layer == int(self.current_layer):
                        display.blit(toblit, (x, y))
                    else:
                        if self.opacity:
                            blit_alpha(display, toblit, (x,y), 100)
                        else:
                            display.blit(toblit, (x, y))

                    if tile["layer"] == 0 and 170 < x < 200 and 90 < y < 120:
                        rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                        self.collidables.append((rect, tile["pos"].copy(), tile["type"]))

            for tile in self.animated_objects[str(layer)].values():
                if self.all_layers[str(layer)]["layerspeed"] < 1:
                    addedlayerspeedx = + (tile["pos"][0] / 2 * self.tile_size)
                    addedlayerspeedy = + (tile["pos"][1] / 2 * self.tile_size)
                elif self.all_layers[str(layer)]["layerspeed"] == 1:
                    addedlayerspeedx = 0
                    addedlayerspeedy = 0
                else:
                    addedlayerspeedx = - (tile["pos"][0] / 2 * self.tile_size)
                    addedlayerspeedy = - (tile["pos"][1] / 2 * self.tile_size)

                if self.all_layers[str(layer)]["layerspeed"] == 0:
                    x = tile["pos"][0] * self.tile_size
                    y = tile["pos"][1] * self.tile_size
                else:
                    x = (tile["pos"][0] - playerpos[0]) * self.tile_size * self.all_layers[str(layer)]["layerspeed"] + addedlayerspeedx
                    y = (tile["pos"][1] - playerpos[1]) * self.tile_size * self.all_layers[str(layer)]["layerspeed"] + addedlayerspeedy
                
                if -380 <= x <= 380 and -220 <= y <= 220:
                    
                    toblit = tile["class"].getframe()

                    if self.current_layer == None or layer == int(self.current_layer):
                        display.blit(toblit, (x, y))
                    else:
                        if self.opacity:
                            blit_alpha(display, toblit, (x,y), 100)
                        else:
                            display.blit(toblit, (x, y))

                    if tile["layer"] == 0 and 170 < x < 200 and 90 < y < 120:
                        rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                        self.collidables.append((rect, tile["pos"].copy(), tile["type"]))

    def calcCollidables(self, playerpos):
        self.collidables = []
        for tile in self.tile_map["0"].values():
            x = (tile["pos"][0] - playerpos[0]) * self.tile_size
            y = (tile["pos"][1] - playerpos[1]) * self.tile_size
            if 170 < x < 200 and 90 < y < 120:
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                self.collidables.append((rect, tile["pos"].copy(), tile["type"]))

        for tile in self.animated_objects["0"].values():
            x = (tile["pos"][0] - playerpos[0]) * self.tile_size
            y = (tile["pos"][1] - playerpos[1]) * self.tile_size
            if 170 < x < 200 and 90 < y < 120:
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                self.collidables.append((rect, tile["pos"].copy(), tile["type"]))

    def collides(self, rect:pygame.Rect, surface:pygame.Surface):
        collisions = rect.collidelistall([obj[0] for obj in self.collidables])
        if len(collisions) == 0:
            return False
        return [self.collidables[r] for r in collisions]

    def isOverLimit(self, plr):
        if self.maplimits[0] > plr.pos[0] or self.maplimits[1] < plr.pos[1] or self.maplimits[2] < plr.pos[0]:
            return True
        
    def showWaypoint(self, surface: pygame.Surface, coords:list[int]):
        end_point = coords.copy()

        # pygame.draw.line(surface, (0,0,255), (190, 110), end_point)

        if coords[0] < 0:
            end_point[0] = 0
        if coords[0] > 380:
            end_point[0] = 370
        if coords[1] < 0:
            end_point[1] = 0
        if coords[1] > 220:
            end_point[1] = 210

        surface.blit(self.waypointicon, end_point)