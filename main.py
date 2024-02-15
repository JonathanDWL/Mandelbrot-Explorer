'''Sources:

Centering text on a surface: https://stackoverflow.com/questions/23982907/how-to-center-text-in-pygame

'''


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

def iterate(z, c, iterate):
    for i in range(iterate):
        z = z**2 + c
        if(abs(z) > 2):
            return(i)
    return(-1)

def gensetman(res, iter, center, zoom, cols):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*(2/zoom)+center.real, (y-halfres)/halfres*(-2/zoom)+center.imag)
            numS = iterate(0, num, iter)
            if(numS < 0):
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = cols[numS%160]
    return(canvas)

def gensetjul(res, iter, center, cols):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*2, (y-halfres)/halfres*-2)
            numS = iterate(num, center, iter)
            if(numS < 0):
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = cols[numS%160]
    return(canvas)

class setdisplay(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super(setdisplay, self).__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft = (x, y))

    def switch(self, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft = self.rect.topleft)

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
        if(self.size < 35):
            self.size = 35
        elif(self.size > 700):
            self.size = 700
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, "WHITE", (0, 0, self.size, self.size), 2)
        self.rect = self.image.get_rect(center = self.rect.center)

    def get_parameters(self, res, center, zoom, pos):
        halfres = res/2-0.5
        mx, my = pos
        newcenter = complex((mx-halfres)/halfres*(2/zoom)+center.real, (my-halfres)/halfres*(-2/zoom)+center.imag)
        newzoom = zoom * res/self.size
        return(newcenter, newzoom)
    
class dashboard(pygame.sprite.Sprite):
    def __init__(self):
        super(dashboard, self).__init__()
        self.image = pygame.Surface((300, 700))
        self.image.fill((178, 179, 207))
        self.rect = self.image.get_rect(topleft = (700, 0))

class button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text):
        super(button, self).__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.size = int(2.5*self.width/len(text))
        self.font = pygame.font.Font(None, self.size)
        self.text = text
        self.textrendered = self.font.render(self.text, False, "WHITE")
        self.textrect = self.textrendered.get_rect(center = (self.width//2, self.height//2))
        self.blacken = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.blacken = self.blacken.convert_alpha()
        self.blackenrect = self.blacken.get_rect(topleft = (0, 0))
        self.blacken.fill((0, 0, 0, 15))

    def collision(self, pos):
        mx, my = pos
        if(mx >= self.rect.left and mx <= self.rect.right and my >= self.rect.top and my <= self.rect.bottom):
            return(True)
        return(False)

    def draw(self, colliding, clicking):
        self.image.fill((149, 143, 179))
        self.image.blit(self.textrendered, self.textrect)
        if(colliding):
            print("YARGHH!")
            self.image.blit(self.blacken, self.blackenrect.topleft)
        if(clicking):
            self.image.blit(self.blacken, self.blackenrect.topleft)

screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Mandelbrot Explorer")

clock = pygame.time.Clock()

cols1 = [(50, 1, 51), (10, 72, 142), (60, 232, 126), (246, 255, 214)]
cols2 = [(246, 255, 214), (235, 191, 59), (142, 40, 11), (50, 1, 51)]
fullscheme = gradient(cols1, 80) + gradient(cols2, 80)
center = complex(0, 0)
zoom = 1

# genset(700, 500, complex(0.5, 0.5), 2, fullscheme).save("set.png")
display = setdisplay("defaultset.png", 0, 0)
gensetjul(100, 500, 0, fullscheme).save("defaultset2.png")
display2 = setdisplay("defaultset2.png", 900, 0)
user = user()
dashboard = dashboard()
buttons = pygame.sprite.Group()
buttons.add(button(700, 0, 200, 100, "Focus Julia"))

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
    if(mousepos[0] <= 0 or mousepos[0] >= 999 or mousepos[1] <= 0 or mousepos[1] >= 999):
        mousepos = None
    if(mousepos != None and mousepos[0] < 699):
        user.move(mousepos)
        user.scale(wheelscroll)
        if(pygame.mouse.get_pressed()[0]):
            center, zoom = user.get_parameters(700, center, zoom, mousepos)
            gensetman(700, 500, center, zoom, fullscheme).save("set.png")
            gensetjul(100, 500, center, fullscheme).save("set2.png")
            display.switch("set.png")
            display2.switch("set2.png")

    screen.blit(display.image, display.rect.topleft)
    screen.blit(user.image, user.rect.topleft)
    screen.blit(dashboard.image, dashboard.rect.topleft)
    screen.blit(display2.image, display2.rect.topleft)
    buttons.draw(screen)
    for button in buttons:
        if(mousepos != None):
            colliding = button.collision(mousepos)
        else:
            colliding = False
        if(colliding):
            clicking = pygame.mouse.get_pressed()[0]
        else:
            clicking = False
        print(colliding,clicking)
        button.draw(colliding, clicking)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()