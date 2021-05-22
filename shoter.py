#Создай собственный Шутер!
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, fileName, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(fileName), (size_x, size_y))
        self.size_x = size_x
        self.size_y = size_y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, fileName, x, y, size_x, size_y, speed):
        super().__init__(fileName, x, y, size_x, size_y, speed)
        self.recharge = 0
    
    def update(self):
        if self.recharge != 0:
            self.recharge -= 1

        keys_pressed = key.get_pressed()
        if (keys_pressed[K_RIGHT] or keys_pressed[K_d]) and self.rect.x < win_width-self.speed-self.size_x:
            self.rect.x += self.speed
        if (keys_pressed[K_LEFT] or keys_pressed[K_a]) and self.rect.x > self.speed:
            self.rect.x -= self.speed
        if keys_pressed[K_SPACE] or keys_pressed[K_UP] or keys_pressed[K_w]:
            self.fire()

    def fire(self):
        if self.recharge == 0:
            self.recharge = 35
            bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 10)
            bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, fileName, x, y, size_x, size_y, speed):
        super().__init__(fileName, x, y, size_x, size_y, speed)
        
    def update(self):
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(0, 350)

            global lost
            lost += 1
        else:
            self.rect.y += self.speed

# class Living_SpaceShip(GameSprite):
#     def __init__(self, fileName, x, y, size_x, size_y, speed):
#         super().__init__(fileName, x, y, size_x, size_y, speed)
        
#     def update(self):
#         pass

class Bullet(GameSprite):
    def __init__(self, fileName, x, y, size_x, size_y, speed):
        super().__init__(fileName, x, y, size_x, size_y, speed)
        
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -50:
            self.kill()
    
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#создай окно игры
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')

#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

player = Player("rocket.png", 250, 350, 100, 150, 5)

enemys = sprite.Group()
for i in range(6):
    enemy = Enemy("ufo.png", randint(0, 350), -50, 150, 50, randint(2, 3))
    enemys.add(enemy)
bullets = sprite.Group()

score = 0
lost = 0

font.init()

font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)

you_win = font2.render("Ты победил!", 1, (255, 255, 0))
you_lose = font2.render("Ты проиграл(", 1, (255, 0, 0))

#игровой цикл
clock = time.Clock()
FPS = 60
game = True
finish = False
while game:
    #обработай событие «клик по кнопке "Закрыть окно"»
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (0, 30))

        text_score = font1.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text_score, (0, 0))


        enemys.update()
        enemys.draw(window)

        bullets.update()
        bullets.draw(window)

        colides = sprite.groupcollide(enemys, bullets, True, True)
        for e in colides:
            score += 1
            enemy = Enemy("ufo.png", randint(0, 350), -50, 150, 50, randint(2, 3))
            enemys.add(enemy)
        
        if lost >= 3:
            window.blit(you_lose, (200, 200))
            finish = True

        if score >= 10:
            window.blit(you_win, (200, 200))
            finish = True
    
    display.update()
    clock.tick(FPS)