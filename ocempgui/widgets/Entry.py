# $Id: Entry.py,v 1.32 2005/09/17 09:07:04 marcusva Exp $
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

"""A widget, which handles text input."""

from Editable import Editable
from Constants import *
import base

class Entry (Editable):
    """Entry (text="") -> Entry

    Creates a new Entry widget suitable for text input.

    The Entry widget is a text input box for a single line of text. It
    allows an unlimited amount of text input, but is usually more
    suitable for a small or medium amount, which can be scrolled, if the
    text size exceeds the visible widget size.
    
    The 'padding' attribute and set_padding() method are used to place a
    certain amount of pixels between the text and the outer edges of the
    Entry.

    entry.padding = 10
    entry.set_padding (10)

    The Entry uses a default size for itself by setting the 'size'
    attribute to a width of 94 pixels and a height of 24 pixels.

    Default action (invoked by activate()):
    See the Editable class.
    
    Mnemonic action (invoked by activate_mnemonic()):
    None

    Signals:
    SIG_MOUSEDOWN - Invoked, when a mouse button gets pressed on the Entry.

    Attributes:
    padding - Additional padding between text and borders. Default is 2.
    """
    def __init__ (self, text=""):
        Editable.__init__ (self)
        self.text = text
        self._padding = 2
        self.size = 94, 24 # Default size to use.

        self._signals[SIG_MOUSEDOWN] = []

    def set_padding (self, padding):
        """E.set_padding (...) -> None

        Sets the padding between the edges and text of the Entry.

        The padding value is the amount of pixels to place between the
        edges of the Entry and the displayed text.
        
        Note: If the 'size' attribute is set, it can influence the
        visible space between the text and the edges. That does not
        mean, that any padding is set.

        Raises a TypeError, if the argument is not a positive integer.
        """
        if (type (padding) != int) or (padding < 0):
            raise TypeError ("Argument must be a positive integer")
        self._padding = padding
        self.dirty = True

    def notify (self, event):
        """E.notify (...) -> None

        Notifies the Entry about an event.
        """
        if not self.eventarea or not self.sensitive:
            return
        
        if event.signal == SIG_MOUSEDOWN:
            if self.eventarea.collidepoint (event.data.pos):
                self.run_signal_handlers (SIG_MOUSEDOWN)
                if (event.data.button == 1):
                    self.activate ()
        
        Editable.notify (self, event)

    def draw (self):
        """E.draw () -> Surface

        Draws the surface of the entry and returns it.

        Creates the visible surface of the Entry and returns it to the
        caller.
        """
        return base.GlobalStyle.draw_entry (self)
    
    padding = property (lambda self: self._padding,
                        lambda self, var: self.set_padding (var),
                        doc = "The additional padding for the Entry.")
