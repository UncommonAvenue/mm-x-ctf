#import psyco
#psyco.full()
#psyco.log()


import pygame, sys, time
from pygame.locals import *

import eventqueue
import controlhandler
import sprite_engine
import updown
import level
import animated_sprite
import newserver


import os	#sloppy hack

#TODO: Turn this into a general purpose loader.  It should be able to load either the client or the server based on the users input
#it will be needed once we have the menu system up and running.


currentprofile = 0
currentlevel = updown
###############################################################################################################################
##  do all the initing and start the game
###############################################################################################################################

def startgame(port):
    ratio = 3
    ###########common init
    pygame.init()
    size = width, height = 800,600
    #screen = pygame.display.set_mode((width,height), FULLSCREEN|HWSURFACE)
    screen = pygame.display.set_mode((width,height))
    Events = eventqueue.event_queue()
    sprite_engin = sprite_engine.sprite_engine(Events, "background.png")
    ############

    #######server startup stuff
    currentlevel.load(sprite_engin)
    server = newserver.server(port,screen, sprite_engin,Events)
    ###############

#    preload :(
#    files = os.listdir("pics")
 #   for file in files:
#	    if file.find(".tga") != -1:
#	    	sprite_engin.load_image("pics/" + file)

    sprite_engin.run(1)		#I don't like the 1 there.  Its only there because the eventqueue is dumb.

    ###Player making
    if not currentprofile:
        MegaMan =  animated_sprite.make_megaman(sprite_engin)
    else:
        MegaMan = animated_sprite.make_megaman(sprite_engin, currentprofile.color)
    MegaMan.loader(currentprofile)
    MegaMan.server = server
    screenview = sprite_engine.centeredview(screen,sprite_engin) #change this!!!
    screenview.target(MegaMan)
    screenview.set_limits(pygame.Rect(0,0,800*ratio,223*8*ratio))
    #sprite_engin.play_music("music/zoolrave.mod")
    ###

    MegaMan2 = animated_sprite.make_megaman(sprite_engin)	#test dummy megaman

    ########start controls
    conhan = controlhandler.controlhandler(Events, MegaMan)
    conhan.run()    #this also does events.run()
    ########
    

if __name__ == '__main__':
    startgame(8182)
