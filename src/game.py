import pygame
from pygame import *
import controller
import time
import math
import random

# Constants
CAMERA = 0
DISPLAY = False
QUIT = 1
SCREEN_SIZE = (800, 600)
PATH = 'C:\\Users\\samen\\cs320-spring2023-gesture-controller\\src\\'

CONTROL_BOX_X = 300
CONTROL_BOX_WIDTH = 200

# Bullet Constants
BULLET_SPEED = 10
UP = -1
DOWN = 1

# Player Constants
PLAYER_STARTX = 370
PLAYER_STARTY = 460

# Enemy Constants
ENEMY_MIN = 1
ENEMY_MAX = 10
ENEMY_SPAWN_RATE = 2
ENEMY_SPAWNX = 0
ENEMY_SPAWNY = 90
ENEMY_SPEEDX = 5
ENEMY_SPEEDY = 40
ENEMY_GOAL_LINE = PLAYER_STARTY - 50

PLAYER_SPEED = 10
PLAYER_COOLDOWN = 1

# Text Constants
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

SCOREX = 700
SCOREY = 50

FONT = 'freesansbold.ttf'
FONT_SIZE = 32
SCORE = "Score: "

# Window Constants
IMAGEX = 100
IMAGEY = 50
# Initialize
pygame.init()
pygame.display.set_caption("Canadian Invasion")
icon = pygame.image.load(PATH + 'target.png')
pygame.display.set_icon(icon)
controller = controller.controller(CAMERA, DISPLAY, SCREEN_SIZE)
quit = False

WELCOME_MESSAGE = "Canadian Invasion!!!"
CENTERX = 370
CENTERY = 350

# Create Window
screen = pygame.display.set_mode(SCREEN_SIZE)

# Load Images
background = pygame.image.load(PATH + 'background.png')
playerIMG = pygame.image.load(PATH + 'player_tank.png')
bulletIMG = pygame.image.load(PATH + "bullet.png")
enemyBulletIMG = pygame.image.load(PATH + "enemyBullet.png")
enemyIMG = pygame.image.load(PATH + 'enemy_tank.png')

# Load Text


def renderScore(text, scoreX, scoreY, background, foreground):
    font = pygame.font.Font(FONT, FONT_SIZE)
    score_text = font.render(text, True, foreground, background)
    score_rect = score_text.get_rect()

    score_rect.center = (scoreX, scoreY)

    text = score_text, score_rect

    return text


def getX(location):
    return location[0][0]


def getTime():
    return time.perf_counter()


def elapsed_time(initial):
    return time.perf_counter() - initial


def convert_image(image):
    frame = pygame.image.frombuffer(
        image.tostring(), image.shape[1::-1], "BGR")

    scaled_frame = pygame.transform.scale(frame, (10, 10))

    return scaled_frame

# Player


class Bullet:
    def __init__(self, id, x, y, image, speed):
        self.id = id
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.offScreen = True

    def getID(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getImage(self):
        return self.image

    def moveUp(self):
        if (self.y > 0):
            self.y -= self.speed
        else:
            self.offScreen = True
            self.y = SCREEN_SIZE[1] + 50

    def moveDown(self):
        if (self.y < SCREEN_SIZE[1]):
            self.y += self.speed
        else:
            self.offScreen = True
            self.y = SCREEN_SIZE[1] + 50

    def check_collision(self, targets):
        for i in range(0, targets.__len__()):
            target = targets[i]
            distance = math.sqrt(
                (math.pow((target.getX() - self.x), 2)) +
                (math.pow((target.getY() - self.y), 2)))
            if distance < 27:
                return i
        return -1


class bulletManager:
    def __init__(self, coolDown, bulletIMG):
        self.lastShot = getTime()
        self.bullets = []
        self.bulletCount = 0
        self.coolDown = coolDown
        self.bulletIMG = bulletIMG

    def getBulletList(self):
        return self.bulletList

    def createBullet(self, x, y):
        bullet = Bullet(self.bulletCount,
                        x + 16, y - 30, self.bulletIMG, BULLET_SPEED)

        self.bulletCount += 1
        self.bullets.append(bullet)

        return bullet

    def removeBullet(self):
        self.bullets.pop(0)
        self.bulletCount -= 1

    def shoot(self, x, y):
        if (elapsed_time(self.lastShot) >= self.coolDown):
            bullet = self.createBullet(x, y)
            bullet.offScreen = False
            self.lastShot = getTime()


class Player:
    def __init__(self, startX, startY, playerIMG, speed):
        self.x = startX
        self.y = startY
        self.dx = 0
        self.dy = 0
        self.playerIMG = playerIMG
        self.speed = speed
        self.coolDown = PLAYER_COOLDOWN
        self.score = 0

        self.bulletManager = bulletManager(self.coolDown, bulletIMG)

        self.bullets = self.bulletManager.bullets

    # Getters
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getImage(self):
        return self.playerIMG

    def getSpeed(self):
        return self.speed

    def getBullets(self):
        return self.bulletManager.bullets

    # Setters

    def updateBullets(self):
        self.bullets = self.bulletManager.bullets

    def move(self, x):
        if (x > 0 and x < (SCREEN_SIZE[0] - 50)):
            self.x = x

    def calculate_move(self, x):
        self.dx = self.x + (x * self.speed)

    def handleMove(self, x):
        self.calculate_move(x)
        self.move(self.dx)

    def shoot(self):
        self.bulletManager.shoot(self.x, self.y)
        self.updateBullets()

# Enemy


class Enemy:
    def __init__(self, startY, enemyIMG, speedX, speedY):
        self.x = 0
        self.y = startY
        self.direction = 1
        self.dx = 0
        self.dy = 0
        self.image = enemyIMG
        self.speedX = speedX
        self.speedY = speedY
        self.bulletManager = bulletManager(
            random.randint(ENEMY_MIN, ENEMY_MAX), enemyBulletIMG)
        self.bullets = self.bulletManager.bullets

    def updateBullets(self):
        self.bullets = self.bulletManager.bullets

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getImage(self):
        return self.image

    def calculate_move(self):
        if (self.direction > 0):
            if ((self.x + self.speedX) < SCREEN_SIZE[0] - 32):
                self.dx = self.x + self.speedX
                self.dy = self.y
            else:
                self.dy = self.y + self.speedY
                self.direction *= -1
        else:
            if ((self.x - self.speedX) > 0 + 32):
                self.dx = self.x - self.speedX
                self.dy = self.y
            else:
                self.dy = self.y + self.speedY
                self.direction *= -1

    def move(self):
        self.calculate_move()
        self.x = self.dx
        self.y = self.dy

    def shoot(self):
        self.bulletManager.shoot(self.x, self.y)
        self.updateBullets()

    def check_victory(self):
        return self.y >= ENEMY_GOAL_LINE


class enemy_spawner:
    def __init__(self, spawnRate, spawnX, spawnY, enemyIMG, enemySpeedX, enemySpeedY):
        self.spawnRate = spawnRate
        self.spawnX = spawnX
        self.spawnY = spawnY
        self.enemyIMG = enemyIMG
        self.enemySpeedX = enemySpeedX
        self.enemySpeedY = enemySpeedY
        self.lastSpawn = getTime()

    def spawnEnemy(self):
        enemies.append(Enemy(self.spawnY, self.enemyIMG,
                       self.enemySpeedX, self.enemySpeedY))

    def spawn(self):
        if (elapsed_time(self.lastSpawn) >= self.spawnRate):
            self.spawnEnemy()
            self.lastSpawn = getTime()


startGame = False
currentCount = 3
# Welcome Screen

while startGame == False:
    screen.blit(background, (0, 0))

    welcome, welcome_rect = renderScore(
        WELCOME_MESSAGE, CENTERX, CENTERY, BLACK, WHITE)
    screen.blit(welcome, welcome_rect)

    prepare, prepare_rect = renderScore(
        "Prepare for Assault in : " + str(currentCount), CENTERX, CENTERY + 80, BLACK, WHITE)
    screen.blit(prepare, prepare_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                break

    location, gesture, count = controller.process()

    # screen.blit(background, (0, 0))
    # frame = convert_image(image)

    # screen.blit(frame, (IMAGEX, IMAGEY))
    if (location != "None"):
        if (currentCount == 0):
            break
        elif (count == currentCount):
            currentCount -= 1
    pygame.display.update()
# Initialize Lists


player = Player(PLAYER_STARTX, PLAYER_STARTY,
                playerIMG, PLAYER_SPEED)
spawner = enemy_spawner(ENEMY_SPAWN_RATE, ENEMY_SPAWNX,
                        ENEMY_SPAWNY, enemyIMG, ENEMY_SPEEDX, ENEMY_SPEEDY)

players = [player]
enemies = []
objects = [player]


def check_move_direction(location):
    location = getX(location)
    if (location < CONTROL_BOX_X):
        direction = -1
    elif (location > (CONTROL_BOX_X + CONTROL_BOX_WIDTH)):
        direction = 1
    else:
        direction = 0
    return direction


def display(objects):
    screen.blit(background, (0, 0))
    # frame = convert_image(image)

    # screen.blit(frame, (IMAGEX, IMAGEY))
    score, score_rect = renderScore(
        SCORE + str(player.score), SCOREX, SCOREY, BLACK, WHITE)
    screen.blit(score, score_rect)
    for list in objects:
        for object in list:
            screen.blit(object.getImage(), (object.getX(), object.getY()))


def updateBullets(bulletManager, targets, direction):
    for bullet in bulletManager.bullets:
        if (bullet.offScreen == False):
            collision = bullet.check_collision(targets)

            if (direction == UP):
                bullet.moveUp()
                if (collision != -1):
                    enemies.pop(collision)
                    player.score += 1
            else:
                bullet.moveDown()
                if (collision != -1):
                    players.pop(collision)
        else:
            bulletManager.removeBullet()


def handle_input(location, gesture):
    if (location != "None"):
        player.handleMove(check_move_direction(location))
        if (gesture == 0):
            player.shoot()
    updateBullets(player.bulletManager, enemies, UP)
    for enemy in enemies:
        updateBullets(enemy.bulletManager, players, DOWN)
    for enemy in enemies:
        enemy.move()
        enemy.shoot()


def move_enemies():
    spawner.spawn()


def check_defeat():
    if (players.__len__() <= 0):
        return True
    for enemy in enemies:
        if (enemy.check_victory()):
            return True
    return False


# Mainloop for Game
while quit == False:

    bullets = []
    for player in players:
        for bullet in player.bullets:
            bullets.append(bullet)
    for enemy in enemies:
        for bullet in enemy.bullets:
            bullets.append(bullet)

    objects = [players, enemies, bullets]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit()

    location, gesture, count = controller.process()

    # Handle player input
    handle_input(location, gesture)
    move_enemies()

    quit = check_defeat()

    display(objects)
    pygame.display.update()

print(player.score)


def quit():
    quit = True

# Exit Screen


quit = False
while quit == False:
    failed, failed_rect = renderScore(
        "You Failed!!", CENTERX, CENTERY, BLACK, RED)

    screen.blit(failed, failed_rect)

    finalScore, finalScore_Rect = renderScore(
        "Your final score was: " + str(player.score), CENTERX, CENTERY + 80, BLACK, RED)

    screen.blit(finalScore, finalScore_Rect)

    location, gesture, count = controller.process()
    if location != "None":
        if gesture == 3:
            quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit()

    pygame.display.update()
