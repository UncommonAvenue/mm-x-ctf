# $Id: Container.py,v 1.13 2005/09/07 18:44:18 marcusva Exp $
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

"""An abstract widget, which can hold other widgets."""

from BaseWidget import BaseWidget

class Container (BaseWidget):
    """Container () -> Container

    A container widget class, which can hold multiple other widgets.

    The Container class is an abstract class, which can hold multiple
    widgets. It is usable to serve as container for various types of
    widgets and allows inheritors to use their own look.

    The 'children' attribute is a list of the widgets added to the
    Container. It is strongly recommended to modify this property using
    the add_widget() and remove_widget() methods only. Doing otherwise
    can lead to misbehaviours of the Container and children.

    children = container.children           # get the list of children
    container.add_widget (widget)           # add a widget
    container.add_widget (widget1, widget2) # add multiple widgets at once
    container.remove_widget (widget)        # remove a widget

    The 'padding' attribute and set_padding() method are used to place a
    certain amount of pixels between the children and the outer edges of
    the Container.

    container.padding = 10
    container.set_padding (10)

    An additional amount of pixels can be placed between the widgets
    using the 'spacing' attribute or set_spacing() method. Dependant on
    the inherited Container class, this places the given amount of
    pixels between the children.

    container.spacing = 10
    container.set_spacing (10)

    Default action (invoked by activate()):
    None
    
    Mnemonic action (invoked by activate_mnemonic()):
    None

    Attributes:
    children - List of widgets packed into the Container.
    spacing  - Spacing in pixels between the children.
    padding  - Padding between the borders and the children of the Container.
    """
    def __init__ (self):
        BaseWidget.__init__ (self)
        self._children = []
        self._spacing = 2
        self._padding = 2

    def set_spacing (self, spacing):
        """C.set_spacing (...) -> None

        Sets the spacing between the children of the Container.

        The spacing value is the amount of pixels to place between the
        children of the Container.

        Raises a TypeError, if the passed argument is not a positive
        integer.
        """
        if (type (spacing) != int) or (spacing < 0):
            raise TypeError ("spacing must be a positive integer")
        self._spacing = spacing

    def set_padding (self, padding):
        """C.set_padding (...) -> None

        Sets the padding between the edges and the children of the Container.
        
        The padding value is the amount of pixels to place between the
        edges of the Container and its child widgets.

        Raises a TypeError, if the passed argument is not a positive
        integer.
        """
        if (type (padding) != int) or (padding < 0):
            raise TypeError ("padding must be a positive integer")
        self._padding = padding

    def set_event_manager (self, manager):
        """C.set_event_manager (...) -> None

        Sets the event manager of the Container.

        Adds the Container to an event manager and causes its children
        to be added to the same, too.
        """
        BaseWidget.set_event_manager (self, manager)
        for child in self.children:
            child.set_event_manager (manager)
    
    def set_sensitive (self, sensitive=True):
        """C.set_sensitive (...) -> None

        Sets the sensitivity of the Container and its children.
        """
        BaseWidget.set_sensitive (self, sensitive)
        for child in self.children:
            child.set_sensitive (sensitive)

    def add_child (self, *children):
        """C.add_child (...) -> None

        Adds one or more children to the Container.
        
        Adds one or more children to the Container and updates the
        parent-child relationships.
        
        Raises a TypeError, if one of the passed arguments does not
        inherit from the BaseWidget class.
        Raises an Exception, if one of the passed arguments is already
        attached to another parent.
        """
        for child in children:
            if not isinstance (child, BaseWidget):
                raise TypeError ("Widget %s must inherit from BaseWidget"
                                 % child)
            if child.parent:
                raise Exception ("Widget %s already packed into another"
                                 "Container" % child)
            child.parent = self
            if not self.sensitive:
                child.set_sensitive (self.sensitive)
            self.children.append (child)
            if self.manager and not child.manager:
                child.manager = self.manager
            self.dirty = True

    def remove_child (self, child):
        """C.remove_widget (...) -> None

        Removes a child from the Container.
        
        Removes the child from the Container and updates the
        parent-child relationship of the child.

        Raises a TypeError, if the passed argument does not inherit from
        the BaseWidget class.
        """
        if not isinstance (child, BaseWidget):
            raise TypeError ("child must inherit from BaseWidget")
        self.children.remove (child)
        child.parent = None
        self.dirty = True

    def destroy (self):
        """C.destroy () -> None

        Destroys the Container and removes it from its event system.
        """
        _pop = self.children.pop
        while len (self.children) > 0:
            widget = _pop ()
            widget.parent = None
            widget.destroy ()
            del widget
        # del self.children
        BaseWidget.destroy (self)

    spacing = property (lambda self: self._spacing,
                        lambda self, var: self.set_spacing (var),
                        doc = "The spacing between the children.")
    padding = property (lambda self: self._padding,
                        lambda self, var: self.set_padding (var),
                        doc = "The additional padding for the Container.")
    children = property (lambda self: self._children,
                         doc = "List of the children for the Container.")
