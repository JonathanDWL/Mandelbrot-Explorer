import pygame
import sys
from PIL import Image

pygame.init()

def lerp(a, b, amount):
    return(a+amount*(b-a))

def gradient(steps, colors):
    list = []
    colors.append("White")
    for i in range(steps):
        interp = i/steps*(len(colors)-2)
        selection = int(interp)
        R = int(lerp(colors[selection][0], colors[selection+1][0], interp-selection))
        G = int(lerp(colors[selection][1], colors[selection+1][1], interp-selection))
        B = int(lerp(colors[selection][2], colors[selection+1][2], interp-selection))
        list.append((R, G, B))
    return(list)

def iterate(c, iterate):
    z = 0
    for i in range(iterate):
        z = z**2 + c
        if(abs(z) > 2):
            return(i)
    return(-1)

def genset(res, iter):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*2, (y-halfres)/halfres*2)
            numS = iterate(num, iter)
            if(numS < 0):
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = (255, 255, 255)
    return(canvas)

class setdisplay(pygame.sprite.Sprite):
    def __init__(self, image):
        super(setdisplay, self).__init__()
        self.image = pygame.image.load("set.png")
        self.rect = self.image.get_rect(topleft = (0, 0))

screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Mandelbrot explorer")

clock = pygame.time.Clock()

display = setdisplay("defaultset.png")

scheme = [(50, 1, 51), (10, 72, 142), (60, 232, 126), (246, 255, 214)]
scheme2 = [(246, 255, 214), (235, 191, 59), (142, 40, 11), (50, 1, 51)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("WHITE")

    screen.blit(display.image, display.rect.topleft)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()