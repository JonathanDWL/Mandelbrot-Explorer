'''https://mycolor.space/gradient'''

import pygame
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

def transform(z, c):
    if(fractal in ["Burning Ship", "Buffalo Fractal", "Burningbrot Hybrid", "Mandelship Hybrid"]):
        z = complex(z.real, -z.imag)
        c = complex(c.real, -c.imag)
    return(z, c)

def findradius():
    if(fractal not in ["Cubic Mandelbrot", "Quartic Mandelbrot", "Quintic Mandelbrot"]):
        return(2)
    elif(fractal == "Cubic Mandelbrot"):
        return(2**(1/2))
    elif(fractal == "Quartic Mandelbrot"):
        return(2**(1/3))
    elif(fractal == "Quintic Mandelbrot"):
        return(2**(1/4))

def escapetime(z, c, iterate, func):
    z, c = transform(z, c)
    radius = findradius()
    for i in range(iterate):
        z = func(z, c, i)
        if(abs(z) > radius):
            return(i)
    return(-1)

def pointtrap(z, c, iterate, func):
    z, c = transform(z, c)
    radius = findradius()
    mindist = 9999
    for i in range(iterate):
        z = func(z, c, i)
        dist = abs(z)
        if(dist < mindist):
            mindist = dist
        if(abs(z) > radius):
            return(int(mindist * 200))
    if(not trapvoid):
        return(int(mindist * 200))
    return(-1)

def ringtrap(z, c, iterate, func):
    z, c = transform(z, c)
    radius = findradius()
    mindist = 9999
    for i in range(iterate):
        z = func(z, c, i)
        dist = abs(abs(z) - 1)
        if(dist < mindist):
            mindist = dist
        if(abs(z) > radius):
            return(int(mindist * 200))
    if(not trapvoid):
        return(int(mindist * 200))
    return(-1)

def fourpointtrap(z, c, iterate, func):
    z, c = transform(z, c)
    radius = 2.5
    mindist = 9999
    for i in range(iterate):
        z = func(z, c, i)
        dist = min(abs(z + complex(1, 1)), abs(z + complex(-1, 1)), abs(z + complex(1, -1)), abs(z + complex(-1, -1)))
        if(dist < mindist):
            mindist = dist
        if(abs(z) > radius):
            return(int(mindist * 200))
    if(not trapvoid):
        return(int(mindist * 200))
    return(-1)

def fourringtrap(z, c, iterate, func):
    z, c = transform(z, c)
    radius = 2**(1/2) + 1
    mindist = 9999
    for i in range(iterate):
        z = func(z, c, i)
        dist = min(abs(abs(z + complex(1, 1)) - 1), abs(abs(z + complex(-1, 1)) - 1), abs(abs(z + complex(1, -1)) - 1), abs(abs(z + complex(-1, -1)) - 1))
        if(dist < mindist):
            mindist = dist
        if(abs(z) > radius):
            return(int(mindist * 200))
    if(not trapvoid):
        return(int(mindist * 200))
    return(-1)

def xtrap(z, c, iterate, func):
    z, c = transform(z, c)
    radius = 2.5
    mindist = 9999
    for i in range(iterate):
        z = func(z, c, i)
        if(z.real + z.imag < 4 and -z.real + z.imag < 4 and z.real - z.imag < 4 and -z.real - z.imag < 4):
            dist = min(abs(z.real - z.imag) * 2**(1/2)/2, abs(z.real + z.imag) * 2**(1/2)/2)
        else:
            dist = min(abs(z + complex(2, 2)), abs(z + complex(-2, 2)), abs(z + complex(2, -2)), abs(z + complex(-2, -2)))
        if(dist < mindist):
            mindist = dist
        if(abs(z) > radius):
            return(int(mindist * 200))
    if(not trapvoid):
        return(int(mindist * 200))
    return(-1)

def imagetrap(z, c, iterate, func):
    z, c = transform(z, c)
    radius = findradius()
    mindist = (9999, complex(9999, 9999), 0)
    for i in range(iterate):
        z = func(z, c, i)
        dist = abs(z)
        if(dist < mindist[0]):
            mindist = (dist, z, i)
        if(abs(z) > radius):
            return(mindist[1], mindist[2])
    if(not trapvoid):
        return(mindist[1], mindist[2])
    return(None, 0)

def iterman(z, c, i):
    return(z**2 + c)

def itercubic(z, c, i):
    return(z**3 + c)

def iterquartic(z, c, i):
    return(z**4 + c)

def iterquintic(z, c, i):
    return(z**5 + c)

def itership(z, c, i):
    return(complex(abs(z.real), abs(z.imag))**2 + c)

def iterceltic(z, c, i):
    z2 = z**2
    return(complex(abs(z2.real), z2.imag) + c)

def iterbuffalo(z, c, i):
    z2 = z**2
    return(complex(abs(z2.real), abs(z2.imag)) + c)

def itertricorn(z, c, i):
    return(complex(z.real, -z.imag)**2 + c)

def iterburningbrot(z, c, i):
    if(i % 2 == 0):
        return(itership(z, c, i))
    else:
        return(iterman(z, c, i))

def itermandelship(z, c, i):
    if(i % 2 == 0):
        return(iterman(z, c, i))
    else:
        return(itership(z, c, i))

def gensetmain(res, iter, center, zoom, cols, funcf, funcm):
    if(funcm == imagetrap):
        return(gensetmainimage(res, iter, center, zoom, cols, funcf))
    if(center.imag == 0 and fractal in ["Mandelbrot Set", "Cubic Mandelbrot", "Quartic Mandelbrot", "Quintic Mandelbrot", "Celtic Fractal", "Mandelbar Tricorn"]):
        return(gensetmainaxis(res, iter, center.real, zoom, cols, funcf, funcm))
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*(2/zoom)+center.real, (y-halfres)/halfres*(-2/zoom)+center.imag)
            numS = funcm(0, num, iter, funcf)
            if(numS < 0):
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = cols[numS%len(cols)]
    return(canvas)

def gensetmainaxis(res, iter, center, zoom, cols, funcf, funcm):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            if(y <= -(-res//2)-1):
                halfres = res/2-0.5
                num = complex((x-halfres)/halfres*(2/zoom)+center, (y-halfres)/halfres*(-2/zoom))
                numS = funcm(0, num, iter, funcf)
                if(numS < 0):
                    pixels[x,y] = (0, 0, 0)
                else:
                    pixels[x,y] = cols[numS%len(cols)]
            else:
                pixels[x,y] = pixels[x,-1-y]
    return(canvas)

def gensetmainimage(res, iter, center, zoom, cols, funcf):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    image = Image.open("imagetrapimage.jpg")
    imagepixels = image.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*(2/zoom)+center.real, (y-halfres)/halfres*(-2/zoom)+center.imag)
            numP, numS = imagetrap(0, num, iter, funcf)
            if(numP == None):
                pixels[x,y] = (0, 0, 0)
            else:
                imgx = int((numP.real/4+1/2)*image.size[0])
                imgy = int((-numP.imag/4+1/2)*image.size[1])
                imgxl = imgx%image.size[0]
                if(imgx//image.size[0]%2 == 1):
                    imgxl *= -1
                imgyl = imgy%image.size[1]
                if(imgy//image.size[1]%2 == 1):
                    imgyl *= -1
                if(numS%2 == 1):
                    imgxl *= -1
                    imgyl *= -1
                pixels[x,y] = imagepixels[imgxl,imgyl]
    return(canvas)

def gensetjulia(res, iter, center, zoom, cols, funcf, funcm):
    if(funcm == imagetrap):
        return(gensetjuliaimage(res, iter, center, zoom, cols, funcf))
    if(zoomjulia):
        center2 = center
    else:
        center2 = 0
        zoom = 1
    if(center2 == 0 and fractal in ["Burning Ship", "Buffalo Fractal", "Burningbrot Hybrid"]):
        return(gensetjuliacross(res, iter, center, zoom, cols, funcf, funcm))
    elif(center2 == 0 and fractal in ["Mandelbrot Set", "Quartic Mandelbrot", "Celtic Fractal", "Mandelbar Tricorn", "Mandelship Hybrid"]):
        return(gensetjuliaorigin(res, iter, center, zoom, cols, funcf, funcm))
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*(2/zoom)+center2.real, (y-halfres)/halfres*(-2/zoom)+center2.imag)
            numS = funcm(num, center, iter, funcf)
            if(numS < 0):
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = cols[numS%len(cols)]
    return(canvas)

def gensetjuliacross(res, iter, center, zoom, cols, funcf, funcm):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        if(x <= -(-res//2)-1):
            for y in range(res):
                if(y <= -(-res//2)-1):
                    halfres = res/2-0.5
                    num = complex((x-halfres)/halfres*(2/zoom), (y-halfres)/halfres*(-2/zoom))
                    numS = funcm(num, center, iter, funcf)
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

def gensetjuliaorigin(res, iter, center, zoom, cols, funcf, funcm):
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    for x in range(res):
        for y in range(res):
            if(x <= -(-res//2)-1):
                halfres = res/2-0.5
                num = complex((x-halfres)/halfres*(2/zoom), (y-halfres)/halfres*(-2/zoom))
                numS = funcm(num, center, iter, funcf)
                if(numS < 0):
                    pixels[x,y] = (0, 0, 0)
                else:
                    pixels[x,y] = cols[numS%len(cols)]
            else:
                pixels[x,y] = pixels[-1-x,-1-y]
    return(canvas)

def gensetjuliaimage(res, iter, center, zoom, cols, funcf):
    if(zoomjulia):
        center2 = center
    else:
        center2 = 0
        zoom = 1
    canvas = Image.new(mode="RGB", size=(res, res), color="WHITE")
    pixels = canvas.load()
    image = Image.open("imagetrapimage.jpg")
    imagepixels = image.load()
    for x in range(res):
        for y in range(res):
            halfres = res/2-0.5
            num = complex((x-halfres)/halfres*(2/zoom)+center2.real, (y-halfres)/halfres*(-2/zoom)+center2.imag)
            numP, numS = imagetrap(0, num, iter, funcf)
            if(numP == None):
                pixels[x,y] = (0, 0, 0)
            else:
                imgx = int((numP.real/4+1/2)*image.size[0])
                imgy = int((-numP.imag/4+1/2)*image.size[1])
                imgxl = imgx%image.size[0]
                if(imgx//image.size[0]%2 == 1):
                    imgxl *= -1
                imgyl = imgy%image.size[1]
                if(imgy//image.size[1]%2 == 1):
                    imgyl *= -1
                if(numS%2 == 1):
                    imgxl *= -1
                    imgyl *= -1
                pixels[x,y] = imagepixels[imgxl,imgyl]
    return(canvas)

def getfunctions():
    if(fractal == "Mandelbrot Set"):
        funcf = iterman
    elif(fractal == "Cubic Mandelbrot"):
        funcf = itercubic
    elif(fractal == "Quartic Mandelbrot"):
        funcf = iterquartic
    elif(fractal == "Quintic Mandelbrot"):
        funcf = iterquintic
    elif(fractal == "Burning Ship"):
        funcf = itership
    elif(fractal == "Celtic Fractal"):
        funcf = iterceltic
    elif(fractal == "Buffalo Fractal"):
        funcf = iterbuffalo
    elif(fractal == "Mandelbar Tricorn"):
        funcf = itertricorn
    elif(fractal == "Burningbrot Hybrid"):
        funcf = iterburningbrot
    elif(fractal == "Mandelship Hybrid"):
        funcf = itermandelship
    if(mode == "Escape Time"):
        funcm = escapetime
    elif(mode == "Point Trap"):
        funcm = pointtrap
    elif(mode == "Ring Trap"):
        funcm = ringtrap
    elif(mode == "Four Point Trap"):
        funcm = fourpointtrap
    elif(mode == "Four Ring Trap"):
        funcm = fourringtrap
    elif(mode == "X Trap"):
        funcm = xtrap
    elif(mode == "Image Trap"):
        funcm = imagetrap
    return(funcf, funcm)

def reloadmain():
    funcf, funcm = getfunctions()
    if(focusjulia == False):
        gensetmain(700, iteration, center, zoom, scheme, funcf, funcm).save("set.png")
        display.switch("set.png")
    else:
        gensetmain(70, iteration, center, zoom, scheme, funcf, funcm).save("set2.png")
        display2.switch("set2.png")
        gensetmain(700, iteration, center, zoom, scheme, funcf, funcm).save("set3.png")

def reloadjulia():
    funcf, funcm = getfunctions()
    if(focusjulia == False):
        gensetjulia(70, iteration, center, zoom, scheme, funcf, funcm).save("set2.png")
        display2.switch("set2.png")
    else:
        gensetjulia(700, iteration, center, zoom, scheme, funcf, funcm).save("set.png")
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
        self.visualsize = 350
        self.image = pygame.Surface((self.visualsize+4, self.visualsize+4), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (0, 0, 0, 64), (0, 0, self.visualsize+4, self.visualsize+4), 6)
        pygame.draw.rect(self.image, "WHITE", (2, 2, self.visualsize, self.visualsize), 2)
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
        self.size += scroll * -15
        if(self.size < 35):
            self.size = 35
        elif(self.size > 2800):
            self.size = 2800
        self.visualsize = lerp(self.visualsize, self.size, 0.3)
        self.image = pygame.Surface((self.visualsize+4, self.visualsize+4), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (0, 0, 0, 64), (0, 0, self.visualsize+4, self.visualsize+4), 6)
        pygame.draw.rect(self.image, "WHITE", (2, 2, self.visualsize, self.visualsize), 2)
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
        self.size = 800
        self.visualsize = 800
        self.cull = True
        self.image = pygame.Surface((self.visualsize+4, self.visualsize+4), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 255, 255, 64), (0, 0, self.visualsize+4, self.visualsize+4), 6)
        pygame.draw.rect(self.image, "BLACK", (2, 2, self.visualsize, self.visualsize), 2)
        self.rect = self.image.get_rect(center = (350, 350))

    def move(self, pos, scale):
        px, py = pos
        pl, pt, = px - scale / 2, py - scale / 2
        self.cull = max(abs(0 - px), abs(700 - px), abs(0 - py), abs(700 - py)) > scale / 2
        if(self.cull):
            self.rect.centerx = lerp(self.rect.centerx, 350, 0.3)
            self.rect.centery = lerp(self.rect.centery, 350, 0.3)
        else:
            self.rect.centerx = 700 * (350 - pl) / scale
            self.rect.centery = 700 * (350 - pt) / scale

    def scale(self, pos, scale):
        px, py = pos
        if(self.cull):
            self.size = 800
        else:
            self.size = 700 * 700 / scale
        self.visualsize = lerp(self.visualsize, self.size, 0.3)
        self.image = pygame.Surface((self.visualsize+4, self.visualsize+4), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 255, 255, 64), (0, 0, self.visualsize+4, self.visualsize+4), 6)
        pygame.draw.rect(self.image, "BLACK", (2, 2, self.visualsize, self.visualsize), 2)
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
            self.changetext("Focus J")
            Image.open("set3.png").save("set.png")
            display.switch("set.png")
            reloadjulia()
        else:
            focusjulia = True
            self.changetext("Unfocus J")
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
            self.changetext("Unzoom J")
        else:
            zoomjulia = False
            self.changetext("Zoom J")
        reloadjulia()

    def update(self):
        if(zoomjulia):
            self.changetext("Unzoom J")
        else:
            self.changetext("Zoom J")

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

class buttonchangemode(button):
    def __init__(self, x, y, width, height, text, amount):
        super(buttonchangemode, self).__init__(x, y, width, height, text)
        self.amount = amount

    def function(self):
        global mode
        mode = modes[(modes.index(mode)+self.amount)%len(modes)]
        modedisplay.changetext("Mode: "+mode)

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

class buttonopenconsole(button):
    def __init__(self, x, y, width, height, text):
        super(buttonopenconsole, self).__init__(x, y, width, height, text)
        self.hr = "------------------------------------------------------------"
        self.decompchars = "0123456789.-/e"
        self.compchars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-=_+[]{};:,.<>/?\|`~"

    def function(self):
        print(self.hr)
        screen.blit(checkconsole.returninfo()[0], checkconsole.returninfo()[1])
        pygame.display.flip()
        optionstring = "Console options:\n0: Exit console\n1: Save image\n2: Export state\n3: Import state\nChoose an option (enter associated digit): "
        while(True):
            option = input(optionstring)
            if(option == "0"):
                print(self.hr)
                print("Console closed.")
                return()
            elif(option == "1"):
                print(self.hr)
                self.saveimage()
            elif(option == "2"):
                print(self.hr)
                self.exportstate()
            elif(option == "3"):
                print(self.hr)
                self.importstate()
            else:
                optionstring = "Invalid answer; try again: "

    def saveimage(self):
        Image.open("set.png").save("savebuffer.png")
        rerenderstring = "Keep the image in its current resolution? (Y/N): "
        while(True):
            rerender = input(rerenderstring).upper()
            if(rerender == "Y"):
                rerenderbool = False
                break
            elif(rerender == "N"):
                rerenderbool = True
                break
            else:
                rerenderstring = "Invalid answer; try again: "
        res = 700
        if(rerenderbool):
            resstring = "Enter new resolution (single integer): "
            while(True):
                try:
                    res = int(input(resstring))
                    break
                except:
                    resstring = "Invalid resolution; try again: "
            funcf, funcm = getfunctions()
            print("Rendering...")
            if(focusjulia == False):
                gensetmain(res, iteration, center, zoom, scheme, funcf, funcm).save("savebuffer.png")
            else:
                gensetjulia(res, iteration, center, zoom, scheme, funcf, funcm).save("savebuffer.png")
        name = input("Enter a name for the image file (do not include extension): ")
        pathstring = "Enter a filepath for the image file (type 'prev' to use previous path): "
        while(True):
            try:
                path = input(pathstring)
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
                pathstring = "Invalid filepath; try again: "
        print(self.hr)

    def compress(self, state):
        num = 0
        for i in range(len(state)):
            num += self.decompchars.index(state[-1-i]) * len(self.decompchars) ** i
        for i in range(len(str(num))):
            placeval = len(self.compchars) ** (i + 1)
            if(placeval > num):
                maxex = i
                break
        comp = ""
        for i in range(maxex, -1, -1):
            digitval = num // (len(self.compchars) ** i)
            num -= digitval * (len(self.compchars) ** i)
            comp += self.compchars[digitval]
        return(comp)

    def decompress(self, state):
        num = 0
        for i in range(len(state)):
            num += self.compchars.index(state[-1-i]) * len(self.compchars) ** i
        for i in range(len(str(num))):
            placeval = len(self.decompchars) ** (i + 1)
            if(placeval > num):
                maxex = i
                break
        decomp = ""
        for i in range(maxex, -1, -1):
            digitval = num // (len(self.decompchars) ** i)
            num -= digitval * (len(self.decompchars) ** i)
            decomp += self.decompchars[digitval]
        if(decomp[0] == "/"):
            decomp = "0" + decomp
        return(decomp)

    def exportstate(self):
        state = str(fractals.index(fractal))+"/"+str(center.real)+"/"+str(center.imag)+"/"+str(zoom)+"/"+str(iteration)+"/"+str(schemes.index(scheme))+"/"+str(modes.index(mode))
        print("State ID: "+self.compress(state))
        print(self.hr)

    def importstate(self):
        global fractal
        global center
        global zoom
        global iteration
        global scheme
        global mode
        statestring = "Enter state ID here: "
        while(True):
            try:
                state = self.decompress(input(statestring))
                slash1 = state.index("/")
                slash2 = slash1 + state[slash1+1:].index("/") + 1
                slash3 = slash2 + state[slash2+1:].index("/") + 1
                slash4 = slash3 + state[slash3+1:].index("/") + 1
                slash5 = slash4 + state[slash4+1:].index("/") + 1
                slash6 = slash5 + state[slash5+1:].index("/") + 1
                fractal = fractals[int(state[:slash1])]
                center = complex(float(state[slash1+1:slash2]), float(state[slash2+1:slash3]))
                zoom = float(state[slash3+1:slash4])
                iteration = int(state[slash4+1:slash5])
                scheme = schemes[int(state[slash5+1:slash6])]
                mode = modes[int(state[slash6+1:])]
                print("Loading state...")
                reloadmain()
                reloadjulia()
                info.updateclick()
                print("State loaded. Close console to see changes.")
                break
            except:
                statestring = "Invalid state; try again: "
        print(self.hr)

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

schemes = [gradient([(50, 1, 51), (10, 72, 142), (60, 232, 126), (246, 255, 214)], 80) + gradient([(246, 255, 214), (235, 191, 59), (142, 40, 11), (50, 1, 51)], 80),
gradient([(55, 5, 50), (120, 55, 72), (172, 115, 100), (215, 182, 146), (252, 252, 212)], 80) + gradient([(252, 252, 212), (215, 182, 146), (172, 115, 100), (120, 55, 72), (55, 5, 50)], 80),
gradient([(48, 5, 56), (55, 48, 104), (45, 89, 148), (16, 131, 186), (0, 174, 215), (52, 196, 221), (93, 217, 224), (132, 238, 227), (165, 243, 223), (193, 247, 222), (217, 251, 227), (237, 255, 235)], 80) + gradient([(237, 255, 235), (225, 248, 208), (220, 240, 179), (220, 229, 147), (226, 217, 115), (228, 188, 90), (228, 159, 74), (224, 129, 66), (195, 83, 71), (153, 45, 74), (102, 18, 70), (48, 5, 56)], 80),
gradient([(45, 7, 112), (0, 63, 153), (0, 102, 172), (0, 136, 176), (0, 168, 174), (63, 186, 172), (105, 202, 169), (145, 218, 165), (176, 226, 173), (203, 233, 186), (227, 241, 201), (246, 250, 220)], 80) + gradient([(246, 250, 220), (237, 224, 183), (233, 195, 151), (230, 165, 129), (224, 133, 117), (213, 108, 112), (198, 83, 112), (179, 60, 115), (154, 38, 114), (125, 19, 114), (91, 7, 114), (45, 7, 112)], 80),
gradient([(247, 87, 129), (247, 177, 101)], 20) + gradient([(247, 177, 101), (242, 250, 130)], 20) + gradient([(242, 250, 130), (101, 247, 106)], 20) + gradient([(101, 247, 106), (101, 247, 242)], 20) + gradient([(101, 247, 242), (87, 98, 247)], 20) + gradient([(87, 98, 247), (233, 109, 247)], 20) + gradient([(233, 109, 247), (247, 87, 129)], 20),
gradient([(102, 7, 75), (247, 87, 129)], 80) + gradient([(247, 87, 129), (102, 7, 7)], 80) + gradient([(102, 7, 7), (247, 177, 101)], 80) + gradient([(247, 177, 101), (102, 78, 7)], 80) + gradient([(102, 78, 7), (242, 250, 130)], 80) + gradient([(242, 250, 130), (43, 102, 7)], 80) + gradient([(43, 102, 7), (101, 247, 106)], 80) + gradient([(101, 247, 106), (50, 168, 117)], 80) + gradient([(50, 168, 117), (101, 247, 242)], 80) + gradient([(101, 247, 242), (7, 53, 102)], 80) + gradient([(7, 53, 102), (87, 98, 247)], 80) + gradient([(87, 98, 247), (53, 7, 102)], 80) + gradient([(53, 7, 102), (233, 109, 247)], 80) + gradient([(233, 109, 247), (102, 7, 75)], 80),
gradient([(24, 19, 57), (33, 22, 63), (41, 24, 69), (51, 26, 74), (60, 28, 79), (90, 34, 88), (119, 40, 94), (148, 49, 96), (196, 75, 92), (230, 113, 81), (249, 160, 71), (249, 211, 74)], 80) + gradient([(249, 211, 74), (184, 194, 75), (128, 172, 84), (82, 148, 91), (48, 121, 92), (15, 105, 94), (0, 88, 90), (0, 71, 82), (0, 59, 81), (0, 47, 77), (4, 34, 70), (24, 19, 57)], 80),
gradient([(91, 40, 102), (158, 69, 103), (202, 118, 104), (225, 174, 122), (233, 233, 167)], 80) + gradient([(233, 233, 167), (174, 196, 137), (119, 158, 112), (68, 121, 88), (12, 85, 66)], 80) + gradient([(12, 85, 66), (31, 115, 108), (62, 145, 152), (101, 175, 195), (146, 205, 236)], 80) + gradient([(146, 205, 236), (117, 165, 211), (102, 125, 182), (96, 83, 145), (91, 40, 102)], 80),
gradient([(50, 28, 26), (83, 46, 38), (117, 67, 48), (149, 91, 56), (180, 118, 62), (194, 137, 71), (207, 156, 82), (219, 176, 93), (222, 189, 112), (226, 202, 131), (230, 214, 152), (235, 226, 172)], 80) + gradient([(235, 226, 172), (212, 212, 149), (186, 199, 129), (159, 187, 110), (129, 174, 94), (107, 160, 86), (85, 146, 79), (63, 132, 72), (50, 114, 67), (39, 96, 61), (31, 78, 54), (26, 61, 45)], 80) + gradient([(26, 61, 45), (41, 53, 29), (49, 44, 22), (53, 35, 22), (50, 28, 26)], 40),
gradient([(255, 255, 255), (204, 240, 235)], 15) + [(39, 35, 48) for i in range(2)] + gradient([(224, 74, 192), (168, 58, 201)], 15) + [(39, 35, 48) for i in range(2)] + gradient([(237, 230, 92), (224, 173, 63)], 15) + [(39, 35, 48) for i in range(2)] + gradient([(74, 224, 217), (65, 136, 217)], 15) + [(39, 35, 48) for i in range(2)]]
scheme = schemes[0]
schemenames = ["Standard", "Rose Gold", "Ice & Fire", "Plant Life", "Rainbow 1", "Rainbow 2", "Arcade", "Cotton Candy", "Sahara", "Pop Out"]
modes = ["Escape Time", "Point Trap", "Ring Trap", "Four Point Trap", "Four Ring Trap", "X Trap", "Image Trap"]
mode = modes[0]
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
trapvoid = False

Image.open("defaultset.png").save("set.png")
Image.open("defaultset2.png").save("set2.png")
display = setdisplay("set.png", 0, 0)
display2 = setdisplay("set2.png", 930, 0)
user = user()
userghost = userghost()
dashboard = dashboard()
buttons = pygame.sprite.Group()
buttons.add(buttonfocusjulia(700, 0, 115, 70, "Focus J"))
buttons.add(buttonzoomjulia(815, 0, 115, 70, "Zoom J"))
buttons.add(buttontoggleviewmode(700, 70, 300, 70, "Enable View Mode"))
info = infodisplay()
buttons.add(buttonreloadall(700, 140, 300, 70, "Reload All"))
iterdisplay = textdisplay(750, 210, 200, 70, "Iterate: "+str(iteration))
buttons.add(buttonchangeiter(700, 210, 75, 70, "-10", -10))
buttons.add(buttonchangeiter(925, 210, 75, 70, "+10", 10))
schemedisplay = textdisplay(750, 280, 200, 70, "Palette: Standard")
buttons.add(buttonchangescheme(700, 280, 75, 70, "Prev", -1))
buttons.add(buttonchangescheme(925, 280, 75, 70, "Next", 1))
modedisplay = textdisplay(750, 350, 200, 70, "Mode: Escape Time")
buttons.add(buttonchangemode(700, 350, 75, 70, "Prev", -1))
buttons.add(buttonchangemode(925, 350, 75, 70, "Next", 1))
fractalnamedisplay = textdisplay(750, 420, 200, 70, "Mandelbrot Set")
buttons.add(buttonchangefractal(700, 420, 75, 70, "Prev", -1))
buttons.add(buttonchangefractal(925, 420, 75, 70, "Next", 1))
buttons.add(buttontogglereallock(700, 490, 150, 70, "Lock Real"))
buttons.add(buttontoggleimaglock(850, 490, 150, 70, "Lock Imag"))
buttons.add(buttonopenconsole(700, 560, 300, 70, "Open Console"))
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
        userghost.scale((user.rect.centerx, user.rect.centery), user.size)
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
    screen.blit(modedisplay.image, modedisplay.rect.topleft)
    modedisplay.draw()
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