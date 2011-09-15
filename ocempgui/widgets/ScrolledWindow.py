# $Id: ScrolledWindow.py,v 1.22 2005/09/17 09:07:04 marcusva Exp $
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

"""A widget class, which can contain other widgets and uses optional
scrollbars."""

import pygame, pygame.locals
from ScrollBar import HScrollBar, VScrollBar
from Bin import Bin
from Constants import *
import base

class ScrolledWindow (Bin):
    """ScrolledWindow (width, height) -> ScrolledWindow

    Creates a new window, which supports horizontal and vertical scrolling.

    The ScrolledWindow is a viewport, which enables its child to be
    scrolled horizontally and vertically. It offers various scrolling
    types, which customize the bahviour of the supplied scrollbars.

    The scrolling behaviour of the ScrolledWindow can be adjusted
    through the 'scrolling' attribute or set_scrolling() method and can
    be one of the SCROLL_TYPES constants.

    Default action (invoked by activate()):
    Gives the ScrolledWindow the input focus.
    
    Mnemonic action (invoked by activate_mnemonic()):
    None

    Signals:
    SIG_KEYDOWN   - Invoked, when a key is pressed while the ScrolledWindow
                    has the input focus.
    SIG_MOUSEDOWN - Invoked, when a mouse button is pressed over the
                    ScrolledWindow.
    
    Attributes:
    scrolling  - The scrolling behaviour of the ScrolledWindow.
    vscrollbar - The vertical scrollbar of the ScrolledWindow.
    hscrollbar - The horizontal scrollbar of the ScrolledWindow.
    """
    def __init__ (self, width, height):
        Bin.__init__ (self)
        self._scrolling = SCROLL_AUTO

        # ScrollBars.
        self._vscroll = VScrollBar (height, height)
        self._vscroll.connect_signal (SIG_VALCHANGE, self.set_dirty, True)
        self._vscroll.parent = self
        self._hscroll = HScrollBar (width, width)
        self._hscroll.connect_signal (SIG_VALCHANGE, self.set_dirty, True)
        self._hscroll.parent = self

        self._hscroll_visible = False
        self._vscroll_visible = False

        # Remove the keyboard events from the scrollbars. We use our own.
        del self._vscroll._signals[SIG_KEYDOWN]
        del self._hscroll._signals[SIG_KEYDOWN]
        
        self.controls.append (self._vscroll)
        self.controls.append (self._hscroll)

        # Respect the scrollbar sizes.
        if width < self._hscroll.size[0]:
            width = self._hscroll.size[0]
        if height < self._vscroll.size[1]:
            height = self._vscroll.size[1]
        self.size = (width, height)

        self._signals[SIG_KEYDOWN] = None # Dummy
        self._signals[SIG_MOUSEDOWN] = []
    
    def set_state (self, state):
        """S.set_state (...) -> None

        Sets the state of the ScrolledWindow.

        Sets the state of the ScrolledWindow. The state of the
        ScrolledWindow is mainly used for the visible or non-visible
        appearance of the ScrolledWindow, so that the user can
        determine the state of the ScrolledWindow easier.
        Usually this method should not be invoked by user code.
        """
        Bin.set_state (self, state)
        if state in (STATE_NORMAL, STATE_INSENSITIVE):
            self.vscrollbar.set_state (state)
            self.hscrollbar.set_state (state)
    
    def set_scrolling (self, scrolling):
        """S.set_scrolling (...) -> None

        Sets the scrolling behaviour for the ScrolledWindow.

        The scrolling can be a value of the SCROLL_TYPES list.
        SCROLL_AUTO causes the ScrolledList to display its scrollbars on
        demand only, SCROLL_ALWAYS will show the scrollbars permanently
        and SCROLL_NEVER will disable the scrollbars.

        Raises a ValueError, if the passed argument is not a value of
        the SCROLL_TYPES tuple.
        """
        if scrolling not in SCROLL_TYPES:
            raise ValueError ("scrolling must be a value from SCROLL_TYPES")
        if self._scrolling != scrolling:
            self.dirty = True
        self._scrolling = scrolling

    def activate (self):
        """S.activate () -> None

        Activates the ScrolledWindow default action.

        Activates the ScrolledWindow default action. This usually means
        giving the ScrolledWindow the input focus.
        """
        if base.debug: print "ScrolledWindow.activate()"
        if not self.sensitive:
            return
        self.focus = True

    def get_scroll_pos (self):
        """S.get_scroll_pos () -> int, int

        Gets the current topleft scrolling position.
        """
        return self.hscrollbar.value, self.vscrollbar.value
    
    def get_scrollable_area (self):
        """S.get_scrollable_area () -> int, int

        Gets the dimensions of the scrollable area.

        The scrollable area is the complete width and height, which are
        _scrollable_. This means the maximum values both scrollbars of
        the ScrolledWindow have.

        This method is especially useful for the scroll_to_pos() method,
        to avoid ValueError exceptions.
        """
        return self.hscrollbar.maximum, self.vscrollbar.maximum
    
    def scroll_to_pos (self, x, y):
        """S.scroll_to_pos (...) -> None

        Causes the ScrolledWindow to scroll to the given position.

        The arguments x and y are a topleft position to scroll to.
        """
        if self._hscroll_visible:
            self.hscrollbar.value = x
        if self._vscroll_visible:
            self.vscrollbar.value = y

    def get_visible_area (self):
        """S.get_visible_area () -> int, int

        Gets the width and height of the inner area of the ScrolledWindow.

        Get the real width and height of the inner area, on which the
        child will be drawn. By default this method respects the
        'shadow' style attribute.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)
        
        width = self.size[0] - 2 * border
        height = self.size[1] - 2 * border
        if self.scrolling != SCROLL_NEVER:
            if self._vscroll_visible:
                width -= self.vscrollbar.width
            if self._hscroll_visible:
                height -= self.hscrollbar.height
        return width, height
    
    def notify (self, event):
        """S.notify (...) -> None

        Notifies the ScrolledWindow about an event.
        """
        if not self.eventarea or not self.sensitive:
            return

        if event.signal == SIG_MOUSEDOWN:
            if self.eventarea.collidepoint (event.data.pos):
                if base.debug: print "ScrolledWindow.MOUSEDOWN"
                self.focus = True
                self.run_signal_handlers (SIG_MOUSEDOWN)
                # Mouse wheel.
                if self._hscroll_visible and \
                   (self.hscrollbar.eventarea.collidepoint (event.data.pos)):
                    # Do not scroll vertical, if the mouse cursor is
                    # over the horizontal scrollbar.
                    pass
                elif self._vscroll_visible:
                    if event.data.button == 4:
                        self.vscrollbar.decrease ()
                    elif event.data.button == 5:
                        self.vscrollbar.increase ()
        
        elif (event.signal == SIG_KEYDOWN) and self.focus:
            if self._hscroll_visible:
                # Horizontal scrollbar key movement
                if event.data.key == pygame.locals.K_RIGHT:
                    self.hscrollbar.increase ()

                elif event.data.key == pygame.locals.K_LEFT:
                    self.hscrollbar.decrease ()

                elif event.data.key == pygame.locals.K_END:
                    self.hscrollbar.value = self.hscrollbar.maximum

                elif event.data.key == pygame.locals.K_HOME:
                    self.hscrollbar.value = self.hscrollbar.minimum

            if self._vscroll_visible:
                # Vertical scrollbar key movement
                if event.data.key == pygame.locals.K_DOWN:
                    self.vscrollbar.increase ()

                elif event.data.key == pygame.locals.K_UP:
                    self.vscrollbar.decrease ()

                elif event.data.key == pygame.locals.K_PAGEUP:
                    val = self.vscrollbar.value - 10 * self.vscrollbar.step
                    if val > self.vscrollbar.minimum:
                        self.vscrollbar.value = val
                    else:
                        self.vscrollbar.value = self.vscrollbar.minimum

                elif event.data.key == pygame.locals.K_PAGEDOWN:
                    val = self.vscrollbar.value + 10 * self.vscrollbar.step
                    if val < self.vscrollbar.maximum:
                        self.vscrollbar.value = val
                    else:
                        self.vscrollbar.value = self.vscrollbar.maximum

                elif event.data.key == pygame.locals.K_END:
                    self.vscrollbar.value = self.vscrollbar.maximum

                elif event.data.key == pygame.locals.K_HOME:
                    self.vscrollbar.value = self.vscrollbar.minimum

        Bin.notify (self, event)
    
    def update_scrollbars (self, border):
        """S.update_scrollbars (...) -> bool, bool

        Updates the size and maximum values of the attached scrollbars.

        Updates the size and values of the attached scrollbars and
        returns boolean values about their visibility in the order
        vscrollbar, hscrollbar.
        """
        old_vals = self._vscroll_visible, self._hscroll_visible

        if self.scrolling == SCROLL_NEVER:
            self.hscrollbar.sensitive = False
            self.vscrollbar.sensitive = False
            self._vscroll_visible = False
            self._hscroll_visible = False
            return False, False

        self.vscrollbar.update ()
        self.hscrollbar.update ()
        
        width = 0
        height = 0
        if self.child:
            width = self.child.width + 2 * self.padding + border
            height = self.child.height + 2 * self.padding + border
        
        # We are using the draw_border() method for the inner surface,
        # so we have to add the borders to the scrolling maximum.
        if self.scrolling == SCROLL_ALWAYS:
            self.vscrollbar.size = (self.vscrollbar.size[0],
                                    self.size[1] - self.hscrollbar.height)
            self.hscrollbar.size = (self.size[0] - self.vscrollbar.width,
                                    self.hscrollbar.size[1])

            if width < self.hscrollbar.size[0]:
                width = self.hscrollbar.size[0]
            else:
                width += border
            self.hscrollbar.maximum = width
            if height < self.vscrollbar.size[1]:
                height = self.vscrollbar.size[1]
            else:
                 height += border
            self.vscrollbar.maximum = height
            self._vscroll_visible = True
            self._hscroll_visible = True
        elif self.scrolling == SCROLL_AUTO:
            # Check the sizes, so we can determine, how the scrollbars
            # need to be adjusted.
            self._hscroll_visible = (self.size[0] - border) < width
            self._vscroll_visible = (self.size[1] - border) < height
            if self._hscroll_visible:
                self._vscroll_visible = (self.size[1] - border -
                                         self.hscrollbar.height) < height
            if self._vscroll_visible:
                self._hscroll_visible = (self.size[0] - border -
                                         self.vscrollbar.width) < width
            
            if self._vscroll_visible and self._hscroll_visible:
                # Both scrollbars need to be shown.
                self.vscrollbar.size = (self.vscrollbar.size[0], self.size[1] -
                                        self.hscrollbar.height)
                self.hscrollbar.size = (self.size[0] - self.vscrollbar.width,
                                        self.hscrollbar.size[1])
                self.vscrollbar.maximum = height + border
                self.hscrollbar.maximum = width + border
                self.vscrollbar.sensitive = True
                self.hscrollbar.sensitive = True
            elif self._vscroll_visible:
                # Only the vertical.
                self.vscrollbar.size = (self.vscrollbar.size[0], self.size[1])
                self.vscrollbar.maximum = height + border
                self.vscrollbar.sensitive = True
                self.hscrollbar.sensitive = False
            elif self._hscroll_visible:
                # Only the horizontal.
                self.hscrollbar.size = (self.size[0], self.hscrollbar.size[1])
                self.hscrollbar.maximum = width + border
                self.hscrollbar.sensitive = True
                self.vscrollbar.sensitive = False
            else:
                # Neither vertical nor horizontal
                self.hscrollbar.sensitive = False
                self.vscrollbar.sensitive = False

        # This is an evil hack[tm] to workaround that lousy dynamic
        # scrollbar behaviour.
        if (old_vals[0] != self._vscroll_visible) or \
           (old_vals[1] != self._hscroll_visible):
            if self.child:
                self.child.dirty = True
                self.child.update ()
            return self.update_scrollbars (border)
        
        return self._vscroll_visible, self._hscroll_visible
    
    def recalculate_child_rect (self):
        """S.recalculate_child_rect () -> None

        Calculates the eventarea size of the child.
        """
        border = base.GlobalStyle.get_border_size (self.__class__, self.style,
                                                   BORDER_SUNKEN)

        if not self.child:
            return
        # Recalculate the visible size of the child rect.
        width, height = self.get_visible_area ()
        re = pygame.Rect (self.position[0] + border, self.position[1] + border,
                          width, height).clip (self.child.rect)
        self.child.eventarea = re

    def draw (self):
        """S.draw () -> Surface

        Draws the ScrolledWindow surface and returns it.

        Creates the visible surface of the ScrolledWindow and returns it
        to the caller.
        """
        return base.GlobalStyle.draw_scrolledwindow (self)
    
    scrolling = property (lambda self: self._scrolling,
                          lambda self, var: self.set_scrolling (var),
                          doc = """The scrolling behaviour for the 
                          ScrolledWindow.""")
    vscrollbar = property (lambda self: self._vscroll,
                           doc = "The vertical scrollbar.")
    hscrollbar = property (lambda self: self._hscroll,
                           doc = "The herizontal scrollbar.")
