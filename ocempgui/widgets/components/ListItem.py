# $Id: ListItem.py,v 1.8 2005/09/17 09:07:04 marcusva Exp $
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

"""Objects suitable for the usage in a list."""
from ocempgui.access import Accessible
from ocempgui.widgets import base
from ocempgui.widgets.Constants import *

class ListItem (Accessible):
    """ListItem () -> ListItem

    Creates a new ListItem suitable for the usage in list or tree widgets.

    The ListItem class is an abstract class for list implementations. It
    is a nonactive sprite, which only provides the Accessible interfaces
    and drawing methods to be displayed in a list or tree-like widget.

    It is not able to react upon events nor has the flexibility and
    capabilities a widget inheriting from the BaseWidget class has, but
    provides a minimalistic set of methods to make it suitable for lists
    of nearly any type.

    The 'image' and 'rect' attributes emulate the pygame.sprite system
    to be conformous with the usual BaseWidget class. 'image' refers to
    the visible surface of the ListItem, which will be blitted on the
    display. 'rect' is a pygame.Rect object indicating the occupied area
    of the ListItem. Those attributes should NOT be modified by user
    code.

    ListItems support a 'style' attribute and get_style() method, which
    enable them to use different look than default one without the need
    to override their draw() method. The 'style' attribute of a ListItem
    usually defaults to a None value and can be set using the
    get_style() method. This causes the ListItem internals to setup the
    specific style for it and can be accessed through the 'style'
    attribute later on. A detailled documentation of the style can be
    found in the Style class.

    if not listitem.style:
        listitem.get_style () # Setup the style internals first.
    listitem.style['font']['size'] = 18
    listitem.get_style ()['font']['name'] = Arial

    The ListItem supports a selection state using the 'selected'
    attribute. This indicates, whether the ListItem was selected or not.

    listitem.selected = False
    listitem.selected = True
    
    TODO: collection

    Attributes:
    image      - The visible surface of the ListItem.
    rect       - The area occupied by the ListItem.
    style      - The style to use for drawing the ListItem.
    selected   - Indicates, whether the ListItem is currently selected.
    collection - The ListItemCollection, the ListItem is attached to.
    dirty      - Indicates, that the LsitItem needs to be updated.    
    """
    def __init__ (self):
        Accessible.__init__ (self)
        
        # Used for drawing.
        self._rect = None
        self._image = None
        self._style = None

        self._selected = False
        self._collection = None # TODO: implement list checks.

        self.dirty = True

    def has_changed (self):
        """S.has_changed () -> None

        Called, when the item has been changed and needs to be refreshed.

        This method will invoke the item_changed() notifier slot of the
        attached collection.
        """
        if (self.collection != None) and self.collection.item_changed:
            self.collection.item_changed (self)
    
    def _select (self, selected=True):
        """S._select (...) -> None

        Internal select handler, which causes the parent to update.
        """
        # TODO: implement update!
        if self._selected != selected:
            self.dirty = True
        self._selected = selected
        self.has_changed ()
    
    def set_collection (self, collection):
        """L.set_collection (...) -> None

        Sets the collection the ListItem is attached to.

        Sets the 'collection' attribute of the ListItem to the passed
        argument. and appends it to the collection if not already done.

        Raises an Exception, if the argument is already attached to a
        collection.
        """
        if collection:
            # TODO: make it type safe!
            if self._collection != None:
                raise Exception ("ListItem already attached to a collection")
            self._collection = collection
            # Add the item if it is not already in the collection.
            if self not in collection:
                collection.append (self)
        else:
            # Remove the item.
            if self._collection != None:
                collection = self._collection
                self._collection = None
                if self in collection:
                    collection.remove (self)
    
    def get_style (self):
        """L.get_style () -> Style
        
        Gets the style for the ListItem.

        Gets the style associated with the ListItem. If the ListItem had
        no style before, a new one will be created for it. More
        information about how a style looks like can be found in the
        Style class documentation.
        """
        if not self._style:
            # Create a new style from the base style class.
            self._style = base.GlobalStyle.copy_style (self.__class__)
        return self._style

    def draw (self, state):
        """L.draw (...) -> Surface

        Draws the ListItem surface and returns it

        Creates the visible surface of the ListItem and returns it to
        the caller.

        This method has to be implemented by inherited classes.
        """
        raise NotImplementedError

    def update (self, state):
        """L.update (...) -> None

        Updates the ListItem and refreshes its image and rect content.
        """
        if not self.dirty:
            return
        
        self._image = self.draw (state)
        self._rect = self._image.get_rect ()
    
    collection = property (lambda self: self._collection,
                           lambda self, var: self.set_collection (var),
                           doc = "The collection the ListItem is attached to.")
    selected = property (lambda self: self._selected,
                         lambda self, var: self._select (var),
                         doc = "The selection state of the ListItem.")
    rect = property (lambda self: self._rect,
                     doc = "The rectangle area occupied by the ListItem.")
    image = property (lambda self: self._image,
                      doc = "The visible surface of the ListItem.")
    style = property (lambda self: self._style,
                      doc = "The style of the ListItem.")

class TextListItem (ListItem):
    """TextListItem (text=None) -> TextListItem

    Creates a new TextListItem, which can display a portion of text.

    The TextListItem is able to display a short amount of text.

    The text to display on the TextListItem can be set through the
    'text' attribute or set_text() method. The TextListItem does not
    support any mnemonic keybindings.

    textlistitem.text = 'Item Text'
    textlistitem.set_text ('Another Text')

    Attributes:
    text - The text to display on the TextListItem.
    """
    def __init__ (self, text=None):
        ListItem.__init__ (self)
        self._text = None
        self.set_text (text)

    def set_text (self, text):
        """L.set_text (...) -> None
        
        Sets the text of the TextListItem to the passed argument.

        Sets the text to display on the TextListItem to the passed
        argument.

        Raises a TypeError, if the passed argument is not a string or
        unicode.
        """
        if text and type (text) not in (str, unicode):
            raise TypeError ("text must be a string or unicode")
        self._text = text
        self.dirty = True
        self.has_changed ()

    def draw (self, state):
        """T.draw (...) -> Surface

        Draws the TextListItem surface and returns it

        Creates the visible surface of the TextListItem and returns it
        to the caller.
        """
        text = self.text or ""
        return base.GlobalStyle.draw_string (text, state, self.__class__,
                                             self.style)
    
    text = property (lambda self: self._text,
                     lambda self, var: self.set_text (var),
                     doc = "The text to display on the TextListItem.")
