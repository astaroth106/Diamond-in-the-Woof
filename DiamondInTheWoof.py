import json, pygame, sys, random
from utils import Tile, Player, event_handler, button, load_map, monster_spawning, wait, vector, TextBox
import os

path = os.path.join(os.getcwd(), 'assets')
os.chdir(path)
    
pygame.init()
# initial source of light alpha value
shadow = 0

#define screen size
SCREENWIDTH = 1080
SCREENHEIGHT = 720
SCREENSIZE = ((SCREENWIDTH, SCREENHEIGHT))
screen = pygame.display.set_mode((SCREENSIZE) , pygame.FULLSCREEN)
light = pygame.Surface( (SCREENSIZE) )
resize = pygame.Surface( (SCREENWIDTH + 200, SCREENHEIGHT + 200) )
light.set_colorkey( (0,0,0) )
light.set_alpha(0)
pygame.display.set_caption("Diamond in the Ruff")
radius = 300
#circle mask
circle_mask = pygame.image.load( "circle_mask.png" ).convert_alpha()
circle_mask = pygame.transform.scale(circle_mask, (radius, radius))

#initialize globlal music
pygame.mixer.pre_init( 44100, -16, 2 )
pygame.mixer.music.load( "Burzum-Den_onde_ysten.wav" )
pygame.mixer.music.play()
dp = pygame.mixer.Sound( "batflyby.wav" )
bark = pygame.mixer.Sound("dogbark.wav")

#direction will store the players directions           
direction = "stop"
mons_dir = "stop"

#get the center of the screen and set the player there
screen_center = screen.get_rect().center
player_imgs = ["dogefront.png","dogeback.png","dogeright.png","dogeleft.png"]
player = Player(player_imgs[0], screen_center)
player.setImage(player_imgs[0])
life = 3

#mob initialization
mobs = Player("bat.png", screen_center)
spawn = False
hurt_time = 0
hurt = False

#get other relevant images
lives = pygame.image.load("Dog Treat 1.png").convert_alpha()

#battery life
outline = pygame.image.load ("Empty Battery Meter 128 px.png").convert_alpha()
fill = pygame.image.load("Battery Meter Fill.png").convert_alpha()
battery_pos = (900, 20)
battery_left_offset = 18
battery_right_offset = 10
battery_width = fill.get_width() - battery_left_offset - battery_right_offset;
mask = pygame.Rect( battery_left_offset, 0 , battery_width, fill.get_height() )

losing_time = 250.00
rnd = 0

jsonMap = "cave2.json"
initial_pos = (412, -1150)

#gameMap = load_map(jsonMap, initial_pos)

IMG_W = 64

frame = 0
frame_timer = 0
FRAME_TIME = 150
FRAME_CT = 3
win_cnt = 0

start_time = pygame.time.get_ticks()
(x,y) = player.rect.x, player.rect.y
(a,b) = (x,y)
#Loading background image
background = pygame.image.load("Background.png")
background = pygame.transform.scale(background,(SCREENWIDTH, SCREENHEIGHT))
#create starting screen
start_screen = pygame.Surface(screen.get_size())
start_screen.fill ((150,150,150))
#display start screen text
font = pygame.font.SysFont("MatisseITC",36)
text = font.render("Diamond in the Ruff",1,(10,10,10))
text_position = text.get_rect()
text_position.centerx = start_screen.get_rect().centerx
start_screen.blit(background,(0,0))
start_screen.blit(text,text_position)
        
#load button images and character portraits
start_button = button("bone1.png")
quit_button = button("bone2.png")

#creating button objects by specifying its pygame.Rect object
start_img_position = pygame.Rect((start_screen.get_rect().x,(text_position.y + 100))
                    ,(start_button.button_image.get_size()))

start_img_position.centerx = start_screen.get_rect().centerx #center the button relatively to screen

start_button.set_button_text("START",16)
start_button.draw(start_screen,start_img_position)

quit_img_position = pygame.Rect((start_screen.get_rect().x,(start_img_position.y + 300))
                    ,(quit_button.button_image.get_size()))

quit_img_position.centerx = start_screen.get_rect().centerx #center the button relatively to screen

quit_button.set_button_text("QUIT",16)
quit_button.draw(start_screen,quit_img_position)

#character selection screen
char_screen = pygame.Surface(screen.get_size())
char_screen.fill ((200,100,100))
#display char screen text
font = pygame.font.SysFont("MatisseITC",36)
text = font.render("Choose your Doge",1,(10,10,10))
text_position = text.get_rect()
text_position.centerx = char_screen.get_rect().centerx
char_screen.blit(background,(0,0))
char_screen.blit(text,text_position)

#create char portraits (clickable like buttons)
doge_portrait = button("Doge.png")
doge_position = pygame.Rect((text_position.x,(text_position.y + 100)),(doge_portrait.button_image.get_size()))
doge_position.centerx = char_screen.get_rect().centerx
doge_portrait.draw(char_screen,doge_position)

chihuahua_portrait = button("Chichi.png")
chihuahua_position = pygame.Rect(((text_position.x*1.2)-text_position.x,(text_position.y + 100)), (chihuahua_portrait.button_image.get_size()))
chihuahua_portrait.draw(char_screen, chihuahua_position)

bloodHound_portrait = button("LadyBird.png")
bloodHound_position = pygame.Rect((text_position.x*1.65,(text_position.y + 100)), (bloodHound_portrait.button_image.get_size()))
bloodHound_portrait.draw(char_screen, bloodHound_position)

#game over screen
game_over_screen = pygame.Surface(screen.get_size())
game_over_screen.fill ((200,200,250))
#display char screen text
font = pygame.font.SysFont("MatisseITC",48)
text = font.render("GAME OVER",1,(10,10,10))
text_position = text.get_rect()
text_position.centerx = game_over_screen.get_rect().centerx
text_position.centery = game_over_screen.get_rect().centery
game_over_screen.blit(background,(0,0))
game_over_screen.blit(text,text_position)

#game over buttons
GO_start_button = button("Bone2.png")
GO_start_button.set_button_text("START",16)
position_start_button = pygame.Rect((game_over_screen.get_rect().centerx,(game_over_screen.get_rect().centery))
                    ,(GO_start_button.button_image.get_size()))
position_start_button.centerx = game_over_screen.get_rect().centerx
GO_start_button.draw(game_over_screen,position_start_button)

#cinematic screen
cinematic_screen = pygame.Surface(screen.get_size())
cinematic_screen.fill((0,0,0))
#cinematic background image
cinematic_background = pygame.image.load("Entrance.png")
cinematic_background = pygame.transform.scale(cinematic_background,(SCREENWIDTH, SCREENHEIGHT))
cinematic_screen.blit(cinematic_background, (0,0))
#scaling player image for cinematic
player_img_idle = pygame.image.load("DogeFront.png")
player_img_moving = pygame.image.load("DogeBack.png")
player_img_idle = pygame.transform.scale(player_img_idle,(192, 64))
player_img_moving = pygame.transform.scale(player_img_moving,(192, 64))
hiker = pygame.image.load("boy.png").convert_alpha()
hiker = pygame.transform.scale(hiker, (192, 96) )
hikerback = pygame.image.load("boyback.png").convert_alpha()
hikerback = pygame.transform.scale(hikerback, (192, 96) )
cinematic_player = Player(player_imgs[0], (500,550))
cinematic_player.image = player_img_idle

#victory screen
victory_screen = pygame.Surface(screen.get_size())
victory_screen.fill ((200,200,250))
#display char screen text
font = pygame.font.SysFont("MatisseITC",48)
text = font.render("YOU WON",1,(10,10,10))
text_position = text.get_rect()
text_position.centerx = victory_screen.get_rect().centerx
text_position.centery = victory_screen.get_rect().centery
victory_screen.blit(background,(0,0))
victory_screen.blit(text,text_position)

#recording state of game
game_state = "start_screen"

#Main Loop
while True:

    #cinematic screen
    if(game_state == "cinematic_screen"):
        cinematic_clock = pygame.time.Clock()
        cinematic_frames_sec = 20
        print "cinematic_screen started"
        player_img_idle = pygame.image.load(player_imgs[0])
        player_img_moving = pygame.image.load(player_imgs[1])
        player_img_idle = pygame.transform.scale(player_img_idle,(192, 64))
        player_img_moving = pygame.transform.scale(player_img_moving,(192, 64))
        cinematic_player = Player(player_imgs[0], (500,550))
        cinematic_player.image = player_img_idle
        current_direction = "down"
        player_location = vector(500,400)
        hiker_location = vector(550, 380)
        velocity = vector(0,-3)
        in_motion = False
        hiker_motion = False
        hikerAni = hiker
        moving_state = 0
        clip_x = 64
        dialogue_state = 0
        #Text for cinematic
        cinematic_font = pygame.font.SysFont("MatisseITC",48)
        cinematic_text = cinematic_font.render("Press Space to Continue || Press 'S' to Start Game",1,(10,10,10))
        cinematic_text_position = cinematic_text.get_rect()
        cinematic_text_position.centerx = cinematic_screen.get_rect().centerx
        cinematic_text_position.centery = 700
        dialogue_font = pygame.font.SysFont("MatisseITC",20)
        dialogue_text = dialogue_font.render("",1,(10,10,10))        
                                   
        while (game_state == "cinematic_screen"):
            delta = cinematic_clock.tick(cinematic_frames_sec)
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state == "quiting"                      
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:                        
                        print "space bar pressed"
                        dialogue_state = dialogue_state + 1
                        if(dialogue_state == 3):
                            bark.play()
                    elif event.key == pygame.K_s:                        
                        print "game started"
                        game_state = "running"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    current_mouse_pos = pygame.mouse.get_pos()
                    if (start_button.pos.collidepoint(current_mouse_pos)):
                        print ""
                
            #handle direction           
            if current_direction == "up":
                cinematic_player.image = player_img_moving
                in_motion = True
                if(player_location.position_y == 250):
                   current_direction == "down"
                   cinematic_player.image = player_img_idle
                   in_motion = False
                   clip_x = 64
                else:
                    player_location.add(velocity)
                
                    
            #handle animation       
            if in_motion == True:
                if(moving_state == 0):
                    clip_x = clip_x +64
                    moving_state = moving_state + 1
                elif(moving_state == 1):
                    clip_x = clip_x - 64
                    moving_state = moving_state + 1
                elif(moving_state == 2):
                    clip_x = clip_x - 64
                    moving_state = moving_state + 1
                elif(moving_state == 3):
                    clip_x = clip_x + 64
                    moving_state = 0
            else:
                in_motion = False
                clip_x = 64
                moving_state = 0

            #makes sure that clip area is not outside of image rect
            if((clip_x > 192) or (clip_x < 0)):
                clip_x = 64
            
            #handle dialogue state            
            if dialogue_state == 1:
                hiker_motion = True
                dialogue_text = dialogue_font.render("Diamond Miner: Look! Diamonds!",1,(10,10,10))
            elif dialogue_state == 2:
                dialogue_text = dialogue_font.render("Doge: I guess I must go in",1,(10,10,10))                
            elif dialogue_state == 3:                
                current_direction = "up"
            elif dialogue_state == 4:
                game_state = "running"
            else:
                dialogue_state = 0
                
            #display screen
            clip2 = pygame.Rect((IMG_W+(64*(frame-1))), 0, 64, 96 )
            if hiker_motion:
                hiker_location.add(velocity)
                hikerAni = hikerback
                if frame_timer > FRAME_TIME:
                    frame_timer -= FRAME_TIME
                    frame = (frame + 1) % (FRAME_CT)
                frame_timer += delta
            idle_clip = pygame.Rect((clip_x,0),(64,64))
            screen.blit(cinematic_screen, (0, 0))
            screen.blit( cinematic_player.image,
                         (player_location.position_x,player_location.position_y),
                         idle_clip)
            if hiker_location.position_y >= 200:
                screen.blit(hikerAni, (hiker_location.position_x,hiker_location.position_y), area=clip2)
            cinematic_screen.blit(cinematic_text,cinematic_text_position)
            owner_textbox = pygame.image.load("OwnerTB.png").convert_alpha()
            owner_textbox.blit(dialogue_text,(50,50))
            cinematic_screen.blit(owner_textbox,(0,0))
            pygame.display.flip()
            
    #Start Screen's loop
    if(game_state == "start_screen"):
        print "start_screen started"
        while (game_state == "start_screen"):
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        game_state = "char_screen"
                        screen.blit(char_screen, (0, 0))
                        pygame.display.flip()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    current_mouse_pos = pygame.mouse.get_pos()
                    if (start_button.pos.collidepoint(current_mouse_pos)):
                        print "start button clicked"
                        game_state = "char_screen"
                        start_button.click = True
                        start_button.state = "clicked"
                    elif (quit_button.pos.collidepoint(current_mouse_pos)):
                        print "quit button clicked"
                        game_state = "quiting"
                        #pygame.quit()
                        #sys.exit()

            #display screen
            screen.blit(start_screen, (0, 0))
            pygame.display.flip()

    #Char Screen's Loop
    if(game_state == "char_screen"):
        print "char_screen started"
        while (game_state == "char_screen"):
			event_list = pygame.event.get()
			for event in event_list:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_s:
						game_state = "cinematic_screen"
						life = 3
						jsonMap = "cave2.json"
						initial_pos = (412, -1150)
						shadow = 0
						losing_time = 250
						(x,y) = player.rect.x, player.rect.y
						gameMap = load_map(jsonMap, initial_pos)
						player_imgs = ["dogefront.png","dogeback.png","dogeright.png","dogeleft.png"]
						player = Player(player_imgs[0], screen_center)
						player.setImage(player_imgs[0])
						radius = 300
						offset = 130
				elif event.type == pygame.MOUSEBUTTONDOWN:
					current_mouse_pos = pygame.mouse.get_pos()
					if (doge_portrait.pos.collidepoint(current_mouse_pos)):
						print "Doge Character Selected"
						game_state = "cinematic_screen"
						doge_portrait.click = True
						doge_portrait.state = "clicked"
						life = 3
						jsonMap = "cave2.json"
						initial_pos = (412, -1150)
						shadow = 0
						losing_time = 250
						(x,y) = player.rect.x, player.rect.y
						gameMap = load_map(jsonMap, initial_pos)
						player_imgs = ["dogefront.png","dogeback.png","dogeright.png","dogeleft.png"]
						player = Player(player_imgs[0], screen_center)
						player.setImage(player_imgs[0])
						radius = 300
						offset = 130
						circle_mask = pygame.transform.scale(circle_mask, (radius, radius))
					elif (chihuahua_portrait.pos.collidepoint(current_mouse_pos)):
						print "Chihuahua Character Selected"
						game_state = "cinematic_screen"
						chihuahua_portrait.click = True
						chihuahua_portrait.state = "clicked"
						life = 4
						jsonMap = "cave2.json"
						initial_pos = (412, -1150)
						shadow = 0
						losing_time = 250
						(x,y) = player.rect.x, player.rect.y
						gameMap = load_map(jsonMap, initial_pos)
						player_imgs = ["chihuahuaFront.png","chihuahuaBack.png","chihuahuaRight.png","chihuahuaLeft.png"]
						player = Player(player_imgs[0], screen_center)
						player.setImage(player_imgs[0])
						radius = 200
						offset = 90
						circle_mask = pygame.transform.scale(circle_mask, (radius, radius))
					elif (bloodHound_portrait.pos.collidepoint(current_mouse_pos)):
						print "Blood Hound Character Selected"
						game_state = "cinematic_screen"
						bloodHound_portrait.click = True
						bloodHound_portrait.state = "clicked"
						life = 2
						jsonMap = "cave2.json"
						initial_pos = (412, -1150)
						shadow = 0
						losing_time = 350
						(x,y) = player.rect.x, player.rect.y
						gameMap = load_map(jsonMap, initial_pos)
						player_imgs = ["BloodHoundFront.png","BloodHoundBack.png","BloodHoundRight.png","BloodHoundLeft.png"]
						player = Player(player_imgs[0], screen_center)
						player.setImage(player_imgs[0])
						radius = 200
						offset = 100
						circle_mask = pygame.transform.scale(circle_mask, (radius, radius))

			#display screen
			screen.blit(char_screen, (0, 0))
			pygame.display.flip()

    #Victory screen
    if(game_state == "victory"):
        print "Victory screen started"
        while (game_state == "victory"):
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        game_state = "start_screen"
                        jsonMap = "cave2.json"
                        initial_pos = (412, -1150)
                        shadow = 0
                        losing_time = 250
                        (x,y) = player.rect.x, player.rect.y
                        gameMap = load_map(jsonMap, initial_pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    current_mouse_pos = pygame.mouse.get_pos()
                    if (GO_start_button.pos.collidepoint(current_mouse_pos)):
                        print "New Game Started"
                        game_state = "start_screen"
                        jsonMap = "cave2.json"
                        initial_pos = (412, -1150)
                        shadow = 0
                        losing_time = 250
                        (x,y) = player.rect.x, player.rect.y
                        gameMap = load_map(jsonMap, initial_pos)
                        GO_start_button.click = True
                        GO_start_button.state = "clicked"
            screen.blit(victory_screen, (0, 0))
            pygame.display.flip()
            
    #game over screen's loop
    if(game_state == "game_over"):
        print "Game Over screen started"
        while (game_state == "game_over"):
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        game_state = "start_screen"
                        life = 3
                        shadow = 0
                        losing_time = 250
                        (x,y) = player.rect.x, player.rect.y
                        gameMap = load_map(jsonMap, initial_pos)
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    current_mouse_pos = pygame.mouse.get_pos()
                    if (GO_start_button.pos.collidepoint(current_mouse_pos)):
                        print "New Game Started"
                        game_state = "start_screen"
                        life = 3
                        shadow = 0
                        losing_time = 250
                        (x,y) = player.rect.x, player.rect.y
                        gameMap = load_map(jsonMap, initial_pos)
                        GO_start_button.click = True
                        GO_start_button.state = "clicked"

            #display screen
            screen.blit(game_over_screen, (0, 0))
            pygame.display.flip()

    #paused state
    if(game_state == "paused"):
        print "Paused screen started"
        textBox = TextBox()
        textBox.rect.x, textBox.rect.y = 200, 300
        textBox.setText("Game Paused")
        textBox = TextBox()
        textBox.rect.x, textBox.rect.y = 150, 350
        textBox.setText("Press p to continue...")
        while (game_state == "paused"):
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state == "start_screen"
            direction, game_state = event_handler(event_list, direction, game_state)

    #quitting state      
    if(game_state == "quitting"):
        print "quitting screen started"
        textBox = TextBox()
        textBox.rect.x, textBox.rect.y = 180, 300
        textBox.setText("Do you wish to quit?")
        textBox = TextBox()
        textBox.rect.x, textBox.rect.y = 200, 320
        textBox.setText("(y/n)")
        while (game_state == "quitting"):
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state == "start_screen"
            direction, game_state = event_handler(event_list, direction, game_state)
        
     #game's main loop       
    if(game_state == "running"):
        while (game_state == "running"):
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state == "start_screen"
            
            #get player's direction and correct image
            direction, game_state = event_handler(event_list, direction, game_state)
            if direction == "right":
                player.setImage(player_imgs[2])
                mobs.rect.x -= 5
                continious = 1
            elif direction == "left":
                player.setImage(player_imgs[3])
                mobs.rect.x += 5
                continious = 1
            elif direction == "up":
                player.setImage(player_imgs[1])
                mobs.rect.y += 5
                continious = 1
            elif direction == "down":
                player.setImage(player_imgs[0])
                mobs.rect.y -= 5
                continious = 1
            elif direction == "stop":
                frame = 1
                frame_timer = 0
                continious = 0

            #game's clock
            delta = pygame.time.get_ticks() - start_time
            start_time = pygame.time.get_ticks()
            
            #clear screen
            screen.fill((0,0,0))

            #check for collision
            layer_pos = 0
            for layer in gameMap.all_layers:
                layer.update(direction)
                layer.draw(screen)
                if int(gameMap.action_layers[layer_pos]) == 1:
                    if pygame.sprite.spritecollideany(player, gameMap.all_layers[4]):
                        if direction == "right":
                            for layers in gameMap.all_layers:
                                layers.update("left")
                        elif direction == "left":
                            for layers in gameMap.all_layers:
                                layers.update("right")
                        elif direction == "up":
                            for layers in gameMap.all_layers:
                                layers.update("down")
                        elif direction == "down":
                            for layers in gameMap.all_layers:
                                layers.update("up")
                        direction = "stop"
                if int(gameMap.action_layers[layer_pos]) == 1:
                    if pygame.sprite.spritecollideany(player, gameMap.all_layers[1]):
                        direction = "win"                        
                        win_cnt += 1
                if int(gameMap.action_layers[layer_pos]) == 1:
                    if pygame.sprite.spritecollideany(player, gameMap.all_layers[2]):
                        shadow = 0
                        losing_time = 250
                if int(gameMap.action_layers[layer_pos]) == 1:
                    if pygame.sprite.spritecollideany(player, gameMap.all_layers[3]) and not spawn and not hurt:
                        rnd = random.randint(1,2)
                        print rnd
                        mons_dir = direction
                        dp.play()
                        mobs.rect.x, mobs.rect.y = (x,y)
                        mobs.rect.center = screen_center
                        if rnd == 1 and (mons_dir == "up" or mons_dir == "down"):
                            mobs.rect.y = y - 400
                        elif rnd == 2 and (mons_dir == "right" or mons_dir == "left"):
                            mobs.rect.x = x - 400
                        elif rnd == 2 and (mons_dir == "up" or mons_dir == "down"):
                            mobs.rect.y = y + 400
                        elif rnd == 1 and (mons_dir == "right" or mons_dir == "left"):
                            mobs.rect.x = x + 400
                        spawn = True
                layer_pos += 1

            #animate the player when it is moving
            clip = pygame.Rect((IMG_W+(64*(frame-1))), 0, 64, 96 )
            if True:
                if frame_timer > FRAME_TIME:
                    frame_timer -= FRAME_TIME
                    frame = (frame + 1) % (FRAME_CT)
                frame_timer += delta
            

            spawn, life, hurt = monster_spawning(spawn, rnd, mons_dir, mobs, player, life, screen, hurt)

            if doge_portrait.click == True:
                tmp = circle_mask.copy()
                tmp.blit( screen,  (-(x - (radius/2.2)-100), -(y - (radius/2.3))) , special_flags=pygame.BLEND_RGBA_MIN )
                screen.fill( (0,0,0) )
                tmp = pygame.transform.scale(tmp, (radius*2, radius*2) )
                screen.blit( tmp, (x - (radius/2.2) - offset, y - (radius/2.3)-offset) )

            elif chihuahua_portrait.click == True:
            #copy the area around the player
                tmp = circle_mask.copy()
                tmp.blit( screen,  (-(x - (radius/2.2)-100), -(y - (radius/2.3))) , special_flags=pygame.BLEND_RGBA_MIN )
                screen.fill( (0,0,0) )
                tmp = pygame.transform.scale(tmp, (radius*2, radius*2) )
                screen.blit( tmp, (x - (radius/2.2) - offset, y - (radius/2.3) - offset) )
            elif bloodHound_portrait.click == True:
				tmp = circle_mask.copy()
				tmp.blit( screen,  (-(x - (radius/2.2)-100), -(y - (radius/2.3))) , special_flags=pygame.BLEND_RGBA_MIN )
				screen.fill( (0,0,0) )
				tmp = pygame.transform.scale(tmp, (radius*2, radius*2) )
				screen.blit( tmp, (x - (radius/2.2) - offset, y - (radius/2.3) - offset) )

            screen.blit( player.image, player.rect, area=clip )
            pygame.draw.circle(light, (1,0,0), (600, 600), 550)
            
            #light's counter to determine intensity of light
            shadow = shadow + .5
            light.set_alpha(shadow)

             #timer for battery
            losing_time = losing_time - .5
            losing_time = min( max(losing_time, 0.0), 250)

            mask.width = ((losing_time * 0.0037) * battery_width)
            mask.left = battery_left_offset + battery_width - mask.width
            fill_pos = (battery_pos[0]+battery_left_offset,battery_pos[1])

            #draw the players lives
            k = 20
            i = 0
            while i < life:
                screen.blit(lives, (k, 20) )
                k += 50
                i+=1

            if hurt or spawn:
                hurt_time += delta
                if hurt:
                    if frame_timer > FRAME_TIME:
                        frame_timer -= FRAME_TIME
                        frame = (frame + 4) % (FRAME_CT)
                    frame_timer += delta
                
                if hurt_time > 5000:
                    hurt_time = 0
                    hurt = False
                    spawn = False
            
            if True:
                screen.blit( outline, battery_pos )
                screen.blit( fill, fill_pos, area=mask)
                
            if life == 0 or shadow > 250:
                print "Game Over", life, shadow
                game_state = "game_over"
                direction = "stop"
                
            if win_cnt == 2:
                print "You won", win_cnt
                jsonMap = "cave2.json"
                initial_pos = (412, -1150)
                game_state = "victory"
                win_cnt = 0
                direction = "stop"
                
            elif direction == "win":
                print win_cnt
                jsonMap = "woof.json"
                initial_pos = (-1000, -1100)

                cinematic = 0
                i = 0
                textBox = TextBox()
                msg = True
                while(cinematic < 2000):
                    if i%2 == 0:
                        for layer in gameMap.all_layers:
                            layer.update("left")
                            layer.draw(screen)
                        tmp = circle_mask.copy()
                        tmp.blit( screen,  (-(x - (radius/2.2)-100), -(y - (radius/2.3))) , special_flags=pygame.BLEND_RGBA_MIN )
                        screen.fill( (0,0,0) )
                        tmp = pygame.transform.scale(tmp, (radius*2, radius*2) )
                        screen.blit( tmp, (x - (radius/2.2) - offset, y - (radius/2.3) - offset))
                        screen.blit(hiker, (player.rect.x, player.rect.y - 150), area = clip )
                        screen.blit( player.image, player.rect, area=clip )
                        pygame.display.flip()
                        wait(delta)
                    elif i%2 == 1:
                        for layer in gameMap.all_layers:
                            layer.update("right")
                            layer.draw(screen)
                        tmp = circle_mask.copy()
                        tmp.blit( screen,  (-(x - (radius/2.2)-100), -(y - (radius/2.3))) , special_flags=pygame.BLEND_RGBA_MIN )
                        screen.fill( (0,0,0) )
                        tmp = pygame.transform.scale(tmp, (radius*2, radius*2) )
                        screen.blit( tmp, (x - (radius/2.2) - offset, y - (radius/2.3) - offset))
                        screen.blit(hiker, (player.rect.x, player.rect.y - 150), area = clip )
                        screen.blit( player.image, player.rect, area=clip )
                        pygame.display.flip()
                        wait(delta)
                    if(cinematic < 1800):
                        screen.fill( (0,0,0) )
                    i += 1
                    if(cinematic > 1000):
                        gameMap = load_map(jsonMap, initial_pos)
                    cinematic += delta
                    delta = pygame.time.get_ticks() - start_time
                    start_time = pygame.time.get_ticks()
                owner_textbox = pygame.image.load("OwnerTB.png").convert_alpha()
                dialogue_text = dialogue_font.render("Diamond Miner: It looks like the entrance is",1,(10,10,10))
                owner_textbox.blit( dialogue_text, (50,50) )
                dialogue_text = dialogue_font.render("blocked, we should find another way out.",1,(10,10,10))
                owner_textbox.blit( dialogue_text, (50,60) )
                dialogue_text = dialogue_font.render("Press enter to continue...",1,(10,10,10))
                owner_textbox.blit( dialogue_text, (50,70) )
                screen.blit(owner_textbox, (0, 400) )
                pygame.display.flip()
                while msg:
                    event_list = pygame.event.get()
                    for event in event_list:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                msg = False
                                direction = "stop"
                                cinematic = 0
                                i = 0
                start_time = pygame.time.get_ticks()
                while(cinematic < 2000 and i < 150):
                    clip2 = pygame.Rect((IMG_W+(64*(frame-1))), 0, 64, 96 )
                    if frame_timer > FRAME_TIME:
                        frame_timer -= FRAME_TIME
                        frame = (frame + 1) % (FRAME_CT)
                    frame_timer += delta
                    for layer in gameMap.all_layers:
                        layer.draw
                    screen.fill( (0,0,0) )
                    screen.blit( tmp, (x - (radius/2.2) - offset, y - (radius/2.3) - offset))
                    screen.blit(hiker, (player.rect.x, player.rect.y - 150 + i), area = clip2 )
                    screen.blit( player.image, player.rect, area=clip )
                    pygame.display.flip()
                    wait(1)
                    delta = pygame.time.get_ticks() - start_time
                    start_time = pygame.time.get_ticks()
                    cinematic += delta
                    i += 1

                screen.blit( tmp, (x - (radius/2.2) - offset, y - (radius/2.3) - offset))
                screen.blit( player.image, player.rect, area=clip )
                owner_textbox = pygame.image.load("OwnerTB.png").convert_alpha()
                dialogue_text = dialogue_font.render("Your owner is now following you.",1,(10,10,10))
                owner_textbox.blit( dialogue_text, (50,50) )
                dialogue_text = dialogue_font.render("Press enter to continue...",1,(10,10,10))
                owner_textbox.blit( dialogue_text, (50,60) )
                screen.blit(owner_textbox, (0, 400) )
                textBox.rect.y -= 100
                #textBox.setText("Your owner is now following you.")
                textBox.rect.y += 100
                #textBox.setText("Press enter to continue...")
                pygame.display.flip()
                
                msg = True
                while msg:
                    event_list = pygame.event.get()
                    for event in event_list:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                msg = False
                                direction = "stop"
                              

            #draw a circle fading in by the alpha
            screen.blit(light, (0,0) )
            pygame.display.flip()

    if(game_state == "quiting"):
        pygame.quit()
        sys.exit()
