
import pygame
import os
import time
def flashing(filename):
    image = pygame.image.load(filename).convert()


    for w in range(0, image.get_width()):
        for h in range(0, image.get_height()):
            pixel = image.get_at((w,h))
            if pixel[1] + 55 < 255:
                newpixel = (pixel[0], pixel[1] + 55, pixel[2], pixel[3])
            else:
                newpixel = pixel
            image.set_at((w,h),newpixel)
    image = pygame.transform.scale(image, (image.get_width()*1.5, image.get_height()*1.5) )
    image = pygame.transform.scale2x(image)
       
    pygame.image.save(image, filename[:-3] + "f" + ".tga")
            

def convert(filename, value):
    val = []
    image = pygame.image.load(filename).convert()


    for w in range(0, image.get_width()):
        for h in range(0, image.get_height()):
                pixel = image.get_at((w,h))
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]

                if value == "black":
                    val = (r,r,r)
                if value == "blue":
                    val = (r,g,b)
                if value == "red":
                    val = (b,r,r)
                if value == "orange":
                    val = (b,g,r)
                if value == "green":
                    val = (r,g,r)
                if value == "maroon":
                    val = (g,r,r)
                if value == "teal":
                    val = (r,g,g)
                if value == "purple":
                    val = (g,r,g)

                
                if (b > r):
                    newpixel = (val[0], val[1], val[2], pixel[3])
                    image.set_at((w,h),newpixel)

    image = pygame.transform.scale(image, (image.get_width()*1.5, image.get_height()*1.5) )
    image = pygame.transform.scale2x(image)
    pygame.image.save(image, filename[:-3] + value + ".tga")
    image.set_colorkey((255,255,255,255))

    screen.blit(image, image.get_rect())
    pygame.display.flip()

    
def convertfolder(folder):
    files = os.listdir(folder)
    for file in files:
        if file.find(".gif") == -1:
            continue
        if file.find("bubble") != -1 or file.find("charge") != -1 or file.find("xbuster") != -1 or file.find("dust") != -1 or file.find("click") != -1:
            image = pygame.image.load(file).convert()
            image = pygame.transform.scale(image, (image.get_width()*1.5, image.get_height()*1.5) )
            image = pygame.transform.scale2x(image)
            pygame.image.save(image, file[:-3] + "tga")
        else:            
            flashing(file)
            convert(file, "black")
            convert(file, "blue")
            convert(file, "red")
            convert(file, "orange")
            convert(file, "green")
            convert(file, "maroon")
            convert(file, "teal")
            convert(file, "purple")

#main
pygame.init()
size = width, height = 800,600
screen = pygame.display.set_mode((width,height))
convertfolder("./")

        
        
