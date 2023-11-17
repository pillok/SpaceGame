import random
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 800))

mixer.init()
mixer.music.load("background_song.mp3")
mixer.music.set_volume(0.3)
mixer.music.play()

clock = pygame.time.Clock()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

GAMEOVER = False

score = 0
current_round = 1

pygame.display.set_caption('aarya\'s game')
icon = pygame.image.load('rando.png')
pygame.display.set_icon(icon)

bullet = pygame.image.load('bullet.png')
bullet = pygame.transform.scale(bullet, (10, 20))
bullets = []
bulletY_change = -2

backgroundimg = pygame.image.load('space.jpg')
backgroundimg = pygame.transform.scale(backgroundimg, (800, 800))

enemyImg = pygame.image.load('ghost.png')
enemyImg = pygame.transform.scale(enemyImg, (75, 75))
enemyX = []
enemyY = []

xSpeedLower = 2
xSpeedHigher = 4

enemyX_change = []
enemyY_change = 40


playerimg = pygame.image.load('space-invaders.png')
playerimg = pygame.transform.scale(playerimg, (75, 75))
playerX = 400 - (75 / 2)
playerY = 650
playerX_change = 0
playerY_change = 0


def increaseRound():
    global current_round
    global GAMEOVER
    if current_round == 10:
        GAMEOVER = True
    current_round += 1
    genEnemies()


def genEnemies():
    global enemyX
    global enemyY
    global enemyX_change
    enemyX = []
    enemyY = []
    enemyX_change = []
    for h in range(10):
        enemyX.append(random.randint(0, 725))
        enemyY.append(random.randint(100, 450))
        enemyX_change.append(random.randint(xSpeedLower + current_round, xSpeedHigher + current_round) / 10)


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def background():
    screen.blit(backgroundimg, (0, 0))


def drawBullet(x, y):
    screen.blit(bullet, (x, y))


def collision(x1, y1, x2, y2):
    if x2 <= x1 <= x2 + 75 and y2 <= y1 <= y2 + 75:
        return True
    return False


genEnemies()

running = True
while running:

    background()

    if GAMEOVER:
        screen.fill((255, 255, 255))
        text = my_font.render('Game Over, Your Score Was: {}'.format(score), False, (0, 0, 0))
        screen.blit(text, (185, 400))
        pygame.display.update()
    else:
        scoreText = my_font.render('Score: {}'.format(score), False, (0, 0, 0))
        roundText = my_font.render('Round: {}'.format(current_round), False, (0, 0, 0))
        screen.blit(scoreText, (50, 100))
        screen.blit(roundText, (50, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.6
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.6
                if event.key == pygame.K_DOWN:
                    playerY_change = 0.4
                if event.key == pygame.K_UP:
                    playerY_change = -0.4
                if event.key == pygame.K_SPACE:
                    if len(bullets) < 1:
                        bullets.append({'bulletX': playerX, 'bulletY': playerY + 10})
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        playerX += playerX_change
        playerY += playerY_change
        for l in range(len(enemyX)):
            enemyX[l] += enemyX_change[l]

        if playerX <= 0:
            playerX = 0
        elif playerX >= 725:
            playerX = 725

        if playerY <= 600:
            playerY = 600
        elif playerY >= 725:
            playerY = 725

        for i in range(len(bullets)):
            drawBullet(bullets[i]['bulletX'] + (75 / 2) - 5, bullets[i]['bulletY'])
            bullets[i]['bulletY'] += bulletY_change
            newEnemiesX = []
            newEnemiesY = []
            newEnemiesChangeX = []
            for j in range(len(enemyX)):
                if collision(bullets[i]['bulletX'], bullets[i]['bulletY'], enemyX[j], enemyY[j]):
                    score += 1
                    pass
                else:
                    newEnemiesX.append(enemyX[j])
                    newEnemiesY.append(enemyY[j])
                    newEnemiesChangeX.append(enemyX_change[j])
            enemyX = newEnemiesX
            enemyY = newEnemiesY
            enemyX_change = newEnemiesChangeX

        newArr = []
        for j in range(len(bullets)):
            if not bullets[j]['bulletY'] <= 0:
                newArr.append(bullets[j])

        bullets = newArr

        for i in range(len(enemyX)):
            if enemyX[i] <= 0 or enemyX[i] > 725:
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change

        player(playerX, playerY)

        enemiesNewX = []
        enemiesNewY = []
        enemiesNewXChange = []
        for n in range(len(enemyX)):
            if enemyY[n] > 500:
                pass
            else:
                enemiesNewX.append(enemyX[n])
                enemiesNewXChange.append(enemyX_change[n])
                enemiesNewY.append(enemyY[n])

        enemyX = enemiesNewX
        enemyY = enemiesNewY
        enemyX_change = enemiesNewXChange

        if len(enemyX) < 1:
            increaseRound()
        else:
            for k in range(len(enemyX)):
                enemy(enemyX[k], enemyY[k])
        pygame.display.update()
    clock.tick(400)
