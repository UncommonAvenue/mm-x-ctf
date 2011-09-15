# $Id: Range.py,v 1.6 2005/09/13 08:36:11 marcusva Exp $
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

"""An abstract widget suitable for scale ranges and numerical adjustments."""

from BaseWidget import BaseWidget
from Constants import *
import base

class Range (BaseWidget):
    """Range (minimum, maximum, step=1.0) -> Range

    Creates a new Range widget with the given limitations and step size.

    The Range widget class is an abstract class suitable for widgets,
    which need numerical adjustment support, scale ranges and similar
    things. It supplies various attributes and methods to enable a
    widget for numerical input and range limit checks.

    A minimum range value (or lower limit) can be set using the
    'minimum' attribute or set_minimum() method. It must not be greater
    than the set maximum value of the Range and any integer or float
    value are valid input for it.

    range.minimum = 1.7
    range.set_minimum (5)

    In contrast of this, the 'maximum' attribute or set_maximum() method
    set the upper limit (or maximum range value) of the Range. As well
    as the 'minimum' attribute any integer or float are a valid value
    and must not be smaller than the minimum value of the Range.

    range.maximum = 123.45
    range.set_maximum (100)

    To in- or decrease the Range value easily (in loops for example),
    the 'step' attribute or set_step() method can be used, which set the
    step value for the increase() and decrease() method.

    range.step = 0.5
    range.set_step (10)

    while x > 100:
        range.increment ()
        x -= 1

    while y > 100:
        range.decrement ()
        y -= 1

    The current set value of the Range widget can be set or retrieved
    with the 'value' attribute or set_value() method.

    range.value = 10.0
    range.set_value (100)

    Note: When you set the 'minimum' or 'maximum' attribute of the Range
    widget, the 'value' attribute will be automatically reset to the
    minimum or maximum value, if it is not within the range of the
    widget.

    Default action (invoked by activate()):
    None
    
    Mnemonic action (invoked by activate_mnemonic()):
    None

    Signals:
    SIG_VALCHANGE - Invoked, when the value of the Range changes.
    
    Attributes:
    minimum - The minimum value of the Range.
    maximum - The maximum value of the Range.
    step    - Step range to use for in- or decreasing the Range.
    value   - The current value of the Range.
    """
    def __init__ (self, minimum, maximum, step=1.0):
        BaseWidget.__init__ (self)

        self._signals[SIG_VALCHANGE] = []
        
        # Ranges and step value.
        self._minimum = minimum  # Set the min and max values temporary
        self._maximum = maximum  # and check them later.
        self._step = 0.0
        self._value = 0.0

        if minimum >= maximum:
            raise ValueError ("minimum must be smaller than maximum")
        self.set_maximum (maximum)
        self.set_minimum (minimum)
        self.set_step (step)

    def set_minimum (self, minimum):
        """R.set_minimum (...) -> None

        Sets the minimum value of the Range.

        Raises a TypeError, if the passed argument is not a float or
        integer.
        Raises a ValueError, if the passed argument is greater than
        the Range its maximum value.
        """
        if type (minimum) not in (float, int):
            raise TypeError ("minimum must be a float or integer")
        if minimum > self.maximum:
            raise ValueError ("minimum must be smaller than %f" % self.maximum)
        self._minimum = minimum
        if minimum > self.value:
            # Adjust the current value on demand.
            self.value = minimum
    
    def set_maximum (self, maximum):
        """R.set_maximum (...) -> None

        Sets the maximum value of the Range.

        Raises a TypeError, if the passed argument is not a float or
        integer.
        Raises a ValueError, if the passed argument is smaller than
        the Range its minimum value.
        """
        if type (maximum) not in (float, int):
            raise TypeError ("maximum must be a float or integer")
        if maximum < self.minimum:
            raise ValueError ("maximum must be greater than %f" % self.minimum)
        self._maximum = maximum
        if maximum < self.value:
            # Adjust the current value on demand.
            self.value = maximum

    def set_step (self, step=1.0):
        """R.set_step (...) -> None

        Sets the step range for in- or decreasing the Range value.

        Raises a TypeError, if the passed argument is not a float or
        integer.
        """
        if type (step) not in (float, int):
            raise TypeError ("step must be a float or integer")
        self._step = step

    def set_value (self, value):
        """R.set_value (...) -> None

        Sets the current value of the Range.

        Sets the current value of the Range and raises a SIG_VALCHANGE
        event, if the new value differs from the old one.

        Raises a TypeError, if the passed argument is not a float or
        integer.
        Raises a ValueError, if the passed argument is not within the
        range of the Range its maximum and minimum value.
        """
        if type (value) not in (float, int):
            raise TypeError ("value must be a float or integer")
        if (self.minimum > value) or (self.maximum < value):
            raise ValueError ("value must be in the range from %f to %f"
                              % (self.minimum, self.maximum))
        if value != self._value:
            self._value = value
            self.run_signal_handlers (SIG_VALCHANGE)
            self.dirty = True

    def increase (self):
        """R.increase () -> None

        Increases the current Range value by one step.
        """
        val = self.value
        if val < self.maximum:
            val += self.step
            if val > self.maximum:
                val = self.maximum
        self.value = val

    def decrease (self):
        """R.decrease () -> None

        Decreases the current Range value by one step.
        """
        val = self.value
        if val > self.minimum:
            val -= self.step
            if val < self.minimum:
                val = self.minimum
        self.value = val

    minimum = property (lambda self: self._minimum,
                        lambda self, var: self.set_minimum (var),
                        doc = "The minimum value of the Range.")
    maximum = property (lambda self: self._maximum,
                        lambda self, var: self.set_maximum (var),
                        doc = "The maximum value of the Range.")
    value = property (lambda self: self._value,
                      lambda self, var: self.set_value (var),
                      doc = "The current value of the Range.")
    step = property (lambda self: self._step,
                     lambda self, var: self.set_step (var),
                     doc = "The step range of the Range.")
