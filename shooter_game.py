
from pygame import *
from random import randint
from time import time as timer 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

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
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
health = 0
lost = 0
score = 0 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1 

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

font.init()
font1 = font.SysFont('Arial', 40)    
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
player = Player('rocket.png', 300, win_height - 80, 80, 100, 10)

asteroids = sprite.Group()
bullets = sprite.Group()
aliens = sprite.Group() 
for i in range(1, 6):
    alien=Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
    aliens.add(alien)
    
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

run = True
finish = False
rel_time = False
num_bullets = 0
clock = time.Clock()

for i in range(1, 3):
        asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
        asteroids.add(asteroid)

while run:
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN: 
            if e.key == K_SPACE:
                if num_bullets <= 5 and rel_time == False:
                    num_bullets += 1
                    fire_sound.play()
                    player.fire()
                if num_bullets >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    
    if not finish:
        window.blit(background, (0, 0)) 
        player.update()
        aliens.update()
        bullets.update()
        asteroids.update()
        player.reset()   
        aliens.draw(window) 
        asteroids.draw(window)
        bullets.draw(window)


        if rel_time == True:
            now_time = timer()
            if now_time - last_time <3:
                reload = font2.render('Перезарядка...',1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_bullets = 0
                rel_time = False

        collisions = sprite.groupcollide(aliens, bullets, True, True)
        for c in collisions:
            score += 1 
            alien = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) 
            aliens.add(alien) 

        
        if sprite.spritecollide(player, aliens, False) or lost >= 3:
            finish = True
            lose = font1.render('ПРОИГРЫШ!', True, (200, 0, 0))
            window.blit(lose, (200, 200))

        if score >= 40:
            finish = True
            win = font1.render('ПОБЕДА!', True, (0, 200, 0))
            window.blit(win, (200, 200))

        text_lose = font1.render('Пропущено:'+ str(lost), 1, (255, 255, 255) )
        text_score = font1.render('Счет:'+ str(score), 1, (255, 255, 255) )
        window.blit(text_score, (10,20))

    display.update()
    clock.tick(FPS) 
