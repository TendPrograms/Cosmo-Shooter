from pygame import *
from random import randint
from time import time as timer

font.init()
mixer.init()
font1 = font.SysFont('Arial', 20)
font2 = font.SysFont('Arial', 50)
mixer.music.load('space.ogg')
fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(player_image), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

reload = font1.render('Wait, reload.....', True, (255, 30, 30))
num_fire = 0
rel_time = False
bullets = sprite.Group()
asteroids = sprite.Group()
lost = 0
window = display.set_mode((700,500))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 300:
            self.speed = 3
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 610)
            self.speed = randint(1,2)
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 610)
            self.speed = randint(1,2)

class Player(GameSprite):
    def gamepad(self):
        key_pressed = key.get_pressed()
        up, down, left, right = False, False, False, False
        if key_pressed[K_LEFT]:
            left = True
        if key_pressed[K_RIGHT]:
            right = True
        if key_pressed[K_UP]:
            up = True
        if key_pressed[K_DOWN]:
            down = True
        if left and self.rect.x > 5:
            self.rect.x -= self.speed
        if right and self.rect.x < 610:
            self.rect.x += self.speed
        if up and self.rect.y > 5:
            self.rect.y -= self.speed
        if down and self.rect.y < 400:
            self.rect.y += self.speed
    def fire(self):
        fire.play()
        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 5, 15, 20)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

display.set_caption('Космос 2D')
player = Player('rocket.png', 10, 400, 6, 80, 100)
ufos = sprite.Group()
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
time = time.Clock()
game = True
finish = False
points = 0
life = 3
win = font2.render('YOU WIN!', True, (30, 255, 30))
lose = font2.render('YOU LOSE!', True, (255, 30, 30))
def run():
    global life
    global points
    global lost
    global num_fire
    global rel_time
    points = 0
    lost = 0
    life = 3
    rel_time = False
    num_fire = 0
    for i in ufos:
        i.kill()
    for i in asteroids:
        i.kill()
    begin()

def begin():
    global game
    global points
    global life
    global finish
    global num_fire
    global rel_time
    mixer.music.play()
    finish = False
    player.rect.x = 10
    player.rect.y = 400
    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if not rel_time:
                        player.fire()
                        last_timer = timer()
                        rel_time = True
        window.blit(background, (0,0))
        player.reset()
        player.gamepad()
        bullets.draw(window)
        bullets.update()
        if finish == False:
            if rel_time:
                now_timer = timer()
                if now_timer - last_timer < 0.2:
                    window.blit(reload, (280,460))
                else:
                    rel_time = False
            if life == 3:
                color = (30, 255, 30)
            if life == 2:
                color = (200, 170, 50)
            if life == 1:
                color = (255, 30, 30)
            life_score = font2.render('HP: ' + str(life), True, color)
            window.blit(life_score, (570, 10))
            score = font1.render('Счёт: ' + str(points), True, (255, 255, 255))
            losing_score = font1.render('Пропущенно: ' + str(lost), True, (255, 255, 255))
            window.blit(losing_score, (5, 40))
            window.blit(score, (5, 10))
            ufo_asteroid = sprite.groupcollide(ufos, asteroids, True, False)
            sprite_group = sprite.groupcollide(bullets, ufos, True, True)
            asteroid_bullet = sprite.groupcollide(bullets, asteroids, True, False)
            sprite_object = sprite.spritecollide(player, ufos, True)
            asteroid_player = sprite.spritecollide(player, asteroids, True)
            ufos.draw(window)
            ufos.update()
            asteroids.draw(window)
            asteroids.update()
            for c in sprite_group:
                if sprite_group:
                    points += 1
                    if life < 3:
                        chanse = randint(1,100)
                        if chanse > 89:
                            life += 1
            if sprite_object or asteroid_player:
                life -= 1
            if life == 0 or lost == 5:
                for i in bullets:
                    i.kill()
                mixer.music.stop()
                text = lose
                finish = True
                if points > 29:
                    mixer.music.stop()
                    text = win
            if len(asteroids) < 3:
                asteroid = Asteroid('asteroid.png', randint(5, 610), 0, randint(1,2), 60, 60)
                asteroids.add(asteroid)
            if len(ufos) < 5:
                enemy = Enemy('ufo.png', randint(5, 610), 0, randint(1,2), 100, 60)
                ufos.add(enemy)
        if finish:
            if rel_time:
                now_timer = timer()
                if now_timer - last_timer < 0.2:
                    window.blit(reload, (280,460))
                else:
                    rel_time = False
            window.blit(text, (240,150))
            restart = font1.render('Ты хочешь начать заново?',True,(230,230,230))
            restart2 = font1.render('Если хочешь, то убей его!',True,(200,50,50))
            window.blit(restart, (240, 210))
            window.blit(restart2, (250, 240))
            rest = Enemy('ufo.png', 300, 270, 0, 100, 60)
            rest.reset()
            bullet_ufo = sprite.spritecollide(rest, bullets, True)
            if bullet_ufo:
                run()
        display.update()
        time.tick(60)

begin()