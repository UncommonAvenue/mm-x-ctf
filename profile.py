#profile.py
import pygame
import string
import pygame
from pygame.locals import *
class profile:
    def __init__(self, name = 'Player'):
        self.name = name
        self.killcount = 0
        self.deathcount = 0
        self.color = 'blue'
        self.currentprofile = 0
        self.keylist = [K_LEFT, K_RIGHT, K_UP, K_a, K_F8]
        ##set defaults for now, right here!
        #self.key_bindings = {K_RIGHT: 'right', K_LEFT: 'left', K_UP: 'up', K_a: 'shoot',
        #                     K_F8: 'save', K_ESCAPE: 'escape', K_RETURN: 'chat', K_TAB: 'tab', K_s: 'dash'}
        #controls should be here, but should keybindings?  Yes, I think so.
        #self.controls = {'rightDOWN': self.goright, 'leftDOWN': self.goleft, 'upDOWN': self.jump, 'rightUP': self.stopgoright,
        #                 'leftUP': self.stopgoleft, 'upUP': self.stopjump, 'shootUP': self.shoot, 'centerxDOWN': self.joystop,
        #                 'saveDOWN': self.save, 'escapeDOWN': self.escape, 'chatDOWN': self.chat, 'tabDOWN': self.tab,
        #                 'tabUP': self.untab, 'shootDOWN': self.charge, 'dashDOWN': self.dash, 'dashUP': self.stopdash}
        #self.complexcontrols = {}
    def save(self):
        try:
            print self.currentprofile
            self.currentprofile.killcount = self.currentprofile.killcount + self.killcount
            self.currentprofile.deathcount = self.currentprofile.deathcount + self.deathcount
            self.profiles = cPickle.load(open('profilelist', 'r'))
            print self.profiles
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
            self.key_bindings = {profile.keylist[1]: 'right', profile.keylist[0]: 'left', profile.keylist[2]: 'up',\
                                 profile.keylist[3]: 'shoot', profile.keylist[4]: 'save',\
                                 K_ESCAPE: 'escape', K_RETURN: 'chat', K_TAB: 'tab'}
            print "megaman is now " + self.currentprofile.name
	    self.name = self.currentprofile.name
	    self.color = profile.color
        except:
            print "did not load profile into megaman"
    
