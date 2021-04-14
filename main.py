import pygame
import random
import math

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Covid Blaster")
icon = pygame.image.load("medical-mask.png")
pygame.display.set_icon(icon)

# Background Image
background = pygame.image.load("b1.jpg")

# player
playerImg = pygame.image.load("virus.PNG")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("cell.PNG"))
    enemyX.append(random.randint(0, 734))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# bullet
# Ready state means you cant see it
# Fire means the bullet is moving

bulletImg = pygame.image.load("bullet.PNG")
bulletX = 0
bulletY = 480
bulletX_change = 0.4
bulletY_change = 1
bullet_state = "Ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 128)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    score = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(score, (5, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def collision(enemyX, enemyY, bulletX, bulletY):
    x2 = enemyX
    x1 = bulletX
    y2 = enemyY
    y1 = bulletY
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance <= 50:
        return True
    else:
        return False


# This is what runs the game
running = True
while running:
    # This is the back ground color
    screen.fill((98, 240, 255))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Lets the game quit
            running = False

        if event.type == pygame.KEYDOWN:  # Means any key was pressed
            if event.key == pygame.K_LEFT:  # Checks for left arrow press
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:  # Checks for right arrow press
                playerX_change = 0.6
            if event.key == pygame.K_SPACE:  # Checks for right space bar press
                if bullet_state == "Ready":
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # Means any key was pressed
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # This created boundary for player
    if playerX < 0:
        playerX = 0
    elif playerX > width - 64:
        playerX = width - 64

    # This created boundary for enemy
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = .5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > width - 64:
            enemyX_change[i] = -.5
            enemyY[i] += enemyY_change[i]

        # Collision Check
        collision_status = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision_status:
            bullet_state = "Ready"
            bulletX = 0
            bulletY = 480
            enemyX[i] = random.randint(34, 734)
            enemyY[i] = random.randint(50, 100)
            score_value += 10

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movment
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"
    if bullet_state == "Fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
