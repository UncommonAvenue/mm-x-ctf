# $Id: Label.py,v 1.20 2005/09/12 12:43:43 marcusva Exp $
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

"""A simple widget, which can display text."""
from ocempgui.draw import Image
from BaseWidget import BaseWidget
from Constants import *
import base

class Label (BaseWidget):
    """Label (text) -> Label

    A simple widget class, which can display text.

    The Label widget is able to display a short amount of text. It
    supports a mnemonic keybinding to activate other widgets.

    The text to display on the Label can be set through the 'text'
    attribute or set_text() method. To create a mnemonic within the
    text, a hash ('#') has to precede the the wanted character. A normal
    hash character can be created using two hashes ('##'). If more than
    one mnemonic identifier are placed in the text (like in '#Two
    #mnemonics', only the first one will be used, while all others will
    be ignored.
    
    label.text = '#Mnemonics' # Use the M character as mnemonic.
    label.text = 'Use ##1'    # Creates the text 'Use #1'.
    label.set_text ('No mnemonic here')
    label.set_text ('#Two #mnemonics') # Only the first '#' will be used.

    A widget can be bound to the mnemonic with the 'widget' attribute or
    set_widget() method. Whenever the mnemonic is activated, the
    connected widget will receive the focus.

    label.widget = widget
    label.set_widget (widget)

    The 'padding' attribute and set_padding() method are used to place a
    certain amount of pixels between the text and the outer edges of the
    Label.

    label.padding = 10
    label.set_padding (10)

    Default action (invoked by activate()):
    None
    
    Mnemonic action (invoked by activate_mnemonic()):
    The activate() method of the connected widget will be invoked.

    Attributes:
    text     - The text to display on the Label.
    widget   - The widget to focus, if the mnemonic is activated. (*)
    padding  - Additional padding between text and borders. Default is 2.
    mnemonic - A tuple with index location character of the mnemonic.

    (*) Only works as supposed using the Renderer class or an similar
    event manager, which takes advantage of the mnemonic functionality.
    """
    def __init__ (self, text):
        BaseWidget.__init__ (self)

        # Mnemonic identifiers in a tuple: (index, key).
        self._mnemonic = (-1, None)
        self._widget = None
        self.__active = False # Internal mnemonic handler.
        
        self._text = None
        self.set_text (text)
        
        self._padding = 2

    def set_text (self, text):
        """L.set_text (...) -> None
        
        Sets the text of the Label to the passed argument.

        Sets the text of the Label to the passed argument. If the text
        contains a hash ('#') character, then the character, the hash
        precedes, will be used as a mnemonic (see also set_widget()).
        Any other single hash character will be dropped and ignored.

        To create a normal hash character to display, use two '##'.

        Raises a TypeError, if the passed argument is not a string or
        unicode.
        """
        if type (text) not in (str, unicode):
            raise TypeError ("text must be a string or unicode")
        text = self._get_mnemonic (text)
        self._text = text
        self.dirty = True

    def _get_mnemonic (self, text):
        """L._get_mnemonic (...) -> text

        Sets the mnemonic position (if any).

        Sets the internal mnemonic position to first position with a
        single '#'.
        """
        self._mnemonic = (-1, None)
        # TODO: this could lead into trouble :-).
        text = text.replace ("##", "<hash>")
        text = text.replace ("#", "<mnemonic>")
        text = text.replace ("<hash>", "#")
        index = text.find ("<mnemonic>")
        text = text.replace ("<mnemonic>", "")
        if index != -1:
            key = unicode (text[index].lower ())
            self._mnemonic = (index, key)
        return text

    def activate (self):
        """L.activate () -> None

        Activates the Label.

        Note: Labels can not be activated by default, thus this method
        does not do anything.
        """
        pass
    
    def activate_mnemonic (self, mnemonic):
        """L.activate_mnemonic (...) -> bool

        Activates the mnemonic widget of the Label.

        Checks, if the Label uses the passed mnemonic, invokes the
        activate() method of its mnemonic widget on a successful check
        and returns True, otherwise False.
        """
        if self.widget and (self._mnemonic[1] == mnemonic):
            try:
                # If the widget does not have an activate() method or
                # raises an exception, just give it the input focus.
                self.widget.activate ()
            except NotImplementedError:
                self.widget.focus = True
            return True
        return False
    
    def set_widget (self, widget):
        """L.set_widget (...) -> None

        Sets the widget to activate, if the mnemonic key gets pressed.

        Note: This method only works as supposed using a render loop,
        which supports the Renderer class specification.

        Raises a TypeError, if the passed argument does not inherit
        from the BaseWidget class.
        """
        if not isinstance (widget, BaseWidget):
            raise TypeError ("widget must inherit from BaseWidget")
        self._widget = widget

    def set_padding (self, padding):
        """L.set_padding (...) -> None

        Sets the padding between the edges and text of the Label.

        The padding value is the amount of pixels to place between the
        edges of the Label and the displayed text.

        Raises a TypeError, if the passed argument is not a positive
        integer.

        Note: If the 'size' attribute is set, it can influence the
        visible space between the text and the edges. That does not
        mean, that any padding is set.
        """
        if (type (padding) != int) or (padding < 0):
            raise TypeError ("padding must be a positive integer")
        self._padding = padding
        self.dirty = True

    def set_focus (self, focus=True):
        """L.set_focus (...) -> bool

        Overrides the default widget input focus.

        Labels cannot be focused by default, thus this method always
        returns False and does not do anything.
        """
        return False
    
    def draw (self):
        """L.draw () -> Surface

        Draws the Label surface and returns it.

        Creates the visible surface of the Label and returns it to the
        caller.
        """
        return base.GlobalStyle.draw_label (self)
    
    text = property (lambda self: self._text,
                     lambda self, var: self.set_text (var),
                     doc = "The text to display on the Label.")
    widget = property (lambda self: self._widget,
                       lambda self, var: self.set_widget (var),
                       doc = "The connected widget for the mnemonic key.")
    padding = property (lambda self: self._padding,
                        lambda self, var: self.set_padding (var),
                        doc = "Additional padding between text and borders.")
    mnemonic = property (lambda self: self._mnemonic,
                         doc = "The index and character of the mnemonic.")

class ImageLabel(Label):
    def __init__ (self, text, image):
        BaseWidget.__init__ (self)

        # Mnemonic identifiers in a tuple: (index, key).
        self._mnemonic = (-1, None)
        self._widget = None
        self.__active = False # Internal mnemonic handler.
        
        self._text = None
        self.set_text (text)
        self._picture = None
        self._path = None
        self.set_picture (image)
        
        self._padding = 2

    def set_picture (self, image):
        """I.set_picture (...) -> None

        Sets the image to be displayed on the ImageButton.

        The image can be either a valid pygame.Surface object or the
        path to an image file. If the argument is a file, the 'path'
        attribute will be set to the file path, otherwise it will be
        None.

        Raises a TypeError, if the passed argument is not a string,
        unicode or pygame.Surface.
        """
        if image:
            if type (image) in (str, unicode):
                self._path = image
                self._picture = Image.load_image (image)
            elif isinstance (image, pygame.Surface):
                self._path = None
                self._picture = image
            else:
                raise TypeError ("image must be a string or unicode or a " \
                                 "pygame.Surface")
        else:
            self._path = None
            self._picture = None
        self.dirty = True
        
    def draw(self):
        return base.GlobalStyle.draw_imagelabel(self)
