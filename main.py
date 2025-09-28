import pygame
import sys
import time 
import random
import math

WIDTH, HEIGHT = 800,600
MAP_W, MAP_H = 1200, 900
FPS = 60
START_TIME = 100  # seconds to survive
RAFT_MATERIALS = 20  # materials needed to win
planksInQuest1 = 2
planksInQuest2 = 4
planksInQuest3 = 6

firstTime1 = True
firstTime2 = True
firstTime3 = True



#INITIALIZE PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Castaway Countdown")

#All of the screens
runTitlescreen = True
runGame = False
runEndscreen = False
runWinScreen = False
questScreen = False
runQuest1 = False
runQuest2 = False
runQuest3 = False
quest1Menu = False
quest2Menu = False
quest3Menu = False

plankCount = 0
planksKilled1 = 0
planksKilled2 = 0
planksKilled3 = 0

quest1_started = False
quest2_started = False
quest3_started = False

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

#Sign background
menuBKG = pygame.image.load("Menu.png").convert()
menuBKG = pygame.transform.scale(menuBKG, (WIDTH, HEIGHT))

#Start background
startBKG = pygame.image.load("startBKG.png").convert()
startBKG = pygame.transform.scale(startBKG, (WIDTH, HEIGHT))

#Battle background
grassBKG = pygame.image.load("grassBKG1.png").convert()
grassBKG = pygame.transform.scale(grassBKG, (WIDTH, HEIGHT))

#Win background
winBKG = pygame.image.load("winBKG.png").convert()
winBKG = pygame.transform.scale(winBKG, (WIDTH, HEIGHT))

#Lose background
loseBKG = pygame.image.load("loseBKG.png").convert()
loseBKG = pygame.transform.scale(loseBKG, (WIDTH, HEIGHT))

#Game background
background = pygame.image.load("Game background dd.png").convert()
background = pygame.transform.scale(background, (MAP_W, MAP_H))

SAND = (194, 178, 128)
SAND_HOVER = (164, 150, 108)
BLACK = (0, 0, 0)

button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 80)

#sprite stuff 

class dock(pygame.sprite.Sprite):
    def __init__(self, x, y, sizeX, sizeY):
        super().__init__()
        self.image = pygame.image.load("Dock.png").convert_alpha()
        # Resize the image
        self.image = pygame.transform.scale(self.image, (sizeX, sizeY))
        self.rect = self.image.get_rect()
        # Set initial center position
        self.rect.center = (x, y)
        self.hitbox = self.rect.copy()
        # self.hitbox = self.rect.inflate(-50, -50)


class Sign(pygame.sprite.Sprite):
    def __init__(self, x, y, quest, sizeX, sizeY):
        super().__init__()
        # Load the image
        self.image = pygame.image.load(quest + ".png").convert_alpha()
        # Resize the image
        self.image = pygame.transform.scale(self.image, (sizeX, sizeY))
        self.rect = self.image.get_rect()
        # Set initial center position
        self.rect.center = (x, y)
        self.hitbox = self.rect.copy()
        # self.hitbox = self.rect.inflate(-50, -50)

class Wood(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the image
        self.image = pygame.image.load("Plank.png").convert_alpha()
        # Resize the image
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        # Set initial center position
        self.rect.center = (x, y)
        self.hitbox = self.rect.inflate(-20, -20)  

    @staticmethod
    def addPlank():
        # Spawn coordinates that keep the sprite on-screen
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        return Wood(x, y)
    def getX(self):
        return self.rect.x
    def getY(self):
        return self.rect.y

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the image
        self.image = pygame.image.load("Monkey.png").convert_alpha()
        # Resize the image
        self.image = pygame.transform.scale(self.image, (200, 200))
        # Get rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-50, -50)
        # Set initial center position
        self.rect.center = (x, y)
        self.hitbox = self.rect.inflate(-90,-90)
        
    def update_hitbox(self):
        # Keep hitbox centered on the sprite
        self.hitbox.center = self.rect.center

class BouncingSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, dx, dy):
        super().__init__()
        # Load and optionally scale image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (125,125))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Set velocity
        self.dx = dx
        self.dy = dy

        self.hitbox = self.rect.inflate(-88, -88)

    def update(self, screen_width, screen_height):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off edges
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.dy *= -1

        # Keep hitbox updated
        self.hitbox.center = self.rect.center

def check_collision(player, bouncer_group):
    if pygame.sprite.spritecollide(player, bouncer_group, False):
        return True
    return False

class Button:
    def __init__(self, x, y, w, h, text, font, color, hover_color, text_color=(0, 0, 0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface, mouse_pos):
        # Pick hover or normal color
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color

        # Draw rectangle
        pygame.draw.rect(surface, color, self.rect, border_radius= 10)

        # Draw text centered inside
        text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(
            text_surf,
            (self.rect.centerx - text_surf.get_width() // 2,
             self.rect.centery - text_surf.get_height() // 2)
        )

    def is_clicked(self, event):
        # Returns True if left mouse button clicked inside rect
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )



dock = dock(WIDTH//2, HEIGHT//2 + 170, 400, 400)

player = Character(100, 100)




player.rect.center = (MAP_W // 2, MAP_H // 2)

all_wood_Quest1 = pygame.sprite.Group()
all_wood_Quest2 = pygame.sprite.Group()
all_wood_Quest3 = pygame.sprite.Group()



def fillPlankGroup(numPlanks, plankGroup):
    for i in range(numPlanks):
        while True:
            plank = Wood.addPlank()
            too_close = False

            for other in all_wood_Quest1:
                dx = plank.rect.centerx - other.rect.centerx
                dy = plank.rect.centery - other.rect.centery

                dist = math.hypot(dx, dy)
                if dist < 50:
                    too_close = True
                    break
            
            if not too_close:
                plankGroup.add(plank)
                break

fillPlankGroup(planksInQuest1, all_wood_Quest1)      


bouncer1 = BouncingSprite("Hunter.png", 100, 100, 4, 2)
bouncer2 = BouncingSprite("Hunter.png", 100, 100, -5, 3)
bouncer3 = BouncingSprite("Hunter.png", 100, 100, 2,6)
bouncer4 = BouncingSprite("Hunter.png", 100, 100, -3, 4)
bouncer5 = BouncingSprite("Hunter.png", 100, 100, 4, -4)
bouncer6 = BouncingSprite("Hunter.png", 100, 100, 3,4)
bouncer7 = BouncingSprite("Hunter.png", 100, 100, -2, 3)
bouncer8 = BouncingSprite("Hunter.png", 100, 100, 4, -1)


all_sprites_Quest1_Bouncers = pygame.sprite.Group()
all_sprites_Quest1_Bouncers.add(bouncer1, bouncer2, bouncer3)

all_sprites_Quest2_Bouncers = pygame.sprite.Group()
all_sprites_Quest2_Bouncers.add(bouncer1, bouncer2, bouncer3, bouncer4, bouncer5)

all_sprites_Quest3_Bouncers = pygame.sprite.Group()
all_sprites_Quest3_Bouncers.add(bouncer1, bouncer2, bouncer3, bouncer4, bouncer5, bouncer6,bouncer7, bouncer8)

PLAYER_SPEED = 5

# Methods
def draw_button(surface, rect, mouse_pos, button_text):

    text = font.render(button_text, True, BLACK)
    if rect.collidepoint(mouse_pos):
        color = SAND_HOVER
    else:
        color = SAND
    pygame.draw.rect(surface, color, rect, border_radius=10)
    surface.blit(text, (rect.centerx - text.get_width()//2,
                        rect.centery - text.get_height() // 2))

# Titlescreen Loop


start_ticks = pygame.time.get_ticks()

bg_x = 0
bg_y = 0  

quest1 = Sign(600, 88, "Quest1", 600, 600)
quest1_group = pygame.sprite.Group()
quest1_group.add(quest1)

quest2 = Sign(80, 315, "Quest2", 600, 600)
quest2_group = pygame.sprite.Group()
quest2_group.add(quest2)

quest3 = Sign(1150, 300 , "Quest3", 300, 300)
quest3_group = pygame.sprite.Group()
quest3_group.add(quest3)

quest1_end_time = 0  # buffer timer for ending quest1
while True:

    # --- Event handling ---
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if runTitlescreen and button_rect.collidepoint(event.pos):
                runTitlescreen = False
                runGame = True

    # --- Timer calculation ---
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining_time = max(0, START_TIME - elapsed_seconds)
    minutes, seconds = divmod(remaining_time, 60)
    time_str = f"{minutes:02}:{seconds:02}"
    timer_text = font.render(time_str, True, (0, 0, 0))
    timer_rect = timer_text.get_rect(topright=(WIDTH-20, 20))
    

    # --- Titlescreen ---
    if runTitlescreen:
        screen.blit(startBKG, (0,0))
        start_button = Button(WIDTH //2 - 100, HEIGHT // 2 - 40, 200, 80,
                      "START", font, SAND, SAND_HOVER)
        start_button.draw(screen, mouse_pos)

    # --- Main Game ---
    elif runGame:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player.rect.y += PLAYER_SPEED
        if keys[pygame.K_a]: player.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player.rect.x += PLAYER_SPEED

        # keep player inside boundaries
        if player.rect.left < -50: player.rect.left = -50
        if player.rect.right > MAP_W: player.rect.right = MAP_W
        if player.rect.top < -50: player.rect.top = -50
        if player.rect.bottom > MAP_H - 150: player.rect.bottom = MAP_H - 150

        # camera offset
        cam_x = max(0, min(player.rect.centerx - WIDTH//2, MAP_W - WIDTH))
        cam_y = max(0, min(player.rect.centery - HEIGHT//2, MAP_H - HEIGHT))
        cam_x_dock = max(0, min(player.rect.centerx - WIDTH//2, MAP_W - WIDTH))
        cam_y_dock = max(0, min(player.rect.centery - HEIGHT//2, MAP_H - HEIGHT))

        

        # draw map 
        screen.fill((0, 0, 0))
        screen.blit(background, (-cam_x, -cam_y))
        player_display = player.rect.move(-cam_x, -cam_y)

        # draw dock
        screen.blit(dock.image, (dock.rect.x - cam_x+ 235, dock.rect.y - cam_y + 230))

        #draw player
        screen.blit(player.image, player_display)

        if player.rect.collidepoint(550, 70 ) or player.rect.collidepoint(70, 310) or player.rect.collidepoint(1150, 300):
            # Display interaction prompt
            prompt_text = font.render("Press E to interact", True, (255, 255, 255))
            prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(prompt_text, prompt_rect)

        # draw quest signs
        for sign in [quest1, quest2, quest3]:
            # screen.blit(sign.image, (sign.rect.x - cam_x, sign.rect.y - cam_y))
            screen.blit(sign.image, (sign.rect.x - cam_x, sign.rect.y - cam_y))

        
            
        keys = pygame.key.get_pressed()
        if player.rect.collidepoint(600,88) and keys[pygame.K_e]:
            # runQuest1 = True
            quest1Menu = True
            runGame = False
            

        keys = pygame.key.get_pressed()
        if player.rect.collidepoint(70, 310) and keys[pygame.K_e]:
            # runQuest2 = True
            quest2Menu = True
            runGame = False

        keys = pygame.key.get_pressed()
        if player.rect.collidepoint(1150, 300) and keys[pygame.K_e]:
            quest3Menu = True
            runGame = False 

        #dock
        keys = pygame.key.get_pressed()
        if player.rect.colliderect(dock.rect) and keys[pygame.K_e] and plankCount >= 20:
            runWinScreen = True
            runGame = False 

        # game over by timer
        if remaining_time <= 0:
            runGame = False
            runEndscreen = True

        screen.blit(timer_text, timer_rect)
        wood_text = font.render(f"Wood: {plankCount}/{RAFT_MATERIALS}", True, (0, 0, 0))
        wood_rect = wood_text.get_rect(topleft=(20, 20))
        screen.blit(wood_text, wood_rect)

        

    # --- Quest1 ---
    elif quest1Menu:
        screen.blit(menuBKG, (0, 0))

        prompt_text = font.render("Quest One : Easy", True, (0,0,0))
        prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT -490))
        screen.blit(prompt_text, prompt_rect)
        prompt_text2 = font.render("Collect materials and avoid the Hunter", True, (0,0,0))
        prompt_rect = prompt_text2.get_rect(center=(WIDTH // 2, HEIGHT -430))
        screen.blit(prompt_text2, prompt_rect)

        prompt_text3 = font.render("Enter either by sacrificing 15s or one wood", True, (0,0,0))
        prompt_rect = prompt_text3.get_rect(center=(WIDTH // 2, HEIGHT -390))
        screen.blit(prompt_text3, prompt_rect)

        purchaseBtn = Button(WIDTH//2 - 145, HEIGHT//2 +10, 300, 80,
                    "Sacrifice 15s", font, SAND, SAND_HOVER)
        purchaseBtn.draw(screen, mouse_pos)
        woodBtn = Button(WIDTH//2 - 145, HEIGHT//2 + 90, 300, 80,
                    "Sacrifice one wood", font, SAND, SAND_HOVER)
        woodBtn.draw(screen, mouse_pos) 

        if quest1Menu and purchaseBtn.is_clicked(event):
            quest1Menu = False
            runQuest1 = True
            start_ticks -= 15000
        elif quest1Menu and woodBtn.is_clicked(event):
            quest1Menu = False
            runQuest1 = True
            plankCount -= 1

    elif runQuest1:
        
        if firstTime1:
            firstTime1 = False 
            starting_positions = [(100,100), (100,100), (100,100)]  # example positions
            for i, bouncer in enumerate(all_sprites_Quest1_Bouncers.sprites()):
                bouncer.rect.center = starting_positions[i]
                bouncer.dx = random.choice([-5, -4, -3, 3, 4, 5])  # give them random initial velocities
                bouncer.dy = random.choice([-5, -4, -3, 3, 4, 5])

        if not quest1_started:

            for bouncer in all_sprites_Quest1_Bouncers:
                bouncer.rect.center = (100, 100)  # fixed starting point

            quest1_started = True
            player.rect.center = (WIDTH//2, HEIGHT//2)
            planksKilled1 = 0
            # Clear old planks and spawn new ones
            all_wood_Quest1.empty()
            fillPlankGroup(planksInQuest1, all_wood_Quest1)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player.rect.y += PLAYER_SPEED
        if keys[pygame.K_a]: player.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player.rect.x += PLAYER_SPEED

        # keep player inside quest1 screen
        if player.rect.left < 0: player.rect.left = 0
        if player.rect.right > WIDTH: player.rect.right = WIDTH
        if player.rect.top < 0: player.rect.top = 0
        if player.rect.bottom > HEIGHT: player.rect.bottom = HEIGHT

        # update bouncers
        all_sprites_Quest1_Bouncers.update(WIDTH, HEIGHT)
        player.update_hitbox()

        # check collisions with bouncers
        for bouncer in all_sprites_Quest1_Bouncers:
            if player.hitbox.colliderect(bouncer.hitbox):
                firstTime1 = True
                runQuest1 = False
                runGame = True  # return to main game

        # check collisions with planks
        for wood in all_wood_Quest1:
            if player.hitbox.colliderect(wood.hitbox):
                wood.kill()
                planksKilled1 += 1
                plankCount += 1

        screen.blit(grassBKG, (0, 0))

        # finished quest1
        if planksKilled1 >= planksInQuest1:
            firstTime1 = True
            runQuest1 = False
            runGame = True
            quest1_started = False

        # draw everything
        all_wood_Quest1.draw(screen)
        all_sprites_Quest1_Bouncers.draw(screen)
        screen.blit(player.image, player.rect)
        screen.blit(timer_text, timer_rect)

        wood_text = font.render(f"Wood: {plankCount}/{RAFT_MATERIALS}", True, (0, 0, 0))
        wood_rect = wood_text.get_rect(topleft=(20, 20))
        screen.blit(wood_text, wood_rect)
    
    elif quest2Menu:
        screen.blit(menuBKG, (0, 0))
    
        prompt_text4 = font.render("Quest Two : Medium", True, (0,0,0))
        prompt_rect = prompt_text4.get_rect(center=(WIDTH // 2, HEIGHT -490))
        screen.blit(prompt_text4, prompt_rect)
        prompt_text5 = font.render("Collect the materials and avoid the Hunters", True, (0,0,0))
        prompt_rect = prompt_text5.get_rect(center=(WIDTH // 2, HEIGHT -430))
        screen.blit(prompt_text5, prompt_rect)

        prompt_text6 = font.render("Enter either by sacrificing 25s or two wood", True, (0,0,0))
        prompt_rect = prompt_text6.get_rect(center=(WIDTH // 2, HEIGHT -390))
        screen.blit(prompt_text6, prompt_rect)

        purchaseBtn3 = Button(WIDTH//2 - 145, HEIGHT//2 +10, 300, 80,
                    "Sacrifice 25s", font, SAND, SAND_HOVER)
        purchaseBtn3.draw(screen, mouse_pos)
        woodBtn2 = Button(WIDTH//2 - 145, HEIGHT//2 + 90, 300, 80,
                    "Sacrifice two wood", font, SAND, SAND_HOVER)
        woodBtn2.draw(screen, mouse_pos) 

        if quest2Menu and purchaseBtn3.is_clicked(event):
            quest2Menu = False
            runQuest2 = True
            start_ticks -= 25000
        elif quest2Menu and woodBtn2.is_clicked(event):
            quest2Menu = False
            runQuest2 = True
            plankCount -= 2

    # --- Quest2 
    elif runQuest2:
        

        if firstTime2:
            firstTime2 = False 
            starting_positions = [(100,100), (100,100), (100,100), (100,100), (100,100)]  # example positions
            for i, bouncer in enumerate(all_sprites_Quest2_Bouncers.sprites()):
                bouncer.rect.center = starting_positions[i]
                bouncer.dx = random.choice([-5, -4, -3, 3, 4, 5])  # give them random initial velocities
                bouncer.dy = random.choice([-5, -4, -3, 3, 4, 5])

        if not quest2_started:
            quest2_started = True
            player.rect.center = (WIDTH//2, HEIGHT//2)
            planksKilled2 = 0
            # Clear old planks and spawn new ones
            all_wood_Quest2.empty()
            fillPlankGroup(planksInQuest2, all_wood_Quest2)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player.rect.y += PLAYER_SPEED
        if keys[pygame.K_a]: player.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player.rect.x += PLAYER_SPEED

        # keep player inside quest2 screen
        if player.rect.left < 0: player.rect.left = 0
        if player.rect.right > WIDTH: player.rect.right = WIDTH
        if player.rect.top < 0: player.rect.top = 0
        if player.rect.bottom > HEIGHT: player.rect.bottom = HEIGHT

        # update bouncers
        all_sprites_Quest2_Bouncers.update(WIDTH, HEIGHT)
        player.update_hitbox()

        # check collisions with bouncers
        for bouncer in all_sprites_Quest2_Bouncers:
            if player.hitbox.colliderect(bouncer.hitbox):
                firstTime2 = True
                runQuest2 = False
                runGame = True  # return to main game
                quest2_started = False

        # check collisions with planks
        for wood in all_wood_Quest2:
            if player.hitbox.colliderect(wood.hitbox):
                wood.kill()
                planksKilled2 += 1
                plankCount += 1


        screen.blit(grassBKG, (0, 0))

        # finished quest1
        if planksKilled2 >= planksInQuest2:
            firstTime2 = True
            runQuest2 = False
            runGame = True
            quest2_started = False

        # draw everything
        all_wood_Quest2.draw(screen)
        all_sprites_Quest2_Bouncers.draw(screen)
        screen.blit(player.image, player.rect)
        screen.blit(timer_text, timer_rect)

        wood_text = font.render(f"Wood: {plankCount}/{RAFT_MATERIALS}", True, (0, 0, 0))
        wood_rect = wood_text.get_rect(topleft=(20, 20))
        screen.blit(wood_text, wood_rect)

    elif quest3Menu:
        screen.blit(menuBKG, (0, 0))

        prompt_text = font.render("Quest Three : Hard", True, (0,0,0))
        prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT -490))
        screen.blit(prompt_text, prompt_rect)
        prompt_text2 = font.render("Collect the materials and avoid the Hunters", True, (0,0,0))
        prompt_rect = prompt_text2.get_rect(center=(WIDTH // 2, HEIGHT -430))
        screen.blit(prompt_text2, prompt_rect)

        prompt_text3 = font.render("Enter either by sacrificing 35s or three wood", True, (0,0,0))
        prompt_rect = prompt_text3.get_rect(center=(WIDTH // 2, HEIGHT -390))
        screen.blit(prompt_text3, prompt_rect)

        purchaseBtn3 = Button(WIDTH//2 - 145, HEIGHT//2 +10, 300, 80,
                    "Sacrifice 35s", font, SAND, SAND_HOVER)
        purchaseBtn3.draw(screen, mouse_pos)
        woodBtn = Button(WIDTH//2 - 145, HEIGHT//2 + 90, 300, 80,
                    "Sacrifice three wood", font, SAND, SAND_HOVER)
        woodBtn.draw(screen, mouse_pos) 

        if quest3Menu and purchaseBtn3.is_clicked(event):
            quest3Menu = False
            runQuest3 = True
            start_ticks -= 35000
        elif quest3Menu and woodBtn.is_clicked(event):
            quest3Menu = False
            runQuest3 = True
            plankCount -= 3
        

    elif runQuest3:
        

        if firstTime3:
            firstTime3 = False 
            starting_positions = [(100,100), (100,100), (100,100), (100,100), (100,100), (100,100), (100,100), (100,100)]  # example positions
            for i, bouncer in enumerate(all_sprites_Quest3_Bouncers.sprites()):
                bouncer.rect.center = starting_positions[i]
                bouncer.dx = random.choice([-5, -4, -3, 3, 4, 5])  # give them random initial velocities
                bouncer.dy = random.choice([-5, -4, -3, 3, 4, 5])


        if not quest3_started:
            quest3_started = True
            player.rect.center = (WIDTH//2, HEIGHT//2)
            planksKilled3 = 0
            # Clear old planks and spawn new ones
            all_wood_Quest3.empty()
            fillPlankGroup(planksInQuest3, all_wood_Quest3)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s]: player.rect.y += PLAYER_SPEED
        if keys[pygame.K_a]: player.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]: player.rect.x += PLAYER_SPEED

        # keep player inside quest3 screen
        if player.rect.left < 0: player.rect.left = 0
        if player.rect.right > WIDTH: player.rect.right = WIDTH
        if player.rect.top < 0: player.rect.top = 0
        if player.rect.bottom > HEIGHT: player.rect.bottom = HEIGHT

        # update bouncers
        all_sprites_Quest3_Bouncers.update(WIDTH, HEIGHT)
        player.update_hitbox()

        # check collisions with bouncers
        for bouncer in all_sprites_Quest3_Bouncers:
            if player.hitbox.colliderect(bouncer.hitbox):
                firstTime3 = True
                runQuest3 = False
                runGame = True  # return to main game

        # check collisions with planks
        for wood in all_wood_Quest3:
            if player.hitbox.colliderect(wood.hitbox):
                wood.kill()
                planksKilled3 += 1
                plankCount += 1

        screen.blit(grassBKG, (0, 0))

        # finished quest3
        if planksKilled3 >= planksInQuest3:
            firstTime3 = True
            runQuest3 = False
            runGame = True
            quest3_started = False

        # draw everything
        # screen.fill((240, 240, 220))
        all_wood_Quest3.draw(screen)
        all_sprites_Quest3_Bouncers.draw(screen)
        screen.blit(player.image, player.rect)
        screen.blit(timer_text, timer_rect)

        wood_text = font.render(f"Wood: {plankCount}/{RAFT_MATERIALS}", True, (0, 0, 0))
        wood_rect = wood_text.get_rect(topleft=(20, 20))
        screen.blit(wood_text, wood_rect)


    elif runWinScreen:
        screen.blit(winBKG, (0, 0))
        # win_text = font.render("You Won!!", True, (0, 0, 0))  
        # center the text on the screen
        # screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - win_text.get_height()//2))
    
       # pygame.display.flip() 



    # --- Endscreen ---
    elif runEndscreen:
        screen.blit(loseBKG, (0, 0))
        #draw_button(screen, button_rect, mouse_pos, "Restart")
        # end_text = font.render("Game Over", True, (0, 0, 0))
        # screen.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2 - end_text.get_height()//2))

    # --- Update display ---
    pygame.display.flip()
    clock.tick(FPS)