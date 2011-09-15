# $Id: ActionListener.py,v 1.9 2005/09/02 20:52:08 marcusva Exp $
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

"""An object class, which can listen to any event it gets connected to."""

from BaseObject import BaseObject
from ocempgui.events.Signals import EventCallback

class ActionListener (BaseObject):
    """ActionListener () -> ActionListener

    Creates a new ActionListener, which can listen to any signal.

    The ActionListener can listen to any signal connected to it
    through an event. While inheritors of the BaseObject ususally
    reassign the internal signal dictionary, the ActionListener will
    automatically create the matching signal entry for it.

    The callbacks connected to the ActionListener need to match the
    following signature:

    def function_name (*data):
        ...

    Dependant on the data list passed on the connect_signal() call,
    the callbacks need to be able to handle that data. The following
    examples will show how to do this:

    def cb_func (arg1, arg2, arg3):
        ...

    ac = ActionListener ()
    ac.connect_signal (signal, cb_func, first, second, third)

    'first', 'second' and 'third' are passed to the cb_func function
    and are available within this function as 'arg1', 'arg2' and
    'arg3'.

    It is also possible to use a more general argument list within the
    callback:

    def cb_func (*args):
        ...
    """
    def __init__ (self):
        BaseObject.__init__ (self)
    
    def connect_signal (self, signal, callback, *data):
        """A.connect_signal (...) -> EventCallback

        Connects a function or method to a signal.

        The function or method is invoked as soon as the signal is emitted
        on the action listener. If *data is supplied, it will be passed as
        arguments to the connected function. The returned EventCallback can
        be used to disconnect the function using disconnect_signal().
        """
        ev = EventCallback (signal, callback, *data)
        if signal in self._signals:
            self._signals[signal].append (ev)
        else:
            self._signals[signal] = [ev]
            if self.manager:
                self.manager.add_object (self, signal)
        return ev

    def notify (self, event):
        """A.notify (...) -> None

        Notifies the ActionListener about an event.

        It invokes the connected EventCallbacks, which match the
        specific event.signal, using EventCallback.run().
        """
        cblist = self._signals.get (event.signal, [])
        for callback in cblist:
            callback.run (event.data)
