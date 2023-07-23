from pygame import *
from random import randint
from time import time as timer



font.init()
font1 = font.SysFont("Modern", 70,)
win = font1.render('Ти виграв!!', True, (0, 255, 0))
lose = font1.render('Ти програв!', True, (180, 0, 0))
font2 = font.SysFont("Modern", 32)


mixer.init()
mixer.music.load('')
mixer.music.play()
fire_sound = mixer.Sound('')


img_back = "galaxy.jpg" 
img_car1 = "pngegg.png"  
img_bullet = "bullet.png" 
img_car2 = "ufo.png" 



goal = 20
score = 0  
life = 3  




class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect > win_height:
            self.rect.y -= self.speed



class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0



win_width = 700
win_height = 500
display.set_caption("Epic Racing")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


car1 = Player(img_car1, 5, win_height - 100, 70, 100, 10)


car2 = sprite.Group()
for i in range(1, 6):
    car2 = Enemy(img_car2, randint(
        80, win_width - 80), -40, 80, 70, randint(1, 5))
    car2.add(car2)

finish = False
run = True

while run:
    if not finish:
    
        window.blit(background, (0, 0))

        # рухи спрайтів
        car1.update()
        car2.update()

 
        #оновлюємо їх у новому місці при кожній ітерації циклу
        car1.reset()
        car2.draw(window)



        if sprite.spritecollide(car1, car2, False):
            sprite.spritecollide(car1, car2, True)
            life = life -1


        if life == 0:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))    


        if score >= goal:
            finish = True
            window.blit(win, (200, 200))      

        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))                  

        time.delay(50)