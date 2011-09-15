import psyco
psyco.full()
psyco.log()
psyco.profile(.05)


import pygame
import eventqueue
import library
import time

from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
#The purpose of this class is to hold all of the images
#This will keep the system from loading multiples of the
#same image.

#This class will also hold all of the sprites as well as
#the background.

#all sprite classes will need to add themselves to the engine on creation
#all views will need to talk to the engine in order to get the collisions
#(using the sprites group) as well as the images it should render.

#Engine might not be the best description of this class, if someone thinks
#of a better one, let me know.


#this is going to start taking care of more than just sprites.
class spawn:
	def __init__(self, sprite_engin, x, y, facing):
		self.engine = sprite_engin
		self.x = x
		self.y = y
		self.facing = facing
		self.collider = pygame.sprite.Sprite()
       		self.collider.rect = pygame.Rect(0,0,30,34)
		self.collider.rect.centery = y
		self.collider.rect.centerx = x
	def can_spawn(self,sprite):
		collides = pygame.sprite.spritecollide(self.collider,self.engine.sprites, 0)
		for sprite in collides:
			if sprite.type == "megaman":
				return 0
		return 1

class team:
    def __init__(self,color = "rgb"):
        self.members = []
        self.score = 0
        self.color = color
        self.spawns = []
        self.nummembers = 0
    def add_member(self,member):
        self.members.append(member)
        self.nummembers = self.nummembers + 1
        member.team = self
    def remove_member(self,member):
        self.members.remove(member)
        self.nummembers = self.nummembers - 1
        member.team = 0

class sprite_engine:
    def __init__(self, event_queue, background = 0, limits = 0):
        self.imagelibrary = library.library()
        self.sprites = pygame.sprite.Group()
        self.background = self.load_image(background)
        self.limits = limits
        self.views = []
        self.currentid = 0
        self.dirtysprites = pygame.sprite.Group()
        self.moved = []
	self.eventqueue = event_queue
        self.soundlibrary = library.library("sound")
        self.musiclibrary = library.library("music")
	self.currentmusic = None

	self.chatbar = pygame.image.load('chatbar.gif').convert()
	self.chatbar.set_alpha(100)
	
	#game conditions
	self.maxdeath = 0
	self.maxkill  = 0
	self.endtime = 0	#length of game in seconds
	self.starttime = time.time()
	
    def load_image(self, imagename):
        return self.imagelibrary.load(imagename)

    def get_image(self,imagename):
        return self.imagelibrary.get(imagename)

    def load_sound(self, soundname):
        return self.soundlibrary.load(soundname)

    def get_sound(self,soundname):
        return self.soundlibrary.get(soundname)

    def load_music(self, musicname):
        return self.musiclibrary.load(musicname)

    def get_music(self,musicname):
        return self.musiclibrary.get(musicname)

    def play_music(self, musicname):
	self.currentmusic = musicname
        for view in self.views:
            view.play_music(musicname)    

    def sendall(self,text):	#I don't know if I like it here
	for view in self.views:
	    view.send(text)

    def addtext(self,(text,num)):	#I don't know if I like it here
        for view in self.views:
            view.addtext((text,num))

    def play_sound(self, soundname, sprite):
       for view in self.views:
            if view.collider.rect.colliderect(sprite.rect):
                view.play_sound(soundname)
    def render(self):
        for view in self.views:
            view.render()

    def check_time_end(self):
	if self.endtime and time.time() > self.endtime + self.starttime:
		self.end_game("Time limit met")
	
    def check_kill_end(self,killcount):
	if self.maxkill and killcount >= self.maxkill:
		self.end_game("Kill count met")
    def check_death_end(self,deathcount):
	if self.maxdeath and deathcount >= self.maxdeath:
		self.end_game("Death count met")
    def end_game(self,reason):
	print reason
	#print results
	winner = 0
	for sprite in self.sprites:
		try:	#if they have a killcount
			print "kills:", sprite.killcount,"	deaths:", sprite.deathcount
			if winner == 0:
				winner = sprite
			elif sprite.killcount > winner.killcount:
				winner = sprite
				
		except:
			pass
	if winner:
		print "Winner:", "kills:", winner.killcount,"	deaths:", winner.deathcount
		
	#stop game and go back to the menus

    def update(self):
	#self.check_time_end()
        for sprite in self.sprites.sprites():
            sprite.automove()

    def run(self, arg):
        pygame.display.flip()   
	self.update()
    	self.render()
    	timerevent = eventqueue.event(.01667, self.run, (1) )
   	self.eventqueue.add(timerevent)
 	pygame.display.flip()
        
#########################################################################################
#Classes that rely on sprite_engine
#########################################################################################
##Probably will make these back into their own files one of these days
##I'm not sure why I'm moving them in here anyways.

#########################################################################################
#Sprite and its classes
#########################################################################################
#This is not all of the simplesprite class and its redone    
class simplesprite(pygame.sprite.Sprite):
    def __init__(self, spriteengine, imagename, x = 0 , y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.engine = spriteengine
        self.image = self.engine.load_image(imagename)
        self.rect = self.engine.get_image(self.image)[0].get_rect()
        self.engine.sprites.add(self)
        self.currentfacing = 1
        self.type = "level"         #more than likely it will be part of the level
        self.rect.centerx = x
        self.rect.centery = y
        self.dead = 0

    def automove(self):
        pass

    def sound(self,soundname):
        self.engine.play_sound(soundname, self)
    
    def check_collisions(self):
        top = 0
        left = 0
        right = 0
        bottom = 0
        
        collisions = pygame.sprite.spritecollide(self,self.engine.sprites, 0)
        
        for sprite in collisions:
            if sprite == self:
                pass
            else:
                side = get_collision_side(self,sprite)
                if side == 0:
                    self.collide_right(sprite)
                    sprite.collide_left(self)
                    right = 1
                if side == 1:
                    self.collide_top(sprite)
                    sprite.collide_bottom(self)
                    top = 1
                if side == 2:
                    self.collide_bottom(sprite)
                    sprite.collide_top(self)
                    bottom = 1
                if side == 3:
                    self.collide_left(sprite)
                    sprite.collide_right(self)
                    left = 1
                            
        if right == 0:
            self.no_collide_right()
        if left == 0:
            self.no_collide_left()
        if top == 0:
            self.no_collide_top()
        if bottom == 0:
            self.no_collide_bottom()

    def death(self):
        self.kill()
        
    def move(self, x, y):
        self.rect = self.rect.move(x,y)
        

    def collide_top(self,sprite):
        if not sprite.rect.bottom == self.rect.top +1:
            sprite.rect.bottom = self.rect.top + 1
            
    def collide_left(self,sprite):
	if sprite.dead:
		return
        if not sprite.rect.right == self.rect.left +1:
            sprite.rect.right = self.rect.left + 1
            
    def collide_right(self,sprite):
	if sprite.dead:
		return
        if not sprite.rect.left == self.rect.right -1:
            sprite.rect.left = self.rect.right -1
 
    def collide_bottom(self,sprite):
        if not sprite.rect.top == self.rect.bottom -1:
            sprite.rect.top = self.rect.bottom -1
            
	
    def no_collide_top(self):
        return 0
    def no_collide_left(self):
        return 0
    def no_collide_right(self):
        return 0
    def no_collide_bottom(self):
        return 0

    def render(self, xoffset = 0, yoffset = 0):
        image = self.image.get_image()
        if self.currentfacing == 1:
           # image[0]
            return
        else:
           # image[1] 
            return
        return 


#########################################################################################
#View and its classes
#########################################################################################
#this is not all of the view class and its redone
class view:
    def __init__(self, surface, spriteengine):
        self.engine = spriteengine
        self.engine.views.append(self)
        self.surface = surface
        self.collider = pygame.sprite.Sprite()
        self.collider.rect = surface.get_rect()
	self.count = 0
	self.font = pygame.font.Font(None, 24)
        self.texts = []
        self.renderer = Renderer()
        self.renderer.set_screen(self.surface)
        self.tabrenderer = Renderer()
        self.tabrenderer.set_screen(self.surface)
        self.hpbar = pygame.image.load("hpbar.gif").convert()
	self.hpbar = pygame.transform.scale(self.hpbar,(self.hpbar.get_width()*3,self.hpbar.get_height()*3))
        self.hpinc = pygame.image.load("hp.gif").convert()
        self.hpinc = pygame.transform.scale(self.hpinc,(self.hpinc.get_width()*3,self.hpinc.get_height()*3))
	
    def get_onscreen(self):
       pass

    def update(self,sprites):   #this will only update some of the sprites on the screen
        #add stuff when you start using dirty rects.
        pass
        
    def render(self):           #this will update the whole screen
        #update the background image for the view
        background = self.engine.get_image(self.engine.background)[0] ##ugly
        #self.surface.blit(background, (background.get_rect().left - self.collider.rect.left, background.get_rect().top - self.collider.rect.top))         
        self.surface.blit(background, (0,0))         
        
        #do a self collide with world and then render everything that
        #collides with the view frame
        onscreen = pygame.sprite.spritecollide(self.collider,self.engine.sprites,0)
        for sprite in onscreen:
            try:
                if sprite.type == "megaman":
                    image = self.engine.get_mega_image(sprite.image)
                    bubble = self.engine.get_image(sprite.bubbles)
                else:
                    image = self.engine.get_image(sprite.image)
            except:
                image = self.engine.get_image(sprite.image) ##ugly
            if sprite.currentfacing == 1:
               image = image[0]
            else:
               image = image[1]
            abc = image.get_rect()
            abc.centerx = sprite.rect.centerx
            abc.centery = sprite.rect.centery
            self.surface.blit(image, (abc.left - self.collider.rect.left, abc.top - self.collider.rect.top) )
            try:
                if sprite.currentfacing == 1:
                    bubble = bubble[0]
                else:
                    bubble = bubble[1] 
                rect = bubble.get_rect()
                rect.centerx = sprite.rect.centerx
                rect.centery = sprite.rect.centery
                self.surface.blit(bubble, (rect.left - self.collider.rect.left, rect.top - self.collider.rect.top) )
            except:
                pass
                
    def play_sound(self, sound):
        try:
            self.engine.soundlibrary.get(sound).get().play()    #wow...
        except:
            print sound, " not found"
    def play_music(self, music):
	try:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play()
	except:
		print music, " not found"
    def send(self, text):
	print text

    def addtext(self,(text,cleartext)):
        print cleartext
        empty = 1
        for string in self.texts:
            if string != "":
                empty = 0
                break
        if empty:
            self.texts = []
        if empty == 0 or text != "":
            if len(self.texts) > 3:
                self.texts[0] = self.texts[1]
                self.texts[1] = self.texts[2]
                self.texts[2] = self.texts[3]
                self.texts[3] = text
            else:
                if empty:
                    cleartext = 1
		    self.texts.append("")
		    self.texts.append("")
		    self.texts.append("")
                self.texts.append(text)		#we want this to be the 4th thing in the list.
                
            if cleartext == 1:
                newchatline = eventqueue.event(2, self.addtext, ("", 1) )
                self.engine.eventqueue.add(newchatline)
                

class centeredview(view):
    def target(self,target):
        self.targetsprite = target
        target.view = self
        
    def set_limits(self, limit):    #limit is a rect for now.  I'd like to make it more flexible, like a series of rects.
        self.limit = limit

    def checklimits(self):
        if self.collider.rect.left    < self.limit.left:
            self.collider.rect.left   = self.limit.left
        elif self.collider.rect.right   > self.limit.right:
            self.collider.rect.right  = self.limit.right
           
        if self.collider.rect.top     < self.limit.top:
            self.collider.rect.top    = self.limit.top
        elif self.collider.rect.bottom  > self.limit.bottom:
            self.collider.rect.bottom = self.limit.bottom
   
    def follow(self):
        self.collider.rect.center = self.targetsprite.rect.center
        self.checklimits()
    
    def render(self):
	view.render(self)
	#HUD STUFF!
	img = self.font.render("Kills:" + str(self.targetsprite.killcount) ,1, (255,255,255,255))
        self.surface.blit(img,(0,600-60))
        img = self.font.render("Deaths:" +str(self.targetsprite.deathcount) ,1, (255,255,255,255))
        self.surface.blit(img,(0,600-30))
        
        self.surface.blit(self.hpbar,(14*3,52*3))
        for x in range(1,self.targetsprite.hp*2+1,2):
            self.surface.blit(self.hpinc,(4*3+14*3,52*3+36*3-x*3))
        
        try:
            img = self.font.render(self.texts[0] ,1, (255,255,255,255))
            self.surface.blit(img,(200,600-130))
            img = self.font.render(self.texts[1] ,1, (255,255,255,255))
            self.surface.blit(img,(200,600-105))
            img = self.font.render(self.texts[2] ,1, (255,255,255,255))
            self.surface.blit(img,(200,600-80))
            img = self.font.render(self.texts[3] ,1, (255,255,255,255))
            self.surface.blit(img,(200,600-55))
        except:
            pass
        
        if self.targetsprite.text != '':
            self.surface.blit(self.engine.chatbar,(200,600-30))
            img = self.font.render(self.targetsprite.text,1,(255,255,255,255))
            self.surface.blit(img,(200,600-30))

        if self.targetsprite.escapemenu:
            self.renderer.add_widget(self.targetsprite.quitbutton)
            self.renderer.add_widget(self.targetsprite.cancelbutton)
            #print "renderer event manager start"
            self.renderer.distribute_events(*self.targetsprite.event)

            self.renderer.update()
            self.renderer.draw(self.surface)

        if self.targetsprite.tabbed:
            self.tabrenderer.add_widget(self.targetsprite.name_label,self.targetsprite.k_label,self.targetsprite.d_label)
            self.tabrenderer.add_widget(self.targetsprite.kill_label,self.targetsprite.death_label)

            self.tabrenderer.update()
            self.tabrenderer.draw(self.surface)
            

            
    def send(self,text):
	print text
	self.addtext((text,0))
#	self.addtext(("Hello World",0))
        

class networkview(centeredview):
    def render(self):
	if self.client.ready == 0:
		return
	onscreen = pygame.sprite.spritecollide(self.collider,self.engine.sprites,0)
	self.client.send(":")
	self.client.send(str(self.engine.background))
	self.client.send(",0,0,0;")
	for sprite in onscreen:
		abc = self.engine.get_image(sprite.image)[0].get_rect()
          	abc.centerx = sprite.rect.centerx
          	abc.centery = sprite.rect.centery
                self.client.send(str(sprite.image))
		self.client.send(",")
		self.client.send(str(abc.left - self.collider.rect.left) )
		self.client.send(",")
		self.client.send(str(abc.top - self.collider.rect.top) )
		self.client.send(",")
		self.client.send(str(sprite.currentfacing) )
		self.client.send(";")
	self.client.send("\n")
	#HUD STUFF
	self.client.send("k:")
	self.client.send(str(self.targetsprite.killcount))
	self.client.send("\n")
	self.client.send("d:")
	self.client.send(str(self.targetsprite.deathcount))
    	self.client.send("\n")
    	self.client.send("h:")
    	self.client.send(str(self.targetsprite.hp))
    	self.client.send("\n")
	
    def send(self, text):
	print text
	self.client.send("t:")
	self.client.send(text)
	self.client.send("\n")
	
    def play_sound(self, sound):
        self.client.send("s:")
        self.client.send(sound)
        self.client.send("\n")

    def play_music(self, music):
        self.client.send("m:")
        self.client.send(music)
        self.client.send("\n")

#########################################################################################
#Helper functions
#########################################################################################
        
#There has got to be a better way to do this!!
def get_collision_side(rect1,rect2):
    #This quick check should take care of a lot of cases.
    if rect1.rect.bottom == rect2.rect.top + 1:
        return 2
    if rect1.rect.left == rect2.rect.right -1:
        return 3
    if rect1.rect.right == rect2.rect.left +1:
        return 0
    if rect1.rect.top == rect2.rect.bottom -1:
        return 1

    right = abs(rect1.rect.right - rect2.rect.left)
    top   = abs(rect1.rect.top - rect2.rect.bottom)
    bottom = abs(rect1.rect.bottom - rect2.rect.top)
    left   = abs(rect1.rect.left - rect2.rect.right)

    least = bottom
    leastnumber = 2

    if right < least:
        least = right
        leastnumber = 0
    if  left < least:
        least = left
        leastnumber = 3
    if top < least:
        least = top
        leastnumber = 1
    return leastnumber
    
