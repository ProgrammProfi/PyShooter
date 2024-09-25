"""
PyShooter *** Made by BlockMaster and Marinad Marinadovich
PyShooter *** Сделано BlockMaster и Маринад Маринадовичом

properties.py required!
properties.py обязателен!
"""

"""Подготовка проекта"""
import pygame
from math import sin, cos, atan2, pi
from random import randint
from properties import *

# Запуск
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyShooter")

# Изображения
player = pygame.image.load("img/player.png").convert_alpha()
player = pygame.transform.scale_by(player, 2)
bullet = pygame.image.load("img/bullet.png").convert_alpha()
bullet = pygame.transform.scale_by(bullet, 2)
bullet = pygame.transform.rotate(bullet, 180)
enemy = pygame.image.load("img/enemy.png").convert_alpha()
enemy = pygame.transform.scale_by(enemy, 2)
wall = pygame.image.load("img/wall.png").convert()
br_wall = pygame.image.load("img/br_wall.png").convert()

# Шрифты
font = pygame.font.Font("fonts/Poppins-Bold.ttf", 10)

# Переменные
bullets = []
enemies = []
walls = []
fl1 = False
dt = clock.tick(FPS) / 1000
pspeed = pspeed * dt
bspeed = bspeed * dt
espeed = espeed * dt


# математические функции
def angle_to(sx, sy, px, py):
    return atan2(py - sy, px - sx)


def rad_to_ang(rad):
    return (180 / pi) * -rad


# Враг
class Enemy:
    def __init__(self, x, y, health, speed, texture):
        self.x = x
        self.y = y
        self.texture = texture
        self.health = health
        self.speed = speed
        self.rect = self.texture.get_rect(topleft=(self.x, self.y))

    # Обновление
    def update(self):
        angle = angle_to(self.x, self.y, playerX, playerY)
        self.x += cos(angle) * self.speed
        self.rect = self.texture.get_rect(topleft=(self.x, self.y))
        for w in walls:
            if self.rect.colliderect(w.rect):
                self.x -= cos(angle) * self.speed
                break
        self.y += sin(angle) * self.speed
        self.rect = self.texture.get_rect(topleft=(self.x, self.y))
        for w in walls:
            if self.rect.colliderect(w.rect):
                self.y -= sin(angle) * self.speed
                break
        self.rect = self.texture.get_rect(topleft=(self.x, self.y))
        screen.blit(self.texture, (self.x, self.y))

    # Попадание
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            enemies.remove(self)


# Создание врага
def spawn_enemy(x, y):
    enemies.append(Enemy(x, y, 3, espeed, enemy))


# Снаряд
class Bullet:
    def __init__(self, x, y, speed, damage, texture, angle):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.angle = angle
        self.texture = texture
        self.ftexture = texture
        self.rect = self.texture.get_rect(topleft=(self.x, self.y))

    # Обновление
    def update(self):
        self.x += cos(self.angle) * self.speed
        self.y += sin(self.angle) * self.speed
        self.rect = self.texture.get_rect(topleft=(self.x, self.y))
        if (not 0 < self.x < WIDTH + 10) or (not 0 < self.y < HEIGHT + 10):
            self.dest()
            return None
        self.ftexture = pygame.transform.rotate(self.texture, rad_to_ang(self.angle))
        screen.blit(self.ftexture, (self.x, self.y))

    # Уничтожение
    def dest(self):
        bullets.remove(self)


# Выстрел!
def shoot():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    bullets.append(Bullet(playerX + 20, playerY + 20, bspeed, 1, bullet, angle_to(playerX + 20, playerY + 20, mouse_x, mouse_y)))


# Стена
class Wall:
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.texture = texture
        self.rect = self.texture.get_rect(topleft=(self.x, self.y))

    # Обновление
    def update(self):
        screen.blit(self.texture, (self.x, self.y))


# Хрупкая стена
class BrWall(Wall):
    def __init__(self, x, y, texture, health):
        super().__init__(x, y, texture)
        self.health = health

    # Удар в стену
    def knock(self, damage):
        self.health -= damage
        if self.health <= 0:
            walls.remove(self)


"""Подготовка к запуску"""

# Таймер врагов
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

# Построение мира
ai = 0
bi = 0
for a in location:
    bi = 0
    for b in a:
        if b == 1:
            walls.append(Wall(bi * 40, ai * 40, wall))
        if b == 2:
            walls.append(BrWall(bi * 40, ai * 40, br_wall, 3))
        bi += 1
    ai += 1

"""Основной цикл"""
running = True
while running:

    # Фон
    screen.fill("grey")

    # Обновление стен
    for w in walls:
        w.update()

    # Коллизия игрока
    player_rect = player.get_rect(topleft=(playerX, playerY))

    # Передвижение
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        playerX += pspeed
        player_rect = player.get_rect(topleft=(playerX, playerY))
        for w in walls:
            if player_rect.colliderect(w.rect):
                playerX -= pspeed
                player_rect = player.get_rect(topleft=(playerX, playerY))
                break
    if keys[pygame.K_a]:
        playerX -= pspeed
        player_rect = player.get_rect(topleft=(playerX, playerY))
        for w in walls:
            if player_rect.colliderect(w.rect):
                playerX += pspeed
                player_rect = player.get_rect(topleft=(playerX, playerY))
                break
    if keys[pygame.K_w]:
        playerY -= pspeed
        player_rect = player.get_rect(topleft=(playerX, playerY))
        for w in walls:
            if player_rect.colliderect(w.rect):
                playerY += pspeed
                player_rect = player.get_rect(topleft=(playerX, playerY))
                break
    if keys[pygame.K_s]:
        playerY += pspeed
        player_rect = player.get_rect(topleft=(playerX, playerY))
        for w in walls:
            if player_rect.colliderect(w.rect):
                playerY -= pspeed
                player_rect = player.get_rect(topleft=(playerX, playerY))
                break

    # Границы мира
    if playerX < 0: playerX = 0
    if playerX > WIDTH - 40: playerX = WIDTH - 40
    if playerY < 0: playerY = 0
    if playerY > HEIGHT - 40: playerY = HEIGHT - 40

    # Клавиша для выстрела
    if pygame.mouse.get_pressed()[0] and not fl1:
        shoot()
        fl1 = True
    if not pygame.mouse.get_pressed()[0]:
        fl1 = False

    # Обновление снарядов
    for bul in bullets:
        bul.update()

    # Обновление врагов
    for en in enemies:
        en.update()

    # Попадание в хрупкую стену
    try:
        for w in walls:
            for bul in bullets:
                if w.rect.colliderect(bul.rect):
                    if isinstance(w, BrWall):
                        w.knock(bul.damage)
                    bul.dest()
    except IndexError:
        pass

    # Попадание во врага
    try:
        for en in enemies:
            for bul in bullets:
                if en.rect.colliderect(bul.rect):
                    en.hit(bul.damage)
                    bul.dest()
    except IndexError:
        pass

    # Отображение игрока
    screen.blit(player, (playerX, playerY))

    # Проигрыш
    for en in enemies:
        if en.rect.colliderect(player_rect):
            running = False
    for bul in bullets:
        if bul.rect.colliderect(player_rect):
            # running = False   Не включать эту строчку!
            pass

    # Отображение FPS
    fps_text = font.render(str(round(clock.get_fps())), True, (176, 30, 30))
    screen.blit(fps_text, (3, 3))

    # Система
    pygame.display.update()

    for ev in pygame.event.get():
        if ev.type == enemy_timer:
            # Спавн врагов
            x = randint(0, WIDTH)
            y = randint(0, HEIGHT)
            if (not abs(x - playerX) < 100) or (not abs(y - playerY) < 100):
                # spawn_enemy(x, y)
                pass
        if ev.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
