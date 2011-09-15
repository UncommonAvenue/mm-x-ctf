# $Id: Signals.py,v 1.9 2005/09/08 15:45:56 marcusva Exp $
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

"""Classes for events and event callbacks, which can be used by the
EventManager class."""

class Event (object):
    """Event (signal, data) -> Event

    Creates a new Event object for the event management system.

    The event object is a simple 'key-value' association containing a
    signal identfier ('signal') and additional data.
    
    Attributes:
    signal  - Identifier of the event (the passed signal).
    data    - Attached data to distribute with the event.
    handled - Indicates, whether the event was handled by an object.
    """

    __slots__ = [ "signal", "data", "handled" ]

    def __init__ (self, signal, data):
        self.signal = signal
        self.data = data
        self.handled = False

class EventCallback (object):
    """EventCallback (signal, callback, *data) -> EventCallback

    Creates a new EventCallback to use as a signal handler for objects.
        
    The EventCallback can be used as container object for event
    mechanisms, which need signal to method bindings.
    The connected callback can be invoked using the EventCallback.run()
    method.
    
    Attributes:
    signal   - Identifier of the event to wait for.
    callback - Function/method to invoke upon receiving the event.
    data     - Data to pass to the function/method.
    """

    __slots__ = ["signal", "data", "callback"]
    
    def __init__ (self, signal, callback, *data):
        self.signal = signal
        if not callable (callback):
            raise TypeError ("callback is not callable")
        self.callback = callback
        self.data = data

    def run (self, *data):
        """E.run (...)

        Invokes the callback of the EventCallback.

        If additional data is supplied via the 'data' argument, the
        already attached callback data in the EventCallback.data
        attribute will be concatenated to it and the result will be
        passed to the callback.
        """
        d = data + self.data
        if len (d) != 0:
            self.callback (*d)
        else:
            self.callback ()
