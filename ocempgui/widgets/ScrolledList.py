# $Id: ScrolledList.py,v 1.34 2005/09/15 23:37:55 marcusva Exp $
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

"""A scrollable widget, which contains list elements."""

import pygame
from BaseWidget import BaseWidget
from ScrolledWindow import ScrolledWindow
from ocempgui.draw import Draw
from ocempgui.widgets.components import ListItemCollection
from Constants import *
import base

class _ListViewPort (BaseWidget):
    """_ListViewPort (scrolledlist) -> _ListViewPort

    The view for the items.

    The _ListViewPort is an internal proxy class, which is attached as
    widget to the ScrolledList.

    TODO: Make this a public class suitable for list and tree widgets.
    """
    def __init__ (self, scrolledlist):
        BaseWidget.__init__ (self)
        self._itemcollection = None
        self.itemcollection = ListItemCollection ()
        self.scrolledlist = scrolledlist
        self._spacing = 2

        self._signals[SIG_MOUSEDOWN] = []
        self._signals[SIG_KEYDOWN] = None # Dummy for keyboard activation.

    def set_position (self, x, y):
        """_L.set_position (...) -> None

        Sets the position of the upper left corner of the _ListViewPort.

        Sets the upper left corner of the _ListViewPort to the passed
        coordinates on the display. In contrast to the set_position()
        method of the BaseWidget class, this one does not set the dirty
        attribute of the _ListViewPort to False.

        Raises a TypeError, if the passed arguments are not integers.
        """
        if (type (x) != int) or (type (y) != int):
            raise TypeError ("x and y must be integers")
        if (self._x != x) or (self._y != y):
            self.dirty = True
        self._x = x
        self._y = y

    def set_focus (self, focus=True):
        """_L.set_focus (focus=True) -> None

        Overrides the set_focus() behaviour for the _ListViewPort.
        """
        return False

    def set_itemcollection (self, collection):
        """_L.set_itemcollection (...) -> None

        Sets the item collection to use by the _ListViewPort.
        """
        if collection and not isinstance (collection, ListItemCollection):
            raise TypeError ("collection must inherit from ListItemCollection")
        if  self._itemcollection != None:
            if self._itemcollection != collection:
                self._itemcollection.item_changed = None
            else:
                return # Already attached.
        self._itemcollection = collection
        collection.item_changed = self._item_has_changed
        self.dirty = True

    def get_item_at_pos (self, position):
        """_L.get_item_at_pos (...) -> ListItem

        Gets the item at the passed position coordinates.
        """
        if not self.eventarea.collidepoint (position):
            return None

        for item in self.itemcollection:
            real_rect = pygame.Rect (item.rect)
            real_rect.x = self.position[0]
            real_rect.y += self.position[1]
            real_rect.width = self.eventarea.width + \
                              self.scrolledlist.hscrollbar.maximum
            if real_rect.bottom > self.eventarea.bottom:
                real_rect.bottom = self.eventarea.bottom
            if real_rect.collidepoint (position):
                return item
        return None
    
    def _item_has_changed (self, item):
        """_L._item_has_changed (...) -> None

        Update method for item_changed() notifications.
        """
        self.dirty = True
    
    def _update_items (self):
        """_L._update_items () -> int, int

        Updates the attached items.

        Updates the attached items and returns the complete width and
        height, which will be occupied by them.
        """
        border = base.GlobalStyle.get_border_size \
                 (self.scrolledlist.__class__, self.style, BORDER_FLAT) * 2
        
        width = 0
        height = 0
        for item in self.itemcollection:
            item.update (self.scrolledlist.state)
            if width < item.rect.width:
                width = item.rect.width + border
            height += item.rect.height + self.scrolledlist.spacing + border
        # The last item does not need any spacing.
        if height > 0:
            height -= self.scrolledlist.spacing
        return width, height
    
    def draw (self):
        """_L.draw () -> Surface

        Draws the _ListViewPort surface and returns it.

        Creates the visible surface of the _ListViewPort and returns it
        to the caller.
        """
        cls = self.scrolledlist.__class__
        style = base.GlobalStyle
        st = self.scrolledlist.style or style.get_style (cls)

        border = style.get_border_size (cls, self.style, BORDER_FLAT)
        color = style.get_style_entry (cls, st, "selcolor", self.state)
        
        width, height = self._update_items ()
        # The surface of the view should match the visible area, if it
        # is smaller.
        tmp = self.scrolledlist.get_visible_area ()[0] - \
              self.scrolledlist.padding - 2 * border
        if (width > 0) and (width < tmp):
            width = tmp
        surface = style.draw_rect (width, height, self.state, cls, self.style)

        posy = 0
        for item in self.itemcollection:
            # The items are already up to date, so we just need to blit
            # their surfaces.
            if item.selected:
                sel_height = item.rect.height + 2 * border
                surface_select = Draw.draw_rect (width, sel_height, color)
                surface_select = style.draw_border (surface_select, self.state,
                                                    cls, self.style,
                                                    BORDER_FLAT, space=1)
                item.rect.x = border
                item.rect.y = border
                surface_select.blit (item.image, item.rect)
                item.rect.y += posy # Set the correct position.
                surface.blit (surface_select, (0, posy))
            else:
                item.rect.x = border
                item.rect.y = posy + border
                surface.blit (item.image, item.rect)

            posy += item.rect.height + self.scrolledlist.spacing + 2 * border
        return surface

    itemcollection = property (lambda self: self._itemcollection,
                               lambda self, var: self.set_itemcollection (var),
                               doc = "The item collection of the ListView.")

class ScrolledList (ScrolledWindow):
    """ScrolledList (width, height, collection=None) -> ScrolledList

    Creates a scrollable list widget.

    The ScrolledList displays data in a listed form and allows to browse
    through it using horizontal and vertical scrolling. Single or
    multiple items of the list can be selected or - dependant on the
    ListItem object - be edited, etc.

    TODO

    Default action (invoked by activate()):
    See the ScrolledWindow class.
    
    Mnemonic action (invoked by activate_mnemonic()):
    None
    
    Signals:
    SIG_SELECTCHANGE - Invoked, when the item selection changes.
    SIG_LISTCHANGE   - Invoked, when the underlying item list changes.
    
    Attributes:
    items         - Item list of the ScrolledList.
    selectionmode - The selection mode for the ScrolledList. Default is
                    SELECTION_MULTIPLE.
    spacing       - Spacing to place between the list items. Default is 2.
    """
    def __init__ (self, width, height, collection=None):
        ScrolledWindow.__init__ (self, width, height)
        self._spacing = 2
        
        # Items and selection.
        self._selectionmode = SELECTION_MULTIPLE
        self.child = _ListViewPort (self)
        if collection:
            self.set_items (collection)

        self._signals[SIG_LISTCHANGE] = []
        self._signals[SIG_SELECTCHANGE] = []

    def _list_has_changed (self, collection):
        """S._list_has_changed (...) -> None

        Update method for list_changed () notifications.
        """
        self.child.dirty = True
        self.dirty = True
        self.run_signal_handlers (SIG_LISTCHANGE)

    def set_child (self, child=None):
        """B.set_child (...) -> None

        Sets (or resets) the child of the ScrolledList.

        Creates a parent-child relationship from the ScrolledLsit to the
        child by associating the ScrolledList with the child and vice versa.

        Raises a TypeError, if the passed argument does not inherit
        from the _ListViewPort class.
        """
        if child and not isinstance (child, _ListViewPort):
            raise TypeError ("child must inherit from _ListViewPort")
        ScrolledWindow.set_child (self, child)
        if child:
            self.child.itemcollection.list_changed = self._list_has_changed
    
    def set_items (self, items):
        """S.set_items (...) -> None

        Sets the ListItemCollection attached to the ScrolledList.

        Raises a TypeError, if the passed argument does not inherit
        from the ListItemCollection class.
        """
        self.child.itemcollection = items
        self.child.itemcollection.list_changed = self._list_has_changed
        self.run_signal_handlers (SIG_LISTCHANGE)
    
    def set_spacing (self, spacing):
        """S.set_spacing (...) -> None

        Sets the spacing to place between the list items of the ScrolledList.

        The spacing value is the amount of pixels to place between the
        items of the ScrolledList.

        Raises a TypeError, if the passed argument is not a positive
        integer.
        """
        if (type (spacing) != int) or (spacing < 0):
            raise TypeError ("spacing must be a positive integer")
        self._spacing = spacing

    def set_selectionmode (self, mode):
        """S.set_selectionmode (...) -> None

        Sets the selection mode for the ScrolledList.

        The selection mode can be one of the SELECTION_TYPES list.
        SELECTION_NONE disables selecting any list item,
        SELECTION_SINGLE allows to select only one item from the list and 
        SELECTION_MULTIPLE allows to select multiple items from the list.

        Raises a ValueError, if the passed argument is not a value of
        the SELECTION_TYPES tuple.
        """
        if mode not in SELECTION_TYPES:
            raise ValueError ("mode must be a value from SELECTION_TYPES")
        self._selectionmode = mode

    def select (self, item):
        """S.select (...) -> None

        Selects a specific item of the ScrolledList.

        Dependant on the set selection mode selecting an item has
        specific side effects. If the selection mode is set to
        SELECTION_SINGLE, selecting an item causes any other item to
        become deselected. As a counterpart SELECTION_MULTIPLE causes
        the item to get selected while leaving any other item untouched.
        The method causes the SIG_SELECTCHANGE event to be emitted,
        whenever the selection changes.

        Raises a LookupError, if the passed argument could not be
        found in the items attribute.
        """
        if item not in self.items:
            raise LookupError ("item could not be found in list")
        if self.selectionmode == SELECTION_SINGLE:
            if not item.selected:
                for i in self.items:
                    if i.selected:
                        i.selected = False
                item.selected = True
                self.run_signal_handlers (SIG_SELECTCHANGE)
        elif self.selectionmode == SELECTION_MULTIPLE:
            if not item.selected:
                item.selected = True
                self.run_signal_handlers (SIG_SELECTCHANGE)
        elif self.selectionmode == SELECTION_NONE:
            # Do nothing here, maybe implement a specific event action
            # or s.th. like that...
            pass

    def deselect (self, item):
        """S.deselect (...) -> None
        
        Deselects the specified item in the ScrolledList.

        The method causes the SIG_SELECTCHANGE event to be emitted, when
        the selection changes.
        """
        for i in self.items:
            if (i == item) and i.selected:
                i.selected = False
                self.run_signal_handlers (SIG_SELECTCHANGE)
    
    def get_selected (self):
        """S.get_selected () -> list

        Returns a list cotaining the selected items.
        """
        l = []
        for item in self.items:
            if item.selected:
                l.append (item)
        return l
        # return [item for item in self.items if item.selected]

    def notify (self, event):
        """S.notify (...) -> None

        Notifies the ScrolledList about an event.
        """
        if not self.eventarea or not self.sensitive:
            return

        if event.signal == SIG_MOUSEDOWN:
            if self.eventarea.collidepoint (event.data.pos):
                if base.debug: print "ScrolledList.MOUSEDOWN"
                self.focus = True
                self.run_signal_handlers (SIG_MOUSEDOWN)
                if event.data.button == 1:
                    # Get the item and toggle the selection.
                    item = self.child.get_item_at_pos (event.data.pos)
                    if item:
                        if item.selected:
                            if pygame.key.get_mods () & \
                                   pygame.locals.KMOD_CTRL:
                                self.deselect (item)
                        else:
                            self.select (item)
                else:
                    # TODO: Mouse wheel scrolling - one item per time.
                    ScrolledWindow.notify (self, event)
        else:
            ScrolledWindow.notify (self, event)
        
    selectionmode = property (lambda self: self._selectionmode,
                              lambda self, var: self.set_selectionmode (var),
                              doc = "The selection mode for the ScrolledList.")
    spacing = property (lambda self: self._spacing,
                        lambda self, var: self.set_spacing (var),
                        doc = "Additional spacing to place between the items.")
    items = property (lambda self: self.child.itemcollection,
                      lambda self, var: self.set_items (var),
                      doc = "The item collection of the ScrolledList.")
