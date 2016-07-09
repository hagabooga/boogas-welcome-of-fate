import pygame
from colors import *

pygame.display.set_icon(pygame.image.load('game/general/icon.png'))
pygame.display.set_caption('''Booga's Welcome of Fate''')
screenW = 1024
screenH = 768
screen = pygame.display.set_mode((screenW,screenH))
clock = pygame.time.Clock()

class Page:
    def __init__(self):
        self.show = False
    def enter(self):
        self.show = True
    def leave(self):
        self.show = False
        
class switchTextbox: # each page has x amount of columns of textboxes
    def __init__(self,pages,column):
        self.text_list = [] # each row has ['aText',aColor]
        startText = []
        for page in range(pages):
            for col in range(column):
                startText.append(['',black])
            self.text_list.append(startText)
            startText = []
        self.column = column
        self.pg_num = 1
        self.pages = pages - 1
    def addText(self,newTextList):
        del self.text_list[0]
        new_text_list = []
        for col in range(self.column):
            new_text_list.append(['',black])            
        self.text_list.append(new_text_list)
        for text in newTextList:
            del self.text_list[self.pages][0]
            self.text_list[self.pages].append(text)
    def reset(self):
        startText = []
        for page in range(self.pages+1):
            for col in range(self.column):
                startText.append(['',black])
            self.addText(startText)
    def showText(self,textSizeList,x,x_dis,y,y_dis):
        xdis = 0
        ydis = 0
        for col in range(self.column):
            textbox(self.text_list[self.pg_num][col][0],textSizeList[col],self.text_list[self.pg_num][col][1],x+xdis,y+ydis)
            x += x_dis
            y += y_dis

def doNone():
    None
    
# place center img
def centerIMG(imgX, imgY, x, y):
    center = ((x - imgX / 2), (y - imgY / 2))
    return center

# Make a textbox
def textObj(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def textbox(msg, size, color, x, y):
    fontSize = pygame.font.Font('game/font/segoeuil.ttf',size)
    textSurf, textRect = textObj(msg, fontSize, color)
    textRect.center = ((x, y))
    screen.blit(textSurf, textRect)

# Rotate an image
def rotate_img(now_direct, want_direct, img):
    rotate_time = want_direct - now_direct
    rotate_time = rotate_time * 45
    newIMG = pygame.transform.rotate(img, rotate_time)
    return newIMG

# rectangle buttons
def button(msg, msgSize, x, y, w, h, color, onColor, action, parameter):
    # print(mouse)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click) (left click,scroll click, right click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, color, (x, y, w, h))
        if click[0] == 1 and parameter != None:
            action(parameter)
        elif click[0] == 1 and parameter == None:
            action()
    else:
        pygame.draw.rect(screen, onColor, (x, y, w, h))
    textbox(msg, msgSize, black, x + w / 2, y + h / 2)

def boolButton(msg, msgSize, x, y, w, h, color, onColor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, color, (x, y, w, h))
        textbox(msg, msgSize, black, x + w / 2, y + h / 2)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, onColor, (x, y, w, h))
        textbox(msg, msgSize, black, x + w / 2, y + h / 2)
        return False


def quitGame():
    pygame.quit()
    quit()
