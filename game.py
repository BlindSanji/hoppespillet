import pygame as pg
import random
from pygame.locals import *
from config import SCREEN_WIDTH, SCREEN_HEIGHT

pg.init()
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()


class Player:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.8

    def __init__(self):
        self.player_jump = False
        self.jump_vel = self.JUMP_VEL
        self.posX = self.X_POS
        self.posY = self.Y_POS

    def update(self, userInput):
        if self.player_jump:
            self.jump()

        if userInput[K_w] and not self.player_jump:
            self.player_jump = True

    def jump(self):
        if self.player_jump:
            self.posY -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.player_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):
        pg.draw.rect(screen, (0, 0, 255), (self.posX, self.posY, 50, 50))


class Obstacle:
    def __init__(self, height):
        self.height = height
        self.posX = SCREEN_WIDTH
        self.posY = SCREEN_HEIGHT - self.height - 238
        self.width = 50

    def update(self):
        self.posX -= game_speed
        if self.posX < -self.width:
            obstacles.pop()

    def draw(self, screen):
        pg.draw.rect(screen, (255, 0, 0), (self.posX, self.posY, self.width, self.height))


def main():
    global game_speed, points, obstacles
    run = True
    player = Player()
    game_speed = 14
    points = 0
    font = pg.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render(f"Points: {points}", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def create_obstacle():
        height = random.randint(35, 150)
        obstacles.append(Obstacle(height))

    while run:
        for event in pg.event.get():
            if event.type == QUIT:
                run = False
                pg.quit()
                return

        SCREEN.fill((255, 255, 255))
        userInput = pg.key.get_pressed()

        pg.draw.line(SCREEN, (0, 255, 0), (0, 350), (SCREEN_WIDTH, 350), 5)

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            create_obstacle()

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.posX + 32 > obstacle.posX and player.posX < obstacle.posX + obstacle.width:
                if player.posY + 50 > obstacle.posY:
                    pg.time.delay(2000)
                    death_count += 1
                    menu(death_count)

        score()
        pg.display.update()
        clock.tick(30)


def menu(death_count):
    global points
    run = True
    while run:
        for event in pg.event.get():
            if event.type == QUIT:
                run = False
                pg.quit()
                return
            if event.type == KEYDOWN:
                if death_count > 0:
                    points = 0
                main()

        SCREEN.fill((255, 255, 255))
        font = pg.font.Font('freesansbold.ttf', 30)

        text = font.render("Press any key to Start", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)

        if death_count > 0:
            score_text = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score_text.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score_text, scoreRect)

        pg.display.update()


menu(death_count=0)
