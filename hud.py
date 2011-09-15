#hud.py

from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.events import EventCallback
import sys

class hud:
    def __init__(self):
        self.text = ''    
        self.escapemenu = 0
        self.quitbutton = 0
        self.tabbed = 0
        self.event = []
        try:	#default their name to so and so if they don't have one.
	    name = self.name
	except:
	    name = "so and so"
	self.name_label = Label(name + '        ' )
	self.k_label = Label("Kills: ")
	self.k_label.position = 10,25
	self.d_label = Label("Deaths: ")
	self.d_label.position = 10,45
        self.kill_label = Label(str(self.killcount))
        self.kill_label.position = 60,25
        self.death_label = Label(str(self.deathcount))
        self.death_label.position = 60,45

        self.quitbutton = Button("Quit")
        self.quitbutton.position = 390,120
        self.quitbutton.connect_signal(SIG_CLICKED, sys.exit)
        self.cancelbutton = Button("Cancel")
        self.cancelbutton.position = 390,100
        self.cancelbutton.connect_signal(SIG_CLICKED, self.cancel)
        
    def quit(self):
        return

    def escape(self):
        self.escapemenu = 1
        print "escape mode"

    def cancel(self):
        self.escapemenu = 0
        self.event = []

    def tab(self):
        try:	#default their name to so and so if they don't have one.
	    name = self.name
	except:
	    name = "so and so"
	self.name_label.text = name
	self.kill_label.text = str(self.killcount)
	self.death_label.text = str(self.deathcount)
        self.tabbed = 1

    def untab(self):
        self.tabbed = 0
        


    def chat(self):
        self.conhan.mode = "text"
        
    def ontext(self):
	try:	#just some error checking, because right now, not everyone has a name by default.
		name = self.name
	except:
		name = "so and so"
        self.engine.sendall(name + ": " + self.text)
	self.text = ''
