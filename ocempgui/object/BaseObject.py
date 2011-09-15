# $Id: BaseObject.py,v 1.11 2005/09/02 20:52:08 marcusva Exp $
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

"""Basic object class, used as abstract class definition for event
capable objects."""

from ocempgui.events import EventManager, EventCallback

class BaseObject (object):
    """BaseObject () -> BaseObject

    An object class, which is able to receive events.

    The BaseObject provides a basic set of methods, which enable it to
    be suitable for event driven systems. It is able to listen to
    specific event types and runs connected callback functions upon
    their occurance.
    
    It is designed for usage with the EventManager class from the
    ocempgui.events package and needs to be inherited to be fully
    usable.  It can be easily connected to an instance of the
    EventManager via the 'manager' attribute (or using the set_manager()
    method), which also will remove it from another instance, it was
    connected to before. Thus the BaseObject can be only connected to
    ONE EventManager instance at a time by default.

    The BaseObject class does not provide any predefined signals, it
    listens on (those will be called slots here). Instead an inherited
    class has to provide its own signal types within the private
    '_signals' dictionary. The entries within the '_signals' dictionary
    need to be key-value pairs, which have a list as value and a free
    choosable type as key (if the default EventCallback class is
    used). A typical example about how to create own signal slots
    follows:

    class OwnObject (BaseObject):
        ...
        def __init__ (self):
            BaseObject.__init__ (self)
            self._signals['ping'] = []
            self._signals['pong'] = []

    The OwnObject class can listen to signals, which are strings being
    'ping' and 'pong'. It is now possible to connect a callback to those
    signals:

    obj = OwnObject ()
    obj.connect_signal ('ping', cb_func, ...)
    obj.connect_signal ('pong', cb_func, ...)

    Any instance of the BaseObject class should be explicitly destroyed
    using the destroy() method, if it is not needed anymore. This method
    takes care of the deletion any callback objects and removes the
    object from the connected event manager.
    
    Attributes:
    manager  - The event manager for emitting events.
    """
    def __init__ (self):
        self._signals = {}
        self._manager = None

    def connect_signal (self, signal, callback, *data):
        """B.connect_signal (...) -> EventCallback

        Connects a function or method to a signal.

        The function or method is invoked as soon as the signal is
        emitted on the object. If *data is supplied, it will be passed
        as argument(s) to the connected function. The returned
        EventCallback can be used to disconnect the function using
        disconnect_signal().
        """
        ev = EventCallback (signal, callback, *data)
        self._signals[signal].append (ev)
        return ev

    def disconnect_signal (self, event):
        """B.disconnect_signal (...) -> None

        Removes a connected EventCallback from the object.
        """
        self._signals[event.signal].remove (event)

    def run_signal_handlers (self, signal, *data):
        """B.run_signal_handlers (...) -> None

        Invokes all connected EventCallbacks for a specific signal.

        The method invokes all connected callbacks for the given
        signal. Additional data will be passed to the callback invoke,
        if given.
        """
        for callback in self._signals[signal]:
            callback.run (*data)

    def set_event_manager (self, manager):
        """B.set_event_manager (...) -> None

        Sets the event manager to use by the object.

        In case the new event manager to set differs from the current
        event manager, the object will be removed from the current one
        and added to the new event manager.
        
        It is possible to remove the object only by passing a None value
        to the method. The object then will remove itself from the
        connected event manager only.

        Raises a TypeError, if the passed manager does not inherit
        from the EventManager class.
        """
        if manager and not isinstance (manager, EventManager):
            raise TypeError ("manager must inherit from EventManager")

        if self._manager and (self._manager != manager):
            self._manager.remove_object (self)
        self._manager = manager

        # An empty list or pygame.sprite.Group evaluates to False in a
        # boolean expression, thus we need to explicitly check for such
        # objects.
        if self._manager != None:
            self._manager.add_object (self, *self._signals.keys ())

    def emit (self, signal, data):
        """B.emit (...) -> bool

        Emits a signal through the connected event manager.

        Emits a signal using the connected event manager (if any), and
        returns True upon success or False upon an error.
        """
        if self.manager:
            self.manager.emit (signal, data)
            return True
        return False
    
    def notify (self, event):
        """B.notify (...) -> None

        Notifies the object about an event.

        This method has to be implemented by inherited classes. Its
        signature matches the basic requirements of the EventManager
        class of the ocempgui.events package.
        """
        raise NotImplementedError

    def destroy (self):
        """B.destroy () -> None

        Destroys the object and disconnects it from its event manager.

        This method should be called, if the object is not needed
        anymore.
        """
        del self._signals
        if self._manager:
            self._manager.remove_object (self)
        del self._manager

    manager = property (lambda self: self._manager,
                        lambda self, var: self.set_event_manager (var),
                        doc = "The event manager to use by the object.")
