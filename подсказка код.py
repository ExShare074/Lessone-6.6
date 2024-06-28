#Пишем код игры арканоида для 2х игроков, отдельно для каждого игрока свой счетчик очков

import pygame
import random

pygame.init()

# Определение размеров экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Arkanoid")


black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)


font = pygame.font.Font(None, 36)

# Классы игры
class Paddle:
    def __init__(self, x, y, width, height, color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

    def move(self, x):
        self.x = x - self.width // 2
        if self.x < 0:
            self.x = 0
        if self.x > screen_width - self.width:
            self.x = screen_width - self.width

    def move_with_keys(self, keys, left_key, right_key):
        if keys[left_key]:
            self.x -= 10
        if keys[right_key]:
            self.x += 10
        if self.x < 0:
            self.x = 0
        if self.x > screen_width - self.width:
            self.x = screen_width - self.width

class Ball:
    def __init__(self):
        self.radius = 10
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.dx = 5
        self.dy = -5

    def draw(self):
        pygame.draw.circle(screen, blue, [self.x, self.y], self.radius)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x >= screen_width:
            self.dx = -self.dx

        if self.y <= 0 or self.y >= screen_height:
            self.dy = -self.dy

class Brick:
    def __init__(self, x, y):
        self.width = 75
        self.height = 20
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, white, [self.x, self.y, self.width, self.height])

# Функция для ввода имени игрока
def get_player_name(player_number):
    running = True
    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 32, 200, 64)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    font = pygame.font.Font(None, 48)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(black)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        prompt_surface = font.render(f"Введите имя {player_number}:", True, white)
        screen.blit(prompt_surface, (screen_width // 2 - prompt_surface.get_width() // 2, screen_height // 2 - 100))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    return text

# Основной игровой цикл
def game_loop(player1_name, player2_name):
    paddle1 = Paddle((screen_width - 100) // 2, screen_height - 20, 100, 10, white)
    paddle2 = Paddle((screen_width - 100) // 2, 10, 100, 10, red)
    ball = Ball()
    bricks = []

    for i in range(7):
        for j in range(5):
            bricks.append(Brick(5 + i * 110, 50 + j * 40))

    player1_score = 0
    player2_score = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        mouse_x, _ = pygame.mouse.get_pos()
        paddle1.move(mouse_x)
        paddle2.move_with_keys(keys, pygame.K_a, pygame.K_d)

        ball.move()

        # Проверка столкновения мяча с ракетками
        if (paddle1.y < ball.y + ball.radius < paddle1.y + paddle1.height and
                paddle1.x < ball.x < paddle1.x + paddle1.width):
            ball.dy = -ball.dy
        if (paddle2.y < ball.y - ball.radius < paddle2.y + paddle2.height and
                paddle2.x < ball.x < paddle2.x + paddle2.width):
            ball.dy = -ball.dy

        # Проверка столкновения мяча с кирпичами
        for brick in bricks[:]:
            if (brick.y < ball.y - ball.radius < brick.y + brick.height and
                    brick.x < ball.x < brick.x + brick.width):
                ball.dy = -ball.dy
                bricks.remove(brick)
                if ball.dy > 0:  # Удар снизу - очки получает игрок 1
                    player1_score += 1
                else:  # Удар сверху - очки получает игрок 2
                    player2_score += 1

        if ball.y > screen_height or ball.y < 0:
            running = False

        screen.fill(black)
        paddle1.draw()
        paddle2.draw()
        ball.draw()

        for brick in bricks:
            brick.draw()

        # Отображение счета
        score_text1 = font.render(f"{player1_name}: {player1_score}", True, white)
        score_text2 = font.render(f"{player2_name}: {player2_score}", True, white)
        screen.blit(score_text1, (10, screen_height - 40))
        screen.blit(score_text2, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


player1_name = get_player_name(1)
player2_name = get_player_name(2)

game_loop(player1_name, player2_name)
