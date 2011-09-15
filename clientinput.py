import pygame, sys, socket, time, string, thread
from pygame.locals import *
import eventqueue, controlhandler
import library
import cPickle
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
#for now.  Will make it so that it will take user input
HOST = "localhost"
PORT = 8182
currentprofile = 0


pygame.init()
try:
    pygame.mixer.init()
except:
    pass
#import psyco
#psyco.full()
#psyco.log()

#this handles import pygame events and translates the keys to the actions they are bound too.
#this is just for the client.  It sends all the real work over to the server to be taken care of.

class client_engine:
    def __init__(self, surface, event_queue):
        self.imagelibrary = library.library()
        self.soundlibrary = library.library("sound")
        self.musiclibrary = library.library("music")
        self.onscreen = []
        self.surface = surface
        self.count = 0
        self.images = []
        self.texts = []
        self.text = ''
        self.font = pygame.font.Font(None, 24)
        self.eventqueue = event_queue
        self.tabbed = 0
        self.kills = 0
        self.deaths = 0
        self.event = []
        self.escapemenu = 0
        self.sercon = 0

        self.renderer = Renderer()
        self.renderer.set_screen(self.surface)

        self.quitbutton = Button("Quit")
        self.quitbutton.position = 390,120
        self.quitbutton.connect_signal(SIG_CLICKED, sys.exit)
        self.cancelbutton = Button("Cancel")
        self.cancelbutton.position = 390,100
        self.cancelbutton.connect_signal(SIG_CLICKED, self.cancel)
        
        self.tabrenderer = Renderer()
        self.tabrenderer.set_screen(self.surface)

        try:	#default their name to so and so if they don't have one.
	    name = self.name
	except:
	    name = "so and so"
	self.name_label = Label(name + '        ' )
	self.k_label = Label("Kills: ")
	self.k_label.position = 10,25
	self.d_label = Label("Deaths: ")
	self.d_label.position = 10,45
        self.kill_label = Label(str(self.kills))
        self.kill_label.position = 60,25
        self.death_label = Label(str(self.deaths))
        self.death_label.position = 60,45

        self.hpbar = pygame.image.load("hpbar.gif").convert()
	self.hpbar = pygame.transform.scale(self.hpbar,(self.hpbar.get_width()*3,self.hpbar.get_height()*3))
        self.hpinc = pygame.image.load("hp.gif").convert()
        self.hpinc = pygame.transform.scale(self.hpinc,(self.hpinc.get_width()*3,self.hpinc.get_height()*3))
        self.hp = 17
        self.chatbar = pygame.image.load('chatbar.gif').convert()
	self.chatbar.set_alpha(100)
        
    def render(self, images):
        for image in self.images:
            image = image.split(",")
            facing = 0
            if image[3] == "-1":
                facing = 1
            self.surface.blit(self.get_image(image[0])[facing],(int(image[1]),int(image[2]) ) ) #sorta ugly

        img = self.font.render("Kills:" + str(self.kills) ,1, (255,255,255,255))
        self.surface.blit(img,(0,600-60))
        img = self.font.render("Deaths:" +str(self.deaths) ,1, (255,255,255,255))
        self.surface.blit(img,(0,600-30))

        self.surface.blit(self.hpbar,(14*3,52*3))
        for x in range(1,self.hp*2+1,2):
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

        if self.text != '':
            self.surface.blit(self.chatbar,(200,600-30))
            img = self.font.render("Say: " + self.text,1,(255,255,255,255))
            self.surface.blit(img,(200,600-30))

        if self.escapemenu:
            self.renderer.add_widget(self.cancelbutton,self.quitbutton)
            self.renderer.distribute_events(*self.event)
            self.renderer.update()
            self.renderer.draw(self.surface)

        if self.tabbed:
            self.tabrenderer.add_widget(self.name_label,self.k_label,self.d_label)
            self.tabrenderer.add_widget(self.kill_label,self.death_label)

            self.tabrenderer.update()
            self.tabrenderer.draw(self.surface)
        
        timerevent = eventqueue.event(0.01667, self.render, () )
        self.eventqueue.add(timerevent)
        pygame.display.update()

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
                self.texts.append(text)
                
            if cleartext == 1:
                newchatline = eventqueue.event(2, self.addtext, ("", 1) )
                self.eventqueue.add(newchatline)

    def cancel(self):
        self.escapemenu = 0
        self.sercon.escapemenu = 0
        self.event = []
                	
    def load_image(self, imagename):
        return self.imagelibrary.load(imagename)

    def get_image(self, imagename):
        return self.imagelibrary.get(imagename)
    
    def run(self):
        timerevent = eventqueue.event(0.1667, self.render, () )
        self.eventqueue.add(timerevent)

class client_connection:
    def __init__(self, client_engin, host = HOST, port = PORT ):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))
        self.engine = client_engin
        
    def recv(self):
        value = ''
        newval = self.sock.recv(1)
	while newval != '\n':
		value = value + newval
		newval = self.sock.recv(1)
	return value + '\n'

    def listen(self, arg):
        while(1):
            value = ''
            value = self.recv()
            type = value[0:value.find(":")]
            data = value[value.find(":")+1:-1]
            self.interpret(type, data)

    def interpret(self, type, data):

	#todo: rename type strings so they are much shorter.  It will save a little on bandwidth and will add up over time
        if type == "is":
            self.engine.imagelibrary.recvsync(data)
            return

        elif type == "ss":
            self.engine.soundlibrary.recvsync(data)
            return
        
        elif type == "ms":
            self.engine.musiclibrary.recvsync(data)
            return

        elif type == "k":
            self.engine.kills = data

        elif type == "d":
            self.engine.deaths = data
         
        elif type == "h":
            self.engine.hp = int(data)
            
        elif type == "t":
            self.engine.addtext((data,0))
            return
        
        elif type == "s":
	    try:	
            	self.engine.soundlibrary.get(data).play()
	    except:
		pass
	    return
        
        elif type == "m":
            try:	
            	pygame.mixer.music.play()
	    except:
		pass
            return
        
        else:
        #begin using the id numbers instead of the filename as the index.  It will save a lot of bandwidth room.
            images = data.split(";")
            images = images[:len(images)-1]
            self.engine.images = images

    def send(self, string):
        try:
            self.sock.send(string)
        except:
            self.disconnect()
            pass
  
def start_listen(connection):
    thread.start_new_thread(connection.listen, ("a",))

#this seems useful, but yet so useless.
#I'll probably take it out at some point
class controller:
    def __init__(self, controls = {}, complexcontrols = {}):
        self.controls = controls
        self.complexcontrols = complexcontrols
    def focus(self):
        pass
    def defocus(self):
        pass
    def on_focus(self):
        pass
    def on_defocus(self):
        pass

class servercontroller(controller):
    def __init__(self, connection, engine):
	self.type = 'sercon'
        self.key_bindings = {K_RIGHT: 'right', K_LEFT: 'left', K_UP: 'up', K_a: 'shoot', K_RETURN: 'chat', K_TAB: 'tab', K_ESCAPE: 'escape'}
        self.controls = {'chatDOWN': self.chat, 'rightDOWN': self.goright, "leftDOWN" : self.goleft, 'upDOWN': self.jump,\
                         'rightUP': self.stopgoright, 'leftUP': self.stopgoleft, 'upUP': self.stopjump, 'shootUP': self.shoot,\
                         'centerxDOWN' : self.joystop, 'tabDOWN': self.tab, 'tabUP': self.untab, 'escapeDOWN': self.escape,\
                         'shootDOWN':self.charge}
        self.complexcontrols = {}
        self.connection = connection
        self.engine = engine
        self.engine.sercon = self
        self.text = ''
        self.escapemenu = 0
        self.event = []
    #It would be nice to figure out a way to minimize the characters that have to be sent here.  The less the better because they will add up over time.
    def goright(self):
        self.connection.send(":rightDOWN\n")
    def goleft(self):
        self.connection.send(":leftDOWN\n")
    def jump(self):
        self.connection.send(":upDOWN\n")
    def stopgoright(self):
        self.connection.send(":rightUP\n")
    def stopgoleft(self):
        self.connection.send(":leftUP\n")
    def stopjump(self):
        self.connection.send(":upUP\n")
    def shoot(self):
        self.connection.send(":shootUP\n")
    def joystop(self):
	self.connection.send(":centerxDOWN\n")
    def charge(self):
        self.connection.send(":shootDOWN\n")
      
    def chat(self):
        self.conhan.mode = "text"
        print "text mode"
    def ontext(self):
        self.connection.send("c:" + self.text + "\n")
        self.text = ''
        self.engine.text = ''
    def quit(self):
        self.connection.send("dc:")
    def tab(self):
        try:	#default their name to so and so if they don't have one.
	    name = self.name
	except:
	    name = "so and so"
	self.engine.name_label.text = name
        self.engine.kill_label.text = str(self.engine.kills)
        self.engine.death_label.text = str(self.engine.deaths)
        self.engine.tabbed = 1

    def untab(self):
        self.engine.tabbed = 0

    def escape(self):
        self.escapemenu = 1
        self.engine.escapemenu = 1

    def save(self):
        print "about to save"
        try:
            self.currentprofile.killcount = self.currentprofile.killcount + int(self.engine.kills)
            self.currentprofile.deathcount = self.currentprofile.deathcount + int(self.engine.deaths)
            print "updated kills and deaths"
            self.profiles = cPickle.load(open('profilelist', 'r'))
            print "loaded profiles"
            for x in range(0, len(self.profiles)):
                if self.profiles[x].name == self.currentprofile.name:
                    self.profiles[x] = self.currentprofile
            cPickle.dump(self.profiles, open('profilelist', 'w'))
            print "Saved!"
        except:
            print "No Profile is loaded"

    def loader(self, profile):
        try:
            self.currentprofile = profile
            self.name = profile.name
            self.key_bindings = {profile.keylist[1]: 'right', profile.keylist[0]: 'left', profile.keylist[2]: 'up',\
                                 profile.keylist[3]: 'shoot', profile.keylist[4]: 'save',K_RETURN: 'chat',\
                                 K_ESCAPE: 'escape', K_TAB: 'tab'}
            print "megaman is now " + self.currentprofile.name
        except:
            print "did not load profile into megaman"


def start_client(host = HOST, port = PORT):
    client_events = eventqueue.event_queue()
    client_engin = client_engine(pygame.display.set_mode((800,600)), client_events)
    connection = client_connection(client_engin, host, port)
    start_listen(connection)
    sercon = servercontroller(connection, client_engin)
    sercon.loader(currentprofile)
    conhan = controlhandler.controlhandler(client_events, sercon)
    sercon.conhan = conhan
    conhan.nodelay = 1      #this dirty hack helps lag a lot! yay!  #I need less lag still though
    connection.send("r:\n")	#this doesn't help lag any.
    client_engin.run()
    conhan.run()

if __name__ == '__main__':

	try:
                start_client("localhost", 8182)
	except:
    	#go back to menu and print error message
    		print "Cannot Connect!"
