import pygame
import math
import random

pygame.init()
#create screen
screen = pygame.display.set_mode((800, 600))

#background
bg = pygame.image.load("bg.jpg")


#set title and title
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pokemon Clone")

#player
playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("ghost.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(20)

#bullet
#ready peluru tidak bisa dilihat di layar
#fire peluru saat ini bergerak
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

score = 0

over_font = pygame.font.Font("freesansbold.ttf", 64)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False
    
#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: "+str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))
    
def game_over_txt():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))
#game loop
running = True
while running:
    #set warna
    screen.fill((0,0,0))
    screen.blit(bg, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #atur kontrol kanan dan kiri
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5
        if event.key == pygame.KSCAN_W:
            if bullet_state == "ready":
                #untuk emndapatkan koordinat x saat ini dari spaceship
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        
    #menahan kapal tetap ditengah dengan nilai 0
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
    playerX += playerX_change
    

    
    #batasan perpindahan pada player dan lawan
    #player       
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    #enemy    
    for i in range(num_enemies):
        
        #game over
        if enemyY[i] >= 410:
            for j in range(num_enemies):
                enemyY[j] = 4100
            game_over_txt()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        
        #collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)
        
    #bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
    