'''Sources:

How the Mandelbrot Set works: https://plus.maths.org/content/what-mandelbrot-set

Centering text on a surface: https://stackoverflow.com/questions/23982907/how-to-center-text-in-pygame

Help with creating color schemes: https://mycolor.space/gradient

'''


import pygame
import sys
from PIL import Image
from copy import deepcopy

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
                pixels[x,y] = cols[numS%len(cols)]
    return(canvas)

def gensetjul(res, iter, center, zoom, cols):
    if(zoom != 1):
        center2 = center
    else:
        center2 = 0
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*(2/zoom)+center2.real, (y-halfres)/halfres*(-2/zoom)+center2.imag)
            numS = iterate(num, center, iter)
            if(numS < 0):
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = cols[numS%len(cols)]
    return(canvas)

def reloadmandelbrot():
    if(focusjulia == False):
        gensetman(700, iteration, center, zoom, scheme).save("set.png")
        display.switch("set.png")
    else:
        gensetman(70, iteration, center, zoom, scheme).save("set2.png")
        display2.switch("set2.png")

def reloadjulia():
    if(focusjulia == False):
        gensetjul(70, iteration, center, juliazoom, scheme).save("set2.png")
        display2.switch("set2.png")
    else:
        gensetjul(700, iteration, center, juliazoom, scheme).save("set.png")
        display.switch("set.png")

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
            if(not axismode):
                self.rect.centery = my
            else:
                self.rect.centery = 350

    def scale(self, scroll):
        self.size += scroll * -10
        if(self.size < 35):
            self.size = 35
        elif(self.size > 650):
            self.size = 650
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, "WHITE", (0, 0, self.size, self.size), 2)
        self.rect = self.image.get_rect(center = self.rect.center)

    def get_parameters(self, res, center, zoom, pos):
        halfres = res/2-0.5
        mx, my = pos
        newcenter = complex((mx-halfres)/halfres*(2/zoom)+center.real, (my-halfres)/halfres*(-2/zoom)+center.imag)
        if(axismode):
            newcenter = complex(newcenter.real, 0)
        newzoom = zoom * res/self.size
        return(newcenter, newzoom)
    
class dashboard(pygame.sprite.Sprite):
    def __init__(self):
        super(dashboard, self).__init__()
        self.image = pygame.Surface((300, 700))
        self.image.fill((178, 179, 207))
        self.rect = self.image.get_rect(topleft = (700, 0))

class textdisplay(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text):
        super(textdisplay, self).__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.size = int(2*self.width/len(text))
        self.font = pygame.font.Font(None, self.size)
        self.text = text
        self.textrendered = self.font.render(self.text, False, "WHITE")
        self.textrect = self.textrendered.get_rect(center = (self.width//2, self.height//2))

    def draw(self):
        self.image.fill((178, 179, 207))
        self.image.blit(self.textrendered, self.textrect)

    def changetext(self, text):
        self.size = int(2*self.width/len(text))
        self.font = pygame.font.Font(None, self.size)
        self.text = text
        self.textrendered = self.font.render(self.text, False, "WHITE")
        self.textrect = self.textrendered.get_rect(center = (self.width//2, self.height//2))

class button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text):
        super(button, self).__init__()
        self.width = width - 8
        self.height = height - 8
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft = (x + 4, y + 4))
        self.size = int(2*self.width/len(text))
        self.font = pygame.font.Font(None, self.size)
        self.text = text
        self.textrendered = self.font.render(self.text, False, "WHITE")
        self.textrect = self.textrendered.get_rect(center = (self.width//2, self.height//2))
        self.blacken = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.blacken = self.blacken.convert_alpha()
        self.blackenrect = self.blacken.get_rect(topleft = (0, 0))
        self.blacken.fill((0, 0, 0, 15))
        self.canpress = True

    def collision(self, pos):
        mx, my = pos
        if(mx >= self.rect.left and mx <= self.rect.right and my >= self.rect.top and my <= self.rect.bottom):
            return(True)
        return(False)

    def draw(self, colliding, clicking):
        self.image.fill((149, 143, 179))
        self.image.blit(self.textrendered, self.textrect)
        if(colliding):
            self.image.blit(self.blacken, self.blackenrect.topleft)
            if(clicking and self.canpress):
                self.image.blit(self.blacken, self.blackenrect.topleft)
                self.function()
                self.canpress = False
        if(not clicking):
            self.canpress = True

    def changetext(self, text):
        self.size = int(2*self.width/len(text))
        self.font = pygame.font.Font(None, self.size)
        self.text = text
        self.textrendered = self.font.render(self.text, False, "WHITE")
        self.textrect = self.textrendered.get_rect(center = (self.width//2, self.height//2))
    
    def function(self):
        pass

    def update(self):
        pass

class buttonfocusjulia(button):
    def __init__(self, x, y, width, height, text):
        super(buttonfocusjulia, self).__init__(x, y, width, height, text)

    def function(self):
        global focusjulia
        global juliazoom
        if(focusjulia):
            focusjulia = False
            self.changetext("Focus Julia")
            Image.open("set3.png").save("set.png")
            display.switch("set.png")
            reloadjulia()
        else:
            focusjulia = True
            self.changetext("Unfocus Julia")
            Image.open("set.png").save("set3.png")
            reloadmandelbrot()
            reloadjulia()

class buttonzoomjulia(button):
    def __init__(self, x, y, width, height, text):
        super(buttonzoomjulia, self).__init__(x, y, width, height, text)

    def function(self):
        global zoomjulia
        global juliazoom
        if(zoomjulia == False):
            zoomjulia = True
            juliazoom = zoom
            self.changetext("Unzoom Julia")
        else:
            zoomjulia = False
            juliazoom = 1
            self.changetext("Zoom Julia")
        reloadjulia()

class buttonreloadall(button):
    def __init__(self, x, y, width, height, text):
        super(buttonreloadall, self).__init__(x, y, width, height, text)

    def function(self):
        reloadmandelbrot()
        reloadjulia()

class buttonchangeiter(button):
    def __init__(self, x, y, width, height, text, amount):
        super(buttonchangeiter, self).__init__(x, y, width, height, text)
        self.amount = amount

    def function(self):
        global iteration
        iteration += self.amount
        if(iteration <= 0):
            iteration = 0
        iterdisplay.changetext("Iterate: "+str(iteration))

    def update(self):
        if(iteration < 500):
            if(iteration < 50):
                if(iteration < 20):
                    self.amount *= 1 / abs(self.amount)
                elif(iteration == 20):
                    if(self.amount / abs(self.amount) == -1):
                        self.amount = -1
                    else:
                        self.amount = 5
                else:
                    self.amount *= 5 / abs(self.amount)
            elif(iteration == 50):
                if(self.amount / abs(self.amount) == -1):
                    self.amount = -5
                else:
                    self.amount = 10
            else:
                self.amount *= 10 / abs(self.amount)
        elif(iteration == 500):
            if(self.amount / abs(self.amount) == -1):
                self.amount = -10
            else:
                self.amount = 100
        else:
            self.amount *= 100 / abs(self.amount)

        self.amount = int(self.amount)
        symbol = ""
        if(self.amount / abs(self.amount) == 1):
            symbol = "+"
        self.changetext(symbol+str(self.amount))

class buttonchangescheme(button):
    def __init__(self, x, y, width, height, text, amount):
        super(buttonchangescheme, self).__init__(x, y, width, height, text)
        self.amount = amount

    def function(self):
        global scheme
        scheme = schemes[(schemes.index(scheme)+self.amount)%len(schemes)]
        if(schemes.index(scheme) == 0):
            schemedisplay.changetext("Palette: Standard")
        elif(schemes.index(scheme) == 1):
            schemedisplay.changetext("Palette: Rose Gold")
        elif(schemes.index(scheme) == 2):
            schemedisplay.changetext("Palette: Ice & Fire")

class buttontoggleaxismode(button):
    def __init__(self, x, y, width, height, text):
        super(buttontoggleaxismode, self).__init__(x, y, width, height, text)

    def function(self):
        global axismode
        if(zoom == 1):
            if(not axismode):
                axismode = True
                self.changetext("Disable Axis Mode")
            else:
                axismode = False
                self.changetext("Enable Axis Mode")

    def update(self):
        if(zoom != 1):
            if(axismode):
                self.changetext("Axis Mode Locked On")
            else:
                self.changetext("Axis Mode Locked Off")

screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Mandelbrot Explorer")

clock = pygame.time.Clock()

schemes = [gradient([(50, 1, 51), (10, 72, 142), (60, 232, 126), (246, 255, 214)], 80) + gradient([(246, 255, 214), (235, 191, 59), (142, 40, 11), (50, 1, 51)], 80),
gradient([(55, 5, 50), (120, 55, 72), (172, 115, 100), (215, 182, 146), (252, 252, 212)], 80) + gradient([(252, 252, 212), (215, 182, 146), (172, 115, 100), (120, 55, 72), (55, 5, 50)], 80),
gradient([(48, 5, 56), (55, 48, 104), (45, 89, 148), (16, 131, 186), (0, 174, 215), (52, 196, 221), (93, 217, 224), (132, 238, 227), (165, 243, 223), (193, 247, 222), (217, 251, 227), (237, 255, 235)], 80) + gradient([(237, 255, 235), (225, 248, 208), (220, 240, 179), (220, 229, 147), (226, 217, 115), (228, 188, 90), (228, 159, 74), (224, 129, 66), (195, 83, 71), (153, 45, 74), (102, 18, 70), (48, 5, 56)], 80)]
scheme = schemes[0]
center = complex(0, 0)
zoom = 1
iteration = 300
zoomjulia = False
focusjulia = False
juliazoom = 1
axismode = False

Image.open("defaultset.png").save("set.png")
Image.open("defaultset2.png").save("set2.png")
display = setdisplay("set.png", 0, 0)
display2 = setdisplay("set2.png", 930, 0)
user = user()
dashboard = dashboard()
buttons = pygame.sprite.Group()
buttons.add(buttonfocusjulia(700, 0, 230, 70, "Focus Julia"))
buttons.add(buttonzoomjulia(700, 70, 300, 70, "Zoom Julia"))
buttons.add(buttonreloadall(700, 140, 300, 70, "Reload All"))
iterdisplay = textdisplay(750, 210, 200, 70, "Iterate: "+str(iteration))
buttons.add(buttonchangeiter(700, 210, 75, 70, "-10", -10))
buttons.add(buttonchangeiter(925, 210, 75, 70, "+10", 10))
schemedisplay = textdisplay(750, 280, 200, 70, "Palette: Standard")
buttons.add(buttonchangescheme(700, 280, 75, 70, "Prev", -1))
buttons.add(buttonchangescheme(925, 280, 75, 70, "Next", 1))
buttons.add(buttontoggleaxismode(700, 350, 300, 70, "Enable Axis Mode"))

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
    if(mousepos != None and mousepos[0] < 699 and focusjulia == False):
        user.move(mousepos)
        user.scale(wheelscroll)
        if(pygame.mouse.get_pressed()[0]):
            center, zoom = user.get_parameters(700, center, zoom, mousepos)
            if(zoomjulia):
                juliazoom = zoom
            reloadmandelbrot()
            reloadjulia()

    screen.blit(display.image, display.rect.topleft)
    if(focusjulia == False):
        screen.blit(user.image, user.rect.topleft)
    screen.blit(dashboard.image, dashboard.rect.topleft)
    screen.blit(display2.image, display2.rect.topleft)
    screen.blit(iterdisplay.image, iterdisplay.rect.topleft)
    iterdisplay.draw()
    screen.blit(schemedisplay.image, schemedisplay.rect.topleft)
    schemedisplay.draw()
    buttons.draw(screen)
    for button in buttons:
        if(mousepos != None):
            colliding = button.collision(mousepos)
        else:
            colliding = False
        button.update()
        button.draw(colliding, pygame.mouse.get_pressed()[0])

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()