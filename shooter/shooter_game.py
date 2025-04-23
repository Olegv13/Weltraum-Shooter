#Создай собственный Шутер!

from pygame import *
from random import randint
mixer.init()
mixer.music.load('TF.mp3')
mixer.music.play()
fire_sound = mixer.Sound('nd.mp3 ')

win_width = 700
win_height = 500
lost = 0
background = transform.scale(image.load('bh.webp'),(win_width,win_height))
font.init()
font1 = font.Font('Arial', 80)
clock = time.Clock()
lost = 0
life = 3
FPS = 60   
score = 0
goal = 20
num_fire = 0
rel_time = 0
max_lost = 10
img_enemy = 'ufo.png'
img_hero = 'rocket.png'
img_bullet = 'bullet.png'
img_back = 'galaxy.jpg'
img_asteroid = 'asteroid.png'
win = font1.render('Красава!', True, (255, 255,255))
lose = font1.render('ПЕРЕДЕЛЫВАЙ!', True, (180, 0 ,0))
font2 = font.Font('Arial', 36)
timer = 1 
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
    


class Player(GameSprite):
    


    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
        
    
class Enemy(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1                
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
window = display.set_mode((win_width,win_height))
display.set_caption('KabYrintS')     
ship = Player('rocket.png',5, win_height - 80, 10, 0, 430)
asteroid = Enemy('asteroid.png',5, win_height - 70, 10 , 0 , 430)
#monster = Enemy('ufo.png', win_width - 80, 280, 2)
text_lose = font1.render('Пропущено:' + str(lost), 1, (255,255, 255))
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group() 
    
asteroids = sprite.Group()
for i in range(1, 6):
    asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)



finish = False
run = True
while run:



    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                num_fire = num_fire + 1
                fire_sound.play()
                ship.fire()



    if not finish:
        window.blit(background,(0,0))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            asteroid= Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True) 
            life = life -1
        if life < 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))
    
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        text = font2.render('Счёт:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 30))
        text_lose = font2.render('Пропущено' + str(lost), 1,(255,255,255))
        
        window.blit(text_lose,(10, 50))
        display.update()
        clock.tick(FPS)
        