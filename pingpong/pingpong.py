from pygame import *

lost = 0
score = 0

#klasa główna dla wszystkich podklas
class GameSprite(sprite.Sprite):
 #konstruktor klasy
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #wywyołanie konstruktora nadklasy
       sprite.Sprite.__init__(self)

       #każdy obiekt musi zawierać wgraną grafikę
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed

       #każdy obiekt musi posiadać hitbox - obiekt prostokątny 
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #metoda do wyświetlania obiektu na scenie gry
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#klasa gracza
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        pass

class Enemy(GameSprite):
    kierunek = "left"
    def update(self, x1, x2):
        if self.rect.x <= x1:
            self.kierunek = "right"
        if self.rect.x >= x2:
            self.kierunek = "left"
        
        if self.kierunek == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


#czcionka i podpisy
font.init()
font1 = font.Font(None, 36)

#tworzenie okna
#Scena gry:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("The Ping Pong")
background = transform.scale(image.load("tlo.png"), (win_width, win_height))

clock = time.Clock()
FPS = 60
#(self, player_image, player_x, player_y, size_x, size_y, player_speed)
mixer.init()

kick = mixer.Sound('ping.ogg')
#Tworzenie spritów
gracz1 = Player('paletka1.png', 5, win_height - 100, 15, 200, 10)

gracz2 = Player('paletka2.png', 680, win_height - 100, 15, 200, 10)

ball =  Enemy("pingpongball.png", 350, win_height - 250, win_width - 685, 15, 5)

#zmienna „game is over”: gdy tylko pojawi się True, duszki przestają działać w głównej pętli
finish = False
#główna pętla gry
run = True #flaga jest resetowana przyciskiem zamknięcia okna
while run:
   # Zdarzenie naciśnięcia przycisku „Zamknij”.
    for e in event.get():
       if e.type == QUIT:
           run = False

    if not finish:
        #update tła
        window.blit(background,(0,0))
        #wywołanie ruchu postaci
        gracz1.update()
        #update postaci
        gracz1.reset()
        
        gracz2.update()
        
        gracz2.reset()

        ball.update(0, win_width - 10)

        ball.reset()

        if sprite.collide_rect(gracz1, ball) or sprite.collide_rect(gracz2, ball):
            kick.play()    
        if sprite.collide_rect(gracz1, ball) or sprite.collide_rect(gracz2, ball):
            kick.play()   

        display.update()

    clock.tick(FPS)