


#import psyco
#psyco.full()
#psyco.log()




import sys, time
import pygame
from pygame.locals import *
import eventqueue

class controlhandler:
    
    def __init__(self, eventqueue, focus):
        self.buffer = ''
        self.eventqueue = eventqueue
        self.focus = focus
        self.mode = "key"
        self.nodelay = 0
        self.focus.conhan = self
        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except:
	    self.joystick = None
            print "no joystick found"
        
    def executebuffer(self, buffer):
        try:
            self.focus.controls[buffer]()
            self.buffer = ''
        except:
            self.buffer = ''
#           n = 0
#            while n <= len(buffer):		#This will only grab the last command?
#                for control in self.focus.controls:
#                    if buffer[n:n+len(control)] == control:
#                        self.focus.controls[control]()
#                        n = n+len(control)-1
#                n += 1 
	    buffer = buffer[1:].split(",")
	    print buffer
	    for value in buffer:
		    try:
			self.focus.controls[value]()
		    except:
			value = value.split("+")
			print value
			for button in value:
				try:
				    self.focus.controls[button]()
				except:
				    pass
	    	   
    def postbuffer(self, buffer):
       if buffer == self.buffer:
           self.executebuffer(buffer)
                    
    def prebuffer(self, control_event):
        if  control_event != '':
            self.buffer = self.buffer  +  "," + control_event
            try:
                self.focus.complexcontrols[self.buffer[1:]]()
                self.buffer = ''
            except:
                self.timer()
                
    def setfocus(self, focus):
        self.focus = focus
                
    def timer(self):
        if self.nodelay:
            self.executebuffer(self.buffer)
        else:
            timerevent = eventqueue.event(.01667, self.postbuffer, self.buffer)
            self.eventqueue.add(timerevent)

    def inputhandler(self, event):
        if self.mode == "text":
           return self.textmode(event)
        else:
           return self.keymode(event)

    def textmode(self, event):                                  #this overall is very ugly.  The menu system needs to be in before this really!
        if event.type == KEYDOWN:
            # backspace
            if event.key == K_BACKSPACE:
                    # remove last character
                    self.focus.text(self.text[:-1] )
            # enter
            elif event.key == K_RETURN:
                    # report it to the manager
                    self.mode = "key"
                    self.focus.ontext()
            else:
                    # convert key to character code
                    character = str( event.unicode )
                    
                    # add it to the buffer
                    self.focus.text = self.focus.text + character
                    print self.focus.text

                    try:
                        if self.focus.type == 'sercon':    #ugly hack
                            self.focus.engine.text = self.focus.text
                    except:
                        pass
            
    def keymode(self, event):
	input = ''
        if event.type == KEYDOWN:
            try:
                input = self.focus.key_bindings[event.key] + "DOWN"
            except:
                pass
        elif event.type == KEYUP:
            try:
                input = self.focus.key_bindings[event.key] + "UP"
            except:
                pass
	########################################
	# Joystick support.  This needs to be made more modular.  it needs to load the key/hat bindings.
	# should be able to adjust sensetivity of the axes.
	# the joystick should return something other than the keyboard.
	######################################
        elif event.type == JOYBUTTONDOWN:
            try:
                input = self.focus.key_bindings[event.button] + "DOWN"
            except:
                pass
        elif event.type == JOYBUTTONUP:
            try:
                input = self.focus.key_bindings[event.button] + "UP"
            except:
                pass
	######################################
        elif event.type == JOYAXISMOTION and event.axis == 0 and event.value > .4:
            input = "rightDOWN"
	elif event.type == JOYAXISMOTION and event.axis == 0 and event.value < -.4:
            input = "leftDOWN"
        elif event.type == JOYAXISMOTION and event.axis == 0 and (event.value < .4 or event.value > -.4):
           input = "centerxDOWN"
        elif event.type == JOYAXISMOTION and event.axis == 1 and event.value > .4:
            input = "downDOWN"
        elif event.type == JOYAXISMOTION and event.axis == 1 and event.value < -.4:
            input = "upDOWN"
        elif event.type == JOYAXISMOTION and event.axis == 1 and (event.value < .4 or event.value > -.4):
            input = "upUP"
	######################################
        return input

    def menurend(self, event):
        self.focus.event.append(event)
        try:
            if self.focus.type == 'sercon':    #ugly hack
                self.focus.engine.event.append(event)
        except:
            pass

    def run(self):
        while 1:
	    input = ''
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = 0
                    self.focus.quit()
                    sys.exit() 
                else:
                    if self.mode == "text":             #ugly stuff man.
                        self.inputhandler(event)
                    elif self.focus.escapemenu:
                        self.menurend(event)
                    else:
			if input == '':
				input = self.inputhandler(event)
			else:
                        	input = input + "+" + self.inputhandler(event)
	    if self.mode == "key":
	    	self.prebuffer(input)
            self.eventqueue.reap()
            #time.sleep(.01667)      #only poll 60 times a second (.01667 = 1/60)
