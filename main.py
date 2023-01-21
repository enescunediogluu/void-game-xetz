import pygame
import time
import os
import random 
import tkinter as tk

pygame.font.init()
pygame.mixer.init()

# Tkinter window
window = tk.Tk()
window.title("VOID")
window.geometry("600x400+450+150")
window.resizable(width=False,height=False)
window.configure(bg="#141110")
name_yellow = ""
name_red = ""


def submit():
    global name_yellow
    global name_red
    name_yellow = player1_entry.get()
    name_red = player2_entry.get()
    window.destroy()

heading = tk.Label(window,fg="#FDDA00",bg="#141110",font="gameplay 40 ",text="VOID")
heading.place(x="235",y="45")

player1 = tk. Label(window,bg="#141110",fg="#FDDA00" ,text="YELLOW PLAYER",font=("gameplay 15 bold"))
player1.place(x="40",y="175")

player1_entry = tk.Entry(window,bg="black",fg = "yellow",font=("Consolas 15"))
player1_entry.place(x="30",y="215")

player2 = tk. Label(window,bg="#141110",fg="#FDDA00" ,text="RED PLAYER",font=("gameplay 15 bold"))
player2.place(x="380",y="175")

player2_entry = tk.Entry(window,bg="black",fg = "yellow",font=("Consolas 15"))
player2_entry.place(x="345",y="215")

button = tk.Button(window,text="Start",width=7,height=1,font=("gameplay 15 bold"),command = submit)
button.place(x="250",y="290")




window.mainloop()


#pygame window
width,height = 900,600
WIN = pygame.display.set_mode((width,height))
pygame.display.set_caption("VOID")

#player ships
RED_SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets","spaceship_red.png")),(70,70))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP,270)


YELLOW_SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets","spaceship_yellow.png")),(70,70))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP,90) # Şeklin yönünü değiştirir

#player lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
RED_LASER = pygame.transform.rotate(RED_LASER,90)
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))
YELLOW_LASER = pygame.transform.rotate(YELLOW_LASER,90)

#background
BG = pygame.image.load(os.path.join("assets","space.png"))

#meteors
SILVER_METEOR = pygame.transform.scale(pygame.image.load(os.path.join("assets","meteor_silver.png")),(80,80))
RED_METEOR = pygame.transform.scale(pygame.image.load(os.path.join("assets","meteor_silver.png")),(80,80))
WHITE_METEOR = pygame.transform.scale(pygame.image.load(os.path.join("assets","meteor_white.png")),(80,80))

class Ship:
    VELOCITY = 6
    COOLDOWN = 30
    yellow_countdown = 0
    red_countdown = 0
    loser = None
    yellow_dene = True
    red_dene = False
    
    def __init__(self,x,y,img,name,health=100):
        self.x = x
        self.y = y
        self.img=img
        self.name = name
        self.lasers = []
        self.yelLaser = YELLOW_LASER
        self.redLaser = RED_LASER
        self.health = health
        self.max_health = health
        self.mask = pygame.mask.from_surface(self.img)
        

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
        self.healthbar(window)
        self.draw_name(window)
        for laser in self.lasers:
            laser.draw(window)

    def move_yel_lasers(self,vel,obj):
        self.yellow_cooldown()
        for laser in self.lasers:
            laser.move_yellow()
            if laser.off_screen(width):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def move_red_lasers(self,vel,obj):
        self.red_cooldown()
        for laser in self.lasers:
            laser.move_red()
            if laser.off_screen(width):
                  self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()
    
    def yellow_cooldown(self):
        if self.yellow_countdown >= self.COOLDOWN:
            self.yellow_countdown=0
        elif self.yellow_countdown > 0:
            self.yellow_countdown += 1

    def red_cooldown(self):
        if self.red_countdown >= self.COOLDOWN:
            self.red_countdown = 0
        elif self.red_countdown > 0:
            self.red_countdown += 1

    def shoot1(self):
        if self.yellow_countdown == 0:
            laser = Laser(self.x,self.y,self.yelLaser)
            self.lasers.append(laser)
            self.yellow_countdown=1

    def shoot2(self):
        if self.red_countdown == 0:
            laser = Laser(self.x,self.y,self.redLaser)
            self.lasers.append(laser)
            self.red_countdown=1

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width() * (self.health/self.max_health), 10))

    def draw_name(self,window):
        player_font = pygame.font.Font("Gameplay.ttf",10)
        name_player = player_font.render(f"{self.name}",1,(153,218,0))
        window.blit(name_player,(self.x,self.y + self.img.get_height() + 25))

class Stones:

    COLOR_MAP = {
            "silver" : (SILVER_METEOR,15),
            "red" : (RED_METEOR,10),
            "white" : (WHITE_METEOR,5)
        }

    def __init__(self,x,y,color,health=100):
        self.x = x
        self.y = y
        self.color = color
        self.img = None
        self.dmg = None
        self.health = health
        self.img,self.dmg = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.img)

    def get_height(self):
        return self.img.get_height()

    def damage(self):
        return self.dmg

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y += vel
    
class Laser:
    laser_vel = 8      
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x, self.y-15)) # I did this because i wanted to make the shoot functon to be in the center.

    def move_yellow(self):
        self.x += Laser.laser_vel

    def move_red(self):
        self.x -= Laser.laser_vel

    def off_screen(self,height):
        return not (self.x <= width and self.y >= 0)

    def collision(self,obj):
        return collide(self,obj)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None
           
def main(): 
    run = True
    FPS = 75
    level = 0
    yellow_wave = 0
    red_wave = 0
    meteor_vel = 2
    meteors = []
    clock = pygame.time.Clock()
    player_yellow = Ship(100,280,YELLOW_SPACESHIP,name_yellow)
    player_red = Ship(800 - player_yellow.get_width(),280,RED_SPACESHIP,name_red)
    main_font = pygame.font.Font("Gameplay.ttf",30)
    

    while run:
        
        clock.tick(FPS)
        pygame.display.update()
        WIN.blit(BG,(0,0))
        name_label = main_font.render("void-ı",1,(135,5,23))
        WIN.blit(name_label,(width/2 - name_label.get_width()/2,100))
        
        player_yellow.draw(WIN)
        player_red.draw(WIN)

        if len(meteors)==0:
            yellow_wave += 1
            red_wave += 1

            for i in range(yellow_wave):
                meteor = Stones(random.randrange(20,width/2 - 60),random.randrange(-2000,-100),random.choice(["red","silver","white"]))
                meteors.append(meteor)
            
            for i in range(red_wave):
                meteor = Stones(random.randrange(width/2+40,width-100),random.randrange(-2000,-100),random.choice(["red","silver","white"]))
                meteors.append(meteor)

        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_q]:
            run = False

        if player_yellow.health <= 0: 
            Ship.loser = name_yellow
            lost_menu()

        elif player_red.health <=0 :
            Ship.loser = name_red
            lost_menu()

        # Yellow player controls

        if keys[pygame.K_s] and player_yellow.get_height() + player_yellow.y + 30 < height:
            player_yellow.y += Ship.VELOCITY
        if keys[pygame.K_w] and player_yellow.y > 0:
            player_yellow.y -= Ship.VELOCITY
        if keys[pygame.K_d] and player_yellow.x + player_yellow.get_width() < width/2:
            player_yellow.x += Ship.VELOCITY
        if keys[pygame.K_a] and player_yellow.x  - 25> 0:
            player_yellow.x -= Ship.VELOCITY

        if keys[pygame.K_SPACE]:  # yellow player shoot mechanism
            player_yellow.shoot1()

        # Red player controls

        if keys[pygame.K_DOWN] and  player_red.y + player_red.get_height() + 30< height:
            player_red.y += Ship.VELOCITY
        if keys[pygame.K_UP] and player_red.y > 0:
            player_red.y -= Ship.VELOCITY
        if keys[pygame.K_RIGHT] and player_red.x + player_yellow.get_width() + 25 < width:
            player_red.x += Ship.VELOCITY
        if keys[pygame.K_LEFT] and player_red.x  > width/2:
            player_red.x -= Ship.VELOCITY

        if keys[pygame.K_KP_ENTER]:  # red player shoot mechanism 
            player_red.shoot2()
        for meteor in meteors:
            meteor.draw(WIN)
        
        for meteor in meteors[:]:
            meteor.move(meteor_vel)
            if collide(meteor,player_yellow):
                player_yellow.health -= meteor.damage()
                meteors.remove(meteor)

            if collide(meteor,player_red):
                player_red.health -= meteor.damage()
                meteors.remove(meteor)

            if meteor.y + meteor.get_height() > height:
                meteors.remove(meteor)

        player_yellow.move_yel_lasers(Laser.laser_vel,player_red)
        player_red.move_red_lasers(-1*Laser.laser_vel,player_yellow)

def lost_menu():
    YELLOW_SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets","spaceship_yellow.png")),(90,90))
    RED_SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets","spaceship_red.png")),(90,90))
    
    REPLAY_BUTTON = pygame.transform.scale(pygame.image.load(os.path.join("assets","repeat_button.png")),(300,130))
    EXIT_BUTTON = pygame.transform.scale(pygame.image.load(os.path.join("assets","exit_button.png")),(300,110))
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.Font("Gameplay.ttf",30)

    while run:
        clock.tick(FPS)
        pygame.display.update()
        WIN.blit(BG,(0,0))
        lost_label = main_font.render(f"{Ship.loser} lost !",1,(253,218,0))

        WIN.blit(REPLAY_BUTTON, (width/2 - REPLAY_BUTTON.get_width()/2, 300))
        WIN.blit(EXIT_BUTTON, (width/2 - REPLAY_BUTTON.get_width()/2, 410))

        name1 = main_font.render(f"{name_yellow}",1,(40, 158, 222))
        WIN.blit(name1,(150 - (name1.get_width() - YELLOW_SPACESHIP.get_width())/2,200))

        name2 = main_font.render(f"{name_red}",1,(40, 158, 222))
        WIN.blit(name2,(width-150-RED_SPACESHIP.get_width() - (name2.get_width() - RED_SPACESHIP.get_width())/2,200))
        

        WIN.blit(YELLOW_SPACESHIP,(150,100))
        WIN.blit(RED_SPACESHIP,(width-150-RED_SPACESHIP.get_width(),100))
        WIN.blit(lost_label,(width/2 - lost_label.get_width()/2,50))

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()         
            
            if keys[pygame.K_q]:
                quit()
        
        mouse_pos  = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()  

        exit_button_rect = EXIT_BUTTON.get_rect(x=width/2 - REPLAY_BUTTON.get_width()/2,y=410)
        replay_button_rect = REPLAY_BUTTON.get_rect(x=width/2 - REPLAY_BUTTON.get_width()/2,y=300)

        if exit_button_rect.collidepoint(mouse_pos):

            if mouse_pressed[0]:
                quit()

        if replay_button_rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                main()

if __name__=="__main__":
        main()









