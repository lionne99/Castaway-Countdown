import pygame
import sys
import time 
#from SpriteClass import Character 

WIDTH, HEIGHT = 800,600
FPS = 60
START_TIME = 2  # seconds to survive
RAFT_MATERIALS = 20  # materials needed to win


#INITIALIZE PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sacrifices Must Be Made")
runTitlescreen = True
runGame = False
runEndscreen = False

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

SAND = (194, 178, 128)
SAND_HOVER = (164, 150, 108)
BLACK = (0, 0, 0)

button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 80)

#sprite stuff 

class Character(pygame.sprite.Sprite):
    def __init__(self, col, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

player = Character((0, 0, 0), 100, 100)
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
while runTitlescreen:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                runTitlescreen = False 
                runGame = True

    screen.fill((240, 240, 220))  # light background
    draw_button(screen, button_rect, mouse_pos, "START")

    pygame.display.flip()
    clock.tick(60)

start_ticks = pygame.time.get_ticks()

# Main Game Loop
while runGame:
    mouse_pos = pygame.mouse.get_pos()


    screen.fill((240, 240, 220))  # light background 
    screen.blit(player.image, player.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.rect.y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player.rect.y += PLAYER_SPEED
    if keys[pygame.K_a]:
        player.rect.x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player.rect.x += PLAYER_SPEED

    # 3. Keep player inside screen boundaries
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > WIDTH:
        player.rect.right = WIDTH
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.bottom > HEIGHT:
        player.rect.bottom = HEIGHT


    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000 # Timer logic
    remaining_time = max(0, START_TIME - elapsed_seconds)

    minutes, seconds = divmod(remaining_time, 60)
    time_str = f"{minutes:02}:{seconds:02}"

    timer_text = font.render(time_str, True, (0, 0, 0))
    text_rect = timer_text.get_rect(topright=(WIDTH-20, 20))
    screen.blit(timer_text, text_rect)

    if remaining_time == 0:
        runGame = False
        runEndscreen = True

    pygame.display.flip()
    clock.tick(60)

# Endscreen Loop
while runEndscreen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # dark background for end screen
    restart_text = "Restart"
    draw_button(screen, button_rect, mouse_pos, restart_text)


    end_text = font.render("Game Over", True, (255, 255, 255))
    text_rect = end_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(end_text, text_rect)

    pygame.display.flip()
    clock.tick(60)


    
# pygame.quit()
