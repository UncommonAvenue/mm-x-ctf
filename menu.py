# Same as the old menu execpt this uses classes for organization #
import pygame
from pygame.locals import *
import cPickle

from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import TextListItem
import ocempgui.draw.Image

import broken
import clientinput
from profile import profile
import updown
import level

global currentrend
currentrend = 0

def changerenderer(renderer):
    global currentrend
    currentrend = renderer
    return currentrend
        
def createprofile(name):
    print name.text
    try:
        profiles = cPickle.load(open('profilelist', 'r'))
        print profiles
    except:
        profiles = []
        #print "did not load profiles"
        pass
    current = profile(name.text)
    load(current)
    profiles.append(current)
    cPickle.dump(profiles, open('profilelist', 'w'))

def loadprofile(list):
        name = list.get_selected()
        print name[0].text
        try:
            profiles = cPickle.load(open('profilelist', 'r'))
            print profiles
        except:
            profiles = []
            #print "did not load profiles"
            pass
        for file in profiles:
            if file.name == name[0].text:
                load(file)
        
def savesettings(keylist):
    try:
        for x in range(0,len(keylist)):
            broken.currentprofile.keylist[x] = keylist[x].value
            clientinput.currentprofile.keylist[x] = keylist[x].value
            print keylist[x].value
    except:
        print "no profile loaded"
        pass
    
def startgame(type, ip, port, list):
    if type == 'host':
        if list.get_selected()[0].text == "updown":
            broken.currentlevel = updown
        else:
            broken.currentlevel = level
        broken.startgame(int(port.text))
    else:
        clientinput.start_client(ip.text, int(port.text))
        
#class profile:
#    def __init__(self, name):
#        self.name = name
#        self.killcount = 0
#        self.deathcount = 0
#        self.color = 'blue'
#        self.keylist = [K_LEFT, K_RIGHT, K_UP, K_a, K_F8]
def load(self):
    self.currentprofile = 1
    currentname.text = self.name
    broken.currentprofile = self
    clientinput.currentprofile = self
    print "success ", broken.currentprofile.name

class Renderers:
    def __init__(self):
        self.main = MenuRenderer(None)
        self.main.create_screen(800,600)
        self.main.title = "MegaMan"
        self.main.color = (0,0,0)
        self.host = MenuRenderer(self.main)
        self.host.create_screen(800,600)
        self.host.title = "MegaMan"
        self.host.color = (0,0,0)
        self.join = MenuRenderer(self.main)
        self.join.create_screen(800,600)
        self.join.title = "MegaMan"
        self.join.color = (0,0,0)
        self.profilescreen = MenuRenderer(self.main)
        self.profilescreen.create_screen(800,600)
        self.profilescreen.title = "MegaMan"
        self.profilescreen.color = (0,0,0)
        self.newprofile = MenuRenderer(self.profilescreen)
        self.newprofile.create_screen(800,600)
        self.newprofile.title = "MegaMan"
        self.newprofile.color = (0,0,0)
        self.settings = MenuRenderer(self.profilescreen)
        self.settings.create_screen(800,600)
        self.settings.title = "MegaMan"
        self.settings.color = (0,0,0)
        self.megamancolor = MenuRenderer(self.settings)
        self.megamancolor.create_screen(800,600)
        self.megamancolor.title = "MegaMan"
        self.megamancolor.color = (0,0,0)
        
class MainPage:
    def __init__(self, rend, Mega):
        hostbutton = Button("Host")
        hostbutton.position = 390,280
        hostbutton.connect_signal(SIG_CLICKED, changerenderer, rend.host)
        joinbutton = Button("Join")
        joinbutton.position = 390,330
        joinbutton.connect_signal(SIG_CLICKED, changerenderer, rend.join)
        profilebutton = Button("Profiles")
        profilebutton.position = 390,380
        profilebutton.connect_signal(SIG_CLICKED, changerenderer, rend.profilescreen)
        rend.main.add_widget(Mega,hostbutton,joinbutton,profilebutton)

class HostPage:
    def __init__(self, rend, Mega):
        port = Label("port: ")
        port.position = 350, 330
        input_port = Entry('8182')
        input_port.position = 410, 330
        levellist = ScrolledList(100,100)
        levellist.position = 350, 380
        levellist.selectionmode = SELECTION_SINGLE
        levellist.items.append(TextListItem('updown'))
        levellist.items.append(TextListItem('level'))
        hoststartbutton = Button("Play")
        hoststartbutton.position = 390,490
        hoststartbutton.connect_signal(SIG_CLICKED, startgame, 'host', 'localhost', input_port,levellist)
        rend.host.add_widget(Mega,port,input_port,levellist,hoststartbutton)

class JoinPage:
    def __init__(self, rend, Mega):
        port = Label("port: ")
        port.position = 350, 330
        ip = Label("ip:")
        ip.position = 350, 280
        input_port = Entry('8182')
        input_port.position = 410, 330
        input_ip = Entry('localhost')
        input_ip.position = 410, 280
        joinstartbutton = Button("Play")
        joinstartbutton.position = 390,380
        joinstartbutton.connect_signal(SIG_CLICKED, startgame, 'join', input_ip, input_port)
        rend.join.add_widget(Mega,ip,input_ip,port,input_port,joinstartbutton)

class ProfileScreenPage:
    def __init__(self, rend, Mega, Settings):
        profilelist = ScrolledList(100,100)
        profilelist.position = 310, 280
        profilelist.selectionmode = SELECTION_SINGLE
        try:
            profiles = cPickle.load(open('profilelist', 'r'))
        except:
            profiles = []
            print "did not load profiles"
            pass
    
        for file in profiles:
            text = file.name
            profilelist.items.append(TextListItem(text))
        newprofilebutton = Button("New Profile")
        newprofilebutton.position = 420,330
        newprofilebutton.connect_signal(SIG_CLICKED, changerenderer, rend.newprofile)
        loadbutton = Button("Load Profile")
        loadbutton.position = 420,280
        loadbutton.connect_signal(SIG_CLICKED, loadprofile, profilelist)
        loadbutton.connect_signal(SIG_CLICKED, changerenderer, rend.settings)
        loadbutton.connect_signal(SIG_CLICKED, self.updatesettings, Settings)
        rend.profilescreen.add_widget(Mega,profilelist,loadbutton,newprofilebutton)
        
    def updatesettings(self,Settings):
        Settings.right._text = pygame.key.name(broken.currentprofile.keylist[1])
        Settings.right.value = broken.currentprofile.keylist[1]
        Settings.left._text = pygame.key.name(broken.currentprofile.keylist[0])
        Settings.left.value = broken.currentprofile.keylist[0]
        Settings.jump._text = pygame.key.name(broken.currentprofile.keylist[2])
        Settings.jump.value = broken.currentprofile.keylist[2]
        Settings.shoot._text = pygame.key.name(broken.currentprofile.keylist[3])
        Settings.shoot.value = broken.currentprofile.keylist[3]
        Settings.save._text = pygame.key.name(broken.currentprofile.keylist[4])
        Settings.save.value = broken.currentprofile.keylist[4]
    
class NewProfilePage:
    def __init__(self, rend, Mega, Settings):
        new = Label("Name: ")
        new.position = 350,280
        name = Entry('Player')
        name.position = 410,280
        saveprofilebutton = Button("Save")
        saveprofilebutton.position = 390, 330
        saveprofilebutton.connect_signal(SIG_CLICKED, createprofile, name)
        saveprofilebutton.connect_signal(SIG_CLICKED, changerenderer, rend.settings)
        saveprofilebutton.connect_signal(SIG_CLICKED, self.updatesettings, Settings)
        rend.newprofile.add_widget(Mega,new,name,saveprofilebutton)
        
    def updatesettings(self, Settings):
        Settings.right._text = pygame.key.name(broken.currentprofile.keylist[1])
        Settings.right.value = broken.currentprofile.keylist[1]
        Settings.left._text = pygame.key.name(broken.currentprofile.keylist[0])
        Settings.left.value = broken.currentprofile.keylist[0]
        Settings.jump._text = pygame.key.name(broken.currentprofile.keylist[2])
        Settings.jump.value = broken.currentprofile.keylist[2]
        Settings.shoot._text = pygame.key.name(broken.currentprofile.keylist[3])
        Settings.shoot.value = broken.currentprofile.keylist[3]
        Settings.save._text = pygame.key.name(broken.currentprofile.keylist[4])
        Settings.save.value = broken.currentprofile.keylist[4]
        
class SettingsPage:
    def __init__(self, rend, Mega):
        settingstable = Table(5,2)
        settingstable.position = 290,330
        r = Label("Right: ")
        self.right = Keysym()
        l = Label("Left: ")
        self.left = Keysym()
        j = Label("Jump: ")
        self.jump = Keysym()
        sh = Label("Shoot: ")
        self.shoot = Keysym()
        sa = Label("Save: ")
        self.save = Keysym()
        keylist = [self.left, self.right, self.jump, self.shoot, self.save]
        settingstable.add_child(0,0,r)
        settingstable.add_child(0,1,self.right)
        settingstable.add_child(1,0,l)
        settingstable.add_child(1,1,self.left)
        settingstable.add_child(2,0,j)
        settingstable.add_child(2,1,self.jump)
        settingstable.add_child(3,0,sh)
        settingstable.add_child(3,1,self.shoot)
        settingstable.add_child(4,0,sa)
        settingstable.add_child(4,1,self.save)
        megamancolorbutton = Button("Set MegaMan's Color")
        megamancolorbutton.position = 480,330
        megamancolorbutton.connect_signal(SIG_CLICKED, changerenderer, rend.megamancolor)
        savesettingsbutton = Button("Save")
        savesettingsbutton.position = 480,410
        savesettingsbutton.connect_signal(SIG_CLICKED, savesettings, keylist)
        savesettingsbutton.connect_signal(SIG_CLICKED, changerenderer, rend.main)
        rend.settings.add_widget(Mega,currentname,settingstable,megamancolorbutton,savesettingsbutton)

class MegamanColorPage:
    def __init__(self, rend, Mega):
        megaimage = ImageLabel('',"pics/idle1.blue.tga")
        megaimage.position = 300,280
        colorlist = ScrolledList(100,160)
        colorlist.position = 425, 275
        colorlist.selectionmode = SELECTION_SINGLE
        colorlist.items.append(TextListItem('Black'))
        colorlist.items.append(TextListItem('Red'))
        colorlist.items.append(TextListItem('Green'))
        colorlist.items.append(TextListItem('Blue'))
        colorlist.items.append(TextListItem('Teal'))
        colorlist.items.append(TextListItem('Maroon'))
        colorlist.items.append(TextListItem('Purple'))
        colorlist.items.append(TextListItem('Orange'))
        colorlist.connect_signal(SIG_SELECTCHANGE, self.previewer, colorlist)
        savemegacolorbutton = Button("Save Color")
        savemegacolorbutton.position = 450,450
        savemegacolorbutton.connect_signal(SIG_CLICKED, self.savecolor, colorlist)
        savemegacolorbutton.connect_signal(SIG_CLICKED, changerenderer, rend.settings)
        rend.megamancolor.add_widget(Mega,megaimage,colorlist,savemegacolorbutton)

    def previewer(colorlist):
        color = colorlist.get_selected()[0].text
        if color == 'Black':
            megaimage.set_picture("pics/idle1.black.tga")
        elif color == 'Red':
            megaimage.set_picture("pics/idle1.red.tga")
        elif color == 'Green':
            megaimage.set_picture("pics/idle1.green.tga")
        elif color == 'Blue':
            megaimage.set_picture("pics/idle1.blue.tga")
        elif color == 'Teal':
            megaimage.set_picture("pics/idle1.teal.tga")
        elif color == 'Maroon':
            megaimage.set_picture("pics/idle1.maroon.tga")
        elif color == 'Purple':
            megaimage.set_picture("pics/idle1.puple.tga")
        elif color == 'Orange':
            megaimage.set_picture("pics/idle1.orange.tga")


    def savecolor(colorlist):
        color = colorlist.get_selected()[0].text
        if color == 'Black':
            broken.currentprofile.color = "black"
        elif color == 'Red':
            broken.currentprofile.color = "red"
        elif color == 'Green':
            broken.currentprofile.color = "green"
        elif color == 'Blue':
            broken.currentprofile.color = "blue"
        elif color == 'Teal':
            broken.currentprofile.color = "teal"
        elif color == 'Maroon':
            broken.currentprofile.color = "maroon"
        elif color == 'Purple':
            broken.currentprofile.color = "purple"
        elif color == 'Orange':
            broken.currentprofile.color = "orange"

if __name__ == "__main__":
    try:
        profiles = cPickle.load(open('profilelist', 'r'))
        print profiles
    except:
        profiles = []
        #print "did not load profiles"
        pass
    cp = "no current name"
    for file in profiles:
        if file.currentprofile:
            cp = file.name
    Rend = Renderers()
    mega = pygame.image.load("megaman2.png").convert()
    mega = pygame.transform.scale(mega,(mega.get_width()*2/3,mega.get_height()*2/3))
    Mega = ImageLabel('', mega)
    Mega.position = 150,80
    currentname = Label(cp)
    currentname.position = 390,280
    Main = MainPage(Rend, Mega)
    Host = HostPage(Rend, Mega)
    Join = JoinPage(Rend, Mega)
    Settings = SettingsPage(Rend, Mega)
    ProfileScreen = ProfileScreenPage(Rend, Mega, Settings)
    NewProfile = NewProfilePage(Rend, Mega, Settings)
    MegamanColor = MegamanColorPage(Rend, Mega)

    currentrend = Rend.main
    play = 1
    while play:
        events = pygame.event.get()
        if not currentrend.distribute_events(*events):
            play = 0
        currentrend.force_update()
        if currentrend.esc and currentrend.previous != None:
            currentrend.esc = 0
            changerenderer(currentrend.previous)
