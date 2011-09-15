# $Id: ImageButton.py,v 1.26 2005/09/12 12:43:43 marcusva Exp $
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

"""A button widget, which can display an image."""

import pygame
from ocempgui.draw import Image
from Button import Button
from Constants import *
import base

class ImageButton (Button):
    """ImageButton (image) -> ImageButton

    Creates a new ImageButton widget with the supplied image.

    The ImageButton widget is able to display nearly any kind of
    image, while providing all the features of the Button widget.

    The image to display can be set with the 'picture' attribute or
    set_picture() method. The image can be either a file name from while
    the image should be loaded or a pygame.Surface object to display.

    button.image = './image.png'
    button.set_image (image_surface)

    If the displayed image is loaded from a file, its file path will be
    saved in the 'path' attribute. This also can be used to determine,
    whether the image was loaded from a file ('path' contains a file
    path) or not ('path' is None).

    Default action (invoked by activate()):
    See the Button class.
    
    Mnemonic action (invoked by activate_mnemonic()):
    See the Button class.
    
    Attributes:
    picture - A pygame.Surface of the set image.
    path    - The path of the set image (if it is loaded from a file).
    """
    def __init__ (self, image):
        Button.__init__ (self, "")
        self._picture = None
        self._path = None
        self.set_picture (image)

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
    
    def draw (self):
        """I.draw () -> Surface

        Draws the surface of the ImageButton and returns it.

        Creates the visible surface of the image button and returns it
        to the caller.
        """
        if self.child:
            self.child.update ()
        return base.GlobalStyle.draw_imagebutton (self)
    
    path = property (lambda self: self._path,
                     doc = "The file path of the image.")
    picture = property (lambda self: self._picture,
                        lambda self, var: self.set_picture (var),
                        doc = "The image to display on the ImageButton.")
