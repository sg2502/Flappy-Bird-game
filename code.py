import pygame
from pygame.locals import *
import random


pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 818

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FlappyBird Game')

font= pygame.font.SysFont('Bauhaus 93', 60)
white =(255, 255, 255)
#game variables
ground_scroll=0
scroll_speed=4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #millisecond
last_pipe = pygame.time.get_ticks()-pipe_frequency
score = 0
pass_pipe = False
#game images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
restart_img= pygame.image.load('img/restart.png')

#draw_text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#reset game
def reset_game():
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(screen_height/2)
    flappy.image = flappy.images[0]
    score=0
    return score



class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0

        for i in range(1, 4):
            img = pygame.image.load(f'img/bird{i}.png')
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel=0
        self.clicked=False

    def update(self):
        if(flying==True):

            #gravity
            self.vel += 0.5
            if self.vel > 8 :
                self.vel=8
            if self.rect.bottom < 708:
                self.rect.y += int(self.vel)
            # else:
                # flying=False

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel*-2)

        if game_over==False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked==False:
                self.vel -= 10
                self.clicked=True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked=False

            self.counter+=1
            flap_change=5

            if self.counter > flap_change:
                self.counter=0
                self.index+=1
                self.index%=3 
                self.image=pygame.transform.rotate(self.images[self.index], self.vel*-2)

        else:
            self.image= pygame.transform.rotate(self.images[self.index], -90)



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if(position == 1):
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y-int(pipe_gap/2)]
        else:
            self.rect.topleft = [x, y+int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed
        if(self.rect.x < -4):
            self.kill()




class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) 

    def draw(self):
        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        #get mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos)==True:
            if(pygame.mouse.get_pressed()[0] == 1):
                game_over=False
                reset_game()
                return True
               
        return False  
                  

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height/2))


bird_group.add(flappy)

restart_button = Button(int(screen_width/2)-50, int(screen_height/2)-100, restart_img)

run=True

while run:
    
    clock.tick(fps)

    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)
    

    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top<0 : 
        game_over = True



    if flappy.rect.bottom >= 708:
        game_over=True
        flying=False

    screen.blit(ground_img, (ground_scroll, 708))

    if flying==True and game_over==False:
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if(time_now-last_pipe > pipe_frequency):
            pipe_height=random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height/2 + pipe_height), -1)
            top_pipe = Pipe(screen_width, int(screen_height/2 + pipe_height), 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now

        #draw and scroll ground
        ground_scroll -=scroll_speed
        if(ground_scroll<-35):
            ground_scroll=0

        pipe_group.update()


    #Check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
             and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
             and pass_pipe == False:
            pass_pipe=True
            # print("he")
        if pass_pipe == True:
            # print(bird_group.sprites()[0].rect.left, pipe_group.sprites()[0].rect.right)
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe=False
                # print("hi")
        # print(score)
    
    draw_text(str(score), font, white, int(screen_width/2), 20)

    if flying==False and game_over==True:
        if restart_button.draw()== True:
            game_over=False
            score = reset_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over==False:
            flying=True



    pygame.display.update()

pygame.quit()
