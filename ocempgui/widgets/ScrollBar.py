# $Id: ScrollBar.py,v 1.33 2005/09/15 16:24:29 marcusva Exp $
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

"""A widget, which allows scrolling through buttons and a slider."""

import pygame.locals
from Range import Range
from Constants import *
import base

class ScrollBar (Range):
    """ScrollBar () -> ScrollBar

    Creates a new ScrollBar widget, which allows scrolling.

    The ScrollBar widget works much the same like a Scale widget except
    that it supports buttons for adjusting the value and that its
    minimum value always is 0. It is suitable for widgets which need
    scrolling ability and a scrolling logic.

    Inheriting widgets have to implement the get_value_from_coords() and
    get_coords_from_value() methods, which calculate the value of the
    Scale using a pair of coordinates and vice versa. Example
    implementations can be found in the HScrollBar and VScrollBar widget
    classes. They also need to implement the get_button_coords()
    method, which has to return a tuple of the both button coordinates
    [(x, y, width, height)].
    
    Default action (invoked by activate()):
    Give the ScrollBar the input focus.
    
    Mnemonic action (invoked by activate_mnemonic()):
    None

    Signals:
    SIG_MOUSEDOWN - Invoked, when a mouse button is pressed on the Scale.
    SIG_MOUSEUP   - Invoked, when a mouse buttor is released on the Scale.
    SIG_MOUSEMOVE - Invoked, when the mouse moves over the Scale.

    Attributes:
    button_dec - Indicates, if the decrease button is pressed.
    button_inc - Indicates, if the increase button is pressed.
    """
    def __init__ (self):
        Range.__init__ (self, 0, 1, 1)

        # Signals.
        self._signals[SIG_MOUSEDOWN] = []
        self._signals[SIG_MOUSEMOVE] = []
        self._signals[SIG_MOUSEUP] = []
        self._signals[SIG_KEYDOWN] = None # Dummy for keyboard activation.
        self._signals[SIG_TICK] = None # Dummy for automatic scrolling.
        
        # Internal state handlers for the events. Those need to be known by
        # the inheritors.
        self._button_dec = False
        self._button_inc = False
        self._click = False

    def activate (self):
        """S.activate () -> None

        Activates the ScrollBar default action.

        Activates the ScrollBar default action. This usually means giving
        the ScrollBar the input focus.
        """
        if base.debug: print "ScrollBar.activate ()"
        if not self.sensitive:
            return
        self.focus = True
    
    def get_button_coords (self):
        """S.get_button_coords () -> tuple

        Gets a tuple with the coordinates of the in- and decrease buttons.
        
        This method has to be implemented by inherited widgets.
        """
        raise NotImplementedError

    def get_coords_from_value (self):
        """S.get_coords_from_value () -> float

        Calculates the slider coordinates for the ScrollBar.
        
        This method has to be implemented by inherited widgets.
        """
        raise NotImplementedError

    def get_value_from_coords (self, coords):
        """S.get_value_from_coords (...) -> float

        Calculates the slider coordinates for the ScrollBar.
        
        This method has to be implemented by inherited widgets.
        """
        raise NotImplementedError

    def get_slider_size (self):
        """S.get_slider_size (...) -> int

        Calculates the size of the slider knob.
        
        This method has to be implemented by inherited widgets.
        """
        raise NotImplementedError
    
    def _check_collision (self, pos, rect):
        """S._check_collirion (...) -> bool

        Checks the collision of the given position with the passed rect.
        """
        # Rect: (x, y, width, height), pos: (x, y).
        return (pos[0] >= rect[0]) and (pos[0] <= (rect[2] + rect[0])) and \
               (pos[1] >= rect[1]) and (pos[1] <= (rect[3] + rect[1]))
    
    def set_minimum (self, minimum):
        """S.set_minimum (...) -> Exception

        This method does not have any use.
        """
        pass

    def notify (self, event):
        """S.notify (...) -> None

        Notifies the ScrollBar about an event.
        """
        if not self.eventarea or not self.sensitive:
            return

        if event.signal == SIG_MOUSEDOWN and \
               self.eventarea.collidepoint (event.data.pos):
            if base.debug: print "ScrollBar.MOUSEDOWN"
            self.focus = True
            # Act only on left clicks or scrollwheel events.
            if event.data.button == 1:
                self.state = STATE_ACTIVE
            self.run_signal_handlers (SIG_MOUSEDOWN)
            if event.data.button == 1:
                buttons = self.get_button_coords ()
                if self._check_collision (event.data.pos, buttons[0]):
                    self._button_dec = True
                    self._button_inc = False
                    self._click = False
                    self.decrease ()
                elif self._check_collision (event.data.pos, buttons[1]):
                    self._button_inc = True
                    self._button_dec = False
                    self._click = False
                    self.increase ()
                else:
                    self._click = True
                    self._button_dec = False
                    self._button_inc = False
                    val = self.get_value_from_coords (event.data.pos)
                    if val != self.value:
                        self.value = val
            # Mouse wheel.
            elif event.data.button == 4:
                self.decrease ()
            elif event.data.button == 5:
                self.increase ()
            
        elif event.signal == SIG_MOUSEMOVE:
            if self.eventarea.collidepoint (event.data.pos):
                if base.debug: print "ScrollBar.MOUSEMOVE (inner)"
                self.focus = True
                if self.state == STATE_NORMAL:
                    self.state = STATE_ENTERED
                self.run_signal_handlers (SIG_MOUSEMOVE)
                buttons = self.get_button_coords ()
                if not self._check_collision (event.data.pos, buttons[0]):
                    self._button_dec = False
                    self.dirty = True
                if not self._check_collision (event.data.pos, buttons[1]):
                    self._button_inc = False
                    self.dirty = True
                if self._click:
                    val = self.get_value_from_coords (event.data.pos)
                    if val != self.value:
                        self.value = val
            elif self.state == STATE_ENTERED:
                if base.debug: print "ScrollBar.MOUSEMOVE (outer)"
                self.state = STATE_NORMAL

        elif event.signal == SIG_MOUSEUP:
            if self.rect.collidepoint (event.data.pos):
                if base.debug: print "ScrollBar.MOUSEUP"
                if event.data.button == 1:
                    if self.state == STATE_ACTIVE:
                        self.state = STATE_ENTERED
                self.run_signal_handlers (SIG_MOUSEUP)
            else:
                self.state = STATE_NORMAL
            if self._click or self._button_inc or self._button_dec:
                self._button_dec = False
                self._button_inc = False
                self._click = False

        # The user holds the mouse clicked over one button.
        elif event.signal == SIG_TICK:
            if self._button_dec:
                self.decrease ()
            elif self._button_inc:
                self.increase ()

        # Keyboard activation.
        elif (event.signal == SIG_KEYDOWN) and self.focus:
            if event.data.key in (pygame.locals.K_KP_PLUS,
                                  pygame.locals.K_PLUS, pygame.locals.K_RIGHT,
                                  pygame.locals.K_DOWN):
                self.increase ()
            elif event.data.key in (pygame.locals.K_KP_MINUS,
                                    pygame.locals.K_MINUS,
                                    pygame.locals.K_LEFT, pygame.locals.K_UP):
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

    button_dec = property (lambda self: self._button_dec,
                           doc = """Indicates, whether the decrease
                           button is pressed.""")
    button_inc = property (lambda self: self._button_inc,
                           doc = """Indicates, whether the increase
                           button is pressed.""")
        
class HScrollBar (ScrollBar):
    """HScrollBar (width, scroll) -> HScrollBar

    Creates a new horizontal ScrollBar widget.

    A ScrollBar widget with a horizontal orientation. By default, it is
    20 pixels high (size[1] = 20) and has the passed width. The
    scrolling area is the passed scroll value minus the width of the
    ScrollBar.

    Thus, if the area to scroll is 200 pixels wide and the ScrollBar is
    about 100 pixels long, the ScrollBar its value range will go from 0
    to 100 (maximum = scroll - width). If the ScrollBar is longer than
    the area to scroll (scroll < width), then the value range will be 0.

    Note: The minimum size of the scrollbar is at least twice its
    size[1] parameter. This means, that with 40 pixels in size it can
    display the both scrolling buttons next to each other. This will
    override the passed width value in the constructor, if necessary.
    """
    def __init__ (self, width, scroll):
        ScrollBar.__init__ (self)
        # Minimum size for the two scrolling buttons next to each other
        height = 20
        if width < 2 * height:
            width = 2 * height
        self.size = (width, height) # Default size.
        self.maximum = scroll

    def set_maximum (self, maximum):
        """H.set_maximum (...) -> None

        Sets the maximum value to scroll.

        The passed maximum value differs from maximum value of the
        slider. The HScrollBar also subtracts its own height from the
        scrolling maximum, so that the real maximum of its value range
        can be expressed in the formula:

        real_maximum = maximum - self.size[1]

        That means, that if the HScrollBar is 100 pixels high and the
        passed maximum value is 200, the scrolling range of the
        HScrollBar will go from 0 to 100 (100 + size = 200).

        Raises a ValueError, if the passed argument is smaller than
        the first element of the ScrollBar its size.
        """
        if maximum < self.size[0]:
            raise ValueError ("maximum must be greater than or equal to %d"
                              % self.size[0])
        ScrollBar.set_maximum (self, maximum - self.size[0])

    def get_button_coords (self):
        """H.get_button_coords () -> tuple

        Gets a tuple with the coordinates of the in- and decrease buttons.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)

        # Respect the set shadow for the ScrollBar.
        button1 = (self.position[0] + border, self.position[1] + border,
                   self.height - 2 * border, self.height - 2 * border)
        button2 = (self.position[0] + self.width - self.height - border,
                   self.position[1] + border,
                   self.height - 2 * border, self.height - 2 * border)
        return (button1, button2)

    def get_slider_size (self):
        """H.get_slider_size () -> int

        Calculates the size of the slider knob.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)

        # Minimum slider size, if the scrollbar is big enough.
        minsize = 10
        if (self.size[0] - 2 * self.size[1]) == 0:
            # If only the both scrolling buttons can be displayed, we will
            # completely skip the slider.
            return 0

        # Full size.
        fullsize = self.size[0] - 2 * self.size[1] + 2 * border
        slider_width = fullsize
        if self.maximum != 0:
            slider_width = fullsize / (float (self.maximum) + fullsize) * \
                           fullsize
            if slider_width < minsize:
                slider_width = minsize
        return int (slider_width)
    
    def get_coords_from_value (self):
        """H.get_coords_from_value () -> int

        Calculates the slider coordinates for the HScrollBar.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)

        val = 0
        if self.maximum > 0:
            slider = self.get_slider_size ()
            sl_x = self.size[1] - border + float (slider) / 2
            slide = self.size[0] - 2 * sl_x
            step = self.maximum / float (slide)
            val = self.value / step + sl_x
            return val
        return self.size[0] / 2
    
    def get_value_from_coords (self, coords):
        """H.get_value_from_coords (...) -> float

        Calculates the slider coordinates for the HScrollBar.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)

        val = 0
        if self.maximum > 0:
            slider = self.get_slider_size ()
            sl_x = self.size[1] - border + float (slider) / 2
            slide = self.size[0] - 2 * sl_x
            n = coords[0] - self.position[0] - sl_x
            step = self.maximum / float (slide)
            val = n * step
            if val > self.maximum:
                val = self.maximum
            elif val < 0:
                val = 0
        return val
    
    def draw (self):
        """H.draw (...) -> Surface

        Draws the HScrollBar surface and returns it.

        Creates the visible surface of the HScrollBar and returns it to
        the caller.
        """
        return base.GlobalStyle.draw_scrollbar (self)

class VScrollBar (ScrollBar):
    """VScrollBar (height, scroll) -> VScrollBar

    Creates a new vertical ScrollBar widget.

    A ScrollBar widget with a vertical orientation. By default, it is 20
    pixels wide (size[1] = 20) and has the passed height. The scrolling
    area is the passed scroll value minus the height of the ScrollBar.

    Thus, if the area to scroll is 200 pixels high and the ScrollBar is
    about 100 pixels high, the ScrollBar its value range will go from 0
    to 100 (maximum = scroll - height). If the ScrollBar is longer than
    the area to scroll (scroll < height), then the value range will be 0.

    Note: The minimum size of the scrollbar is at least twice its
    size[0] parameter. This means, that with 40 pixels in size it can
    display the both scrolling buttons next to each other. This will
    override the passed width value in the constructor, if necessary.
    """
    def __init__ (self, height, scroll):
        ScrollBar.__init__ (self)
        # Minimum size for the two scrolling buttons next to each other.
        width = 20
        if height < 2 * width:
            height = 2 * width
        self.size = (width, height) # Default size.
        self.maximum = scroll

    def set_maximum (self, maximum):
        """V.set_maximum (...) -> None

        Sets the maximum value to scroll.

        The passed maximum value differs from maximum value of the
        slider. The VScrollBar also subtracts its own width from the
        scrolling maximum, so that the real maximum of its value range
        can be expressed in the formula:

        real_maximum = maximum - self.size[0]

        That means, that if the VScrollBar is 100 pixels long and the
        passed maximum value is 200, the scrolling range of the
        VScrollBar will go from 0 to 100 (100 + size = 200).

        Raises a ValueError, if the passed argument is smaller than
        the second element of the ScrollBar its size.
        """
        if maximum < self.size[1]:
            raise ValueError ("maximum must be greater than or equal to %d"
                              % self.size[1])
        ScrollBar.set_maximum (self, maximum - self.size[1])

    def get_button_coords (self):
        """V.get_button_coords () -> tuple

        Gets a tuple with the coordinates of the in- and decrease buttons.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)

        # Respect the set shadow for the ScrollBar.
        button1 = (self.position[0] + border, self.position[1] + border,
                   self.width - 2 * border, self.width - 2 * border)
        button2 = (self.position[0] + border,
                   self.position[1] + self.height - self.width - border,
                   self.width - 2 * border, self.width - border)
        return (button1, button2)

    def get_slider_size (self):
        """V.get_slider_size () -> int

        Calculates the size of the slider knob.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)
        
        # Minimum slider size.
        minsize = 10
        if (self.size[1] - 2 * self.size[0]) == 0:
            # If only the both scrolling buttons can be displayed, we will
            # completely skip the slider.
            return 0
        
        # Full size.
        fullsize = self.size[1] - 2 * self.size[0] + 2 * border
        slider_height = fullsize
        if self.maximum != 0:
            slider_height = fullsize / (float (self.maximum) + fullsize) * \
                            fullsize
            if slider_height < minsize:
                slider_height = minsize
        return int (slider_height)
    
    def get_coords_from_value (self):
        """V.get_coords_from_value () -> int

        Calculates the slider coordinates for the VScrollBar.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)
        
        val = 0
        if self.maximum > 0:
            slider = self.get_slider_size ()
            sl_y = self.size[0] - border + float (slider) / 2
            slide = self.size[1] - 2 * sl_y
            step = self.maximum / float (slide)
            val = self.value / step + sl_y
            return val
        return self.size[1] / 2
    
    def get_value_from_coords (self, coords):
        """V.get_value_from_coords (...) -> float

        Calculates the slider coordinates for the VScrollBar.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)

        val = 0
        if self.maximum > 0:
            slider = self.get_slider_size ()
            sl_y = self.size[0] - border + float (slider) / 2
            slide = self.size[1] - 2 * sl_y
            n = coords[1] - self.position[1] - sl_y
            step = self.maximum / float (slide)
            val = n * step
            if val > self.maximum:
                val = self.maximum
            elif val < 0:
                val = 0
        return val
    
    def draw (self):
        """V.draw (...) -> Surface

        Draws the VScrollBar surface and returns it.

        Creates the visible surface of the VScrollBar and returns it to
        the caller.
        """
        return base.GlobalStyle.draw_scrollbar (self)
