# $Id: Bin.py,v 1.19 2005/09/17 09:07:04 marcusva Exp $
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

"""An abstract widget, which can hold exactly one other widget."""

from BaseWidget import BaseWidget

class Bin (BaseWidget):
    """Bin () -> Bin

    A container widget class, which can hold one other widget.

    The bin widget class is an abstract class, which can hold exactly
    one other widget. It is usable to serve as a container class, which
    can hold various types of widgets and allows inheritors to use their
    own look.

    The widget to hold can be set or removed using the 'child' attribute
    and set_child() method. The child will not be automatically modified
    by rebinding any of its attributes.
    
    bin.child = widget
    bin.set_child (widget)

    The 'padding' attribute and set_padding() method are used to place a
    certain amount of pixels between the child widget and the outer
    edges of the Bin.

    bin.padding = 10
    bin.set_padding (10)

    Binding the Bin to a new event manager using the 'manager' attribute
    or set_event_manager() method will cause the event manager of the
    child to be set to the same.

    Default action (invoked by activate()):
    None
    
    Mnemonic action (invoked by activate_mnemonic()):
    None
    
    Attributes:
    child   - The widget hold by the Bin.
    padding - Additional padding between the child and outer edges of
              the Bin. Default is 2.
    """
    def __init__ (self):
        BaseWidget.__init__ (self)

        self._child = None
        self._padding = 2

    def set_child (self, child=None):
        """B.set_child (...) -> None

        Sets (or resets) the child of the Bin.

        Creates a parent-child relationship from the Bin to the child by
        associating the Bin with the child and vice versa.

        Raises a TypeError, if the passed argument does not inherit
        from the BaseWidget class.
        Raises an Exception, if the passed argument is already
        attached to another parent.
        """
        if child:
            if not isinstance (child, BaseWidget):
                raise TypeError ("child must inherit from BaseWidget")
            if child.parent:
                raise Exception ("child already has a parent")
            child.parent = self
            if self.manager and not child.manager:
                child.set_event_manager (self.manager)
            # Set the states for the child.
            if not self.sensitive:
                child.set_sensitive (self.sensitive)
        if self._child:
            self._child.parent = None
        self._child = child
        self.dirty = True

    def set_event_manager (self, manager):
        """B.set_event_manager (...) -> None

        Sets the event manager of the Bin.

        Adds the Bin to an event manager and causes its child to be
        added to the same, too.
        """
        BaseWidget.set_event_manager (self, manager)
        if self.child:
            self.child.set_event_manager (manager)

    def set_sensitive (self, sensitive=True):
        """B.set_sensitive (...) -> None

        Sets the sensitivity of the Bin and its child.
        """
        BaseWidget.set_sensitive (self, sensitive)
        if self.child:
            self.child.set_sensitive (sensitive)
    
    def set_padding (self, padding):
        """B.set_padding (...) -> None

        Sets the padding between the child and edges of the Bin.

        The padding value is the amount of pixels to place between the
        edges of the Bin and the contained child.

        Raises a TypeError, if the passed argument is not a positive
        integer.

        Note: If the 'size' attribute is set, it can influence the
        visible space between the child and the edges. That does not
        mean, that any padding is set.
        """
        if (type (padding) != int) or (padding < 0):
            raise TypeError ("padding must be a positive integer")
        self._padding = padding

    def destroy (self):
        """B.destroy () -> None

        Destroys the Bin and removes it from its event system.
        """
        if self.child:
            w = self.child
            w.parent = None
            self.child = None
            w.destroy ()
            del w
            del self._child
        BaseWidget.destroy (self)
    
    child = property (lambda self: self._child,
                      lambda self, var: self.set_child (var),
                      doc = "The The widget hold by the Bin.")
    padding = property (lambda self: self._padding,
                        lambda self, var: self.set_padding (var),
                        doc = "Additional padding between child and borders.")
