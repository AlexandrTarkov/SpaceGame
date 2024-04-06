#Импорт модулей
import pygame as pg
from random import randint
from time import time as tm

#Инициализация модулей
pg.init()
pg.mixer.init()
pg.font.init()

font = pg.font.SysFont("Franklin Gothic Medium", 40)
font2 = pg.font.SysFont("Franklin Gothic Medium", 140)
font3 = pg.font.SysFont("Franklin Gothic Medium", 90)

Font_Item = pg.font.SysFont("Franklin Gothic Medium", 40)
Font_Item_Select = pg.font.SysFont("Franklin Gothic Medium", 45)

WHITE = (10, 10, 10)

clock = pg.time.Clock()

#Загрузка музыки
pg.mixer.music.load('music2.ogg')
pg.mixer.music.set_volume(0.01)
pg.mixer.music.play()

kick = pg.mixer.Sound("fire.ogg")
kick.set_volume(0.01)

#Установка скоростей
speed = 5
speed2 = randint(1,3)
speed3 = 1

speedBullet = 3

lifes = 3

colour = (21, 255, 0)

#Создание окна
window = pg.display.set_mode((900, 700))
FPS = 120
timer = 0

items = ["ИГРАТЬ", "УПРАВЛЕНИЕ", "", "РАЗРАБОТЧИК", "", "", "ВЫХОД"]
select = 0 #Переменная хранящая в себе выбранный пункт. По индексам списка items.
selectADD = 0 # Переменная, которая используется при нажатии на кнопки.

pg.display.set_caption('Shooter')

bgMenu = pg.transform.scale(pg.image.load("back.jpg"), (900, 700))

bg = pg.transform.scale(pg.image.load("galaxy.jpg"), (900, 700))

lose = font2.render("LOSE", True, (255, 170, 0))
win = font2.render("WIN", True, (255, 170, 0))

#счетчики
score = 0  
lost = 0

#Создание счетчиков 
scoreLabel = font.render("Счет:", True, (255, 255, 255))
counter1 = font.render(str(score), True, (255,255,255))

LostLabel = font.render("Пропущено:", True, (255, 255, 255))
counter2 = font.render(str(lost), True, (255,255,255))

LifesCounter = font3.render(str(lifes), True, colour)

bullets = pg.sprite.Group()

#Классы
class GameSprite(pg.sprite.Sprite):
    def __init__(self, player_image, player_x,player_y, player_speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= speedBullet
        if self.rect.y <= 10:   
            self.kill()   

#Класс игрока
class Player(GameSprite):
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[pg.K_d] and self.rect.x < 825:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet2.png", player.rect.centerx - 30, player.rect.top - 50, speedBullet)
        bullets.add(bullet)

    def fireUpgrade(self):
        bullet1 = Bullet("bullet2.png", player.rect.centerx - 30, player.rect.top - 50, speedBullet)
        bullet2 = Bullet("bullet2.png", player.rect.centerx - 0, player.rect.top - 50, speedBullet)
        bullet3 = Bullet("bullet2.png", player.rect.centerx + 30, player.rect.top - 50, speedBullet)
        bullets.add(bullet1)
        bullets.add(bullet2)
        bullets.add(bullet3)

#Класс врагов
class meteors(GameSprite):
    def update(self):
        if self.rect.y <= 700:
            self.rect.y += self.speed

        if self.rect.y > 700:
            self.rect.y -= randint(800,1000)
            speed2 = randint(1,2)
            global lost
            lost += 1
    

class someone(GameSprite):
    def update(self):
        if self.rect.y <= 700:
            self.rect.y += self.speed

        if self.rect.y > 700:
            self.rect.y -= randint(1000,2000)
        
            

class ClearLost(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y -= randint(1000, 1100)
    def up(self):
        self.rect.x == randint(100,700)
        self.rect.y -= randint(5000, 6000)

           
#Создание спрайтов и групп

a = "A - left"
b = "D - right"
c = "R - restart"
d = "SPACE - fire"
e = "W - triple fire"

bulletAmount = 0

player = Player("rocket3.png", 450, 570, speed)

asteroids = pg.sprite.Group()

someones = pg.sprite.Group()

lostClear = ClearLost('rocket.png', randint(100,700), randint(-5000, -4000), 3)

creator = font.render("https://vk.com/atarkov", True, (255, 170, 0))

control1 = font.render(a, True, (255, 170, 0))
control2 = font.render(b, True, (255, 170, 0))
control3 = font.render(c, True, (255, 170, 0))
control4 = font.render(d, True, (255, 170, 0))
control5 = font.render(e, True, (255, 170, 0))

reloadTitle = font.render("reload...", True, (255, 0, 0))

bulletCounter = font.render(str(bulletAmount), True, (255, 255, 255))
bulletCounterLabel = font.render("Пуль выпущено:", True, (255, 255, 255))

for i in range(5):
    enemy = meteors("asteroid.png", randint(50, 800), randint(-200, -50), randint(1,2))
    asteroids.add(enemy)

for i in range(3):
    a = someone("ufo.png", randint(50,800), randint(-2000,-1000), speed3)
    someones.add(a)



game = True
finish = False

bulletsNum = 0

relTime = False

clock = pg.time.Clock()
keys = pg.key.get_pressed()

blits = False

blits2 = False

play = True

restart = False

countTime = 3

startTime = tm()

while play:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            play = False
            game = False

        #Управление меню
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_DOWN: selectADD =  1
            elif e.key == pg.K_UP: selectADD = - 1

            if blits == True:
                if e.key == pg.K_ESCAPE:
                    blits = False
            
            if blits2 == True:
                if e.key == pg.K_ESCAPE:
                    blits2 = False

            # Управление клавишами
            elif e.key in [pg.K_RETURN, pg.K_SPACE]:
                if items[select] == "ВЫХОД":
                    play = False
                    game = False

                if items[select] == "ИГРАТЬ":
                    play = False
                
                if items[select] == "РАЗРАБОТЧИК":
                    blits = True
                
                if items[select] == "УПРАВЛЕНИЕ":
                    blits2 = True

            #Задаём границы пунктов меню. Чтобы нельзя было выбрать несуществующий элемент.
            select = (select + selectADD) % len(items)
            while items[select] == "":# цикл, который проверяет выбранн элемент меню или пустая строка.
                select = (select + selectADD) % len(items)#Если выбрана пустая строка, то делается шаг.

            selectADD = 0

    timer += 1
    #Отрисовка меню
    window.fill(WHITE)
    for i in range(len(items)):
        #Выделение выделенного пункта
        if i == select and timer % 30 > 15: # Строка с timer добавлена для мерцания.
            text = Font_Item_Select.render(items[i], True, (67, 54, 214))

        else:
            text = Font_Item.render(items[i], True, (102, 42, 232)) #Сглаживание отсутствует или нет True/False. render - метод отрисовки текста.

        # Расположение элементов меню
        rect = text.get_rect(center = (700 // 2, 200 + 50 * i))
        window.blit(text, rect)#отображение текста. Чего и где.
        if blits == True:
            window.blit(creator, (200,650))
        
        if blits2 == True:
            window.blit(control1, (500,50))
            window.blit(control2, (500,90))
            window.blit(control3, (500,130))
            window.blit(control4, (500,170))
            window.blit(control5, (500,210))


    pg.display.update()
    clock.tick(FPS)

#! Игрововй цикл
while game:

    #if lost == 3:
        #window.blit(lose, (300, 300))
        #finish = True

    if score == 101:
        window.blit(win, (330, 300))
        finish = True


    #TODO Обработка выхода из игры 

    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
        
        if e.type == pg.KEYDOWN:
                if e.key == pg.K_m:
                    play = True
    
        if not relTime:

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    player.fire()
                    kick.play()
                    bulletsNum += 1
                    bulletAmount += 1

        if score >= 5:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_w:
                    player.fireUpgrade()
                    kick.play()
                    score -= 5
                    bulletsNum += 1
                    bulletAmount += 3

        if lifes <= 0:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_r:
                    restart = True


    #? Отрисовка спрайтов и счетчиков
    if finish != True:

        window.blit(bg, (0, 0)) 

        counter1 = font.render(str(score), True, (255,255,255))

        window.blit(counter1, (100, 20))
        window.blit(scoreLabel, (5, 20))

        counter2 = font.render(str(lost), True, (255,255,255))

        window.blit(counter2, (230, 70))
        window.blit(LostLabel, (5, 70))

        bulletCounter = font.render(str(bulletAmount), True, (255, 255, 255))

        window.blit(bulletCounterLabel, (5, 120))
        window.blit(bulletCounter, (300, 120))

        LifesCounter = font3.render(str(lifes), True, colour)

        window.blit(LifesCounter, (800, 90))

        lostClear.update()
        lostClear.reset()

        player.update()
        player.reset()

        asteroids.update()
        asteroids.draw(window)

        someones.update()
        someones.draw(window)

        bullets.update()
        bullets.draw(window)

        if bulletsNum >= 5:
            relTime = True
    
        if relTime:
            nowTime = tm()

            if nowTime - startTime < countTime:
                relTime = True
                window.blit(reloadTitle, (400, 650))
            
            if nowTime - startTime > countTime:
                startTime = tm()
                relTime = False
                bulletsNum = 0
                
        
    #* Реакция на столкновение
    if pg.sprite.spritecollide(player, asteroids, True):
        lifes -= 1
        enemy = meteors("asteroid.png", randint(50, 800), randint(-200, -50), randint(1,2))
        asteroids.add(enemy)
    
    if pg.sprite.groupcollide(bullets, asteroids, True, True):
        score += 1
        enemy = meteors("asteroid.png", randint(50, 800), randint(-200, -50), randint(1,2))
        asteroids.add(enemy)
    
    if pg.sprite.spritecollide(lostClear, bullets, True):
        lostClear.up()
        lifes = 3
    
    if pg.sprite.spritecollide(player, someones, True):
        lifes -= 1
    
    if lifes <= 0:
        window.blit(lose, (300, 300))
        finish = True
    
    if lifes == 3:
        colour = (21, 255, 0)

    elif lifes == 2:
        colour = (255, 213, 0)

    elif lifes == 1:
        colour = (255, 0, 0)
    
    if restart:
        if lifes == 0:
            lifes = 3
        lost = 0
        bulletAmount = 0
        score = 0
        enemy.rect.y -= randint(800, 1200)
        finish = False
        restart = False
    

    clock.tick(FPS)
    pg.display.update()



