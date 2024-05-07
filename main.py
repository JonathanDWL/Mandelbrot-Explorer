'''Sources:

How the Mandelbrot Set works: https://plus.maths.org/content/what-mandelbrot-set

Centering text on a surface: https://stackoverflow.com/questions/23982907/how-to-center-text-in-pygame

Help with creating color schemes: https://mycolor.space/gradient

'''

import pygame
import random
import sys
from PIL import Image

pygame.init()

def hextorgb(colors):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    list = []
    for i in range((len(colors) + 2)//9):
        color = colors[9*i:9*i+7]
        R = 16 * numbers.index(color[1].lower()) + numbers.index(color[2].lower())
        G = 16 * numbers.index(color[3].lower()) + numbers.index(color[4].lower())
        B = 16 * numbers.index(color[5].lower()) + numbers.index(color[6].lower())
        list.append((R, G, B))
    return(list)

def lerp(a, b, amount):
    return(a+amount*(b-a))

def lerpcolor(color1, color2, amount):
    R = int(lerp(color1[0], color2[0], amount))
    G = int(lerp(color1[1], color2[1], amount))
    B = int(lerp(color1[2], color2[2], amount))
    return((R, G, B))

def gradient(colors, steps):
    list = []
    colors.append("White")
    for i in range(steps):
        interp = i/steps*(len(colors)-2)
        index = int(interp)
        list.append(lerpcolor(colors[index], colors[index+1], interp-index))
    return(list)

def iterman(z, c, iterate):
    for i in range(iterate):
        z = z**2 + c
        if(abs(z) > 2):
            return(i)
    return(-1)

def itercubic(z, c, iterate):
    for i in range(iterate):
        z = z**3 + c
        if(abs(z) > 2**(1/2)):
            return(i)
    return(-1)

def iterquartic(z, c, iterate):
    for i in range(iterate):
        z = z**4 + c
        if(abs(z) > 2**(1/3)):
            return(i)
    return(-1)

def iterquintic(z, c, iterate):
    for i in range(iterate):
        z = z**5 + c
        if(abs(z) > 2**(1/4)):
            return(i)
    return(-1)

def itership(z, c, iterate):
    z = complex(z.real, -z.imag)
    c = complex(c.real, -c.imag)
    for i in range(iterate):
        z = complex(abs(z.real), abs(z.imag))**2 + c
        if(abs(z) > 2):
            return(i)
    return(-1)

def iterceltic(z, c, iterate):
    for i in range(iterate):
        z2 = z**2
        z = complex(abs(z2.real), z2.imag) + c
        if(abs(z) > 2):
            return(i)
    return(-1)

def iterbuffalo(z, c, iterate):
    z = complex(-z.real, z.imag)
    c = complex(-c.real, c.imag)
    for i in range(iterate):
        z2 = z**2
        z = complex(abs(z2.real), abs(z2.imag)) - c
        if(abs(z) > 2):
            return(i)
    return(-1)

def itertricorn(z, c, iterate):
    for i in range(iterate):
        z = complex(z.real, -z.imag)**2 + c
        if(abs(z) > 2):
            return(i)
    return(-1)

def iterburningbrot(z, c, iterate):
    z = complex(z.real, -z.imag)
    c = complex(c.real, -c.imag)
    for i in range(iterate):
        if(i % 2 == 0):
            z = complex(abs(z.real), abs(z.imag))**2 + c
        else:
            z = z**2 + c
        if(abs(z) > 2):
            return(i)
    return(-1)

def itermandelship(z, c, iterate):
    z = complex(z.real, -z.imag)
    c = complex(c.real, -c.imag)
    for i in range(iterate):
        if(i % 2 == 0):
            z = z**2 + c
        else:
            z = complex(abs(z.real), abs(z.imag))**2 + c
        if(abs(z) > 2):
            return(i)
    return(-1)

def gensetmain(res, iter, center, zoom, cols, func):
    if(center.imag == 0 and fractal in ["Mandelbrot Set", "Cubic Mandelbrot", "Quartic Mandelbrot", "Quintic Mandelbrot", "Celtic Fractal", "Mandelbar Tricorn"]):
        return(gensetmainaxis(res, iter, center.real, zoom, cols, func))
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*(2/zoom)+center.real, (y-halfres)/halfres*(-2/zoom)+center.imag)
            numS = func(0, num, iter)
            if(numS < 0):
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = cols[numS%len(cols)]
    return(canvas)

def gensetmainaxis(res, iter, center, zoom, cols, func):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            if(y <= -(-res//2)-1):
                halfres = res/2-0.5
                num = complex((x-halfres)/halfres*(2/zoom)+center, (y-halfres)/halfres*(-2/zoom))
                numS = func(0, num, iter)
                if(numS < 0):
                    pixels[x,y] = (0, 0, 0)
                else:
                    pixels[x,y] = cols[numS%len(cols)]
            else:
                pixels[x,y] = pixels[x,-1-y]
    return(canvas)

def gensetjulia(res, iter, center, zoom, cols, func):
    if(zoomjulia):
        center2 = center
    else:
        center2 = 0
        zoom = 1
    if(center2 == 0 and fractal in ["Burning Ship", "Buffalo Fractal", "Burningbrot Hybrid"]):
        return(gensetjuliacross(res, iter, center, zoom, cols, func))
    elif(center2 == 0 and fractal in ["Mandelbrot Set", "Quartic Mandelbrot", "Celtic Fractal", "Mandelbar Tricorn", "Mandelship Hybrid"]):
        return(gensetjuliaorigin(res, iter, center, zoom, cols, func))
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*(2/zoom)+center2.real, (y-halfres)/halfres*(-2/zoom)+center2.imag)
            numS = func(num, center, iter)
            if(numS < 0):
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = cols[numS%len(cols)]
    return(canvas)

def gensetjuliacross(res, iter, center, zoom, cols, func):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        if(x <= -(-res//2)-1):
            for y in range(res):
                if(y <= -(-res//2)-1):
                    halfres = res/2-0.5
                    num = complex((x-halfres)/halfres*(2/zoom), (y-halfres)/halfres*(-2/zoom))
                    numS = func(num, center, iter)
                    if(numS < 0):
                        pixels[x,y] = (0, 0, 0)
                    else:
                        pixels[x,y] = cols[numS%len(cols)]
                else:
                    pixels[x,y] = pixels[x,-1-y]
        else:
            for y in range(res):
                pixels[x,y] = pixels[-1-x,y]
    return(canvas)

def gensetjuliaorigin(res, iter, center, zoom, cols, func):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            if(x <= -(-res//2)-1):
                halfres = res/2-0.5
                num = complex((x-halfres)/halfres*(2/zoom), (y-halfres)/halfres*(-2/zoom))
                numS = func(num, center, iter)
                if(numS < 0):
                    pixels[x,y] = (0, 0, 0)
                else:
                    pixels[x,y] = cols[numS%len(cols)]
            else:
                pixels[x,y] = pixels[-1-x,-1-y]
    return(canvas)

def getfunction(fractal):
    if(fractal == "Mandelbrot Set"):
        return(iterman)
    elif(fractal == "Cubic Mandelbrot"):
        return(itercubic)
    elif(fractal == "Quartic Mandelbrot"):
        return(iterquartic)
    elif(fractal == "Quintic Mandelbrot"):
        return(iterquintic)
    elif(fractal == "Burning Ship"):
        return(itership)
    elif(fractal == "Celtic Fractal"):
        return(iterceltic)
    elif(fractal == "Buffalo Fractal"):
        return(iterbuffalo)
    elif(fractal == "Mandelbar Tricorn"):
        return(itertricorn)
    elif(fractal == "Burningbrot Hybrid"):
        return(iterburningbrot)
    elif(fractal == "Mandelship Hybrid"):
        return(itermandelship)

def reloadmain():
    func = getfunction(fractal)
    if(focusjulia == False):
        gensetmain(700, iteration, center, zoom, scheme, func).save("set.png")
        display.switch("set.png")
    else:
        gensetmain(70, iteration, center, zoom, scheme, func).save("set2.png")
        display2.switch("set2.png")
        gensetmain(700, iteration, center, zoom, scheme, func).save("set3.png")

def reloadjulia():
    func = getfunction(fractal)
    if(focusjulia == False):
        gensetjulia(70, iteration, center, zoom, scheme, func).save("set2.png")
        display2.switch("set2.png")
    else:
        gensetjulia(700, iteration, center, zoom, scheme, func).save("set.png")
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
        self.image = pygame.Surface((self.size+4, self.size+4), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (0, 0, 0, 64), (0, 0, self.size+4, self.size+4), 6)
        pygame.draw.rect(self.image, "WHITE", (2, 2, self.size, self.size), 2)
        self.rect = self.image.get_rect(center = (9999, 9999))

    def move(self, pos):
        if(pos != None):
            mx, my = pos
            if(not reallock):
                self.rect.centerx = mx
            else:
                self.rect.centerx = 350
            if(not imaglock):
                self.rect.centery = my
            else:
                self.rect.centery = 350

    def scale(self, scroll):
        self.size += scroll * -10
        if(self.size < 35):
            self.size = 35
        elif(self.size > 14000):
            self.size = 14000
        self.image = pygame.Surface((self.size+4, self.size+4), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (0, 0, 0, 64), (0, 0, self.size+4, self.size+4), 6)
        pygame.draw.rect(self.image, "WHITE", (2, 2, self.size, self.size), 2)
        self.rect = self.image.get_rect(center = self.rect.center)

    def get_parameters(self, res, center, zoom, pos):
        halfres = res/2-0.5
        mx, my = pos
        newcenter = complex((mx-halfres)/halfres*(2/zoom)+center.real, (my-halfres)/halfres*(-2/zoom)+center.imag)
        if(reallock):
            newcenter = complex(center.real, newcenter.imag)
        if(imaglock):
            newcenter = complex(newcenter.real, center.imag)
        newzoom = zoom * res/self.size
        return(newcenter, newzoom)

class userghost(pygame.sprite.Sprite):
    def __init__(self):
        super(userghost, self).__init__()
        self.size = 350
        self.image = pygame.Surface((self.size+4, self.size+4), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 255, 255, 64), (0, 0, self.size+4, self.size+4), 6)
        pygame.draw.rect(self.image, "BLACK", (2, 2, self.size, self.size), 2)
        self.rect = self.image.get_rect(center = (9999, 9999))

    def move(self, pos, scale):
        px, py = pos
        self.rect.centerx = px
        self.rect.centery = py

    def scale(self, scale):
        self.size = 490000 / scale
        self.image = pygame.Surface((self.size+4, self.size+4), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 255, 255, 64), (0, 0, self.size+4, self.size+4), 6)
        pygame.draw.rect(self.image, "BLACK", (2, 2, self.size, self.size), 2)
        self.rect = self.image.get_rect(center = self.rect.center)
    
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
    
class textdisplay2(pygame.sprite.Sprite):
    def __init__(self, x, y, size, text):
        super(textdisplay2, self).__init__()
        self.x = x
        self.y = y
        self.size = size
        self.font = pygame.font.Font(None, self.size)
        self.text = text
        self.textprerendered = self.font.render(self.text, False, "WHITE")
        self.excess = self.size - self.textprerendered.get_size()[1]
        self.textrendered = pygame.Surface((self.textprerendered.get_size()[0]+self.excess, self.size), pygame.SRCALPHA, 32)
        self.textrendered.convert_alpha()
        self.textrendered.fill((0, 0, 0, 64))
        self.textrendered.blit(self.textprerendered, (self.excess/2, self.excess/2))
        self.textrect = self.textrendered.get_rect(topleft = (self.x, self.y))

    def changetext(self, text):
        self.font = pygame.font.Font(None, self.size)
        self.text = text
        self.textprerendered = self.font.render(self.text, False, "WHITE")
        self.excess = self.size - self.textprerendered.get_size()[1]
        self.textrendered = pygame.Surface((self.textprerendered.get_size()[0]+self.excess, self.size), pygame.SRCALPHA, 32)
        self.textrendered.convert_alpha()
        self.textrendered.fill((0, 0, 0, 64))
        self.textrendered.blit(self.textprerendered, (self.excess/2, self.excess/2))
        self.textrect = self.textrendered.get_rect(topleft = (self.x, self.y))

    def returninfo(self):
        return(self.textrendered, self.textrect)

class textdisplay3(pygame.sprite.Sprite):
    def __init__(self, x, y, size, text):
        super(textdisplay3, self).__init__()
        self.x = x
        self.y = y
        self.size = size
        self.font = pygame.font.Font(None, self.size)
        self.text = text
        self.textprerendered = self.font.render(self.text, False, "WHITE")
        self.excess = self.size - self.textprerendered.get_size()[1]
        self.textrendered = pygame.Surface((self.textprerendered.get_size()[0]+self.excess, self.size), pygame.SRCALPHA, 32)
        self.textrendered.convert_alpha()
        self.textrendered.fill((0, 0, 0, 192))
        self.textrendered.blit(self.textprerendered, (self.excess/2, self.excess/2))
        self.textrect = self.textrendered.get_rect(center = (self.x, self.y))

    def changetext(self, text):
        self.font = pygame.font.Font(None, self.size)
        self.text = text
        self.textprerendered = self.font.render(self.text, False, "WHITE")
        self.excess = self.size - self.textprerendered.get_size()[1]
        self.textrendered = pygame.Surface((self.textprerendered.get_size()[0]+self.excess, self.size), pygame.SRCALPHA, 32)
        self.textrendered.convert_alpha()
        self.textrendered.fill((0, 0, 0, 192))
        self.textrendered.blit(self.textprerendered, (self.excess/2, self.excess/2))
        self.textrect = self.textrendered.get_rect(center = (self.x, self.y))

    def returninfo(self):
        return(self.textrendered, self.textrect)

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
            reloadmain()
            reloadjulia()

class buttonzoomjulia(button):
    def __init__(self, x, y, width, height, text):
        super(buttonzoomjulia, self).__init__(x, y, width, height, text)

    def function(self):
        global zoomjulia
        if(zoomjulia == False):
            zoomjulia = True
            self.changetext("Unzoom Julia")
        else:
            zoomjulia = False
            self.changetext("Zoom Julia")
        reloadjulia()

    def update(self):
        if(zoomjulia):
            self.changetext("Unzoom Julia")
        else:
            self.changetext("Zoom Julia")

class buttonreloadall(button):
    def __init__(self, x, y, width, height, text):
        super(buttonreloadall, self).__init__(x, y, width, height, text)

    def function(self):
        reloadmain()
        reloadjulia()
        info.updateclick()

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
        schemedisplay.changetext("Palette: "+schemenames[schemes.index(scheme)])

class buttonchangefractal(button):
    def __init__(self, x, y, width, height, text, amount):
        super(buttonchangefractal, self).__init__(x, y, width, height, text)
        self.amount = amount

    def function(self):
        global fractal
        fractal = fractals[(fractals.index(fractal)+self.amount)%len(fractals)]
        fractalnamedisplay.changetext(fractal)

class buttontogglereallock(button):
    def __init__(self, x, y, width, height, text):
        super(buttontogglereallock, self).__init__(x, y, width, height, text)

    def function(self):
        global reallock
        if(not reallock):
            reallock = True
            self.changetext("Unlock Real")
        else:
            reallock = False
            self.changetext("Lock Real")
    
    def update(self):
        if(reallock):
            self.changetext("Unlock Real")
        else:
            self.changetext("Lock Real")

class buttontoggleimaglock(button):
    def __init__(self, x, y, width, height, text):
        super(buttontoggleimaglock, self).__init__(x, y, width, height, text)

    def function(self):
        global imaglock
        if(not imaglock):
            imaglock = True
            self.changetext("Unlock Imag")
        else:
            imaglock = False
            self.changetext("Lock Imag")

    def update(self):
        if(imaglock):
            self.changetext("Unlock Imag")
        else:
            self.changetext("Lock Imag")

class buttontoggleviewmode(button):
    def __init__(self, x, y, width, height, text):
        super(buttontoggleviewmode, self).__init__(x, y, width, height, text)

    def function(self):
        global viewmode
        if(not viewmode):
            viewmode = True
            self.changetext("Disable View Mode")
        elif(viewmode):
            viewmode = False
            self.changetext("Enable View Mode")

class infodisplay(pygame.sprite.Sprite):
    def __init__(self):
        super(infodisplay, self).__init__()
        self.image = pygame.Surface((700, 700), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.frac = textdisplay2(10, 10, 25, "Fractal: "+fractal)
        self.center = textdisplay2(10, 35, 25, "Center: "+str(center.real)+" + "+str(center.imag)+"i")
        self.zoom = textdisplay2(10, 60, 25, "Zoom: "+str(zoom))
        self.iter = textdisplay2(10, 85, 25, "Iteration: "+str(iteration))
        self.newcenter = textdisplay2(10, 110, 25, "Projected Center: "+str(center.real)+" + "+str(center.imag)+"i")
        self.newzoom = textdisplay2(10, 135, 25, "Projected Zoom: "+str(zoom))

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.center.returninfo()[0], self.center.returninfo()[1])
        self.image.blit(self.frac.returninfo()[0], self.frac.returninfo()[1])
        self.image.blit(self.zoom.returninfo()[0], self.zoom.returninfo()[1])
        self.image.blit(self.iter.returninfo()[0], self.iter.returninfo()[1])
        self.image.blit(self.newcenter.returninfo()[0], self.newcenter.returninfo()[1])
        self.image.blit(self.newzoom.returninfo()[0], self.newzoom.returninfo()[1])

    def updateclick(self):
        self.frac.changetext("Fractal: "+fractal)
        self.center.changetext("Center: "+str(center.real)+" + "+str(center.imag)+"i")
        self.zoom.changetext("Zoom: "+str(zoom))
        self.iter.changetext("Iteration: "+str(iteration))

    def updatestep(self):
        try:
            newcenter, newzoom = user.get_parameters(700, center, zoom, mousepos)
            if(mousepos[0] >= 699 or focusjulia):
                newzoom = 1/0
            self.newcenter.changetext("Projected Center: "+str(newcenter.real)+" + "+str(newcenter.imag)+"i")
            self.newzoom.changetext("Projected Zoom: "+str(newzoom))
        except:
            pass

class buttonsaveimage(button):
    def __init__(self, x, y, width, height, text):
        super(buttonsaveimage, self).__init__(x, y, width, height, text)

    def function(self):
        screen.blit(checkconsole.returninfo()[0], checkconsole.returninfo()[1])
        pygame.display.flip()
        while(True):
            dosave = input("Save an image? (Y/N): ").upper()
            if(dosave == "Y"):
                break
            elif(dosave == "N"):
                return()
            else:
                print("Invalid answer; try again.")
        Image.open("set.png").save("savebuffer.png")
        while(True):
            rerender = input("Keep the image in its current resolution? (Y/N): ").upper()
            if(rerender == "Y"):
                rerenderbool = False
                break
            elif(rerender == "N"):
                rerenderbool = True
                break
            else:
                print("Invalid answer; try again.")
        res = 700
        if(rerenderbool):
            while(True):
                try:
                    res = int(input("Enter new resolution (single integer): "))
                    break
                except:
                    print("Invalid resolution; try again.")
            func = getfunction(fractal)
            print("Rendering...")
            if(focusjulia == False):
                gensetmain(res, iteration, center, zoom, scheme, func).save("savebuffer.png")
            else:
                gensetjulia(res, iteration, center, zoom, scheme, func).save("savebuffer.png")
        name = input("Enter a name for the image file (do not include extension): ")
        while(True):
            try:
                path = input("Enter a filepath for the image file (type 'prev' to use previous path): ")
                if(path.lower() == "prev"):
                    savepath = open("savepath.txt", "r")
                    path = savepath.read()
                    savepath.close()
                else:
                    savepath = open("savepath.txt", "w")
                    savepath.write(path)
                    savepath.close()
                Image.open("savebuffer.png").save(path+"/"+name+".png")
                print("Image saved at "+path+".")
                break
            except:
                print("Invalid filepath; try again.")

class buttonresetzoom(button):
    def __init__(self, x, y, width, height, text):
        super(buttonresetzoom, self).__init__(x, y, width, height, text)

    def function(self):
        global center
        global zoom
        global iteration
        global zoomjulia
        global reallock
        global imaglock
        center = complex(0, 0)
        zoom = 1
        iteration = 300
        zoomjulia = False
        reallock = False
        imaglock = False
        reloadmain()
        reloadjulia()
        iterdisplay.changetext("Iterate: "+str(iteration))
        info.updateclick()

screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Fractal Explorer")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

"#321c1a, #532e26, #754330, #955b38, #b4763e, #c28947, #cf9c52, #dbb05d, #debd70, #e2ca83, #e6d698, #ebe2ac"
"#ebe2ac, #d4d495, #bac781, #9fbb6e, #81ae5e, #6ba056, #55924f, #3f8448, #327243, #27603d, #1f4e36, #1a3d2d"

schemes = [gradient([(50, 1, 51), (10, 72, 142), (60, 232, 126), (246, 255, 214)], 80) + gradient([(246, 255, 214), (235, 191, 59), (142, 40, 11), (50, 1, 51)], 80),
gradient([(55, 5, 50), (120, 55, 72), (172, 115, 100), (215, 182, 146), (252, 252, 212)], 80) + gradient([(252, 252, 212), (215, 182, 146), (172, 115, 100), (120, 55, 72), (55, 5, 50)], 80),
gradient([(48, 5, 56), (55, 48, 104), (45, 89, 148), (16, 131, 186), (0, 174, 215), (52, 196, 221), (93, 217, 224), (132, 238, 227), (165, 243, 223), (193, 247, 222), (217, 251, 227), (237, 255, 235)], 80) + gradient([(237, 255, 235), (225, 248, 208), (220, 240, 179), (220, 229, 147), (226, 217, 115), (228, 188, 90), (228, 159, 74), (224, 129, 66), (195, 83, 71), (153, 45, 74), (102, 18, 70), (48, 5, 56)], 80),
gradient([(45, 7, 112), (0, 63, 153), (0, 102, 172), (0, 136, 176), (0, 168, 174), (63, 186, 172), (105, 202, 169), (145, 218, 165), (176, 226, 173), (203, 233, 186), (227, 241, 201), (246, 250, 220)], 80) + gradient([(246, 250, 220), (237, 224, 183), (233, 195, 151), (230, 165, 129), (224, 133, 117), (213, 108, 112), (198, 83, 112), (179, 60, 115), (154, 38, 114), (125, 19, 114), (91, 7, 114), (45, 7, 112)], 80),
gradient([(247, 87, 129), (247, 177, 101)], 20) + gradient([(247, 177, 101), (242, 250, 130)], 20) + gradient([(242, 250, 130), (101, 247, 106)], 20) + gradient([(101, 247, 106), (101, 247, 242)], 20) + gradient([(101, 247, 242), (87, 98, 247)], 20) + gradient([(87, 98, 247), (233, 109, 247)], 20) + gradient([(233, 109, 247), (247, 87, 129)], 20),
gradient([(102, 7, 75), (247, 87, 129)], 80) + gradient([(247, 87, 129), (102, 7, 7)], 80) + gradient([(102, 7, 7), (247, 177, 101)], 80) + gradient([(247, 177, 101), (102, 78, 7)], 80) + gradient([(102, 78, 7), (242, 250, 130)], 80) + gradient([(242, 250, 130), (43, 102, 7)], 80) + gradient([(43, 102, 7), (101, 247, 106)], 80) + gradient([(101, 247, 106), (50, 168, 117)], 80) + gradient([(50, 168, 117), (101, 247, 242)], 80) + gradient([(101, 247, 242), (7, 53, 102)], 80) + gradient([(7, 53, 102), (87, 98, 247)], 80) + gradient([(87, 98, 247), (53, 7, 102)], 80) + gradient([(53, 7, 102), (233, 109, 247)], 80) + gradient([(233, 109, 247), (102, 7, 75)], 80),
gradient([(24, 19, 57), (33, 22, 63), (41, 24, 69), (51, 26, 74), (60, 28, 79), (90, 34, 88), (119, 40, 94), (148, 49, 96), (196, 75, 92), (230, 113, 81), (249, 160, 71), (249, 211, 74)], 80) + gradient([(249, 211, 74), (184, 194, 75), (128, 172, 84), (82, 148, 91), (48, 121, 92), (15, 105, 94), (0, 88, 90), (0, 71, 82), (0, 59, 81), (0, 47, 77), (4, 34, 70), (24, 19, 57)], 80),
gradient([(91, 40, 102), (158, 69, 103), (202, 118, 104), (225, 174, 122), (233, 233, 167)], 80) + gradient([(233, 233, 167), (174, 196, 137), (119, 158, 112), (68, 121, 88), (12, 85, 66)], 80) + gradient([(12, 85, 66), (31, 115, 108), (62, 145, 152), (101, 175, 195), (146, 205, 236)], 80) + gradient([(146, 205, 236), (117, 165, 211), (102, 125, 182), (96, 83, 145), (91, 40, 102)], 80)]
scheme = schemes[0]
schemenames = ["Standard", "Rose Gold", "Ice & Fire", "Plant Life", "Rainbow 1", "Rainbow 2", "Space Magic", "Sunrise"]
center = complex(0, 0)
zoom = 1
iteration = 300
zoomjulia = False
focusjulia = False
reallock = False
imaglock = False
fractals = ["Mandelbrot Set", "Cubic Mandelbrot", "Quartic Mandelbrot", "Quintic Mandelbrot", "Burning Ship", "Celtic Fractal", "Buffalo Fractal", "Mandelbar Tricorn", "Burningbrot Hybrid", "Mandelship Hybrid"]
fractal = fractals[0]
viewmode = False

Image.open("defaultset.png").save("set.png")
Image.open("defaultset2.png").save("set2.png")
display = setdisplay("set.png", 0, 0)
display2 = setdisplay("set2.png", 930, 0)
user = user()
userghost = userghost()
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
fractalnamedisplay = textdisplay(750, 350, 200, 70, "Mandelbrot Set")
buttons.add(buttonchangefractal(700, 350, 75, 70, "Prev", -1))
buttons.add(buttonchangefractal(925, 350, 75, 70, "Next", 1))
buttons.add(buttontogglereallock(700, 420, 150, 70, "Lock Real"))
buttons.add(buttontoggleimaglock(850, 420, 150, 70, "Lock Imag"))
buttons.add(buttontoggleviewmode(700, 490, 300, 70, "Enable View Mode"))
info = infodisplay()
buttons.add(buttonsaveimage(700, 560, 300, 70, "Save Image"))
checkconsole = textdisplay3(500, 350, 100, "Check Console Window")
buttons.add(buttonresetzoom(700, 630, 300, 70, "Reset Zoom"))

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
    if(mousepos != None and mousepos[0] < 699 and focusjulia == False and viewmode == False):
        user.move(mousepos)
        user.scale(wheelscroll)
        userghost.move((user.rect.centerx, user.rect.centery), user.size)
        userghost.scale(user.size)
        if(pygame.mouse.get_pressed()[0]):
            center, zoom = user.get_parameters(700, center, zoom, mousepos)
            reloadmain()
            reloadjulia()
            info.updateclick()

    screen.blit(display.image, display.rect.topleft)
    if(focusjulia == False and viewmode == False):
        screen.blit(userghost.image, userghost.rect.topleft)
        screen.blit(user.image, user.rect.topleft)
    screen.blit(dashboard.image, dashboard.rect.topleft)
    screen.blit(display2.image, display2.rect.topleft)
    screen.blit(iterdisplay.image, iterdisplay.rect.topleft)
    iterdisplay.draw()
    screen.blit(schemedisplay.image, schemedisplay.rect.topleft)
    schemedisplay.draw()
    screen.blit(fractalnamedisplay.image, fractalnamedisplay.rect.topleft)
    fractalnamedisplay.draw()
    buttons.draw(screen)
    if(not viewmode):
        screen.blit(info.image, info.rect.topleft)
        info.draw()
        info.updatestep()
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