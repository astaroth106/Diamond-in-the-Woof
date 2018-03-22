import pygame, sys, json

pygame.init()
pygame.mixer.pre_init( 44100, -16, 2 )
dp = pygame.mixer.Sound( "Dog Whine.wav" )

class Tile(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.currentx = 0
        self.currenty = 0

    def update(self, direction):
        if direction == "right":
            self.rect.right -= self.speed
            self.rect.x -= self.speed
    
        elif direction == "left":
            self.rect.left += self.speed
            self.rect.x += self.speed
            
        elif direction == "up":
            self.rect.top += self.speed
            self.rect.y += self.speed
            
        elif direction == "down":
            self.rect.bottom -= self.speed
            self.rect.y -= self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self, image, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.width = 32
        self.rect.height = 32
    def setImage(self, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (192,64) )

def event_handler(event_list, direction, game_state):
    for event in event_list:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                direction = "right"
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                direction = "left"
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                direction = "up"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                direction = "down"
            elif event.key == pygame.K_p and game_state == "running":
                direction = "stop"
                game_state = "paused"
            elif event.key == pygame.K_p and game_state == "paused":
                direction = "stop"
                game_state = "running"
            elif event.key == pygame.K_ESCAPE:
                game_state = "quitting"
            elif event.key == pygame.K_y and game_state == "quitting":
                game_state = "start_screen"
            elif event.key == pygame.K_n and game_state == "quitting":
                direction = "stop"
                game_state = "running"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                direction = "stop"
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                direction = "stop"
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                direction = "stop"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                direction = "stop"
     
    return(direction, game_state)

# button class
class button:
    def __init__(self,img_filename):
        self.button_image = pygame.image.load(img_filename).convert_alpha()
        self.pos = pygame.Rect(0,0,self.button_image.get_width(),self.button_image.get_height())
        #state of the buttons
        self.state = "idle"
        self.click = False

    def get_state(self):
        return self.state

    def is_clicked(self):
        return self.click

    def draw(self,surface, rect):
        surface.blit(self.button_image, rect)
        self.pos = rect

    def set_button_text(self, text,font_size):
        font = pygame.font.SysFont("MatisseITC",font_size)
        new_text = font.render(text,1,(10,10,10))
        new_text_position = new_text.get_rect()
        new_text_position.centerx = self.button_image.get_rect().centerx
        new_text_position.centery = self.button_image.get_rect().centery
        self.button_image.blit(new_text,new_text_position)

#vector class
class vector:

    def __init__(self,pos_x,pos_y):
        self.position_x = pos_x
        self.position_y = pos_y

    def scale(self,factor):
        output = self
        output.position_x = self.position_x * factor
        output.position_y = self.position_y * factor
        return output

    def add(self,aVector):
        self.position_x = self.position_x + aVector.position_x
        self.position_y = self.position_y + aVector.position_y
        return self

    def subtract(self,aVector):
        output = self
        output.position_x = self.position_x - aVector.position_x
        output.position_y = self.position_y - aVector.position_y
        return output

    def magnitude(self):
        return math.sqrt((math.pow(self.position_x,2))+(math.pow(self.position_y,2)))

    def normalize(self):
        mag = self.magnitude()
        output = self
        if(mag == 0):
            return output
        else:
            output.position_x = self.position_x / mag
            output.position_y = self.position_y / mag            
            return output
        
    def __str__(self):
        return "({},{})".format(self.position_x,self.position_y)
    
class load_map:
    def __init__(self, MapName, initialPos):
        jsonMap = MapName
        initial_pos = ( (initialPos) )
        #read map from the *.json file
        mapfile = open(jsonMap).read()
        mapdict = json.loads(mapfile)
        tilesets = mapdict["tilesets"]
        layers = mapdict["layers"]
        height = mapdict["height"]
        width = mapdict["width"]

        self.all_tiles_from_sets = []
        #load the tiles on the sprisheets used for the map
        for tileset in tilesets:
            tileset_image = pygame.image.load(tileset["image"])
            imageheight = tileset["imageheight"]
            imagewidth = tileset["imagewidth"]
            tilewidth = tileset["tilewidth"]
            tileheight = tileset["tileheight"]
            for y in range(0, imageheight, tileheight):
                for x in range (0, imagewidth, tilewidth):
                    tile = pygame.Surface((tilewidth, tileheight))
                    tile.blit(tileset_image, (0,0), (x, y, tilewidth, tileheight))
                    self.all_tiles_from_sets.append(tile)

        #initial position of the map/player
        initial_map_pos = (initial_pos)

        #arrays to get the layers of the map
        self.all_layers = []
        self.action_layers = []

        #get all the layers that have the property "collision = 1"
        for layer in layers:
            data = layer["data"]
            layerheight = layer["height"]
            layerwidth = layer["width"]
            current_layer = pygame.sprite.Group()
            properties = layer["properties"]
            collision = properties["collision"]
            self.action_layers.append(collision)
            data_pos = 0
            #get the tiles' positions on the layer with collision
            for y in range (0, layerheight):
                for x in range (0, layerwidth):
                    gid = data[data_pos]
                    if gid > 0:
                        tile = Tile(self.all_tiles_from_sets[gid - 1])
                        tilex = (x * tilewidth) + initial_map_pos[0]
                        tiley = y * tileheight + initial_map_pos[1]
                        tile.rect.topleft = (tilex, tiley)
                        tile.image.set_colorkey((0,0,0))
                        current_layer.add(tile)
                    data_pos += 1

            self.all_layers.append(current_layer)

class TextBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.initFont()
        self.initImage()
        self.initGroup()

    def initFont(self):
        pygame.font.init()
        self.font = pygame.font.Font(None,36)

    def initImage(self):
        self.image = pygame.Surface((500,800))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = 550,0       

    def setText(self,text):
        tmp = pygame.display.get_surface()
        x_pos = self.rect.left+10
        y_pos = self.rect.top+10

        for t in text:
            x = self.font.render(t,1,(255,255,255))
            tmp.blit(x,(x_pos,y_pos))
            x_pos += 15

            if (x_pos > self.image.get_width()-20):
                x_pos = self.rect.left+20
                y_pos += 20
                
            pygame.display.flip()

    def initGroup(self):
        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

def monster_spawning(spawn, rnd, mons_dir, mobs, player, life, screen, hurt):
    
    if spawn and rnd == 1 and (mons_dir == "up" or mons_dir == "down"):

        screen.blit(mobs.image, (mobs.rect.x - 30, mobs.rect.y))
        mobs.rect.y += 8
        if mobs.rect.y > player.rect.y +200 or mobs.rect.x > player.rect.x +200:
            mobs.rect.x, mobs.rect.y = player.rect.x, player.rect.y
            print "bye1"
            spawn = False
        elif (mobs.rect.x + 16 >= player.rect.centerx and mobs.rect.x - 16 <= player.rect.centerx) and (mobs.rect.y + 16 >= player.rect.centery and mobs.rect.y - 16 <= player.rect.centery)  and not hurt:
            mobs.rect.x, mobs.rect.y = player.rect.x, player.rect.y
            print "collision"
            life -= 1
            hurt = True
            dp.play()
                
    elif spawn and rnd == 2 and (mons_dir == "right" or mons_dir == "left"):

        screen.blit(mobs.image, (mobs.rect.x, mobs.rect.y))
        mobs.rect.x += 8
        if mobs.rect.x > player.rect.x +200 or mobs.rect.y > player.rect.y +200:
            mobs.rect.x, mobs.rect.y = player.rect.x, player.rect.y
            print "bye2"
            spawn = False
        elif (mobs.rect.x + 16 >= player.rect.centerx and mobs.rect.x - 16 <= player.rect.centerx) and (mobs.rect.y + 16 >= player.rect.centery and mobs.rect.y - 16 <= player.rect.centery)  and not hurt:
            mobs.rect.x, mobs.rect.y = player.rect.x, player.rect.y
            print "collision"
            life -= 1
            hurt = True
            dp.play()
               
    elif spawn and rnd == 2 and (mons_dir == "up" or mons_dir == "down"):

        screen.blit(mobs.image, (mobs.rect.x - 30, mobs.rect.y))
        mobs.rect.y -= 8
        if mobs.rect.x < 100 or mobs.rect.y < 100:
            mobs.rect.x, mobs.rect.y = player.rect.x, player.rect.y
            print "bye3"
            spawn = False
        elif (mobs.rect.x + 16 >= player.rect.centerx and mobs.rect.x - 16 <= player.rect.centerx) and (mobs.rect.y + 16 >= player.rect.centery and mobs.rect.y - 16 <= player.rect.centery)  and not hurt:
            mobs.rect.x, mobs.rect.y = player.rect.x, player.rect.y
            print "collision"
            life -= 1
            hurt = True
            dp.play()
                    
    elif spawn and rnd == 1 and (mons_dir == "right" or mons_dir == "left"):

        screen.blit(mobs.image, (mobs.rect.x, mobs.rect.y))
        mobs.rect.x -= 8
        if mobs.rect.x < 100 or mobs.rect.y < 100:
            mobs.rect.x, mobs.rect.y = player.rect.x, player.rect.y
            print "bye4"
            spawn = False
        elif (mobs.rect.x + 16 >= player.rect.centerx and mobs.rect.x - 16 <= player.rect.centerx) and (mobs.rect.y + 16 >= player.rect.centery and mobs.rect.y - 16 <= player.rect.centery)  and not hurt:
            mobs.rect.x, mobs.rect.y = player.rect.x, player.rect.y
            print "collision"
            life -= 1
            hurt = True
            dp.play()
    return (spawn, life, hurt)

def wait(delta):
    i = 0
    while(i < 80000):
        i += delta
