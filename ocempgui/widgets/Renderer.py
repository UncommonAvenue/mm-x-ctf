# $Id: Renderer.py,v 1.26 2005/09/17 09:07:04 marcusva Exp $
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

"""A specialized event manager and render group class for widgets."""

import pygame
from pygame.locals import *
from ocempgui.events import EventManager
from ocempgui.access import Indexable
from RenderLayer import RenderLayer
from BaseWidget import BaseWidget
from Constants import *
import base

class Renderer (EventManager, RenderLayer, Indexable):
    """Renderer (title, width=1, height=1) -> Renderer

    A Renderer, which can deal with events and sprites.

    The Renderer class incorporates an event management system based on
    the EventManager class from the ocempgui.events module as well as a
    layered render group, which can work with pygam.sprite.Sprite
    objects. It contains several attributes and methods to create and
    manipulate a pygame window as well as interfaces to support a higher
    range of accessibility features such as keyboard navigation.

    The Renderer class can be used as standalone render engine and event
    loop for a pygame application or be integrated in an existing loop
    easily.

    The 'title' attribute and set_title() method will set the caption
    title of the pygame window. This works independant of if the
    Renderer works in a standalon or integrated mode.

    The 'screen' attribute and set_screen() method allow you to set up
    the background surface the Renderer shall use for blitting
    operations. This can be especially useful, if only portions of the
    complete visible screen contain elements, which should be handled by
    the Renderer and/or if the Renderer is not used as standalone render
    engine. If you instead want to use the Renderer as standalone, the
    create_screen() method should be used to create the pygame window
    with the desired size.

    # Screen already exists:
    renderer.screen = mainscreen
    renderer.set_screen (own_screen_portion)

    # Renderer will be used as standalone render engine with a pygame
    # window of 800x600 size.
    renderer.create_screen (800, 600)

    It is possible to set the background color of the set screen by
    adjusting the 'color' attribute or set_color() method. By default it
    uses a clear white color with the RBG value (255, 255, 255). It is
    possible to change that value by any time. It will be used in the
    next update cycles then.

    renderer.color = (255, 0, 0)
    renderer.set_color (100, 220, 100)

    The Renderer supports an update timer value (~ FPS setting), which
    defaults to 40. That means, that the timer will cause the screen to
    update 40 times a second, which is a good value for most cases. On
    demand it can be adjusted using the 'timer' attribute or set_timer()
    method. Be careful with it. High values will cause higher CPU load.

    Keyboard navigation
    -------------------
    The Renderer class implements keyboard navigation through the
    ocempgui.access.Indexable interface class. It uses the TAB key for
    switching between attached objects. Objects can be attached and
    removed using the add_index() and remove_index() method (Note:
    objects inheriting from the BaseWidget class, will do that
    automatically by default). Switching is done via the switch_index()
    method, which will be activated automatically by sending a KEYDOWN
    event with the TAB key as value.

    Objects which should be added to the navigation indexing, need to
    have a 'index' and 'sensitive' attribute and a set_focus() method,
    which receives a bool value as argument and returns True on
    successfully setting the focus or False otherwise. In case that
    False will be returned the method will try to set the focus on the
    next object.

    The index is needed for the order the objects shall be navigated
    through. Objects with a lower index will be focused earlier than
    objects with a higher index.

    The Renderer supports automatic cycling through the objects, which
    means, that if the end of the index list is reached it will start
    from the beginning of the list.

    Mnemonic support
    ----------------

    The Renderer supports mnemonic keys (also known as hotkeys) for
    object activation through the <ALT><Key> combination. If it receives
    a KEYDOWN event, in which the ALT modifier is set, it will not
    escalate the event to its children, but instead loop over its
    indexing list in order to activate a matching child.

    As stated in 'Keyboard Navigation' the objects need to have a
    'sensitive' attribute. Additionally they must have
    'activate_mnemonic()' method, which receives a unicode as argument
    and returns True on successfuls mnemonic activation or False
    otherwise. If the widget's 'sensitive' attribute does not evaluate
    to True, the Renderer will not try to invoke the activate_mnemonic()
    method of the widget.

    Using the Renderer as standalone engine
    ---------------------------------------

    Using the Renderer as standalone engine is very simple. You usually
    have to type the following code to get it to work:

    renderer = Renderer ()
    renderer.create_screen (width, height)
    renderer.title = 'Window caption title'
    renderer.color = (100, 200, 100)
    ...
    re.start ()
    
    The first line will create a new Renderer object. The second creates
    a new pygame window with the passed width and height. The third and
    fourth line are not necessary, but useful and will set the window
    caption of the pygame window and the background color to use for the
    window.
    
    After those few steps you can add objects to the Renderer via the
    add_widget() method, use the inherited Group.add() method of the
    pygame.sprite system or the add_object() method from the inherited
    ocempgui.events.EventManager class.

    When you are done with that, an invocation of the start() method
    will run the event loop of the Renderer.

    Integrating the Renderer in an existing environment
    ---------------------------------------------------
    
    If an event loop and window already exists or an own event loop is
    necessary, the Renderer can be integrated into it with only a few
    lines of code. First you will need to set the screen, on which the
    Renderer should blit its objects:

    renderer = Renderer ()
    renderer.screen = your_main_screen_or_surface

    Then you can send the events processed in your event loop to the
    Renderer and its objects via the distribute_events() method:

    def your_loop ():
        ...
        renderer.distribute_events (received_events)
    
    Attributes:
    title  - The title caption to display on the pygame window.
    screen - The screen to draw on.
    timer  - Speed of the event and update loop. Default is 40 fps.
    color  - The background color of the screen. Default is (255, 255, 255).
    """
    def __init__ (self):
        EventManager.__init__ (self)
        RenderLayer.__init__ (self)

        self._title = None
        self._screen = None
        self._background = None
        self._color = (255, 255, 255)

        # Timer value for the event system. 40 frames per second should
        # be enough as default.
        self._timer = 40

        # Internal widget(!) list for fast access to the widgets.
        self._index = []

        self.esc = 0
    
    def set_title (self, title):
        """R.set_title (...) -> None

        Sets the title to display on the pygame window.

        Raises a TypeError, if the passed argument is not a string or
        unicode.
        """
        if type (title) not in (str, unicode):
            raise TypeError ("title must be a string or unicode")
        self._title = title
        pygame.display.set_caption (self._title)
        
    def set_screen (self, screen):
        """R.set_screen (...) -> None

        Sets the screen to use for the Renderer and its widgets.

        Sets the screen surface, the renderer will draw the widgets on
        (usually, you want this to be the entire screen).

        Raises a TypeError, if the passed argument does not inherit
        from pygame.Surface.
        """
        if screen and not isinstance (screen, pygame.Surface):
            raise TypeError ("screen must inherit from Surface")
        self._screen = screen
        self._create_bg ()

    def set_timer (self, timer=40):
        """R.set_timer (...) -> None

        Sets the speed of the event and update loop for the Renderer.

        Sets the speed for the internal event and update loop of the
        renderer. The higher the value, the faster the loop will go,
        which can cause a higher CPU usage. As a rough rule of thumb the
        timer value can be seen as the frames per second (FPS) value. A
        good value (also the default) is around 40 (~40 FPS) for modern
        computers.

        Raises a TypeError, if the passed argument is not a positive
        integer.
        """
        if (type (timer) != int) or (timer <= 0):
            raise TypeError ("timer must be a positive integer > 0")
        self._timer = timer

    def set_color (self, color):
        """R.set_color (...) -> None

        Sets the background color of the attached screen.
        """
        self._color = color
        if self.screen:
            self._create_bg ()

    def _create_bg (self):
        """R._create_bg () -> None

        Creates the background for refreshing the window.
        """
        self._background = pygame.Surface (self.screen.get_size ()).convert ()
        self._background.fill (self.color)
        
    def create_screen (self, width, height):
        """R.create_screen (...) -> None

        Creates a new pygame window for the renderer.

        Initializes the pygame engine and creates a new pygame window
        with the given width and height and associates its entire
        surface with the 'screen' attribute to draw on.

        Raises a TypeError, if the passed arguments are not positive
        integers.
        Raises a ValueError, if the passed arguments are not positive
        integers greater than 0.
        """
        if (type (width) != int) or (type (height) != int):
            raise TypeError ("width and height must be positive integers > 0")
        if (width <= 0) or (height <= 0):
            raise ValueError ("width and height must be positive integers > 0")
        pygame.init ()
        self.screen = pygame.display.set_mode ((width, height))
        pygame.key.set_repeat (500, 30)
        
    def add_widget (self, *widgets):
        """R.add_widget (...) -> None

        Adds one or more widgets to the Renderer.

        Adds one or more widgets to the event system and the RenderGroup
        provided by the Renderer class. The widgets will be added to the
        internal indexing system for keyboard navigation, too.

        Raises a TypeError, if one of the passed arguments does not
        inherit from the BaseWidget class.
        """
        for widget in widgets:
            if not isinstance (widget, BaseWidget):
                raise TypeError ("Widget %s must inherit from BaseWidget"
                                 % widget)
            widget.manager = self
            if not self.has (widget):
                self.add (widget)

    def remove_widget (self, widget):
        """R.remove_widget (...) -> None

        Removes a widget from the Renderer.

        Removes a widget from the event system, the RenderGroup and the
        indexing systen of the Renderer class.
        """
        self.remove_object (widget)
        self.remove (widget)
        self.remove_index (widget)

    def add_index (self, *objects):
        """R.add_index (...) -> None

        Adds one or more widgets to the indexing system.

        The indexing system of the Renderer provides easy keyboard
        navigation using the TAB key. Widgets will by activated using
        their index, if they are added to to the indexing system.

        Raises a TypeError, if one of the passed arguments does not
        inherit from the BaseWidget class.
        """
        for widget in objects:
            if not isinstance (widget, BaseWidget):
                raise TypeError ("Widget %s must inherit from BaseWidget"
                                 % widget)

            if widget not in self._index:
                self._index.append (widget)
        # Sort the widget list, so we can access the index keys more
        # quickly.
        self._index.sort (lambda x, y: cmp (x.index, y.index))

    def remove_index (self, *objects):
        """R.remove_index (...) -> None

        Removes a widget from the indexing system.

        Removes a wigdget from the indexing system of the Renderer.
        """
        for widget in objects:
            self._index.remove (widget)

    def force_update (self, wait=0):
        """R.force_update (...) -> None

        Forces the renderer to update the screen.

        Forces the renderer to update the screen and to wait for a
        specific amount of time (in milliseconds).
        """
        self.update ()
        if self.screen:
            self.screen.blit (self._background, (0, 0))
            self.draw (self.screen)
            pygame.display.flip ()
        if wait > 0.0:
            pygame.time.wait (wait)

    def start (self):
        """R.start () -> None

        Starts the main loop of the Renderer.
        """
        self._loop ()

    def switch_index (self):
        """R.switch_index () -> None

        Passes the input focus to the next widget.

        Passes the input focus to the widget, which is the next
        focusable after the one with the current focus.
        """
        length = len (self._index)
        if length == 0:
            return

        # Check, if at least one widget can be activated.
        widgets = [wid for wid in self._index if wid.sensitive]
        if len (widgets) == 0:
            # None can be activated, return.
            return

        # Get the widget with focus.
        current = None
        try:
            current = [wid for wid in self._index if wid.focus][0]
        except IndexError:
            # None is focused.
            pass

        if not current:
            pos = -1
        else:
            pos = widgets.index (current)
        
        # Reslice the list and traverse it.
        widgets = widgets[pos + 1:] + widgets[:pos + 1]
        for wid in widgets:
            if wid.set_focus (True):
                # Found a widget, which allows to be focused, exit here.
                return
        # No focus set, print a debug message.
        if base.debug: print "Renderer.switch_index () got no focus"
    
    def _is_mod (self, mod):
        """R._is_mod (...) -> bool

        Determines, if the passed key value is a key modificator.
        
        Returns True if the pass key value is a key modificator
        (KMOD_ALT, KMOD_CTRL, etc.), False otherwise.
        """
        if (mod & KMOD_ALT) or (mod & KMOD_LALT) or (mod & KMOD_RALT) or \
               (mod & KMOD_SHIFT) or (mod & KMOD_LSHIFT) or \
               (mod & KMOD_RSHIFT) or (mod & KMOD_CTRL) or \
               (mod & KMOD_RCTRL) or (mod & KMOD_LCTRL):
            return True
        return False

    def _activate_mnemonic (self, event):
        """R._activate_mnemonic (...) -> None

        Activates the mnemonic key method of a widget.

        This method iterates over the widgets of the indexing system and
        tries to activate the mnemonic key method (activate_mnemonic())
        of them. It breaks right after the first widget's method
        returned True.
        """
        for wid in self._index:
            if wid.sensitive and wid.activate_mnemonic (event.unicode):
                break

    def distribute_events (self, *events):
        """R.distribute_events (...) -> bool

        Distributes one ore more events to the widgets of the Renderer.

        The method distributes the received events to the attached
        objects. If the events contain KEYDOWN events, the Indexable
        interface method for keyboard navigation will be invoked before
        the Renderer tries to send them to its objects.

        The method returns False, as soon as it receives a QUIT event.
        If all received events passed it successfully, True will be
        returned.
        """
        for event in events:
            ev = None
            if event.type == QUIT:
                return False

            elif event.type == MOUSEMOTION:
                ev = (SIG_MOUSEMOVE, event)

            elif event.type == MOUSEBUTTONDOWN:
                ev = (SIG_MOUSEDOWN, event)

            elif event.type == MOUSEBUTTONUP:
                ev = (SIG_MOUSEUP, event)

            elif event.type == KEYDOWN:
                # Check, if it is the TAB key and call the index function.
                if (event.key == K_TAB) and not self._is_mod (event.mod):
                    if base.debug: print "Index switch detected..."
                    self.switch_index ()

                elif event.key == K_ESCAPE:
                    self.esc = 1
                elif event.mod & KMOD_ALT:
                    self._activate_mnemonic (event)
                else:
                    ev = (SIG_KEYDOWN, event)

            elif event.type == KEYUP:
                ev = (SIG_KEYUP, event)

            if ev:
                self.emit (ev[0], ev[1])
        return True
    
    def _loop (self):
        """R._loop () -> None
        
        The main event loop of the Renderer.

        Main event loop of the renderer. This loop hooks up on the
        event loop of pygame and distributes all its event to the attached
        objects.
        """
        clock = pygame.time.Clock ()
        while True:
            clock.tick (self.timer)

            # Emit tick events.
            self.emit (SIG_TICK, None)

            # Get events and distribute them.
            events = pygame.event.get ()
            if not self.distribute_events (*events):
                return  # QUIT event
            self.force_update ()
    
    title = property (lambda self: self._title,
                      lambda self, var: self.set_title (var),
                      doc = "The title of the pygame window.")
    screen = property (lambda self: self._screen,
                       lambda self, var: self.set_screen (var),
                       doc = "The screen to draw on.")
    timer = property (lambda self: self._timer,
                      lambda self, var: self.set_timer (var),
                      doc = "The speed of the event and update loop.")
    color = property (lambda self: self._color,
                      lambda self, var: self.set_color (var),
                      doc = "The background color of the pygame window.")
    
class MenuRenderer(Renderer):
    def __init__(self, previous):
        self.previous = previous
        Renderer.__init__(self)
