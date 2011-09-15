# $Id: EventManager.py,v 1.14 2005/09/17 09:07:04 marcusva Exp $
#
# Copyright (c) 2004-2005, Marcus von Appen
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Event management system for any type of events and objects."""

from Signals import Event

class EventManager (object):
    """EventManager () -> EventManager

    An event distribution system.

    The EventManager enables objects to receive events. Each object can
    register several signal types, on which occurance the EventManager
    will call the object's 'notify' method with that event.

    Events also can be distributed by invoking the 'emit()' method of
    the EventManager.

    Attributes:
    queues       - A dict with signal-list associations of registered objects.
    eventgrabber - The event grabbing object, which will receive all events.
    """
    
    __slots__ = ["queues", "_grabber"]
    
    def __init__ (self):
        self.queues = {}
        self._grabber = None

    def add_object (self, obj, *signals):
        """E.add_object (...) -> None

        Adds an object to the EventManger.

        Adds an object as listener for one or more events to the
        EventManager. Each event type in the *signals argument will
        cause the object to be added to a respective queue, on which
        events with the same type will be emitted.

        Raises an AttributeError, if the passed 'obj' argument does
        not have a callable notify attribute.
        """
        if not hasattr (obj, "notify") or not callable (obj.notify):
            raise AttributeError ("notify() method not found in object %s"
                                  % obj)
        for key in signals:
            self.queues.setdefault (key, []).append (obj)

    def remove_object (self, obj, *signals):
        """E.remove_object (...) -> None

        Removes an object from the EventManager.

        Removes the object from the queues passed as the 'signals'
        arguments. If 'signals' is None, the object will be removed
        from all queues of the EventManager.
        """
        if signals:
            evlist = signals
        else:
            evlist = self.queues.keys ()

        for signal in evlist:
            if obj in self.queues[signal]:
                self.queues[signal].remove (obj)
    
    def grab_events (self, obj):
        """E.grab_events (...) -> None

        Sets an event grabber object for the EventManager.

        Causes the EventManager to send _all_ its event only to this
        object instead of the objects in its queues. It is up to the
        event grabbing object to filter the events, it received.
        """
        if obj and (not hasattr (obj, "notify") or not callable (obj.notify)):
            raise AttributeError ("notify() method not found in object %s"
                                  % obj)
        self._grabber = obj
    
    def emit (self, signal, data):
        """E.emit (...) -> None

        Emits an event, which will be sent to the objects.

        Emits an event on a specific queue of the EventManager, which
        will be sent to the objects in that queue. If one of the
        receiving objects sets the 'handled' attribute of the event to
        True, the emission will stop immediately so that following
        objects will not receive the event.
        """
        ev = Event (signal, data)
        if self.eventgrabber:
            self.eventgrabber.notify (ev)
            return

        evlist = self.queues.get (signal, [])
        for obj in evlist:
            obj.notify (ev)
            if ev.handled:
                break
    
    eventgrabber = property (lambda self: self._grabber,
                             lambda self, var: self.grab_events (var),
                             doc = "Sets the event grabber object.")
