import pygame
from pygame.locals import *
import cPickle

from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import TextListItem
import ocempgui.draw.Image

import broken
import clientinput
import updown
import level

global currentrend
currentrend = 0

def changerenderer(renderer):
    global currentrend
    currentrend = renderer
    return currentrend

def updatesettings():
    currentname.text = broken.currentprofile.name + '      '    #ugly hack
    right._text = pygame.key.name(broken.currentprofile.keylist[1])
    right.value = broken.currentprofile.keylist[1]
    left._text = pygame.key.name(broken.currentprofile.keylist[0])
    left.value = broken.currentprofile.keylist[0]
    jump._text = pygame.key.name(broken.currentprofile.keylist[2])
    jump.value = broken.currentprofile.keylist[2]
    shoot._text = pygame.key.name(broken.currentprofile.keylist[3])
    shoot.value = broken.currentprofile.keylist[3]
    save._text = pygame.key.name(broken.currentprofile.keylist[4])
    save.value = broken.currentprofile.keylist[4]

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


def savecolor():
    if black._active:
        broken.currentprofile.color = "black"
    elif red._active:
        broken.currentprofile.color = "red"
    elif green._active:
        broken.currentprofile.color = "green"
    elif blue._active:
        broken.currentprofile.color = "blue"
    elif teal._active:
        broken.currentprofile.color = "teal"
    elif maroon._active:
        broken.currentprofile.color = "maroon"
    elif purple._active:
        broken.currentprofile.color = "purple"
    elif orange._active:
        broken.currentprofile.color = "orange"
        
def createprofile(name):
    print name.text
    try:
        profiles = cPickle.load(open('profilelist', 'r'))
        print profile
    except:
        profiles = []
        #print "did not load profiles"
        pass
    current = profile(name.text)
    current.load()
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
                file.load()
        
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
        
class profile:
    def __init__(self, name):
        self.name = name
        self.killcount = 0
        self.deathcount = 0
        self.color = 'blue'
        self.keylist = [K_LEFT, K_RIGHT, K_UP, K_a, K_F8]

    def load(self):
        broken.currentprofile = self
        clientinput.currentprofile = self
        print "success ", broken.currentprofile.name

if __name__ == "__main__":
    #create all the renderers
    main = MenuRenderer(None)
    main.create_screen(800,600)
    main.title = "MegaMan"
    main.color = (0,0,0)
    host = MenuRenderer(main)
    host.create_screen(800,600)
    host.title = "MegaMan"
    host.color = (0,0,0)
    join = MenuRenderer(main)
    join.create_screen(800,600)
    join.title = "MegaMan"
    join.color = (0,0,0)
    profilescreen = MenuRenderer(main)
    profilescreen.create_screen(800,600)
    profilescreen.title = "MegaMan"
    profilescreen.color = (0,0,0)
    newprofile = MenuRenderer(profilescreen)
    newprofile.create_screen(800,600)
    newprofile.title = "MegaMan"
    newprofile.color = (0,0,0)
    settings = MenuRenderer(profilescreen)
    settings.create_screen(800,600)
    settings.title = "MegaMan"
    settings.color = (0,0,0)
    megamancolor = MenuRenderer(settings)
    megamancolor.create_screen(800,600)
    megamancolor.title = "MegaMan"
    megamancolor.color = (0,0,0)

    #create the widgets in each renderer
    mega = pygame.image.load("megaman2.png").convert()
    mega = pygame.transform.scale(mega,(mega.get_width()*2/3,mega.get_height()*2/3))
    Mega = ImageLabel('', mega)
    Mega.position = 150,80
    #man = pygame.image.load("Man.gif").convert()
    #man = pygame.transform.scale(man,(man.get_width()*2/3,man.get_height()*2/3))
    #Man = ImageLabel('',man)
    #Man.position = 270,160
    port = Label("port: ")
    port.position = 350, 330
    ip = Label("ip:")
    ip.position = 350, 280
    input_port = Entry('8182')
    input_port.position = 410, 330
    input_ip = Entry('localhost')
    input_ip.position = 410, 280
    levellist = ScrolledList(100,100)
    levellist.position = 350, 380
    levellist.selectionmode = SELECTION_SINGLE
    levellist.items.append(TextListItem('updown'))
    levellist.items.append(TextListItem('level'))
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
    new = Label("Name: ")
    new.position = 350,280
    name = Entry('default')
    name.position = 410,280
    currentname = Label("no current name")
    currentname.position = 390,280
    settingstable = Table(5,2)
    settingstable.position = 290,330
    r = Label("Right: ")
    right = Keysym()
    l = Label("Left: ")
    left = Keysym()
    j = Label("Jump: ")
    jump = Keysym()
    sh = Label("Shoot: ")
    shoot = Keysym()
    sa = Label("Save: ")
    save = Keysym()
    keylist = [left, right, jump, shoot, save]
    settingstable.add_child(0,0,r)
    settingstable.add_child(0,1,right)
    settingstable.add_child(1,0,l)
    settingstable.add_child(1,1,left)
    settingstable.add_child(2,0,j)
    settingstable.add_child(2,1,jump)
    settingstable.add_child(3,0,sh)
    settingstable.add_child(3,1,shoot)
    settingstable.add_child(4,0,sa)
    settingstable.add_child(4,1,save)
    megaimage = ImageLabel('',"pics/idle1.blue.tga")
    megaimage.position = 300,280
    hostbutton = Button("Host")
    hostbutton.position = 390,280
    hostbutton.connect_signal(SIG_CLICKED, changerenderer, host)
    joinbutton = Button("Join")
    joinbutton.position = 390,330
    joinbutton.connect_signal(SIG_CLICKED, changerenderer, join)
    hoststartbutton = Button("Play")
    hoststartbutton.position = 390,490
    hoststartbutton.connect_signal(SIG_CLICKED, startgame, 'host', 'localhost', input_port,levellist)
    joinstartbutton = Button("Play")
    joinstartbutton.position = 390,380
    joinstartbutton.connect_signal(SIG_CLICKED, startgame, 'join', input_ip, input_port)
    profilebutton = Button("Profiles")
    profilebutton.position = 390,380
    profilebutton.connect_signal(SIG_CLICKED, changerenderer, profilescreen)
    newprofilebutton = Button("New Profile")
    newprofilebutton.position = 420,330
    newprofilebutton.connect_signal(SIG_CLICKED, changerenderer, newprofile)
    loadbutton = Button("Load Profile")
    loadbutton.position = 420,280
    loadbutton.connect_signal(SIG_CLICKED, loadprofile, profilelist)
    loadbutton.connect_signal(SIG_CLICKED, changerenderer, settings)
    loadbutton.connect_signal(SIG_CLICKED, updatesettings)
    saveprofilebutton = Button("Save")
    saveprofilebutton.position = 390, 330
    saveprofilebutton.connect_signal(SIG_CLICKED, createprofile, name)
    saveprofilebutton.connect_signal(SIG_CLICKED, changerenderer, settings)
    saveprofilebutton.connect_signal(SIG_CLICKED, updatesettings)
    megamancolorbutton = Button("Set MegaMan's Color")
    megamancolorbutton.position = 480,330
    megamancolorbutton.connect_signal(SIG_CLICKED, changerenderer, megamancolor)
    savesettingsbutton = Button("Save")
    savesettingsbutton.position = 480,410
    savesettingsbutton.connect_signal(SIG_CLICKED, savesettings, keylist)
    savesettingsbutton.connect_signal(SIG_CLICKED, changerenderer, main)

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
    colorlist.connect_signal(SIG_SELECTCHANGE, previewer, colorlist)
    
    savemegacolorbutton = Button("Save Color")
    savemegacolorbutton.position = 450,450
    savemegacolorbutton.connect_signal(SIG_CLICKED, savecolor)
    savemegacolorbutton.connect_signal(SIG_CLICKED, changerenderer, settings)
    

    #add widgets to renderer
    main.add_widget(Mega,hostbutton,joinbutton,profilebutton)
    host.add_widget(Mega,port,input_port,levellist,hoststartbutton)
    join.add_widget(Mega,ip,input_ip,port,input_port,joinstartbutton)
    profilescreen.add_widget(Mega,profilelist,loadbutton,newprofilebutton)
    newprofile.add_widget(Mega,new,name,saveprofilebutton)
    settings.add_widget(Mega,currentname,settingstable,megamancolorbutton,savesettingsbutton)
    megamancolor.add_widget(Mega,megaimage,colorlist,savemegacolorbutton)

    #start main loop
    currentrend = main
    play = 1
    while play:
        events = pygame.event.get()
        if not currentrend.distribute_events(*events):
            play = 0
        currentrend.force_update()
        if currentrend.esc and currentrend.previous != None:
            currentrend.esc = 0
            changerenderer(currentrend.previous)
