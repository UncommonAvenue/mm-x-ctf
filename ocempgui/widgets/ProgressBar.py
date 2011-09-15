# $Id: ProgressBar.py,v 1.15 2005/09/17 09:07:04 marcusva Exp $
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

"""A self-filling widget for progress states."""

from BaseWidget import BaseWidget
from Constants import *
import base

class ProgressBar (BaseWidget):
    """ProgressBar () -> ProgressBar

    Creates a new ProgressBar widget, which can display a progress state.

    The Progressbar widget is a graphical state indicator, which can
    interactively show the effort of an operation by a filling bar. Its
    value ranges from 0 to 100 (percent) and can increase or decrease.
    To allow high interactivity, each method value changing method of
    the ProgressBar will raise a SIG_VALCHANGE event.

    The increment of the ProgressBar can be set with the 'step'
    attribute or set_step() method. To allow a high resolution for long
    running tasks and operations, which should be visualized using the
    ProgressBar, the increment accepts floating point values.

    progressbar.step = 0.1
    progressbar.set_step (10)

    The 'value' attribte and set_value() method allow setting the
    ProgressBar value directly without calling the respective increment
    or decerement methods.

    progressbar.value = 50.0
    progressbar.set_value (3)

    The ProgressBar value can be in- or decreased using the increase()
    and decrease() methods. Those will in- or decrease the current value
    by the value of the 'step' attribute until either 100 or 0 is
    reached.

    progressbar.increase()
    progressbar.decrease()

    Dependant on the width of the ProgressBar the filled range per in-
    or decreasement can differ. The complete width is always used as the
    maximum value of 100, thus longer progressBar widgets allow better
    visible changes, if a finer grained increment is given.
    The ProgressBar uses a default size for itself by setting the 'size'
    attribute to a width of 104 pixels and a height of 24 pixels.

    Default action (invoked by activate()):
    None
    
    Mnemonic action (invoked by activate_mnemonic()):
    None

    Signals:
    SIG_VALCHANGE - Invoked, when the value of the ProgressBar changes.

    Attributes:
    step  - Step range.
    value - Current value.
    text  - The text to display on the ProgressBar.
    """
    def __init__ (self):
        BaseWidget.__init__ (self)
        self.size = 104, 24 # Use a fixed size.

        # The current value, max is 100 (%), min is 0 (%) and step range.
        self._value = 0
        self._step = 0.1 

        self._text = None
        self._signals[SIG_VALCHANGE] = []

    def set_focus (self, focus=True):
        """P.set_focus (focus=True) -> None

        Overrides the set_focus() behaviour for the ProgressBar.

        The ProgressBar class is not focusable by default. It is an
        information displaying class only, so it does not need to get
        the input focus and thus it will return false without doing
        anything.
        """
        return False
    
    def set_text (self, text):
        """P.set_text (...) -> None
        
        Sets the text to display on the ProgressBar.

        Sets the text text to display on the ProgressBar. The text will
        be centered on it.
        
        Raises a TypeError, if the passed argument is not a string or
        unicode.
        """
        if type (text) not in (str, unicode):
            raise TypeError ("text must be a string or unicode")
        self._text = text
        self.dirty = True

    def set_step (self, step=0.1):
        """P.set_step (...) -> None

        Sets the step range for in- or decreasing the ProgressBar value.

        The step range is the value used by the increase and decrease
        methods of the ProgressBar.

        Raises a TypeError, if the passed argument is not a float or
        integer.
        """
        if type (step) not in (float, int):
            raise TypeError ("step must be a float or integer")
        self._step = step

    def set_value (self, value):
        """P.set_value (...) -> None

        Sets the current value of the ProgressBar.

        Sets the current value of the ProgressBar and raises a
        SIG_VALCHANGE event, if the new value differs from the old one.

        Raises a TypeError, if the passed argument is not a float or
        integer.
        Raises a ValueError, if the passed argument, is not
        within the allowed range of 0.0 to 100.0.
        """
        if type (value) not in (float, int):
            raise TypeError ("value must be a float or integer")
        if (0.0 > value) or (100.0 < value):
            raise ValueError ("value must be in the range from 0.0 to 100.0")
        if value != self._value:
            self._value = value
            self.run_signal_handlers (SIG_VALCHANGE)
            self.dirty = True

    def increase (self):
        """P.increase () -> None

        Increases the current value by one step.
        """
        val = self.value
        if val < 100.0:
            val += self.step
            if val > 100.0:
                val = 100.0
        self.value = val

    def decrease (self):
        """P.decrease () -> None

        Decreases the current value by one step.
        """
        val = self.value
        if val > 0.0:
            val -= self.step
            if val < 0.0:
                val = 0.0
        self.value = val

    def draw (self):
        """P.draw () -> Surface

        Draws the ProgressBar surface and returns it.

        Creates the visible surface of the ProgressBar and returns it
        to the caller.
        """
        return base.GlobalStyle.draw_progressbar (self)
    
    value = property (lambda self: self._value,
                      lambda self, var: self.set_value (var),
                      doc = "The current value.")
    step = property (lambda self: self._step,
                     lambda self, var: self.set_step (var),
                     doc = "The step range of the ProgressBar.")
    text = property (lambda self: self._text,
                     lambda self, var: self.set_text (var),
                     doc = "The text to display on the ProgressBar.")
