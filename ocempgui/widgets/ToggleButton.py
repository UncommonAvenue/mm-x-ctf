# $Id: ToggleButton.py,v 1.22 2005/09/15 23:37:55 marcusva Exp $
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

"""A button widget, which can retain its state."""

from Button import Button
from Constants import *
import base

class ToggleButton (Button):
    """ToggleButton (text) -> ToggleButton

    A button widget class, which can retain its state.

    The default ToggleButton widget looks and behaves usually the same
    as the Button widget except that it will retain its state upon clicks.

    The state of the ToggleButton can be set with the 'active' attribute
    or set_active() method. If the ToggleButton is active, the 'state'
    attribute will be set to STATE_ACTIVE by default and will be reset,
    if the ToggleButton is not active anymore.

    toggle.active = True
    toggle.set_active (False)
    
    Default action (invoked by activate()):
    The Button emulates a SIG_TOGGLED event and runs the connected
    callbacks.
    
    Mnemonic action (invoked by activate_mnemonic()):
    See the Button class.
    
    Signals:
    SIG_TOGGLED - Invoked, when the ToggleButton is toggled.

    Attributes:
    active - The current state of the ToggleButton as boolean.
    """
    def __init__ (self, text):
        Button.__init__ (self, text)

        # Internal click handler
        self.__click = False
        self._active = False
        
        # The ToggleButton emits a 'toggled' event.
        self._signals[SIG_TOGGLED] = []

    def set_active (self, active):
        """T.set_active (...) -> None

        Sets the state of the ToggleButton.
        """
        if active:
            if not self._active:
                self._active = True
                if self.sensitive:
                    self.state = STATE_ACTIVE
                # Enforce an update here, because the state might have
                # been already modified in the notify() method.
                self.dirty = True
        else:
            if self._active:
                self._active = False
                if self.sensitive:
                    self.state = STATE_NORMAL
                # Enforce an update here, because the state might have
                # been already modified in the notify() method.
                self.dirty = True
    
    def activate (self):
        """T.activate () -> None

        Activates the ToggleButton default action.

        Activates the Button default action. This usually means toggling
        the button, emulated by inverting the 'active' attribute and
        running the attached callbacks for the SIG_TOGGLED signal.
        """
        if base.debug: print "ToggleButton.activate ()"
        if not self.sensitive:
            return
        self.focus = True
        self.set_active (not self.active)
        self.run_signal_handlers (SIG_TOGGLED)

    def notify (self, event):
        """T.notify (event) -> None

        Notifies the ToggleButton about an event.
        """
        if not self.eventarea or not self.sensitive:
            return # Not completely realized or sensitive.
        
        elif event.signal == SIG_MOUSEDOWN:
            if self.eventarea.collidepoint (event.data.pos):
                if base.debug: print "ToggleButton.MOUSEDOWN"
                self.focus = True
                # The button only acts upon left clicks.
                if event.data.button == 1:
                    self.__click = True
                    self.state = STATE_ACTIVE
                self.run_signal_handlers (SIG_MOUSEDOWN)
        
        elif event.signal == SIG_MOUSEUP:
            if self.eventarea.collidepoint (event.data.pos):
                if base.debug: print "ToggleButton.MOUSEUP"
                self.run_signal_handlers (SIG_MOUSEUP)
                if event.data.button == 1:
                    if self.__click:
                        # The usual order for a ToggleButton: get a
                        # click and toggle state upon it.
                        if base.debug: print "ToggleButton.CLICKED"
                        self.run_signal_handlers (SIG_CLICKED)
                        self.set_active (not self.active)
                        if base.debug: print "ToggleButton.TOGGLED"
                        self.run_signal_handlers (SIG_TOGGLED)
                        if not self.active:
                            self.state = STATE_ENTERED
            elif (event.data.button == 1) and self.__click and not self.active:
                # Only a half click was made, reset the state of the
                # ToggleButton.
                self.state = STATE_NORMAL

        elif event.signal == SIG_MOUSEMOVE:
            # If the state was set in any way although the button's
            # not active, reset the state.
            if (not self.active) and (self.state == STATE_ACTIVE):
                self.state = STATE_NORMAL
            Button.notify (self, event)
        else:
            # Any other event will be escalated to the parent(s).
            Button.notify (self, event)

    active = property (lambda self: self._active,
                       lambda self, var: self.set_active (var),
                       doc = "The state of the ToggleButton.")
