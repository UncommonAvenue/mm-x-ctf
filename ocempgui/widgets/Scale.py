# $Id: Scale.py,v 1.29 2005/09/15 16:24:29 marcusva Exp $
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

"""Slider widgets for selecting a value from a range."""

import pygame.locals
from Range import Range
from Constants import *
import base

class Scale (Range):
    """Scale (minimum, maximum, step=1.0) -> Scale

    Creates an abstract scaling widget for numerical value selections.

    The Scale is an abstract widget class, which enhances the Range by
    different events and an activation method. Concrete Implementations
    of it are the HScale, a horizontal scale widget, and the VScale,
    vertical scale widget.
    
    Inheriting widgets have to implement the get_value_from_coords() and
    get_coords_from_value() methods, which calculate the value of the
    Scale using a pair of coordinates and vice versa. Example
    implementations can be found in the HScale and VScale widget
    classes.
    
    Default action (invoked by activate()):
    Give the Scale the input focus.
    
    Mnemonic action (invoked by activate_mnemonic()):
    None

    Signals:
    SIG_MOUSEDOWN - Invoked, when a mouse button is pressed on the Scale.
    SIG_MOUSEUP   - Invoked, when a mouse buttor is released on the Scale.
    SIG_MOUSEMOVE - Invoked, when the mouse moves over the Scale.
    """
    def __init__ (self, minimum, maximum, step=1.0):
        Range.__init__ (self, minimum, maximum, step)

        # Internal click detection.
        self.__click = False

        self._signals[SIG_MOUSEDOWN] = []
        self._signals[SIG_MOUSEMOVE] = []
        self._signals[SIG_MOUSEUP] = []
        self._signals[SIG_KEYDOWN] = None # Dummy for keyboard activation.

    def activate (self):
        """S.activate () -> None

        Activates the Scale default action.

        Activates the Scale default action. This usually means giving
        the Scale the input focus.
        """
        if base.debug: print "Scale.activate ()"
        if not self.sensitive:
            return
        self.focus = True
    
    def get_value_from_coords (self, coords):
        """S.get_value_from_coords (...) -> float

        Calculates the integer value of the scale from the passed
        coordinates tuple.
        
        This method has to be implemented by inherited widgets.
        """
        raise NotImplementedError

    def get_coords_from_value (self):
        """S._get_coords_from_value () -> float

        Calculates the coordinates from the current value of the scale.

        This method has to be implemented by inherited widgets.
        """
        raise NotImplementedError
    
    def notify (self, event):
        """S.notify (...) -> None

        Notifies the Scale about an event.
        """
        if not self.eventarea or not self.sensitive:
            return

        if event.signal == SIG_MOUSEDOWN:
            if self.eventarea.collidepoint (event.data.pos):
                if base.debug: print "Scale.MOUSEDOWN"
                self.focus = True
                if event.data.button == 1:
                    # Guarantee a correct look, if the signal handlers run a
                    # long time
                    self.state = STATE_ACTIVE
                self.run_signal_handlers (SIG_MOUSEDOWN)
                if event.data.button == 1: # Only react upon left clicks.
                    self.__click = True
                    val = self.get_value_from_coords (event.data.pos)
                    if val != self.value:
                        self.value = val
                # Mouse wheel.
                elif event.data.button == 4:
                    val = self.value - 2 * self.step
                    if val > self.minimum:
                        self.value = val
                    else:
                        self.value = self.minimum
                elif event.data.button == 5:
                    val = self.value + 2 * self.step
                    if val < self.maximum:
                        self.value = val
                    else:
                        self.value = self.maximum
        
        elif event.signal == SIG_MOUSEUP:
            if self.eventarea.collidepoint (event.data.pos):
                if base.debug: print "Scale.MOUSEUP"
                if event.data.button == 1:
                    if self.state == STATE_ACTIVE:
                        self.state = STATE_ENTERED
                    else:
                        self.state = STATE_NORMAL
                    self.__click = False
                self.run_signal_handlers (SIG_MOUSEUP)
            elif (event.data.button == 1) and self.__click:
                self.state = STATE_NORMAL
                self.__click = False
        
        elif event.signal == SIG_MOUSEMOVE:
            if self.eventarea.collidepoint (event.data.pos):
                if base.debug: print "Scale.MOUSEMOVE (inner)"
                self.focus = True
                if self.state == STATE_NORMAL:
                    self.state = STATE_ENTERED
                self.run_signal_handlers (SIG_MOUSEMOVE)
                if self.__click and self.focus:
                    val = self.get_value_from_coords (event.data.pos)
                    if val != self.value:
                        self.value = val
            elif self.state == STATE_ENTERED:
                if base.debug: print "Scale.MOUSEMOVE (outer)"
                self.state = STATE_NORMAL

        elif (event.signal == SIG_KEYDOWN) and self.focus:
            if event.data.key in (pygame.locals.K_KP_PLUS,
                                  pygame.locals.K_PLUS, pygame.locals.K_RIGHT,
                                  pygame.locals.K_DOWN):
                self.increase ()
            elif event.data.key in (pygame.locals.K_KP_MINUS,
                                  pygame.locals.K_MINUS, pygame.locals.K_LEFT,
                                  pygame.locals.K_UP):
                self.decrease ()
            elif event.data.key == pygame.locals.K_PAGEUP:
                val = self.value - 10 * self.step
                if val > self.minimum:
                    self.value = val
                else:
                    self.value = self.minimum
            elif event.data.key == pygame.locals.K_PAGEDOWN:
                val = self.value + 10 * self.step
                if val < self.maximum:
                    self.value = val
                else:
                    self.value = self.maximum
            elif event.data.key == pygame.locals.K_END:
                self.value = self.maximum
            elif event.data.key == pygame.locals.K_HOME:
                self.value = self.minimum

        Range.notify (self, event)

class HScale (Scale):
    """HScale (minimum, maximum, step=1.0) -> HScale

    A horizontal scaling widget for selecting numerical values.

    The HScale widget is a scaling widget with a horizontal orientation
    and allows the user to select and adjust a value from a range moving
    a slider.

    Default action (invoked by activate()):
    See the Scale class.
    
    Mnemonic action (invoked by activate_mnemonic()):
    See the Scale class.
    """
    def __init__ (self, minimum, maximum, step=1.0):
        Scale.__init__ (self, minimum, maximum, step)
        self.size = 120, 20 # Default size.

    def get_value_from_coords (self, coords):
        """H.get_value_from_coords (...) -> float

        Calculates the float value of the Scale.

        Calculates the float value of the Scale from the passed
        coordinates tuple.
        """
        # We need this for a proper calculation.
        st = self.style or base.GlobalStyle.get_style (self.__class__)
        slider = base.GlobalStyle.get_style_entry (self.__class__, st,
                                                   "slider")
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)
        
        # The slide range, in which the slider can move.
        slide = self.width - slider[0] - 2 * border

        # Calculate the absolute current position
        n = coords[0] - self.position[0] - slider[0] / 2.0 - border

        # Step range in dependance of the width and value range of the
        # Scale.
        step = (self.maximum - self.minimum) / float (slide)

        # Calculate it.
        val = self.minimum + step * n
        if val > self.maximum:
            val = self.maximum
        elif val < self.minimum:
            val = self.minimum
        return val

    def get_coords_from_value (self):
        """H.get_coords_from_value () -> float

        Calculates the coordinates from the current value of the HScale.
        """
        # We need this for a proper calculation.
        st = self.style or base.GlobalStyle.get_style (self.__class__)
        slider = base.GlobalStyle.get_style_entry (self.__class__, st,
                                                   "slider")
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)
        
        width = self.size[0]
        if self.rect:
            width = self.width
        
        # The slide range in which the slider can move.
        slide = width - slider[0] - 2 * border

        # Step range in dependance of the width and value range of the
        # Scale.
        step = (self.maximum - self.minimum) / float (slide)

        # Calculate the value
        val  = (self.value - self.minimum) / step + slider[0] / 2.0 + border
        return val

    def draw (self):
        """H.draw () -> Surface

        Draws the HScale surface and returns it.

        Creates the visible surface of the HScale and returns it to the
        caller.
        """
        return base.GlobalStyle.draw_scale (self)
        
class VScale (Scale):
    """VScale (minimum, maximum, step=1.0) -> VScale

    The VScale widget is a scaling widget with a vertical orientation
    and allows the user to select and adjust a value from a range moving
    a slider.
    
    Default action (invoked by activate()):
    See the Scale class.
    
    Mnemonic action (invoked by activate_mnemonic()):
    See the Scale class.
    """
    def __init__ (self, minimum, maximum, step=1.0):
        Scale.__init__ (self, minimum, maximum, step)
        self.size = 20, 120 # Default size.
    
    def get_value_from_coords (self, coords):
        """V.get_value_from_coords (...) -> float

        Calculates the float value of the VScale.

        Calculates the float value of the VScale from the passed
        coordinates tuple.
        """
        # We need this for a proper calculation.
        st = self.style or base.GlobalStyle.get_style (self.__class__)
        slider = base.GlobalStyle.get_style_entry (self.__class__, st,
                                                   "slider")
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)
        
        # The slide range, in which the slider can move.
        slide = self.height - slider[1] - 2 * border

        # Calculate the absolute current position
        n = coords[1] - self.position[1] - slider[1] / 2.0 - border

        # Step range in dependance of the width and value range of the
        # Scale.
        step = (self.maximum - self.minimum) / float (slide)

        # Calculate it.
        val = self.minimum + step * n
        if val > self.maximum:
            val = self.maximum
        elif val < self.minimum:
            val = self.minimum
        return val

    def get_coords_from_value (self):
        """V.get_coords_from_value () -> float

        Calculates the coordinates from the current value of the VScale.
        """
        # We need this for a proper calculation.
        st = self.style or base.GlobalStyle.get_style (self.__class__)
        slider = base.GlobalStyle.get_style_entry (self.__class__,st,
                                                   "slider")
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)
        
        height = self.size[1]
        if self.rect:
            height = self.height
        
        # The slide range in which the slider can move.
        slide = height - slider[1] - 2 * border

        # Step range in dependance of the width and value range of the
        # Scale.
        step = (self.maximum - self.minimum) / float (slide)

        # Calculate the value
        val  = (self.value - self.minimum) / step + slider[1] / 2.0 + border
        return val

    def draw (self):
        """V.draw () -> Surface

        Draws the VScale surface and returns it.

        Creates the visible surface of the VScale and returns it to the
        caller.
        """
        return base.GlobalStyle.draw_scale (self)
