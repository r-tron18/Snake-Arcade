from tkinter import *
import random
import time
import pygame
import threading

root = Tk()
root.title("Snake Arcade")
background  = "#%02x%02x%02x" % (100, 40, 54)

can = Canvas(root, width = 600, height = 600, bg=background)
can.pack()

## directions
## 0 right
## 1 up
## 2 left
## 3 down          

dire = 0

def playMusic(delay,file):
    time.sleep(delay)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)
    
def upKey(event):
    global dire
    if dire in (0, 2):
        dire=1
        
def downKey(event):
    global dire
    if dire in (0, 2):
        dire = 3

def leftKey(event):
    global dire
    if dire in (1, 3):
        dire = 2

def rightKey(event):
    global dire
    if dire in (1, 3):
        dire = 0

root.bind('<Up>', upKey)
root.bind('<Down>', downKey)
root.bind('<Right>', rightKey)
root.bind('<Left>', leftKey)

border = []
def make_border():
    color = ["grey", "black"]
    for i in range(60):
        coord = [i*10,0,(i+1)*10,10]
        rec = can.create_rectangle(*coord, fill=color[i%2])
        border.append(coord)

        if i not in(0, 59):
            coord = [i*10, 590, (i+1)*10, 600]
            rec = can.create_rectangle(*coord, fill=color[(i+1)%2])
            border.append(coord)

    for i in range(1,60):
        coord =[0,i*10,10,(i+1)*10]
        rec = can.create_rectangle(*coord, fill=color[i%2])
        border.append(coord)

        coord =[590,i*10,600,(i+1)*10]
        rec = can.create_rectangle(*coord, fill=color[(i+1)%2])
        border.append(coord)
                                
make_border()
class Snake:

    def __init__(self):
        self.body = []
        self.color = ["blue", "yellow"]
        self.coord = []
        self.food_coord = None
        self.food = None
        for  i in range(6):
            rec = can.create_rectangle(100+i*10,100,110 + i*10,110,fill= self.color[0])
            self.coord.append([100+i*10,100,110+i*10,110])
            self.body.append(rec)

    def move(self):
        X = [1, 0, -1, 0]
        Y = [0, -1, 0, 1]
        
        x1, y1, x2, y2 = self.coord[-1]

        next_coord = [x1+10*X[dire],y1+10*Y[dire],x2+10*X[dire],y2+10*Y[dire]]

        if next_coord == self.food_coord: ## food found
            print("food found")
            can.delete(self.food)
            self.food = None

        elif next_coord in self.coord or next_coord in border:
            pygame.mixer.music.stop()
            loseLifeThread.start()
            time.sleep(0.5)
            color = ["white", "blue"]
            for i in range(5):
                for rec in self.body:
                    can.itemconfig(rec, fill=color[i%2])
                root.update()
                root.after(300)

            time.sleep(0.4)
            pygame.mixer.music.stop()
            return 0
        else:
            can.delete(self.body.pop(0))
            self.coord.pop(0)
            
        rec = can.create_rectangle(*next_coord, fill = self.color[0])
        self.coord.append(next_coord)
        self.body.append(rec)

        root.update()

        if self.food == None:
            self.produce_food()

        return 1

    def produce_food(self):
        x = random.randint(1, 58) * 10
        y = random.randint(1, 58) * 10

        coord = [x,y,x+10, y+10]
        while coord in self.coord:
            x = random.randint(1, 58) * 10
            y = random.randint(1, 58) * 10    
            coord = [x,y,x+10, y+10]

        self.food = can.create_rectangle(*coord, fill = "green" )
        self.food_coord = coord[:]
        
s = Snake()            
s.produce_food()
musicThread = threading.Thread(target = playMusic, args=(1,'blue bird.mp3'))
loseLifeThread=threading.Thread(target = playMusic, args=(0,'lose the life.mp3'))
musicThread.start()

while True:
    status = s.move()
    if status==0:
        img = PhotoImage(file="gameover.png")
        root.after(300)
        can.create_image(0, 0, image = img, anchor = NW)
        break
    else:
        root.after(50)

def ret(event):
    root.destroy()

root.bind('<Return>', ret)
