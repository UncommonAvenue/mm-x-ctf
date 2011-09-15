import random, sys
import string
import pygame
from pygame.locals import *
import sprite_engine

import hud
import profile


teams = []
team1 = sprite_engine.team("blue")
team2 = sprite_engine.team("red")
teams.append(team1)
teams.append(team2)

class animatedsprite(sprite_engine.simplesprite):
    def __init__(self, spriteengine, image, states, animations, startingstate, x, y):

        sprite_engine.simplesprite.__init__(self, spriteengine, image, x, y)

	self.currentstate = startingstate
	self.states = states
	self.animations = animations

    def animate(self):
        animation = self.animations
	newstate = []
        for state in self.states:           #need better naming convention
	    animation = animation[state.getstate()]
	    newstate.append(state.getstate())
            #once it goes through all levels of states,
            #in most cases 2, it will have an animation object

	if str(animation.__class__) == "<type 'function'>": #silly checky thing to be really cool
            animation = animation()[0]
	
	if newstate != self.currentstate:			#seems like an ugly hack to me.
		if newstate[0] != self.currentstate[0]:
			animation.currentframe = 0
			
		animation.animate(self, 1)
		self.currentstate = newstate
		
		return
	animation.animate(self, 0)
#I don't quite like how the below states system is
###############################################
class states:
    def __init__(self):
        self.states = {}
        self.priority = []
        self.default = ''

    def getstate(self):
        for value in self.priority:
            if self.states[value]:
                return value
        return self.default

    def __getitem__(self,item):
	try:
	    return self.states[item]
	except:
	    return None
    def __setitem__(self, item, value):
	self.states[item] = value
		
class megamainstates(states):
	def __init__(self):
		self.states = 	{"death"       : 0,
               			"injured"     : 0,  
               			"wallsliding" : 0,
               			"climbing"    : 0,
              			"falling"     : 0,
               			"jumping"     : 0,
               			"dashing"     : 0,
               			"running"     : 0,
                                "landing"     : 0,
               			"idle"        : 1,
                		 } 
		self.priority =	["death", "injured", "wallsliding", "climbing", "falling", "jumping", "dashing", "running", "landing", "idle"]
		self.default  = "idle"

class megasubstates(states):
	def __init__(self):
		self.states =	{"shooting" : 0,
                  		"charging" : 0,
                 		"normal"   : 1
                 		}
		self.priority = ["shooting", "charging", "normal"]
		self.default = "normal"
#################################################
class megaman(animatedsprite, hud.hud, profile.profile):
    def __init__(self, spriteengine, x, y, color, team):        #this is so ugly, there is no reason for this.

        self.engine = spriteengine
	####################################I want this junk somewhere else I think.  Or somehow condensed.
	#####################################
	#####################################
	jump_list = [self.engine.load_image("pics/jump1" + "." + color + ".tga"),
                self.engine.load_image("pics/jump2" + "." + color + ".tga"),
                self.engine.load_image("pics/jump3" + "." + color + ".tga"),
                self.engine.load_image("pics/jump4" + "." + color + ".tga")]

 	charge_jump_list = [self.engine.load_image("pics/jump1.f.tga"),
                self.engine.load_image("pics/jump2.f.tga"),
                self.engine.load_image("pics/jump3.f.tga"),
                self.engine.load_image("pics/jump4.f.tga")]

	fall_list = [self.engine.load_image("pics/jump5" + "." + color + ".tga"),
			self.engine.load_image("pics/jump5" + "." + color + ".tga"),
			self.engine.load_image("pics/jump5" + "." + color + ".tga")]

        charge_fall_list = [self.engine.load_image("pics/jump5.f.tga"),
			self.engine.load_image("pics/jump5.f.tga"),
			self.engine.load_image("pics/jump5.f.tga")]

        landing_list = [self.engine.load_image("pics/jump6" + "." + color + ".tga"),
                        self.engine.load_image("pics/jump7" + "." + color + ".tga")]
		
	run_list = [self.engine.load_image("pics/run1" + "." + color + ".tga"),
			self.engine.load_image("pics/run2" + "." + color + ".tga"),
			self.engine.load_image("pics/run3" + "." + color + ".tga"),
			self.engine.load_image("pics/run4" + "." + color + ".tga"),
			self.engine.load_image("pics/run5" + "." + color + ".tga"),
			self.engine.load_image("pics/run6" + "." + color + ".tga"),
			self.engine.load_image("pics/run7" + "." + color + ".tga"),
			self.engine.load_image("pics/run8" + "." + color + ".tga"),
			self.engine.load_image("pics/run9" + "." + color + ".tga"),
			self.engine.load_image("pics/run10" + "." + color + ".tga"),
			self.engine.load_image("pics/run11" + "." + color + ".tga")]

        charge_run_list = [self.engine.load_image("pics/run1.f.tga"),
			self.engine.load_image("pics/run2.f.tga"),
			self.engine.load_image("pics/run3.f.tga"),
			self.engine.load_image("pics/run4.f.tga"),
			self.engine.load_image("pics/run5.f.tga"),
			self.engine.load_image("pics/run6.f.tga"),
			self.engine.load_image("pics/run7.f.tga"),
			self.engine.load_image("pics/run8.f.tga"),
			self.engine.load_image("pics/run9.f.tga"),
			self.engine.load_image("pics/run10.f.tga"),
			self.engine.load_image("pics/run11.f.tga")]

	
	shoot_run_list = [  self.engine.load_image("pics/runshoot1" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot2" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot3" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot4" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot5" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot6" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot7" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot8" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot9" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot10" + "." + color + ".tga"),
				self.engine.load_image("pics/runshoot1" + "." + color + ".tga")]
	
	shoot_idle_list = [ self.engine.load_image("pics/idleshoot1" + "." + color + ".tga"),
                            self.engine.load_image("pics/idleshoot2" + "." + color + ".tga"),
                            self.engine.load_image("pics/idleshoot1" + "." + color + ".tga"),
			    self.engine.load_image("pics/idleshoot2" + "." + color + ".tga")]

	
	idle_list = [self.engine.load_image("pics/idle1" + "." + color + ".tga"),
			self.engine.load_image("pics/idle1" + "." + color + ".tga")]

	charge_idle_list = [self.engine.load_image("pics/idle1.f.tga"),
                            self.engine.load_image("pics/idle1.f.tga"),
                            self.engine.load_image("pics/idle1.f.tga")]

	death_list = [self.engine.load_image("pics/death1" + "." + color + ".tga"),
                      self.engine.load_image("pics/death2" + "." + color + ".tga"),
                      self.engine.load_image("pics/death3" + "." + color + ".tga"),
                      self.engine.load_image("pics/death3" + "." + color + ".tga")]
			
	idleblink_list = [self.engine.load_image("pics/idle1" + "." + color + ".tga"),
			self.engine.load_image("pics/idle2" + "." + color + ".tga"),
			self.engine.load_image("pics/idle3" + "." + color + ".tga"),
			self.engine.load_image("pics/idle4" + "." + color + ".tga"),
			self.engine.load_image("pics/idle1" + "." + color + ".tga")]

	bubbles1_list = [self.engine.load_image("pics/bubble1_1.tga"),
                         self.engine.load_image("pics/bubble1_2.tga"),
                         self.engine.load_image("pics/bubble1_3.tga"),
                         self.engine.load_image("pics/bubble1_4.tga"),
                         self.engine.load_image("pics/bubble1_5.tga"),
                         self.engine.load_image("pics/bubble1_6.tga"),
                         self.engine.load_image("pics/bubble1_7.tga"),
                         self.engine.load_image("pics/bubble1_8.tga"),
                         self.engine.load_image("pics/bubble1_9.tga"),
                         self.engine.load_image("pics/bubble1_10.tga"),
                         self.engine.load_image("pics/bubble1_11.tga")]

	bubbles2_list = [self.engine.load_image("pics/bubble2_1.tga"),
                         self.engine.load_image("pics/bubble2_2.tga"),
                         self.engine.load_image("pics/bubble2_3.tga"),
                         self.engine.load_image("pics/bubble2_4.tga"),
                         self.engine.load_image("pics/bubble2_5.tga"),
                         self.engine.load_image("pics/bubble2_6.tga"),
                         self.engine.load_image("pics/bubble2_7.tga"),
                         self.engine.load_image("pics/bubble2_8.tga"),
                         self.engine.load_image("pics/bubble2_9.tga"),
                         self.engine.load_image("pics/bubble2_10.tga"),
                         self.engine.load_image("pics/bubble2_11.tga")]

        dash_list = [self.engine.load_image("pics/dash1" + "." + color + ".tga"),
                     self.engine.load_image("pics/dash2" + "." + color + ".tga"),
                     self.engine.load_image("pics/dash2" + "." + color + ".tga"),
                     self.engine.load_image("pics/dash2" + "." + color + ".tga")]
        
                  
        dashshoot_list = [self.engine.load_image("pics/dashshoot1" + "." + color + ".tga"),
                         self.engine.load_image("pics/dashshoot2" + "." + color + ".tga"),
                         self.engine.load_image("pics/dashshoot2" + "." + color + ".tga"),
                         self.engine.load_image("pics/dashshoot2" + "." + color + ".tga")]

        dash = animation(dash_list, [0,0,.2,0], [0,0,0,0],0)
        dashshoot = animation(dashshoot_list, [0,0,.2,0], [0,0,megaman.stopshoot,0],0)

	dashcharge_list = [self.engine.load_image("pics/dash1.f.tga"),
                     self.engine.load_image("pics/dash2.f.tga"),
                     self.engine.load_image("pics/dash2.f.tga"),
                     self.engine.load_image("pics/dash2.f.tga")]
	
        dashcharge = animation(dashcharge_list, [0,0,.2,0], [0,0,0,0],0)

	
	death = animation(death_list, [.1,.1,.4,.5], [0,0,0,megaman.respawn], 0 )
	
	jump = animation(jump_list, [0.1,0.1, .01667 ,0.2], [0,0,0,0], 0)
        chargejump = animation(charge_jump_list, [0.1,0.1, .01667 ,0.2], [0,0,0,0], 0)

	landing = animation(landing_list, [.1,.1],[0,megaman.land],0)

	fall = animation(fall_list, [0,0,0], [], 0)
	chargefall = animation(charge_fall_list, [0,0,0], [], 1)

	run = animation(run_list, [0,0,0,0,0,0,0,0,0,0,0], [], 1)
	chargerun = animation(charge_run_list, [0,0,0,0,0,0,0,0,0,0,0], [], 1)

	idle = animation(idle_list, [0,0], [], 1)
	chargeidle = animation(charge_idle_list, [0,0,0], [], 1)
	idleblink = animation(idleblink_list, [5, 0, 0, 0, 5], [], 1)

	

	self.charge1 = bubbleanimation(bubbles1_list, [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,megaman.chargelevel],1)
	self.charge2 = bubbleanimation(bubbles2_list, [0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,megaman.chargelevel],1)

        wallsliding = [self.engine.load_image("pics/wallslide1" + "." + color + ".tga"),
                        self.engine.load_image("pics/wallslide2" + "." + color + ".tga"),
                       self.engine.load_image("pics/wallslide3" + "." + color + ".tga"),
                       self.engine.load_image("pics/wallslide3" + "." + color + ".tga")]

        wall = animation(wallsliding, [0.1,0.1,0.1,0.1], [0,0, megaman.turn, 0], 0)

        wallshooting = [ self.engine.load_image("pics/wallslideshoot4" + "." + color + ".tga"),
                        self.engine.load_image("pics/wallslideshoot3" + "." + color + ".tga"),
                         self.engine.load_image("pics/wallslideshoot2" + "." + color + ".tga"),
                         self.engine.load_image("pics/wallslideshoot1" + "." + color + ".tga")]
        wallshoot = animation(wallshooting, [0.1,0.1,0.1,0.1], [0,0,megaman.turn, 0], 0)


        wallcharging = [self.engine.load_image("pics/wallslide1.f.tga"),
                        self.engine.load_image("pics/wallslide2.f.tga"),
                       
                       self.engine.load_image("pics/wallslide3.f.tga"),
                        self.engine.load_image("pics/wallslide3.f.tga")]
                       

        wallcharge = animation(wallcharging, [0.1,0.1,0.1,0.1], [0,0, megaman.turn, 0], 0)

	walljumping = [self.engine.load_image("pics/wallslide4" + "." + color + ".tga"),
                        self.engine.load_image("pics/wallslide6" + "." + color + ".tga"),
                       self.engine.load_image("pics/jump3" + "." + color + ".tga"),
                       self.engine.load_image("pics/jump3" + "." + color + ".tga"),
                       self.engine.load_image("pics/jump3" + "." + color + ".tga")]
                       

	walljump = animation(walljumping, [0.1, 0,0.1, .01667 ,0.2], [megaman.walljump1,0,megaman.walljump2,megaman.walljump3,0], 0)


        injured_list = [self.engine.load_image("pics/injured1." + color + ".tga"),
                        self.engine.load_image("pics/injured2." + color + ".tga"),
                        self.engine.load_image("pics/injured3." + color + ".tga"),
                        self.engine.load_image("pics/injured4." + color + ".tga"),
                        self.engine.load_image("pics/injured5." + color + ".tga"),
                        self.engine.load_image("pics/injured6." + color + ".tga"),
                        self.engine.load_image("pics/injured7." + color + ".tga"),
                        self.engine.load_image("pics/injured8." + color + ".tga"),
                        self.engine.load_image("pics/injured9." + color + ".tga"),
                        self.engine.load_image("pics/injured10." + color + ".tga"),
                        self.engine.load_image("pics/injured11." + color + ".tga")
                        ]
        injured = animation(injured_list,[0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,megaman.uninjure],0)

        self.injured = 0

        self.walljumping = 0
        self.runningdirection = 0
	shootidle = animation(shoot_idle_list, [0,0,0,0], [0, 0, megaman.stopshoot, 0], 1)
	shootrun = animation(shoot_run_list, [0,0,0,0,0,0,0,0,0,0,0], [megaman.stopshoot,megaman.stopshoot,megaman.stopshoot,megaman.stopshoot,megaman.stopshoot,megaman.stopshoot,megaman.stopshoot,megaman.stopshoot,megaman.stopshoot,megaman.stopshoot,megaman.stopshoot], 1)
	self.color = color
###########################################
	self.bubbles = None
	self.currentstate = ["idle", "normal"]
	self.states = [megamainstates(),megasubstates()]
	self.animations = {
		"death":    	{   "normal" : death,
				"shooting": death,
				"charging": death
				},
		
		"injured":   	{   "normal" : injured,
				"shooting": injured,
				"charging": injured
				},
		"wallsliding": 	{   "normal"  : wall,
				"shooting": wallshoot,
				"charging": wallcharge
				},
		"falling":   	{   "normal" : fall,
				"shooting": fall,
				"charging": chargefall
				},
                "jumping":      {"normal" : lambda: self.walljumping and [walljump] or [jump],  #all I can say is wow.
				"shooting": lambda: self.walljumping and [walljump] or [jump],
				"charging": lambda: self.walljumping and [walljump] or [chargejump] 
				},
		"dashing":   	{   "normal" : dash,
				"shooting": dashshoot,
				"charging": dashcharge
				},
		"running":   	{   "normal" : run,
				"shooting": shootrun,
				"charging": chargerun
				},
                "landing":   	{   "normal" : landing,
				"shooting": landing,
				"charging": landing
                                },
		"idle":   	{   "normal" : idle,
				"shooting": shootidle,
				"charging": chargeidle
                                }
			}
###########################################
	animatedsprite.__init__(self, self.engine, "pics/idle1" + "." + color + ".tga", self.states, self.animations, self.currentstate, x, y)
	self.type = "megaman"
	self.projectiles = 0
	self.chargestage = 0
        self.hp = 17
        self.dead = 0
	self.view = None
	
        
        self.conhan = 0
        
        self.sliding = 0
	self.team = team

	self.deathcount = 0
        self.killcount = 0

        hud.hud.__init__(self)
        profile.profile.__init__(self)


        self.charging = 0

    def turn(self):
        self.currentfacing = self.currentfacing * -1


    def automove(self):     
        x, y = 0, 0
         #determine speed from states
        
        if self.states[0]["running"] and not self.states[0]["dashing"]:
            x = 5*self.currentfacing*6
        if self.states[0]["jumping"]:
            y = -5*6
            if self.states[0]["dashing"] == 1:
                y = y - 3*6
            self.jumping = self.jumping + 1
            if self.jumping >= 15:
                self.stopjump()
        if self.states[0]["falling"]:
            y = 10*6
        if self.states[0]["dashing"]:
            self.dashing = self.dashing + 1
            if self.dashing % 2 == 0:
                if self.states[0]["jumping"] == 0 and self.states[0]["falling"] == 0 and self.states[0]["wallsliding"] == 0:
                    dust(self.engine, self.rect.centerx, self.rect.bottom - 5)
            if self.dashing >= 12:
                self.stopdash()
            x = 5*2*6*self.currentfacing
        if self.states[0]["wallsliding"]:
            x = 0
            y = 1*6
#            if self.currentfacing == 1:
#               dust(self.engine,self.rect.left,self.rect.centery + 5)
#           else:
#               dust(self.engine,self.rect.right,self.rect.centery + 5)
        if self.states[0]["injured"]:
	    x = -2*self.currentfacing
            y = 1*-2
        if self.states[0]["death"]:
            x = 0
            y = -3

        self.move(x,y)
        self.check_collisions()
	try:
            if self.charging > 0:
                if self.charging % 2 == 1:
                    self.states[1].states["charging"] = 1
                else:
                    self.states[1].states["charging"] = 0
                self.charging = self.charging + 1
                if self.charging > 30:
                    self.chargelevel()
                    self.charging = 1
            self.animate()
            if self.chargestage == 2:
                self.charge2.animate(self, 0)
            elif self.chargestage == 1: # or self.states[1].states["charging"]:
                self.charge1.animate(self, 0)
    
            else:
                self.bubbles = None
	    self.view.follow()	#I moved this out from self.move because here it won't give a bounce after check collisions.
	    if self.view.collider.rect.colliderect(self.rect) == 0:
		self.death(self)
	except:
            pass
	
    def can_act(self):
	if self.dead == 1:
		return 0
	return 1	
    
    def death(self, sprite):
	if self.dead == 0:
		self.deathcount = self.deathcount + 1
		#should switch on what is sent, based on if it is a self kill or not.  Pass killer sprite into death maybe?
		try:	#default their name to so and so if they don't have one.
			name = self.name
		except:
			name = "so and so"
		if sprite == self:
 			self.engine.sendall( name + " has killed himself.")
		else:
			try:	#default their name to so and so if they don't have one.
				name2 = sprite.name
			except:
				name2 = "so and so"
			self.engine.sendall( name + " was killed by " + name2 + ".")
		
       		self.engine.check_death_end(self.deathcount)
		self.dead = 1   
		self.states[0].states["death"] = 1

    def respawn(self):
        #check for a respawn timer
  	spawns = []	#maybe I should just generate this at the beginning?
  	try:
            for spawn in self.team.spawns:
                if spawn.can_spawn(self):
			spawns.append(spawn)
	except:
            for spawn in self.engine.respawns:
                if spawn.can_spawn(self):
                        spawns.append(spawn)
            
	#set it to a random spawn point
	if len(spawns) == 0: #if there are no open spawn points, just respawn in place
		pass
	else:
        	spawn = spawns[random.randint(0,len(spawns) - 1 ) ] 
        	self.rect.centerx = spawn.x
        	self.rect.centery = spawn.y 
		self.currentfacing = spawn.facing
        self.states[0].states["death"] = 0
        self.hp = 17    #make not a constant
        self.dead = 0
        #play spawn animation

    def goright(self):
	if self.can_act():
        	self.states[0]["running"] = 1	#this is pretty ugly
        	self.currentfacing = 1
		self.runningdirection = 1

    def goleft(self):
	if self.can_act():
		self.states[0]["running"] = 1	#this is pretty ugly
		self.currentfacing = -1
		self.runningdirection = -1

    def stopgoright(self):
	if self.currentfacing == 1:
        	self.states[0]["running"] = 0	
		self.runningdirection = 0 
	if self.states[0]["wallsliding"]:
            self.states[0]["wallsliding"] = 0
	    self.states[0]["running"] = 0
	    self.runningdirection = 0
		
    
    def stopgoleft(self):
	if self.currentfacing == -1:
        	self.states[0]["running"] = 0
		self.runningdirection = 0	
	if self.states[0]["wallsliding"]:
            self.states[0]["wallsliding"] = 0
	    self.states[0]["running"] = 0
	    self.runningdirection = 0
			
    def joystop(self):
        self.runningdirection = 0
        if self.states[0]["wallsliding"]:
            self.states[0]["wallsliding"] = 0
        else:
           self.states[0]["running"] = 0	#this is pretty ugly

    def walljump1(self):
        if self.sliding == -1 and self.currentfacing == -1:
            return
        elif self.sliding == 1 and self.currentfacing == 1:     #facing the same way as sliding
            return
        else:
            self.turn()

    def walljump2(self):
        self.rect.centerx = self.rect.centerx + self.rect.width * self.currentfacing / 2
        if self.runningdirection != self.currentfacing:
            self.currentfacing = self.currentfacing * -1

    def walljump3(self):
        self.rect.centerx = self.rect.centerx + self.rect.width * -1 * self.currentfacing / 2
 
    def jump(self):
        if self.can_act():
                if self.states[0]["wallsliding"]:
                    self.states[0]["wallsliding"] = 0
                    self.walljumping = 1   
                self.states[0]["jumping"] = 1
                self.jumping = 1
		
    def stopjump(self):
	if self.walljumping:
		self.walljumping = 0
	self.states[0]["jumping"] = 0
	self.jumping = 0
	
    def stopshoot(self):
	self.states[1]["shooting"] = 0
        
    def startfall(self):
        if self.states[0]["jumping"] == 0 and self.states[0]["wallsliding"] == 0:
            self.states[0]["falling"] = 1
            self.walljumping = 0
        if self.runningdirection != 0:
            self.states[0].states["running"] = 1
            
    def stopfall(self):
        if self.states[0]["falling"] == 1:
            self.states[0]["falling"] = 0

    def charge(self):
        if self.can_act():
            self.states[1].states["charging"] = 1
            self.charging = 1
            print "charging"

    def chargelevel(self):
        if self.chargestage < 2:
            self.chargestage += 1                
            print "increase power"

    def stopfall(self):
        if self.states[0]["falling"] == 1:
            self.states[0]["falling"] = 0
            self.states[0]["landing"] = 1

    def land(self):
        self.states[0]["landing"] = 0
        
 
    def dash(self):
        if self.states[0]["falling"] or self.states[0]["jumping"] or self.states[0]["wallsliding"]:
            return
        self.states[0].states["dashing"] = 1
        click(self.engine,self.rect.centerx, self.rect.bottom)
        self.dashing = 1
        
    def stopdash(self):
        self.states[0].states["dashing"] = 0
        self.dashing = 0

    def shoot(self):
	if self.can_act():
                self.charging = 0
		if self.projectiles >= 3:
			return
		self.engine.play_sound("sounds/Colt45.wav", self)
		if self.chargestage == 2:
                    shot = proj_charge2(self.engine, self.rect.centerx + 10*self.currentfacing, self.rect.centery, self)
                elif self.chargestage == 1:
                    shot = proj_charge1(self.engine, self.rect.centerx + 10*self.currentfacing, self.rect.centery, self)
                else:
                    shot = projectile(self.engine, self.rect.centerx + 10*self.currentfacing, self.rect.centery, self)
		if self.currentfacing == 1:
			shot.rect.left = self.rect.right + 1
		else:
			shot.rect.right = self.rect.left - 1
		self.projectiles = self.projectiles + 1
		self.states[1].states["shooting"] = 1
		self.states[1].states["charging"] = 0
		self.chargestage = 0
		
    def collide_top(self, sprite):
        if sprite.type == "projectile":
            self.no_collide_top()                   #act like there was no collide
            return
	if sprite.type == "megaman":
	    if not sprite.rect.bottom == self.rect.top + 1:
                    self.rect.top = sprite.rect.bottom - 1
        if sprite.type == "level":
            self.stopjump()
        
    def collide_bottom(self, sprite):
        if sprite.type == "projectile" or sprite.type == "flag":
            self.no_collide_bottom()                #act like there was no collide
            return
	if sprite.type == "megaman":
	    if not sprite.rect.top == self.rect.bottom - 1:
                    self.rect.bottom = sprite.rect.top + 1
        self.stopfall()
	if self.states[0].states["wallsliding"] == 1:
		self.states[0].states["running"] = 0
        self.states[0].states["wallsliding"] = 0
        if self.runningdirection == 0:
		self.states[0].states["running"] = 0
	else:
        	self.currentfacing = self.runningdirection
        	self.states[0].states["running"] = 1
        
    def collide_right(self, sprite):
         if sprite.type == "projectile":
            return
	 if sprite.type == "megaman":
             if (self.states[0]["running"] == 1 or self.states[0]["dashing"] ) and self.currentfacing == 1:
                 if not sprite.rect.left == self.rect.right - 1:
                    self.rect.right = sprite.rect.left
		    return
	 if sprite.type == "level":
             #sets initial wallslide	
             if self.states[0].states["running"] and (self.states[0].states["falling"] or self.states[0].states["jumping"]) and self.currentfacing == 1:
                 self.states[0].states["falling"] = 0
                 self.states[0].states["jumping"] = 0
                 self.states[0].states["wallsliding"] = 1
                 click(self.engine,self.rect.right, self.rect.bottom)
                 self.sliding = 1

            

    def collide_left(self, sprite):
        if sprite.type == "projectile":
            return
        if sprite.type == "megaman":
             if (self.states[0]["running"] == 1 or self.states[0]["dashing"] ) and self.currentfacing == -1:
                 if not sprite.rect.right == self.rect.left + 1:
                    self.rect.left = sprite.rect.right
		    return
        if sprite.type == "level":
            if self.states[0].states["running"] and (self.states[0].states["falling"] or self.states[0].states["jumping"]) and self.currentfacing == -1:
                self.states[0].states["falling"] = 0
                self.states[0].states["jumping"] = 0
                self.states[0].states["wallsliding"] = 1
                click(self.engine,self.rect.left, self.rect.bottom)
                self.sliding = -1

          
    def no_collide_left(self):
        #print self.sliding
        if self.sliding == -1:
            self.states[0].states["wallsliding"] = 0
            self.startfall()
            self.sliding = 0

    def no_collide_right(self):
        #print self.sliding
        if self.sliding == 1:
            self.states[0].states["wallsliding"] = 0
            self.startfall()
            self.sliding = 0

    def no_collide_bottom(self):
        self.startfall()

    def injure(self):
        self.injured = 1
        self.states[0].states["injured"] = 1

    def uninjure(self):
        self.injured = 0
        self.states[0].states["injured"] = 0
    
    	
   

class dust(animatedsprite):
    def __init__(self,engine,x,y):
        dustlist = [engine.load_image("pics/dust2.tga"),
			 engine.load_image("pics/dust2.tga"),
			 engine.load_image("pics/dust3.tga"),
			 engine.load_image("pics/dust4.tga"),
                         engine.load_image("pics/dust5.tga")]
        self.dustanim = animation(dustlist, [.0,0.0,0.0,0.0], [0,0,0,0,dust.death], 0)
        animations = {"normal" : self.dustanim}
        duststates = states()
        duststates.states = {"normal" : 1}
        dust.priority = ["normal"]
        animatedsprite.__init__(self, engine, "pics/dust1.tga", [duststates], animations, ["normal"], x, y)
        self.type = "dust"
        self.check_collisions()
    def automove(self):
        self.move(0, -7)
        self.dustanim.animate(self,0)

    def collide_top(self, sprite):
        pass
    def collide_right(self, sprite):
        pass
    def collide_left(self, sprite):
        pass    
    def collide_bottom(self, sprite):
        pass
    
class click(sprite_engine.simplesprite):
    def __init__(self,engine,x,y):
        sprite_engine.simplesprite.__init__(self, engine, "pics/xbuster3.gif",x, y)
        self.timer = 3
        self.type = "click"
    def automove(self):
        self.timer = self.timer - 1
        if self.timer == 0:
            self.death()
    def collide_top(self, sprite):
        pass
    def collide_right(self, sprite):
        pass
    def collide_left(self, sprite):
        pass    
    def collide_bottom(self, sprite):
        pass
    
class projectile(animatedsprite):
    def __init__(self, sprite_engine, x, y, owner = None):
	self.damage = 1
	self.owner = owner
	projstates = states()
	projstates.states = {"flying" : 1, "exploding": 0}
	projstates.priority = ["exploding", "flying"]
	try:
		 color = self.owner.color
	except:
		color = "rgb"
	flyinglist = [sprite_engine.load_image("pics/xbuster.tga"),
      		      sprite_engine.load_image("pics/xbusterfly1.tga"),
		      sprite_engine.load_image("pics/xbuster.tga")]

	
	explodinglist = [sprite_engine.load_image("pics/xbuster1.tga"),
			 sprite_engine.load_image("pics/xbuster2.tga"),
			 sprite_engine.load_image("pics/xbuster3.tga"),
			 sprite_engine.load_image("pics/xbuster3.tga")]

	
	flyinganim = animation(flyinglist, [0,0,0], [0,0,0], 1 )
	explodinganim = animation(explodinglist, [0,0,0.01,0.01], [0,0,0,projectile.death], 0)
	
	animations = {"flying" : flyinganim,
		      "exploding": explodinganim}
	
	
	animatedsprite.__init__(self, sprite_engine, "pics/xbuster.tga", [projstates], animations, ["flying"], x, y)
	self.type = "projectile"
	self.dead = 0
	
        if self.owner:
		if self.owner.currentfacing == -1:
			self.currentfacing = -1
	self.check_collisions()	#go ahead and see if it hits anything right away

    def death(self):
        self.owner.projectiles = self.owner.projectiles - 1
        animatedsprite.death(self)
    
    def automove(self):
	if self.states[0]["flying"]:
        	self.move(60*self.currentfacing , 0)
	self.check_collisions()
	self.animate()
	############# Check the projectiles distance from its owner.  kill if it goes off screen.
        if self.owner.view:                                                             ##if it has a view, check if it is contained within view
            if self.owner.view.collider.rect.contains(self.rect):
                pass
            else:                                                   ##kill it if it isn't
                self.death()
        else:
            if abs(self.rect.centerx - self.owner.rect.centerx) > 400:
                self.death()

    def can_injure(self,sprite):
	if sprite.dead == 1 or self.dead == 1:
	    return 0
	if sprite.injured == 1:
            return 0
	if sprite.team == self.owner.team:	#no .team right now
	    return 0
	else:
	    return 1
    
    def collide(self, sprite):
	if self.dead:
		return
        if sprite.type == "megaman" and sprite !=self.owner:   
            if self.can_injure(sprite):
                sprite.injure()
                sprite.hp = sprite.hp - self.damage
                if sprite.hp <= 0:
                        self.owner.killcount = self.owner.killcount + 1 #give the owner a kill
                        sprite.death(self.owner)
                        self.engine.check_kill_end(self.owner.killcount)
        if sprite.type != "projectile" and sprite != self.owner: #do nothing to anyone else.
            self.dead = 1
            self.states[0]["flying"] = 0
            self.states[0]["exploding"] = 1
#	    self.death()
	    
    def collide_top(self, sprite):
        self.collide(sprite)
            
    def collide_right(self, sprite):
        self.collide(sprite)
	if self.dead:
		self.rect.centerx = sprite.rect.left
            
    def collide_left(self, sprite):
        self.collide(sprite)
	if self.dead:
		self.rect.centerx = sprite.rect.right
            
    def collide_bottom(self, sprite):
        self.collide(sprite)

class proj_charge1(projectile):
    def __init__(self, sprite_engine, x, y, owner = None):
	self.damage = 2
	self.owner = owner
	projstates = states()
	projstates.states = {"flying" : 1, "exploding": 0}
	projstates.priority = ["exploding", "flying"]
	try:
		 color = self.owner.color
	except:
		color = "rgb"
	flyinglist = [sprite_engine.load_image("pics/charge1_1.tga"),
      		      sprite_engine.load_image("pics/charge1_2.tga"),
		      sprite_engine.load_image("pics/charge1_3.tga"),
                      sprite_engine.load_image("pics/charge1_4.tga"),
                      sprite_engine.load_image("pics/charge1_5.tga"),
                      sprite_engine.load_image("pics/charge1_6.tga"),
                      sprite_engine.load_image("pics/charge1_7.tga")]

	
	explodinglist = [sprite_engine.load_image("pics/xbuster1.tga"),
			 sprite_engine.load_image("pics/xbuster2.tga"),
			 sprite_engine.load_image("pics/xbuster3.tga"),
			 sprite_engine.load_image("pics/xbuster3.tga")]

	
	flyinganim = animation(flyinglist, [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], 1 )
	explodinganim = animation(explodinglist, [0,0,0.01,0.01], [0,0,0,projectile.death], 0)
	
	animations = {"flying" : flyinganim,
		      "exploding": explodinganim}
	
	
	animatedsprite.__init__(self, sprite_engine, "pics/charge1_1.tga", [projstates], animations, ["flying"], x, y)
	self.type = "projectile"
	self.dead = 0
	
	if self.owner:
		if self.owner.currentfacing == -1:
			self.currentfacing = -1
	self.check_collisions()	#go ahead and see if it hits anything right away

class proj_charge2(projectile):
    def __init__(self, sprite_engine, x, y, owner = None):
	self.damage = 4
	self.owner = owner
	print self.owner
	projstates = states()
	projstates.states = {"flying" : 1, "exploding": 0}
	projstates.priority = ["exploding", "flying"]
	flyinglist = [sprite_engine.load_image("pics/charge2_1.tga"),
      		      sprite_engine.load_image("pics/charge2_2.tga"),
		      sprite_engine.load_image("pics/charge2_3.tga"),
                      sprite_engine.load_image("pics/charge2_4.tga"),
                      sprite_engine.load_image("pics/charge2_5.tga")]

	
	explodinglist = [sprite_engine.load_image("pics/xbuster1.tga"),
			 sprite_engine.load_image("pics/xbuster2.tga"),
			 sprite_engine.load_image("pics/xbuster3.tga"),
			 sprite_engine.load_image("pics/xbuster3.tga")]

	
	flyinganim = animation(flyinglist, [0,0,0,0,0], [0,0,0,0,0], 1 )
	explodinganim = animation(explodinglist, [0,0,0.01,0.01], [0,0,0,projectile.death], 0)
	
	animations = {"flying" : flyinganim,
		      "exploding": explodinganim}
	
	
	animatedsprite.__init__(self, sprite_engine, "pics/charge2_1.tga", [projstates], animations, ["flying"], x, y)
	self.type = "projectile"
	self.dead = 0
	
	if self.owner:
		if self.owner.currentfacing == -1:
			self.currentfacing = -1
	self.check_collisions()	#go ahead and see if it hits anything right away
	
class animation:	#this whole thing needs to be rewritten.
    def __init__(self, images, delays, functions, cycles):
        self.images = images
        self.delays = delays
        self.functions = functions
        self.cycles = cycles
        self.currentframe = 0
        self.currentdelay = 0

    def animate(self, sprite, nodelay):
        self.sprite = sprite
	if self.delays[self.currentframe] <= self.currentdelay or nodelay:	#nodelay is mainly for switching between two different animations.
            self.currentdelay = 0.0
            if self.currentframe >= (len(self.images) - 1): 
	    	if self.cycles:
               		self.currentframe = 1 #or whatever the beginning of the cycle will be#
		else:
			self.currentframe = len(self.images) - 1
                self.sprite.image = self.images[self.currentframe]
            elif self.currentframe < (len(self.images) - 1) and self.currentframe != 0:
               self.currentframe = self.currentframe + 1
               self.sprite.image = self.images[self.currentframe]
            elif self.currentframe == 0:
               self.sprite.image = self.images[self.currentframe]
               self.currentframe = self.currentframe + 1
            try:
                self.functions[self.currentframe](sprite)
	    except:
                pass
        else:
            self.currentdelay = self.currentdelay + .01667

class bubbleanimation(animation):
    def animate(self, sprite, nodelay):
        self.sprite = sprite
	if self.delays[self.currentframe] <= self.currentdelay or nodelay:	#nodelay is mainly for switching between two different animations.
            self.currentdelay = 0.0
            if self.currentframe >= (len(self.images) - 1): 
	    	if self.cycles:
               		self.currentframe = 1 #or whatever the beginning of the cycle will be#
		else:
			self.currentframe = len(self.images) - 1
                self.sprite.bubbles = self.images[self.currentframe]
            elif self.currentframe < (len(self.images) - 1) and self.currentframe != 0:
               self.currentframe = self.currentframe + 1
               self.sprite.bubbles = self.images[self.currentframe]
            elif self.currentframe == 0:
               self.sprite.bubbles = self.images[self.currentframe]
               self.currentframe = self.currentframe + 1
            try:
                self.functions[self.currentframe](sprite)
	    except:
                pass
        else:
            self.currentdelay = self.currentdelay + .01667

class flag(sprite_engine.simplesprite):

    def __init__(self, team, spriteengine, x, y):
   #     self.engine = spriteengine
    #    normal = [self.engine.load_image("flag.jpg"),
     #             self.engine.load_image("flag.jpg")]

      #  flag = animation(normal, [.1,.1],[0,0],1)
       # self.states = 'idle'
       # self.animations = {'idle':flag}
       # animatedsprite.__init__(self, spriteengine, 'flag.jpg', self.states, self.animations, 'idle', x, y)
        sprite_engine.simplesprite.__init__(self,spriteengine,"flag.jpg",x,y)
        self.carried = 0
        self.type = 'flag'
        self.team = team
        self.spawnx = x
        self.spawny = y

    def automove(self):
        self.check_collisions()
        if self.carried:
            
            if self.carried.dead:
                self.carried = 0
            elif self.carried.currentfacing == 1:
                self.rect.centery = self.carried.rect.centery
                self.rect.right = self.carried.rect.left
            else:
                self.rect.centery = self.carried.rect.centery
                self.rect.left = self.carried.rect.right
        

    def collide(self, sprite):
        if sprite.type == 'flag':
            if sprite.rect.centerx == sprite.spawnx and sprite.rect.centery == sprite.spawny:
                    #increase score
                self.respawn()
                
        if sprite.type == 'megaman' and self.carried == 0:
            if sprite.team == self.team:
                self.respawn()
            else:
                self.carried = sprite
             
              

    def collide_top(self, sprite):
        self.collide(sprite)
            
    def collide_right(self, sprite):
        self.collide(sprite)
            
    def collide_left(self, sprite):
        self.collide(sprite)
            
    def collide_bottom(self, sprite):
        self.collide(sprite)

    def respawn(self):
        self.carried = 0
        self.rect.centerx = self.spawnx
        self.rect.centery = self.spawny 

def make_megaman(sprite_engin, color = ''):

        if teams:
            least = teams[0].nummembers
            leastteam = teams[0]
            for team in teams:
                if team.nummembers < least:
                    least = team.nummembers
                    leastteam = team
            color = leastteam.color
        else:
            if color == '':
                for num in range(0,3):
                        a = random.randint(1,3)
                        if a == 1:
                                color = color + "r"
                        if a == 2:
                                color = color + "g"
                        if a == 3:
                                color = color + "b"
	
	#for now team = color
	#later it should be based on user input, and color should be based on team
	newmega = megaman(sprite_engin, 0, 0, color, color)
	try:
            leastteam.add_member(newmega)
            sprite_engin.sendall("New player has joined the game.")	#change to using their name & team color
        except:
            sprite_engin.sendall("New player has joined the game.")	#change to using their name, once that is fully in.
	
        newmega.respawn()
	return newmega
		
		

