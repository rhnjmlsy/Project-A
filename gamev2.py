import pygame
import random
import sys

#colour RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Images for the sprites
background = pygame.image.load('backdrop_space.png')

spaceshipImg = pygame.image.load('spaceship.png')
spaceship = pygame.transform.scale(spaceshipImg, (60, 60))  

rockImg = pygame.image.load('rock.png') 
rock = pygame.transform.scale(rockImg, (50, 50)) 

laserImg = pygame.image.load('laser.png')
laser_image = pygame.transform.scale(laserImg, (16, 40))

# initinalise pygame
pygame.init()

# set screen size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# game name
pygame.display.set_caption("Laser Block Game")

# player block
player = pygame.Rect(200, 550, 50, 20)

score = 0
font = pygame.font.SysFont(None, 30)

# player speed
player_speed = 5

# list for lasers and stuff
lasers = []

# laser speed
laser_speed = 10

# falling enemies (blocks) list
blocks = []

# speed of the balling enemies
block_speed = 3

# Set the frequency of falling blocks (in frames)
block_frequency = 60

# clock to control frame rate
clock = pygame.time.Clock()

def set_level(score, SPEED):

    block_speed = score/7 + 3
    return block_speed

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True
    return False



#game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a new laser
                laser = pygame.Rect(player.centerx - 2, player.top - 10, 16, 40)
                lasers.append(laser)

    # move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # laser movemnt
    for laser in lasers:
        laser.y -= laser_speed

    # lasers disappear at top of screen
    lasers = [laser for laser in lasers if laser.y > 0]

    # add new enemy when its time
    if random.randint(0, block_frequency) == 0:
        block = pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), -20, 50, 50)
        blocks.append(block)

    # falling enemies movement 
    for block in blocks:
        block.y += block_speed

    # delete enemeies that fall to the very bottom of the screen
    blocks = [block for block in blocks if block.y < SCREEN_HEIGHT]

    # detect collision for shooting enemies (lasers and enemies)
    for laser in lasers:
        for block in blocks:
            if laser.colliderect(block):
                lasers.remove(laser)
                blocks.remove(block)

    # detect collision from player to enemy
    for block in blocks: 
        if player.colliderect(block):
            # Game over!
            pygame.quit()
            sys.exit()

    # white screen (replaced with custom background)
    screen.fill(WHITE)
    #background image
    screen.blit(background, (0, 0))

    # player picture
    #pygame.draw.rect(screen, BLACK, player)
    screen.blit(spaceship, (player.x, player.y))

    # laser picture
    for laser in lasers:
        #pygame.draw.rect(screen, BLACK, laser)
        screen.blit(laser_image, (laser.x, laser.y))

    # enemy picture
    for block in blocks:
        #pygame.draw.rect(screen, BLACK, block)
        screen.blit(rock, (block.x, block.y))


    #update display
    pygame.display.flip()

    # limit frame rate to 60 fps
    clock.tick(60)     