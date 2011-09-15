# $Id: Editable.py,v 1.14 2005/09/17 09:07:04 marcusva Exp $
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

# TODO: Handle text selections

"""Abstract text editing class."""

import pygame.locals
from BaseWidget import BaseWidget
from Constants import *
import base

class Editable (BaseWidget):
    """Editable () -> Editable

    Creates an abstract Editable widget, which can handle text input.

    The Editable is an abstract class, which can handle (unicode) text
    input. It supports a caret for the input cursor, undo of text input
    using the ESC key and input notifications via the RETURN/ENTER key.

    Text can be set directly using the 'text' attribute or the
    set_text() method. By assigning the attribute or using the method,
    the caret position will be reset to 0.

    editable.text = 'Test'
    editable.set_text (text)

    The 'caret' attribute indicates the current cursor position for
    input operations within the text and can be modified
    programmatically by reassigning it or using the set_caret() method.

    editable.caret = 5
    editable.set_caret (5)

    It is possible to prevent the text from editing using the
    'editable' attribute or set_editable() method. If 'editable' is
    False, no text input can be made and an input notification or undo
    operation will not be possible.

    editable.editable = False
    editable.set_editable (False)

    Note: Dependant on the font set in the style of the Editable, it is
    possible, that certain characters are not displayed correctly. It is
    strongly recommended to use a fully unicode capable font, if
    non-ascii characters should be displayed.

    Default action (invoked by activate()):
    Give the Editable the input focus for text editing.
    
    Mnemonic action (invoked by activate_mnemonic()):
    None

    Signals:
    SIG_KEYDOWN - Invoked, when a key is pressed while the Editable has
                  the input.
    SIG_INPUT   - Invoked, when the input is validated or aborted using
                  RETURN or ESC.

    Attributes:
    text          - The text displayed on the Editable.
    editable      - Indicates, whether the text can be edited or not.
    caret         - Caret ( | ) position on input.
    caret_visible - Indicates, whether the caret is currently visible.
    """
    def __init__ (self):
        BaseWidget.__init__ (self)
        
        self._text = None
        self._editable = True

        # Caret | position.
        self._caret = 0
        self._caret_visible = True

        # Internal counter for tick events (time measuring).
        self._counter = 50

        self._signals[SIG_KEYDOWN] = []
        self._signals[SIG_INPUT] = []
        self._signals[SIG_TICK] = None # No events for this one.

        # Temporary placeholder for text input and ESCAPE.
        self._temp = None

    def set_text (self, text):
        """E.set_text (...) -> None

        Sets the text of the Editable to the passed argument.

        Raises a TypeError, if the passed argument is not a string or
        unicode.
        """
        if type (text) not in (str, unicode):
            raise TypeError ("text must be a string or unicode")
        self._text = text
        self._temp = self._text
        self.caret = 0   # Reset caret.
        self.dirty = True

    def set_caret (self, pos):
        """E.set_caret (...) -> None

        Sets the caret to the passed position.

        Moves the input caret to the given position within the text.
        0 is the very first position within the text (before the first
        character), a value equal to or greater than the length of the
        text will set the caret behind the last character position.

        Raises a TypeError, if the passed argument is not a positive
        integer.
        """
        if (type (pos) != int) or (pos < 0):
            raise TypeError ("pos must be a positive integer")
        if pos > len (self.text):
            self._caret = len (self.text)
        else:
            self._caret = pos
        self.dirty = True

    def set_editable (self, editable):
        """T.set_editable (...) -> None

        Enables or disables text editing of the Editable.

        This causes the Editable to ignore SIG_KEYDOWN events, which
        would modify the text of it. It also blocks input
        notifications and undo operations.
        """
        self._editable = editable

    def set_focus (self, focus=True):
        """E.set_focus (...) -> bool
        
        Sets the input and action focus of the Editable.
        
        Sets the input and action focus of the Editable and returns True
        upon success or False, if the focus could not be set.

        Note: This method only works as supposed using
        a render loop, which supports the Renderer class specification.
        """
        if not self.sensitive:
            return False
        
        BaseWidget.set_focus (self, focus)
        if focus:
            # Save the text after activation and reset the caret blink
            # effects.
            self._caret_visible = True
            self._temp = self.text
            self._caret_visible = True
            self._counter = 0
            self.state = STATE_ACTIVE
        elif self._temp != self.text:
            # If the Editable looses its input focus _and_ has changed text,
            # it will be validated by default.
            if base.debug: print "Editable.INPUT"
            self._temp = self.text
            self.state = STATE_NORMAL
            self.run_signal_handlers (SIG_INPUT)
        else:
            # The Editable looses its input focus without any change.
            self.state = STATE_NORMAL
            self._caret = 0
        return True
    
    def activate (self):
        """E.activate () -> None

        Activates the Editable default action.

        Activates the Editable default action. This usually means
        giving the Editable the input focus.
        """
        if base.debug: print "Editable.activate()"
        if not self.sensitive:
            return
        self.focus = True
    
    def notify (self, event):
        """E.notify (...) -> None

        Notifies the Editable about an event.
        """
        if not self.sensitive:
            return

        # The next few events are only available, if the entry is focused.
        if self.focus:
            # Blinking caret.
            # TODO: TICK events are not the best idea to use here.
            if event.signal == SIG_TICK:
                if self._counter == 50:
                    self._caret_visible = not self._caret_visible
                    self._counter = 0
                    self.dirty = True
                self._counter += 1
            
            elif event.signal == SIG_KEYDOWN:
                if base.debug: print "Editable.KEYDOWN"
                self.run_signal_handlers (SIG_KEYDOWN, event.data)
                self._input (event.data)
                self._counter = 0
                self._caret_visible= True

        BaseWidget.notify (self, event)

    def _input (self, event):
        """E._input (...) -> None

        Receives the SIG_KEYDOWN events and updates the text.
        """
        if event.key == pygame.locals.K_ESCAPE:
            if self.editable:
                self._text = self._temp # Undo text input.
                # TODO: Maybe SIG_INPUT should be raise only, if there
                # were changes in the text.
                if base.debug: print "Editable.INPUT"
                self.run_signal_handlers (SIG_INPUT)
                self._caret = 0 # Reset caret.
            self.focus = False

        elif event.key == pygame.locals.K_RETURN:
            if self.editable:
                if base.debug: print "Editable.INPUT"
                # TODO: Maybe SIG_INPUT should be raise only, if there
                # were changed in the text.
                self.run_signal_handlers (SIG_INPUT)
                self._caret = 0 # Reset caret.
            self.focus = False
        
        # Move caret right and left on the corresponding key press.
        elif event.key == pygame.locals.K_RIGHT:
            if self._caret < len (self._text):
                self._caret += 1
        elif event.key == pygame.locals.K_LEFT:
            if self._caret > 0:
                self._caret -= 1

        # Go the start (home) of the text.
        elif event.key == pygame.locals.K_HOME:
            self._caret = 0

        # Go to the end (end) of the text.
        elif event.key == pygame.locals.K_END:
            self._caret = len (self._text)

        # The next statements directly influence the text, thus we
        # have to check, if it is editable or not.
        elif self.editable:
            # Delete at the position (delete).
            if event.key == pygame.locals.K_DELETE:
                if self._caret < len (self._text):
                    self._text = self._text[:self._caret] + \
                                 self._text[self._caret + 1:]

            # Delete backwards (backspace).
            elif event.key == pygame.locals.K_BACKSPACE:
                if self._caret > 0:
                    self._text = self._text[:self._caret - 1] + \
                                 self._text[self._caret:]
                    self._caret -= 1

            # Non-printable characters or maximum exceeded.
            elif (event.key < 32):
                 # I hope, that does not lead into problems. If so, the
                 # unicode character range should be checked instead.
                return

            # Any other case is okay, so show it.
            else:
                self._text = self._text[:self._caret] + event.unicode + \
                             self._text[self._caret:]
                self._caret += 1
        self.dirty = True

    # properties
    text = property (lambda self: self._text,
                     lambda self, var: self.set_text (var),
                     doc = "The text to display on the Editable.")
    caret = property (lambda self: self._caret,
                      lambda self, var: self.set_caret (var),
                      doc = "The caret position.")
    editable = property (lambda self: self._editable,
                         lambda self, var: self.set_editable (var),
                         doc = "Indicates, if the text can be edited or not.")
    caret_visible = property (lambda self: self._caret_visible,
                              doc = "Indicates, if the caret is currently " \
                              "visible.")
