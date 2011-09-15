import time
import pygame

#import psyco
#psyco.full()
#psyco.log()

class event:
    def __init__(self, delay, function, argument):
        if delay == "END":
            self.time = "END"
        else:
            self.time = time.time() + delay
            self.function = function
            self.argument = argument


    def execute(self):
        #print self.function, self.argument
        self.function(self.argument)

    def delay(self,delay):
        self.time = self.time + delay

    def make_null(self):
        self.time = "END"
        self.function = ''
        self.argument = ''


class event_heap:
    def __init__(self):
        self.nullevent = event("END","", "")
        self.nullevent.make_null()
        self.heap = [self.nullevent]
    def put(self,event):
        length = len(self.heap)
        hops = (length - 1) / 2
        offset = length / 2
        pointer = length / 2
        while hops > 0:
            if self.heap[pointer].time <= event.time:
                offset = -max(offset / 2,1)
            else:
                offset = max(offset / 2,1)
                pointer = pointer + offset
            hops = max(hops - 1,0)

        if pointer == 0:
            self.heap.insert(1,event)
        elif self.heap[pointer].time <= event.time:
            self.heap.insert(pointer,event)
        else:
            self.heap.insert(pointer + 1 ,event)
    def get(self):
        next = self.heap.pop()
        if next.time == "END":
            self.heap.append(self.nullevent)
        return next
    def next(self):
        """Returns the next node without removing it from the heap."""
        return self.heap[-1]


class event_queue:
    def __init__(self):
            self.start_time = time.time()
            self.heap = event_heap()
            self.clock = pygame.time.Clock()

            
    def run(self, inputhandler):
            self.running = 1
            while self.running:
                self.reap()
                #time.sleep(.01667)

    def add(self,event):
       self.heap.put(event)
	

    def reap(self):
        now = time.time()
        next_event = self.heap.next()
        while next_event.time != "END" and next_event.time <= now:
           self.heap.get().execute()
           next_event = self.heap.next()
        self.clock.tick()
        #print self.clock.get_fps()
