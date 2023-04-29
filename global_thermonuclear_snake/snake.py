# TheaterWide BioToxic Snake  -  A Snake Game
import pygame
import random
import math
import tkinter as tk
from tkinter import messagebox

class segment(object):
    rows = 20
    w = 500
    def __init__(self,start,move_x=1,move_y=0,color=(255,0,0)):
        self.pos = start
        self.move_x = 1
        self.move_y = 0
        self.color = color
      
    def move(self, move_x, move_y):
        self.move_x = move_x
        self.move_y = move_y
        self.pos = (self.pos[0] + self.move_x, self.pos[1] + self.move_y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        row = self.pos[0]
        col = self.pos[1]

        pygame.draw.rect(surface, self.color, (row*dis+1,col*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (row*dis+centre-radius,col*dis+8)
            circleMiddle2 = (row*dis + dis -radius*2, col*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = segment(pos)
        self.body.append(self.head)
        self.move_x = 0
        self.move_y = 1

    # move snake
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.move_x = -1
                    self.move_y = 0
                    self.turns[self.head.pos[:]] = [self.move_x, self.move_y]

                elif keys[pygame.K_RIGHT]:
                    self.move_x = 1
                    self.move_y = 0
                    self.turns[self.head.pos[:]] = [self.move_x, self.move_y]

                elif keys[pygame.K_UP]:
                    self.move_x = 0
                    self.move_y = -1
                    self.turns[self.head.pos[:]] = [self.move_x, self.move_y]

                elif keys[pygame.K_DOWN]:
                    self.move_x = 0
                    self.move_y = 1
                    self.turns[self.head.pos[:]] = [self.move_x, self.move_y]

        for idx, seg in enumerate(self.body):
            p = seg.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                seg.move(turn[0],turn[1])
                if idx == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if seg.move_x == -1 and seg.pos[0] <= 0: seg.pos = (seg.rows-1, seg.pos[1])
                elif seg.move_x == 1 and seg.pos[0] >= seg.rows-1: seg.pos = (0,seg.pos[1])
                elif seg.move_y == 1 and seg.pos[1] >= seg.rows-1: seg.pos = (seg.pos[0], 0)
                elif seg.move_y == -1 and seg.pos[1] <= 0: seg.pos = (seg.pos[0],seg.rows-1)
                else: seg.move(seg.move_x,seg.move_y)

    # Check if snake has collided with itself or the wall and reset if so    
    def reset(self, pos):
        self.head = segment(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.move_x = 0
        self.move_y = 1

    # Add a segment to the snake
    def addSegment(self):
        tail = self.body[-1]
        mx, my = tail.move_x, tail.move_y

        if mx == 1 and my == 0:
            self.body.append(segment((tail.pos[0]-1,tail.pos[1])))
        elif mx == -1 and my == 0:
            self.body.append(segment((tail.pos[0]+1,tail.pos[1])))
        elif mx == 0 and my == 1:
            self.body.append(segment((tail.pos[0],tail.pos[1]-1)))
        elif mx == 0 and my == -1:
            self.body.append(segment((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].move_x = mx
        self.body[-1].move_y = my

    # Draw the snake
    def draw(self, surface):
        for idx, seg in enumerate(self.body):
            if idx ==0:
                seg.draw(surface, True)
            else:
                seg.draw(surface)

# Draw the grid lines
def drawGrid(w, rows, surface):
    size = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + size
        y = y + size

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))

# Draw the window        
def buildWindow(surface):
    global rows, width, s, mutantrat
    surface.fill((0,0,0))
    s.draw(surface)
    mutantrat.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()

# Generate a random position for the mutantrat which when the snake eats it, it will grow
def randomMutantrat(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break       
    return (x,y)

# Display a message box
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
    
def main():
    global width, rows, s, mutantrat
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    mutantrat = segment(randomMutantrat(rows, s), color=(0,255,0))
    flag = True

    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == mutantrat.pos:
            s.addSegment()
            mutantrat = segment(randomMutantrat(rows, s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('Game Over!', 'Shall We Play Again?')
                s.reset((10,10))
                break         
        buildWindow(win)
        
if __name__ == '__main__':
    main()