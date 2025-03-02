#Create your own shooter

from typing import Any
from pygame import *
from random import *
from time import time as timer

class Gamesprite(sprite.Sprite):
    def __init__(self,spr_img,rect_x,rect_y,size_x,size_y,speed):
        super().__init__()
        self.image = transform.scale(image.load(spr_img),(size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.speed = speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(Gamesprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        elif key_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("/Users/macbook/Desktop/source/Shooterasset/bullet.png",self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)
loss = 0
score = 0
class Enemy(Gamesprite):
    def update(self):
        global loss
        self.rect.y += self.speed
        if self.rect.y > win_height:
            loss += 1
            self.rect.y = 0
            self.rect.x = randint(80,win_width-80)

class Asteroid(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80,win_width-80)

class Bullet(Gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("shooter")
background = transform.scale(image.load("/Users/macbook/Desktop/source/Shooterasset/galaxy.jpg"),(win_width,win_height))
fps = 60
clock = time.Clock()
run = True
finnish = False
mixer.init()
mixer.music.load("/Users/macbook/Desktop/source/Shooterasset/space.ogg")
mixer.music.play()
mixer.music.set_volume(0.05)
fire = mixer.Sound("/Users/macbook/Desktop/source/Shooterasset/fire.ogg")

font.init()
font2 = font.Font(None,36)

player = Player("/Users/macbook/Desktop/source/Shooterasset/rocket.png",5,win_height-100,80,100,10)
enemies = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

for i in range(5):
    enemy = Enemy("/Users/macbook/Desktop/source/Shooterasset/ufo.png",randint(80,win_width-80),-40,80,50,randint(1,5))
    enemies.add(enemy)

for i in range(3):
    asteroid = Asteroid("/Users/macbook/Desktop/source/Shooterasset/asteroid.png",randint(80,win_width-80),-40,50,50,randint(3,5))
    asteroids.add(asteroid)

life = 3
num_fire = 0
reload = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if reload == False:
                    if num_fire < 10:
                        fire.play()
                        player.fire()
                        num_fire += 1
                        print(num_fire)
                        print(reload)
                    elif num_fire >= 10 :
                        last_time = timer()
                        reload = True

    if finnish != True:
        window.blit(background,(0,0))
        score_counter = font2.render("score: "+str(score),1,(255,255,255))
        missed_counter = font2.render("missed: "+str(loss),1,(255,255,255))
        if life == 3:
            life_counter = font2.render("life: "+str(life),1,(0, 199, 40))
        elif life == 2:
            life_counter = font2.render("life: "+str(life),1,(255, 213, 0))
        else:
            life_counter = font2.render("life: "+str(life),1,(255, 0, 0))   

        window.blit(score_counter,(5,5))
        window.blit(missed_counter,(5,30))
        window.blit(life_counter,(5,60))
        player.update()
        player.reset()
        bullets.draw(window)
        bullets.update()
        enemies.draw(window)
        enemies.update()
        asteroids.draw(window)
        asteroids.update()
        if reload == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_time = font2.render("wait, reload",1,(255,255,255))
                window.blit(reload_time,(win_width/2,450))
                print(now_time-last_time)
            else:
                num_fire = 0
                reload = False
        collides = sprite.groupcollide(bullets,enemies,True,True)

        for i in collides:
            score += 1
            enemy = Enemy("/Users/macbook/Desktop/source/Shooterasset/ufo.png",randint(80,win_width-80),-40,80,50,randint(1,5))
            enemies.add(enemy)
        if sprite.spritecollide(player,enemies,False) or sprite.spritecollide(player,asteroids,False):
            sprite.spritecollide(player,enemies,True)
            sprite.spritecollide(player,asteroids,True)
            life -= 1
        if loss >= 3 or life == 0:
            lose = font2.render("YOU LOSE",1,(255,255,255))
            window.blit(lose,(350,250))
            finnish = True
        if score >= 10:
            win = font2.render("YOU WIN",1,(255,255,255))
            window.blit(win,(350,250))
            finnish = True
        # elif loss >= 3 or sprite.spritecollide(player,enemies,False) or sprite.spritecollide(player,asteroids,False):
        #     life =- 1
        #     lose = font2.render("YOU LOSE",1,(255,255,255))
        #     window.blit(lose,(350,250))
        #     finnish = True
        clock.tick(fps)
        display.update()
    else :
        finnish = False
        loss = 0
        score = 0
        life = 3
        for b in bullets:
            b.kill()
        for e in enemies:
            e.kill()   
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(5):
            enemy = Enemy("/Users/macbook/Desktop/source/Shooterasset/ufo.png",randint(80,win_width-80),-40,80,50,randint(1,5))
            enemies.add(enemy)
        for i in range(3):
            asteroid = Asteroid("/Users/macbook/Desktop/source/Shooterasset/asteroid.png",randint(80,win_width-80),-40,50,50,randint(3,5))
            asteroids.add(asteroid)
    time.delay(50)