import string
import pygame

try:
	pygame.mixer.init()
except:
	nosound = 1
	print "There will be no sounds."
	
class entry:
	def __init__(self, id, name, data = None):		#this class should only be init'ed by the library class
		self.id = id			#numerical id of the entry
		self.name = name		#name of the file the data is loaded from
		self.data = data		#the data once it is loaded from the file

	def load(self, filename):
		#there should be some error detection when a file is not loaded correctly.
		pass
	def sendfile(self, socket):
		pass

class imageentry(entry):
	def load(self, filename):
		#there should be some error detection when a file is not loaded correctly.
		image = pygame.image.load(filename).convert()
		#image.set_alpha(225)
#		image = pygame.transform.scale2x(image)
#		image = pygame.transform.scale2x(image)
		image.set_colorkey((255,255,255,255))
		imageflip = pygame.transform.flip(image, 1, 0 )
		#imageflip.set_alpha(225)
        	self.data = (image, imageflip )    #uglky
        
	def get(self, flip = 0):
		return self.data[flip]

	def __getitem__(self, flip):
            return self.data[flip]
		
class soundentry(entry):
	def load(self, filename):
		try:
			self.data = pygame.mixer.Sound(filename)
		except:
			pass
	def get(self):
		return self.data
		
class musicentry(entry):
	def load(self, filename):
		try:
			self.data = pygame.mixer.music.load(filename)
		except:
			pass
	def get(self):
		return self.data

class library:
	def __init__(self, libtype = "image"):
		self.type = libtype
		self.currentid = 0
		self.entries = {}

	def load(self, filename):
		if self.get(filename):
#			return filename
			return self.get(filename).id
		self.create(self.currentid, filename)
		self.currentid = self.currentid + 1
#		return filename	#I think this is for legacy support
		return self.currentid - 1  #when I move to sending the id instead of the name
			
	def create(self, id, filename):
		if self.type == "image":
			newentry = imageentry(id, filename)
			
		if self.type == "sound":
			newentry = soundentry(id, filename)

		if self.type == "music":
			newentry = musicentry(id, filename)	
		newentry.load(filename)
		self.entries[id] = newentry
		return newentry

	def get(self, id):
		#should be able to get on id and on filename
		try:	#if its an int
			return self.entries[int(id)]		#they should be stored in the correct order based on id number.
		except:
			for entry in self.entries.values():		
				if entry.name == id:
					return entry
		return None 
	
	def sendsync(self, socket):
		socket.send( self.type[0] + "s:" )
		for entry in self.entries.values():
			socket.send( str(entry.id) + "," + entry.name + ";" )
		socket.send("\n")
	
	def recvsync(self, value):				#rename like all the variables in this, so it makes more sense?
		values = value.split(";")
        	values = values[:len(values)-1]
		for data in values:				#this needs to be tested to make sure it works.
            		data = data.split(",")
            		data[0] = int(data[0])
            		self.create(data[0], data[1])
        	#there should be some error detection when a file is not loaded correctly.

	def sendfile(self, id, socket):
		pass

	def recvfile(self, socket):
		pass
