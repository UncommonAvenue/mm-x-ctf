# $Id: BaseWidget.py,v 1.39 2005/09/15 16:24:29 marcusva Exp $
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

"""Basic widget class, used as an abstract definition for widgets."""

# TODO: Add ControlCollection class to the components.

import pygame
from ocempgui.object import BaseObject
from ocempgui.access import Accessible, Indexable
from Constants import *
import base

class BaseWidget (Accessible, BaseObject, pygame.sprite.Sprite):
    """BaseWidget () -> BaseWidget

    A basic widget class for user interface elements.

    The BaseWidget is the most basic widget class, from which any other
    widget class should be inherited. It provides the most basic
    attributes and methods, every widget needs.

    The widget is a visible (or non-vissible) element on the display,
    which allows the user to interact with it (active or passive) in a
    specific way. It has several methods and attributes to allow
    developers to control this interaction and supports accessibility
    through the ocempgui.access module.

    The widget can be placed on the display using the 'position'
    attribute or the set_position() method. The xy-coordinate (0, 0) is
    usually the topleft corner of the display. Note, that moving the
    widget automatically by reassigning this attribute is only
    guaranteed to work as supposed with the Renderer class.

    widget.position = 10, 10
    widget.set_positon (100, 40)

    To force a specific minimum size to occupy by the widget, the 'size'
    attribute or the respective set_size() method can be used. The
    occupied area of the widget will not be smaller than the size, but
    can be bigger.

    widget.size = 100, 50
    widget.set_size (10, 33)

    To get the actual dimensions of the widget, it provides the
    read-only 'width' and 'height' attributes. As mentioned above, those
    can differ from the 'size' attributes of the widget.

    if (widget.width > 50) or (widget.height > 50):
       ...

    The 'image' and 'rect' attributes are used and needed by the
    pygame.sprite system. 'image' refers to the visible surface of the
    widget, which will be blitted on the display. 'rect' is a
    pygame.Rect object indicating the occupied area of the widget. Those
    attributes should NOT be modified by user code.

    The 'index' attribute and set_index() method set the navigation
    index position for the widget. It is highly recommended to set this
    value in order to provide a better accessibility. The attribute can
    be used in ocempgui.access.Indexable implementations for example.

    widget.index = 3
    widget.set_index (0)

    Widgets support a 'style' attribute and get_style() method, which
    enable them to use different look than default one without the need
    to override their draw() method. The 'style' attribute of a widget
    usually defaults to a None value and can be set using the
    get_style() method. This causes the widget internals to setup the
    specific style for the widget and can be accessed through the
    'style' attribute later on. A detailled documentation of the style
    can be found in the Style class.

    if not widget.style:
        widget.get_style () # Setup the style internals first.
    widget.style['font']['size'] = 18
    widget.get_style ()['font']['name'] = Arial

    Widgets can be in different states, which cause the widgets to have
    a certain behaviour and/or look. Dependant on the widget and the
    actions it supports and actions, which have taken place, the state
    of the widget can change. The actual state of the widget can be looked
    up via the 'state' attribute and is one of the STATE_TYPES constants.

    if widget.state == STATE_INSENSITIVE:
        print 'The widget is currently insensitive and does not react.'

    Any widget supports layered drawing through the 'depth' attribute
    and a layer supporting render group, e.g. the RenderLayer class.
    The higher the depth is, the higher the layer will be, on which the
    widget will be drawn. Inherited widgets might use the flag to set
    themselves on top or bottom of the display, but it usually should
    NOT be modified by user code.

    # The widget will be placed upon all widgets with a depth lower than 4.
    widget.depth = 4
    widget.set_depth (4)
    
    Widgets will be redrawn automatically by a render group, which can
    consume much time by redrawing widgets, which visually did not
    change. The 'dirty' attribute and set_dirty() method work around
    this behaviour. Inherited widgets should set the 'dirty' attribute
    to True, whenever an update of the widget surface is necessary. In
    user code, 'dirty' usually does not need to be modified manually.

    If the 'parent' attribute of the widget is set, the parent its dirty
    attribute will be set to True, too.

    # Force redrawing the widget on the next update cycle of the render
    # group.
    widget.dirty = True

    Widgets support a focus mode, which denotes that the widget has the
    current input and action focus. Setting the focus can be done via
    the 'focus' attribute or the set_focus() method.

    widget.focus = True
    widget.set_focus (True)

    'sensitive' is an attribute, which can block the widget's reaction
    upon events temporarily. It also influences the look of the widget
    by using other style values (see STATE_INSENSITIVE in the Style
    class).

    widget.sensitive = False
    widget.set_sensitive (False)

    Widgets allow parent-child relationships via the 'parent' attribute.
    Parental relationships are useful for container classes, which can
    contain widgets and need to be informed, when the widget is
    destroyed, for example. Take a look the Bin and Container classes
    for details about possible implementations.
    Do NOT modify the 'parent' attribute value, if you do not know, what
    might happen.

    Widgets can consist of other widgets. To guarantee that all of them
    will be added to the same event management system, set the same
    state, etc., the 'controls' attribute exists. It is a collection to
    and from which widgets can be attached or detached. Several methods
    make use of this attribute by iterating over the attached widgets
    and invoking their methods to put them into the same state, etc. as
    the main widget.

    widget.controls.append (sub_widget)
    for sub in widget.controls:
        ...

    To simplify the event checking mechanisms for events, that use
    screen coordinates (e.g. mouse clicks or mouse movement), the
    'eventarea' attribute can be used. It usually defaults to the 'rect'
    attribute of the widget, but can be set to another pygame.Rect
    object to allow more simple position checks and so on.

    widget.eventarea = pygame.Rect (self.position[0], self.position[1], 10, 10)
    ...

    Default action (invoked by activate()):
    None, will raise an NotImplementedError

    Mnemonic action (invoked by activate_mnemonic()):
    None

    Signals:
    SIG_FOCUS - Invoked, when the widget receives the focus
                (widget.focus=True).
    
    Attributes:
    position  - Topleft coordinate of the widget in the form x, y. (*)
    size      - Guaranteed size of the widget.
    width     - Width of the widget.
    height    - Height of the widget.
    image     - The visible surface of the widget.
    rect      - The area occupied by the widget.
    index     - Navigation index of the widget.
    style     - The style to use for drawing the widget.
    state     - The current state of the widget.
    depth     - The z-axis layer depth of the widget. (*)
    dirty     - Indicates, that the widget needs to be updated. (*)
    focus     - Indicates, that the widget has the current input focus.
    sensitive - Indicates, if the user can interact with the widget.
    parent    - Slot for the creation of parent-child relationships.
    controls  - Collection of attached controls for complex widgets.
    eventarea - The area of the widget, which can get events
                (defaults to rect).
    
    (*) Only works as supposed with a pygame.sprite.Group, which
    supports a layer system. An example implementation can be found in
    the ocempgui.widgets.RenderLayer class.
    """
    def __init__ (self):
        Accessible.__init__ (self)
        BaseObject.__init__ (self)
        pygame.sprite.Sprite.__init__ (self)

        self._x = 0
        self._y = 0
        self._width = 0   # Guaranteed sizes for the widget, see also 
        self._height = 0  # the size attribute and set_size () method.
        
        self._image = None
        self._rect = None
        self._eventarea = None

        self._style = None
        self._index = 0
        self._state = STATE_NORMAL
        self._focus = False
        self._sensitive = True

        self._controls = []
        self.parent = None
        self._newdepth = 0
        self._depth = 0
        self._dirty = True
    
        # Signals, the widget listens to by default
        self._signals[SIG_FOCUS] = []

    def set_position (self, x, y):
        """W.set_position (...) -> None

        Sets the position of the upper left corner of the widget.

        Sets the upper left corner of the widget to the passed
        coordinates on the display.

        Raises a TypeError, if the passed arguments are not integers.

        Note: This method only works as supposed using a render loop,
        which supports the Renderer class specification.
        """
        if (type (x) != int) or (type (y) != int):
            raise TypeError ("x and y must be integers")
        if (self._x != x) or (self._y != y):
            self.dirty = True
        self._x = x
        self._y = y

    def set_size (self, width, height):
        """W.set_size (...) -> None

        Sets the minimum size to occupy for the widget.

        Minimum size means that the widget can exceed the size by any
        time, but its width and height will never be smaller than these
        values.

        Raises a TypeError, if the passed arguments are not integers.
        Raises a ValueError, if the passed arguments are not positive.
        """
        if (type (width) != int) or (type (height) != int):
            raise TypeError ("width and height must be positive integers")
        if (width < 0) or (height < 0):
            raise ValueError ("width and height must be positive integers")
        self._width = width
        self._height = height
        self.dirty = True

    def set_index (self, index):
        """W.set_index (...) -> None
        
        Sets the tab index of the widget.

        Sets the index position of the widget to the given value. It can
        be used by ocempgui.access.Indexable implementations to allow
        easy navigation access and activation for the widgets.

        Raises a TypeError, if the passed argument is not a positive
        integer.
        """
        if (type (index) != int) or (index < 0):
            raise TypeError ("index must be a positive integer")
        self._index = index

    def set_depth (self, depth):
        """S.set_depth (...) -> None

        Sets the z-axis layer depth for the widget.

        Sets the z-axis layer depth for the widget. This will need a
        renderer, which makes use of layers such as the RenderLayer
        class. By default, the higher the depth value, the higher the
        drawing layer of the widget is. That means, that a widget with a
        depth of 1 is placed upon widgets with a depth of 0.

        Note: To allow efficient comparisions of the depth before and
        after the invocation of update(), the depth 'attribute' will
        contain the passed value after the update() method.

        widget.depth = 3
        print widget.depth  # Will print 0.
        widget.update ()
        print widget.depth  # Will print 3.
        
        Raises a TypeError, if the passed argument is not a positive
        integer.
        """
        if type (depth) != int:
            raise TypeError ("depth must be an integer")
        self._newdepth = depth
        self.dirty = True
        
    def set_dirty (self, dirty):
        """S.set_dirty (...) -> None

        Marks the widget as dirty.

        Marks the widget as dirty, so that it will be updated within the
        next cycle. This method also sets the parent its dirty attribute
        to True.
        """
        # FIXME?: This can lead to circular update() loops. Maybe a lock
        # should be integrated.
        if dirty and self.parent:
            self.parent.dirty = True
        self._dirty = dirty

    def set_event_manager (self, manager):
        """B.set_event_manager (...) -> None

        Sets the event manager of the widget an its controls.

        Adds the widget to an event manager and causes its controls to
        be added to the same, too.
        If the event manager implements the Indexable interface, the
        widget will invoke the add_index() method for itself.
        """
        BaseObject.set_event_manager (self, manager)
        indexable = isinstance (manager, Indexable)
        if indexable:
            manager.add_index (self)
        for control in self.controls:
            control.set_event_manager (manager)

    def get_style (self):
        """W.get_style () -> Style
        
        Gets the style for the widget.

        Gets the style associated with the widget. If the widget had no
        style before, a new one will be created for it, based on the
        class name of the widget. The style will be copied internally
        and associated with the widget, so that modifications on it will
        be instance specific.
        
        More information about how a style looks like and how to modify
        them can be found in the Style class documentation.
        """
        if not self._style:
            # Create a new style from the base style class.
            self._style = base.GlobalStyle.copy_style (self.__class__)
        return self._style

    def set_style (self, style):
        """W.set_style (...) -> None

        Sets the style of the widget.

        Sets the style of the widget to the passed style dictionary.
        This method currently does not perform any checks, if the passed
        dictionary matches the criteria of the Style class.

        This method is intended for internal usage of the toolkit and
        its widget components. It usually should not be invoked by user
        code. Please use the get_style() method instead and modify the
        retured style dictionary.

        Raises a TypeError, if the passed argument is not a dict type.
        """
        if type (style) != dict:
            raise TypeError ("style must be a dictionary")
        s = self._style
        self._style = style
        del s
        self.dirty = True
    
    def set_focus (self, focus=True):
        """W.set_focus (...) -> bool

        Sets the input and action focus of the widget.
        
        Sets the input and action focus of the widget and returns True
        upon success or False, if the focus could not be set.

        Note: This method only works as supposed using
        a render loop, which supports the Renderer class specification.
        """
        if not self.sensitive:
            return False
        if focus:
            if not self._focus:
                self._focus = True
                self.dirty = True
                self.emit (SIG_FOCUS, self)
                self.run_signal_handlers (SIG_FOCUS)
        else:
            if self._focus:
                self.dirty = True
            self._focus = False
        return True

    def set_sensitive (self, sensitive=True):
        """W.set_sensitive (...) -> None

        Sets the sensitivity of the widget.

        In a sensitive state (the default), widgets can react upon user
        interaction while they will not do so in an insensitive
        state.
        
        To support the visibility of this, the widget style should
        support the STATE_INSENSITIVE flag, while inheriting widgets
        should check for the sensitivity to enable or disable the event
        mechanisms.
        """
        if sensitive != self._sensitive:
            self.dirty = True

            if sensitive:
                self._sensitive = True
                self.state = STATE_NORMAL
            else:
                self._sensitive = False
                self.state = STATE_INSENSITIVE
        for control in self.controls:
            control.set_sensitive (sensitive)

    def set_state (self, state):
        """W.set_state (...) -> None

        Sets the state of the widget.

        Sets the state of the widget. The state of the widget is mainly
        used for the visible or non-visible appearance of the widget,
        so that the user can determine the state of the widget
        easier.
        Usually this method should not be invoked by user code.

        Raises a ValueError, if the passed argument is not a value of
        the STATE_TYPES tuple.
        """
        if state not in STATE_TYPES:
            raise ValueError ("state must be a value from STATE_TYPES")
        if self._state != state:
            self.dirty = True
        self._state = state

    def set_event_area (self, area):
        """W.set_event_area (...) -> None

        Sets the area of the widget, which reacts upon events.

        The event area defines a rectangle area of the widget, which can
        be tested for events, that use screen coordinates such as clicks
        or mouse movement events. It defaults to the 'rect' attribute of
        the widget.

        The 'eventarea' never should be modified directly, but instead
        should be assigned a new pygame.Rect object.

        Raises a TypeError, if the passed argument is not a
        pygame.Rect.
        """
        if not isinstance (area, pygame.Rect):
            raise TypeError ("area must inherit from pygame.Rect")
        self._eventarea = area
    
    def activate (self):
        """W.activate () -> None

        Activates the widget.

        Activates the widget, which means, that the default action of
        the widget will be invoked.

        This method should be implemented by inherited widgets.
        """
        raise NotImplementedError

    def activate_mnemonic (self, mnemonic):
        """W.activate_mnemonic (...) -> bool

        Activates the widget through the set mnemonic.

        Activates the widget through the set mnemonic for it and returns
        True upon successful activation or False, if the widget was not
        activated.

        The BaseWidget.activate_mnemonic () method always returns False
        by default, so that this method should be implemented by
        inherited widgets, if they need explicit mnemonic support.

        Note: This method only works as supposed using
        a render loop, which supports the Renderer class specification.
        """
        return False
    
    def draw (self):
        """W.draw () -> Surface

        Draws the widget surface and returns it.

        Creates the visible surface of the widget and returns it to the
        caller.
        
        This method has to be implemented by inherited widgets.
        """
        raise NotImplementedError

    def notify (self, event):
        """W.notify (...) -> None

        Notifies the widget about an event.

        Note: Widgets, which are not visible (not shown) or are in a
        specific state (e.g. STATE_INSENSITIVE), usually do not receive
        any events. But dependant on the widget, this behaviour can be
        different, thus checking the visibility depends on the widget
        and implementation.
        """
        if not self.sensitive:
            return
        
        if (event.signal == SIG_FOCUS) and (event.data != self):
            if base.debug: print "BaseWidget.SIG_FOCUS (loose)"
            self.focus = False

    def update (self, *args):
        """W.update (...) -> None

        Updates the widget and refreshes its image and rect content.

        Updates the widget and refreshes its image and rect content, if
        the 'dirty' attribute evaluates to True. The *args arguments are
        silently ignored by this method. If they are needed, the method
        should be overriden and called within the overriding.
        """
        if not self.dirty:
            return
        self._image = self.draw ().convert ()

        renew = (self._eventarea is self._rect) or (self._eventarea == None)
        self._rect = self._image.get_rect ()
        self._rect.x = self._x
        self._rect.y = self._y
        self._depth = self._newdepth
        if renew:
            self._eventarea = self._rect
        self.dirty = False

    def destroy (self):
        """W.destroy () -> None

        Destroys the widget and removes it from its event system.

        Causes the widget to destroy itself as well as its controls and
        removes all from the connected event manager and sprite groups
        using the sprite.kill() method. If the event manager supports
        the Indexable interface, the widget will invoke the
        remove_index() of it.

        Note: This method only works as supposed using a render loop,
        which supports the Renderer class specification.
        """
        if self.parent:
            raise ValueError ("widget still has a parent relationship")
        
        # Clear the associated controls.
        _pop = self._controls.pop
        while len (self._controls) > 0:
            control = _pop ()
            control.parent = None
            control.destroy ()
            del control
        del self._controls

        if self.manager and isinstance (self.manager, Indexable):
            self.manager.remove_index (self)
        
        BaseObject.destroy (self) # Clear BaseObject internals.
        self.kill ()              # Clear Sprite
        del self.parent
        del self._style
        del self._image
        del self._rect
        del self

    position = property (lambda self: (self._x, self._y),
                         lambda self, (x, y): self.set_position (x, y),
                         doc = "The position of the topleft corner.")
    width = property (lambda self: self._rect.width,
                      doc = "The width of the widget.")
    height = property (lambda self: self._rect.height,
                       doc = "The height of the widget.")
    size = property (lambda self: (self._width, self._height),
                     lambda self, (w, h): self.set_size (w, h),
                     doc = "The guaranteed size of the widget.")
    image = property (lambda self: self._image,
                      doc = "The visible surface of the widget.")
    rect = property (lambda self: self._rect,
                     doc = "The area occupied by the widget.")
    index = property (lambda self: self._index,
                      lambda self, var: self.set_index (var),
                      doc = "The tab index position of the widget.")
    style = property (lambda self: self._style,
                      lambda self, var: self.set_style (var),
                      doc = "The style of the widget.")
    state = property (lambda self: self._state,
                      lambda self, var: self.set_state (var),
                      doc = "The current state of the widget.")
    focus = property (lambda self: self._focus,
                      lambda self, var: self.set_focus (var),
                      doc = "The focus of the widget.")
    sensitive = property (lambda self: self._sensitive,
                          lambda self, var: self.set_sensitive (var),
                          doc = "The sensitivity of the widget.")
    dirty = property (lambda self: self._dirty,
                      lambda self, var: self.set_dirty (var),
                      doc = """Indicates, whether the widget need to be
                      redrawn.""")
    controls = property (lambda self: self._controls,
                         doc = "Widgets associated with the widget.")
    eventarea = property (lambda self: self._eventarea,
                          lambda self, var: self.set_event_area (var),
                          doc = "The area, which gets the events.")
    depth = property (lambda self: self._depth,
                      lambda self, var: self.set_depth (var),
                      doc = "The z-axis layer depth of the widget.")
