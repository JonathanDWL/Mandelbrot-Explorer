import pygame
import sys
from PIL import Image

pygame.init()

def lerp(a, b, amount):
    return(a+amount*(b-a))

def gradient(colors, steps):
    list = []
    colors.append("White")
    for i in range(steps):
        interp = i/steps*(len(colors)-2)
        index = int(interp)
        R = int(lerp(colors[index][0], colors[index+1][0], interp-index))
        G = int(lerp(colors[index][1], colors[index+1][1], interp-index))
        B = int(lerp(colors[index][2], colors[index+1][2], interp-index))
        list.append((R, G, B))
    return(list)

def iterate(c, iterate):
    z = 0
    for i in range(iterate):
        z = z**2 + c
        if(abs(z) > 2):
            return(i)
    return(-1)

def genset(res, iter, center, zoom, cols):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*(2/zoom)+center.real, (y-halfres)/halfres*(-2/zoom)+center.imag)
            numS = iterate(num, iter)
            if(numS < 0):
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = cols[numS%160]
    return(canvas)

class setdisplay(pygame.sprite.Sprite):
    def __init__(self, image):
        super(setdisplay, self).__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft = (0, 0))

    def switch(self, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft = (0, 0))

class user(pygame.sprite.Sprite):
    def __init__(self):
        super(user, self).__init__()
        self.size = 350
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, "WHITE", (0, 0, self.size, self.size), 2)
        self.rect = self.image.get_rect(center = (9999, 9999))

    def move(self, pos):
        if(pos != None):
            mx, my = pos
            self.rect.centerx = mx
            self.rect.centery = my

    def scale(self, scroll):
        self.size += scroll * -10
        if(self.size < 70):
            self.size = 70
        elif(self.size > 700):
            self.size = 700
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, "WHITE", (0, 0, self.size, self.size), 2)
        self.rect = self.image.get_rect(center = self.rect.center)

    def get_parameters(self, res, center, zoom, pos):
        halfres = halfres = res/2-0.5
        mx, my = pos
        newcenter = complex((mx-halfres)/halfres*(2/zoom)+center.real, (my-halfres)/halfres*(-2/zoom)+center.imag)
        newzoom = zoom * res/self.size
        return(newcenter, newzoom)

screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Mandelbrot explorer")

clock = pygame.time.Clock()

cols1 = [(50, 1, 51), (10, 72, 142), (60, 232, 126), (246, 255, 214)]
cols2 = [(246, 255, 214), (235, 191, 59), (142, 40, 11), (50, 1, 51)]
fullscheme = gradient(cols1, 80) + gradient(cols2, 80)
center = complex(0, 0)
zoom = 1

# genset(700, 500, complex(0.5, 0.5), 2, fullscheme).save("set.png")
display = setdisplay("defaultset.png")
user = user()

running = True
while running:
    wheelscroll = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            wheelscroll = event.y

    screen.fill("WHITE")

    mousepos = pygame.mouse.get_pos()
    if(mousepos[0] <= 0 or mousepos[0] >= 699 or mousepos[1] <= 0 or mousepos[1] >= 699):
        mousepos = None
    user.move(mousepos)
    user.scale(wheelscroll)
    if(pygame.mouse.get_pressed()[0] and mousepos != None):
        center, zoom = user.get_parameters(700, center, zoom, mousepos)
        genset(700, 500, center, zoom, fullscheme).save("set.png")
        display.switch("set.png")

    screen.blit(display.image, display.rect.topleft)
    screen.blit(user.image, user.rect.topleft)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()