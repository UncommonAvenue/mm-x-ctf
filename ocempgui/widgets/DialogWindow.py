# $Id: DialogWindow.py,v 1.12 2005/09/17 09:07:04 marcusva Exp $
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

"""A modal window suitable for dialogs and similar purposes."""

from Window import Window
from Bin import Bin
from Container import Container
from ocempgui.events import EventManager

class DialogWindow (Window):
    """DialogWindow (title=None) -> DialogWindow

    Creates a modal window, which blocks any other input.

    The DialogWindow sets itself and its children in a modal state by
    limiting the event distribution to itself only.
    
    Default action (invoked by activate()):
    See the Window class.
    
    Mnemonic action (invoked by activate_mnemonic()):
    See the Window class.
    """
    def __init__ (self, title=None):
        Window.__init__ (self, title)
        self._stop_events = False

    def set_event_manager (self, manager):
        """D.set_event_manager (...) -> None

        Sets the event manager of the DialogWindow.

        Sets the event manager of the DialogWindow and invokes the
        grab_events() method for the DialogWindow.
        """
        if not manager and self.manager:
            self.manager.eventgrabber = None
        Window.set_event_manager (self, manager)
        if self.manager:
            self.manager.eventgrabber = self

    def _notify_children (self, widget, event):
        """D._notify_childre (...) -> None

        Notifies all widgets of the DialogWindow.
        """
        if not self._stop_events:
            if not event.handled:
                widget.notify (event)
                if not self._stop_events:
                    if isinstance (widget, Bin):
                        self._notify_children (widget.child, event)
                    elif isinstance (widget, Container):
                        for child in widget.children:
                            self._notify_children (child, event)
    
    def notify (self, event):
        """D.notify (...) -> None

        Notifies the DialogWindow about an event.
        """
        Window.notify (self, event)
        # Recursively notify all attached children.
        if self.child:
            self._notify_children (self.child, event)
    
    def destroy (self):
        """D.destroy () -> None

        Destroys the DialogWindow and removes it from its event system.
        """
        self._stop_events = True
        if self.manager:
            self.manager.eventgrabber = None
        Window.destroy (self)
