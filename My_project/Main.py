# Importing pygame, math and random modules, initializing pygame
import pygame
import math
import random
from pygame import mixer
pygame.init()


# The screen
screen = pygame.display.set_mode((800, 600))


# Background music
mixer.music.load('Background.wav')
mixer.music.play(-1)


# Window title, icon and backgroud details
pygame.display.set_caption("Wanted")
icon = pygame.image.load("Icon.png")
pygame.display.set_icon(icon)
weapon_choice = pygame.image.load("Weapon.png")
background = pygame.image.load("Background.png")
car = pygame.image.load("Car.png")


# Player image, step and starting position
player_image = pygame.image.load("Player.png")
playerX = 350
playerY = 270
player_step = 5

def Player (playerX, playerY):
    screen.blit(player_image, (playerX, playerY))


# Enemy image, step and starting position
enemy_image = []
enemyX = []
enemyY = []
enemy_step = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemy_image.append(random.choice([pygame.image.load("Enemy.png"),pygame.image.load("Enemy1.png")]))
    enemyX.append(random.randint(0,150))
    enemyY.append(random.randint(0,150))
    enemy_step.append(random.randint(1,2))

def Enemy(enemyX, enemyY, i):
    screen.blit(enemy_image[i], (enemyX, enemyY))


# Collision with enemies
def Collision_enemies (enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((math.pow(enemyX-playerX,2)) + (math.pow(enemyY-playerY,2)))
    if distance < 80:
        return True
    else:
        return False
    

# Bullet (ball)
bullet_image = pygame.image.load('Bullet.png')
bulletX = -50
bulletY = -50
bullet_step = 30
bullet_state = "ready"
bullet_sound = mixer.Sound("Ball_launched.wav")

def Fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x, y)) 

    
# Collision with bullet
def Collision (enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 50:
        return True
    else:
        return False


# Score and game over details
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 35)
textX = 2
textY = 2

def Score_show(x,y):
    score = font.render("Score:" + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

game_over_font = pygame.font.Font("freesansbold.ttf", 80)

Game_over = False

def Game_over_text():
    game_over = game_over_font.render("WASTED!", True, (0,181,114))
    screen.blit(game_over,(220,230))
    


# ======= Main game loop ========
opened = True
while opened:
    screen.blit(background, (0,0))    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            opened = False

    # Key reactions movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and playerX > player_step:
        playerX -= player_step
    if keys[pygame.K_RIGHT] and playerX < 750:
        playerX += player_step
    if keys[pygame.K_UP] and playerY > player_step:
        playerY -= player_step
    if keys[pygame.K_DOWN] and playerY < 580:
        playerY += player_step
    
    # Mouse reaction (shooting by left click)
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 and bullet_state == "ready":
            bullet_dest_x, bullet_dest_y = pygame.mouse.get_pos()
            bullet_start_x, bullet_start_y = playerX, playerY
            # Calculation the angle in radians between the start point and end point.
            x_diff = bullet_dest_x - bullet_start_x
            y_diff = bullet_dest_y - bullet_start_y                   
            angle = math.atan2(y_diff, x_diff)
            bulletX = playerX
            bulletY = playerY
            bullet_sound.play()
            Fire_bullet(bulletX, bulletY)    

    # Making the enemies to chase the Player
    for i in range(num_of_enemies):
        # global enemyX[i], enemyY[i]
        if enemyX[i] > playerX:
            enemyX[i] -= enemy_step[i]
        if enemyX[i] < playerX:
            enemyX[i] += enemy_step[i]
        if enemyY[i] > playerY:
            enemyY[i] -= enemy_step[i]
        if enemyY[i] < playerY:
            enemyY[i] += enemy_step[i]

        # Collision enemy - bullet
        hit_happened = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if hit_happened:
            hit_sound = mixer.Sound("Hit.wav")
            hit_sound.play()
            bulletY = playerY + 20
            bulletX = playerX + 40
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.choice([10,20,740,750])
            enemyY[i] = random.choice([10,20,540,550])
        Enemy(enemyX[i], enemyY[i], i)

        # Collision enemy - player (Game Over)
        collison_with_enemy = Collision_enemies(enemyX[i], enemyY[i], playerX, playerY)
        if collison_with_enemy:
            for j in range(num_of_enemies):
                enemyY[j] = 3000
            Game_over = True
            game_over__sound = mixer.Sound("Game_over.wav")
            game_over__sound.play()
            break

    # Bullet handling / movement
    if bulletY <= 0 or bulletY >= 600 or bulletX >= 800 or bulletX <= 0:
        bulletY = playerY
        bulletX = playerX
        bullet_state = "ready"
    if bullet_state == "fire":
        Fire_bullet(bulletX, bulletY)
        # Taking into account the angle, calculate our change_x and change_y.
        bulletX += math.cos(angle) * bullet_step
        bulletY += math.sin(angle) * bullet_step
    
    # Refreshing the screen after all changes
    if Game_over == True:
        Game_over_text()
    Player(playerX, playerY)
    
    screen.blit(weapon_choice, (730, 7))
    screen.blit(car, (-25, 30))
    screen.blit(car, (710, 380))
    Score_show(textX,textY)
    pygame.display.flip()
    




