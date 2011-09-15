# $Id: RadioButton.py,v 1.25 2005/09/12 12:43:43 marcusva Exp $
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

"""A button, which switches its state in dependance of other buttons."""

from ToggleButton import ToggleButton
from Constants import *
import base

class RadioButton (ToggleButton):
    """RadioButton (text, group=None) -> RadioButton

    Creates a new RadioButton widget.

    The RadioButton can be grouped with other radio button to allow a
    selection of a limited amount of choices. The constructor of the
    RadioButton allows you, to assign it to an already existing group of
    RadioButton. If no group is provided, the radio button will become a
    group.

    The RadioButton can be assigned to a group of RadioButton by setting
    the 'group' attribute to the specified RadioButton group or by using
    the set_group() method.

    radiobutton.group = other_radio_button
    radiobutton.set_group (other_radio_button)

    The 'active' attribute and set_active() method allow you to toggle
    the state of the RadioButton. Whenever a RadioButton of a respective
    group will be activated, any other active RadioButton of that group
    will lose its state.

    radiobutton.active = True
    radiobutton.set_active (True)

    It is possible to add and remove RadioButtons to or from a specific
    group using the add_button() and remove_button() methods.

    radiobutton.add_button (other_radio_button)
    radiobutton.remove_button (other_radio_button)

    Note: It is possible to create nested sub groups of radio buttons by
    adding a radio button to another one, which is already in a group.

    Default action (invoked by activate()):
    See the ToggleButton class.
    
    Mnemonic action (invoked by activate_mnemonic()):
    See the ToggleButton class.
    
    Attributes:
    group - The radio button group the button belongs to.
    list  - List of attached RadioButtons.
    """
    def __init__ (self, text, group=None):
        ToggleButton.__init__ (self, text)

        # Group, the RadioButton is attached to.
        self._group = None

        # List for attached RadioButtons.
        self._list = []

        if group:
            group.add_button (self)
        else:
            self._list.append (self)

    def set_group (self, group):
        """R.set_group (...) -> None

        Sets the group of RadioButtons, the RadioButton belongs to.

        Adds the RadioButton to a group, which causes the group to act
        as a RadioButton group, if it is not already one. If the button
        is already in another group, it will be removed from that group
        first.

        Raises a TypeError, if the passed argument does not inherit from
        the RadioButton class.
        """
        if group and not isinstance (group, RadioButton):
            raise TypeError ("group must inherit from RadioButton")
        if self._group:
            if self._group != group:
                g = self._group
                self._group = None
                if self in g.list:
                    g.remove_button (self)
        self._group = group
        if group:
            group.add_button (self)
            
    def set_active (self, active):
        """R.set_active (...) -> None

        Sets the state of the radio button.

        Sets the state of the RadioButton. if the active argument
        evaluates to True, the radio button will be activated and any
        other button of the same group deactivated.
        """
        l = self.list or self.group.list
        if active:
            ToggleButton.set_active (self, active)
            for button in l:
                if button != self:
                    button.set_active (False)
        else:
            found = False
            for button in l:
                if button.active and (button != self):
                   found = True
                   break
            if found:
                ToggleButton.set_active (self, active)
    
    def add_button (self, button):
        """R.add_button (...) -> None

        Adds a RadioButton to the group of RadioButtons.

        Adds a RadioButton to the RadioButtons causing it to become a
        RadioButton group, if it was not before.

        Raises a TypeError, if the passed argument does not inherit
        from the RadioButton class.
        """
        if not isinstance (button, RadioButton):
            raise TypeError ("button must inherit from RadioButton")
        if button not in self.list:
            self.list.append (button)
            button.group = self

    def remove_button (self, button):
        """R.remove_button (...) -> None

        Removes a RadioButton from the group of RadioButtons.

        Removes a RadioButton from the group and sets its 'group'
        attribute to None.
        """
        self.list.remove (button)
        button.group = None

    def draw (self):
        """R.draw () -> Surface

        Draws the RadioButton surface and returns it.

        Creates the visible surface of the RadioButton and returns it to
        the caller.
        """
        if self.child:
            self.child.update ()
        return base.GlobalStyle.draw_radiobutton (self)
    
    def destroy (self):
        """R.destroy () -> None

        Destroys the RadioButton and removes it from its event system.
        """
        if self.group:
            self.group.remove_button (self)
        else:
            while len (self.list) > 0:
                self.remove_button (self.list[0])
        del self._list
        del self._group
        ToggleButton.destroy (self)

    group = property (lambda self: self._group,
                      lambda self, var: self.set_group (var),
                      doc = "The group the RadioButton belongs to.")
    list = property (lambda self: self._list,
                     doc = "The attached RadionButtons.")
