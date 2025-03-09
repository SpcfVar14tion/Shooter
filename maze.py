#create a Maze game!
from pygame import*
# from pygame.sprite import _Group
class Gamesprite(sprite.Sprite):
    def __init__(self,spr_img,rect_x,rect_y,speed):
        super().__init__()
        self.image = transform.scale(image.load(spr_img),(65,65))
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
        elif key_pressed[K_RIGHT] and self.rect.x < 700-65:
            self.rect.x += self.speed
        elif key_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif key_pressed[K_DOWN] and self.rect.y < 500-65:
            self.rect.y += self.speed
class Enemy(Gamesprite):
    direct = "left"
    def update(self):
        if self.rect.x >= 600:
            self.direct = "left"
        elif self.rect.x <= 500:
            self.direct = "right"
        if self.direct == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(sprite.Sprite):
    def __init__(self,color_1,color_2,color_3,wall_x,wall_y,wall_width,wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width,self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
win_width = 700
win_height = 500

window = display.set_mode((win_width,win_height))
display.set_caption("Maze")
bg = transform.scale(image.load("background.jpg"),(win_width,win_height))
sprite1 = Player("cat.jpg",5,win_height-80,4) 
sprite2 = Enemy("cyborg.png",win_width-80,280,2)
sprite3 = Gamesprite("treasure.png",win_width-120,win_height-80,0)
wall1 = Wall(190, 247, 197,100,20,450,10)
wall2 = Wall(190, 247, 197,100,480,350,10)
wall3 = Wall(190, 247, 197,100,20,10,380)
wall4 = Wall(190, 247, 197,200,100,200,10)
wall5 = Wall(190, 247, 197,200,100,10,380)
wall6 = Wall(190, 247, 197,200,200,300,10)
wall7 = Wall(190, 247, 197,300,200,10,100)
game = True
finnish = False
clock = time.Clock()
fps = 60
font.init()
font = font.Font(None,70)
win = font.render("YOU WIN",True,(255, 221, 87))
lose = font.render("YOU LOSE",True,(173, 0, 0))
mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()
money = mixer.Sound("money.ogg")
kick = mixer.Sound("kick.ogg")

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finnish != True:
        window.blit(bg,(0,0))
        sprite1.reset()
        sprite1.update()
        sprite2.reset()
        sprite2.update()
        sprite3.reset()
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        wall6.draw_wall()
        wall7.draw_wall()
        if sprite.collide_rect(sprite1,sprite3):
            finnish = True
            window.blit(win,(200,200))
            money.play()
        if sprite.collide_rect(sprite1,sprite2) or sprite.collide_rect(sprite1,wall1) or sprite.collide_rect(sprite1,wall3) or sprite.collide_rect(sprite1,wall4) or sprite.collide_rect(sprite1,wall2) or sprite.collide_rect(sprite1,wall5) or sprite.collide_rect(sprite1,wall6) or sprite.collide_rect(sprite1,wall7):
            window.blit(lose,(200,200))
            kick.play()
            sprite1.rect.x = 5
            sprite1.rect.y = win_height-80

            
    clock.tick(fps)
    display.update()