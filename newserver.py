#import psyco
#psyco.full()
#psyco.log()


#new server
import socket, string, thread
import pygame
import sprite_engine, animated_sprite, eventqueue
import controlhandler

class server_connection:
    def __init__(self, server ,client, surface, sprite_engin, eventqueue):
        self.sock = client
        self.server = server
        self.server.clients.append(self)
        self.eventqueue = eventqueue
        self.engine = sprite_engin
        self.engine.imagelibrary.sendsync(self)
	self.engine.soundlibrary.sendsync(self)
	self.engine.musiclibrary.sendsync(self)
	self.ready = 0
	

	megaman = animated_sprite.make_megaman(sprite_engin)
        self.focus = megaman
        self.conhan = controlhandler.controlhandler(self.eventqueue,self.focus)

        self.view = sprite_engine.networkview(surface, sprite_engin)
        self.view.target(megaman)
        self.view.set_limits(pygame.Rect(0,0,800*4,600*4) )
        self.view.client = self
	if self.engine.currentmusic:
		self.view.play_music(self.engine.currentmusic)
        self.listen()


    def recv(self):       	#would be nice to do some buffering 
	value = ''
        newval = self.sock.recv(1)
	while newval != '\n':
		value = value + newval
		newval = self.sock.recv(1)
	return value + '\n'

    def listen(self):
        while 1:
            value = ''
            value = self.recv()
            type = value[0:value.find(":")]         #this probably adds some lag.  Right now I need it for chat data.  That sucks.
            data = value[value.find(":")+1:-1]      #this too!              I need a new way of doing things!!!
            self.interpret(type, data)


    def interpret(self, type, data):    #switches on the type
      	if type == "r":
	    self.ready = 1
	    return
        elif type == "c":
	    self.engine.sendall(data)
            return
        elif type =="dc":
            self.disconnect()
	    return
        self.conhan.executebuffer(data)
            
    def disconnect(self):               #disconnects from the server
        try:
            self.server.clients.remove(self)
            self.view.engine.views.remove(self.view)
            self.sock.close()
        except:
            pass
        

    def send(self,string):
        try:
            self.sock.send(string)
        except:
            self.disconnect()
            pass
    

class server:
    def __init__(self, port, surface, sprite_engin, eventqueue):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	self.sock.bind(('',port))
	self.sock.listen(5)
	self.surface = surface
	self.engine = sprite_engin
        self.running = 1
        self.clients = []
        thread.start_new_thread(self.listen,())
        self.eventqueue = eventqueue


    def listen(self):
        while self.running:
            try:
                clientsocket,address = self.sock.accept()
                thread.start_new_thread(server_connection,(self, clientsocket, self.surface, self.engine, self.eventqueue)) #creates a new thread per client
            except: 
                pass
    def shutdown(self):
        self.running = 0
