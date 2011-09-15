# $Id: Window.py,v 1.19 2005/09/17 09:07:04 marcusva Exp $
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

"""Toplevel Window class."""

from Bin import Bin
from Constants import *
import base

class Window (Bin):
    """Window (title=None) -> Window

    A window-like widget class, which supports drag operations.

    The Window class is a container, which provides a window-like look
    and feel and can be moved around the screen. It supports an
    additional caption and allows the user to minimize it.

    The title to display on the Window caption bar can be set using the
    'title' attribute or set_title() method.

    window.title = 'Window caption'
    window.set_title ('Another title')

    Additionally it can be moved around the screen by pressing and
    holding the left mouse button on its caption bar and moving the
    mouse around. The Window widget also supports minimizing it to its
    caption bar by pressing the middle mouse button on the caption bar.
    
    Default action (invoked by activate()):
    None
    
    Mnemonic action (invoked by activate_mnemonic()):
    None

    Signals:
    SIG_MOUSEDOWN - Invoked, when a mouse button is pressed on the Window.
    SIG_MOUSEUP   - Invoked, when a mouse button is released on the Window.
    SIG_MOUSEMOVE - Invoked, when the mouse moves over the Window.
    
    Attributes:
    title - The caption of the window.
    align - Alignment of the child.
    """
    def __init__ (self, title=None):
        Bin.__init__ (self)
        self._title = None
        self.set_title (title)

        self._align = ALIGN_NONE
        
        # Rectangle area for mouse click & movement on the window
        # caption.
        self._caption_rect = None

        # State variables for button pressing and mouse movements.
        self.__pressed = False
        self.__old_pos = None
        self.__minimized = False
        
        self._signals[SIG_MOUSEDOWN] = []
        self._signals[SIG_MOUSEUP] = []
        self._signals[SIG_MOUSEMOVE] = []

    def set_title (self, text=None):
        """W.set_title (...) -> None

        Sets the title caption to display on the Window.

        Sets the text to display as title on the Window.

        Raises a TypeError, if the passed argument is not a string or
        unicode.
        """
        if text and (type (text) not in (str, unicode)):
            raise TypeError ("text must be a string or unicode")
        self._title = text
        self.dirty = True

    def set_align (self, align):
        """W.set_align (...) -> None

        Sets the alignment for the child of the Window.
        """
        # TODO: Add check for the align types.
        self._align = align
        self.dirty = True
    
    def _move_to_position (self, pos):
        """W._move_to_position (...) -> None

        Moves the Window to the position relative from itself.
        """
        diffx = pos[0] - self.__old_pos[0]
        diffy = pos[1] - self.__old_pos[1]
        self.position = self.position[0] + diffx, self.position[1] + diffy

    def notify (self, event):
        """W.notify (event) -> None

        Notifies the window about an event.
        """
        if not self.sensitive or not self.eventarea:
            return

        if event.signal == SIG_MOUSEDOWN:
            if self.rect.collidepoint (event.data.pos):
                if base.debug: print "Window.MOUSEDOWN"
                self.focus = True
                self.run_signal_handlers (SIG_MOUSEDOWN)
                if self._caption_rect.collidepoint (event.data.pos):
                    if event.data.button == 1:
                        # Initiate window movement.
                        self.state = STATE_ACTIVE
                        self.__pressed = True
                        self.__old_pos = event.data.pos
                    elif event.data.button == 2:
                        # Minimize/maximize window.
                        self.__minimized = not self.__minimized
                        self.dirty = True
        
        elif event.signal == SIG_MOUSEUP:
            if self.eventarea.collidepoint (event.data.pos):
                if base.debug: print "Window.MOUSEUP"
                self.run_signal_handlers (SIG_MOUSEUP)
                if event.data.button == 1:
                    if self.__pressed:
                        self.__pressed = False
                        self.state = STATE_NORMAL

        elif event.signal == SIG_MOUSEMOVE:
            if self.__pressed:
                # The window is moved.
                self._move_to_position (event.data.pos)
                self.__old_pos = event.data.pos
            else:
                if self.eventarea.collidepoint (event.data.pos):
                    if base.debug: print "Window.MOUSEMOVE (inner)"
                    self.run_signal_handlers (SIG_MOUSEMOVE)

        Bin.notify (self, event)

    def _align_child (self, width, height, border, caption_height):
        """S._align_child (...) -> None

        Moves the child to the correct position within the Window.
        """
        posx = 0
        posy = 0
        posx = (width - self.child.width) / 2
        posy = caption_height + \
               (height - caption_height - self.child.height) / 2
        if self.align & ALIGN_LEFT:
            posx = border + self.padding
        elif self.align & ALIGN_RIGHT:
            posx = width - self.child.width - border - self.padding
        if self.align & ALIGN_TOP:
            posy = caption_height + self.padding
        elif self.align & ALIGN_BOTTOM:
            posy = height - self.child.height - border - self.padding

        self.child.position = self.position[0] + posx, self.position[1] + posy
    
    def draw (self):
        """W.draw () -> None

        Draws the Window surface and returns it.
        """
        cls = self.__class__
        style = base.GlobalStyle
        border = style.get_border_size (cls, self.style, BORDER_FLAT)

        width = 2 * (self.padding + border)
        height = 2 * self.padding + border

        if not self.__minimized:
            if self.child:
                self.child.update ()
                width += self.child.width
                height += self.child.height
       
        # Guarantee size.
        if width < self.size[0]:
            width = self.size[0]
        if not self.__minimized:
            if height < self.size[1]:
                height = self.size[1]

        # Overall surface.
        surface_caption = style.create_caption (width, self.title, self.state,
                                                cls, self.style)
        rect_cap = surface_caption.get_rect ()
        self._caption_rect = rect_cap
        self._caption_rect.x = self.position[0]
        self._caption_rect.y = self.position[1]
        height += rect_cap.height # rect_cap.height usually includes a border.
        if width < rect_cap.width:
            width = rect_cap.width
        surface = style.draw_rect (width, height, self.state, cls, self.style)
        surface = style.draw_border (surface, self.state, cls, self.style,
                                     BORDER_FLAT)

        # Create and draw the caption.
        surface.blit (surface_caption, (0, 0))

        # Position and blit the child.
        if not self.__minimized:
            if self.child:
                self._align_child (width, height, border, rect_cap.height)
                self.child.update ()
                surface.blit (self.child.image,
                              (self.child.position[0] - self.position[0],
                               self.child.position[1] - self.position[1]))
                #(self.padding + border,
                #               self.padding + rect_cap.height))
        return surface
    
    title = property (lambda self: self._title,
                      lambda self, var: self.set_title (var),
                      doc = "The title caption of the Window.")
    align = property (lambda self: self._align,
                      lambda self, var: self.set_align (var),
                      doc = "The alignment of the child.")
