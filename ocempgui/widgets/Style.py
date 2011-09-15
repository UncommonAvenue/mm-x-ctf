# $Id: Style.py,v 1.26 2005/09/15 23:37:55 marcusva Exp $
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

"""Style class for widgets."""

import os.path, copy, pygame
from ocempgui.draw import Draw, String, Image
from Constants import *
import Numeric
import base

class Style (object):
    """Style () -> Style

    Style class for drawing objects.

    Style definitions: Any object can register its own style definition
    and request it using the correct key. A button widget for example,
    could register its style definition this way:

    Style.styles['button'] = { .... }

    Any other button widget then can use this style, so their look is
    all the same. It is however possible to override instance specific
    styles easily, if the style types are copied and modified.

    mystyle = style.styles['button'].copy ()
    mystyle['bgcolor'][...] = ...

    Besides this way of ensuring specific styles it is also possible to
    pass an own type dictionary to the drawing methods of the Style
    class in order to get a surface, which can be shown on the screen
    then:

    own_style = { ... }
    surface = style.draw_rect (width, height, own_style)

    The BaseWidget class offers a get_style() method, which will copy
    the style of the widget class to the specific widget. Thus you can
    safely modify the instance specific style for the widget without
    touching the style for all widgets of that class.

    The style dictionaries registered within the 'styles' dictionary of
    the Style class need to match some prerequisites to be useful. On
    the one hand they need to incorporate specific key-value pairs,
    which can be evaluated by the various drawing functions, on the
    other they need to have some specific key-value pairs, which are
    evaluated by the Style class.

    The following lists will give an overview about the requirements the
    object style dictionaries to match, so that the basic Style class
    can work as supposed.

    Style entries:
    --------------
    The registered style dictionaries for the objects need to contain
    key-value pairs required by the functions of the referenced
    modules. The following key-value pairs are needed to create the
    surfaces:

    bgcolor = { STATE_TYPE : color, ... }

    The background color to use for the widget surface.
    
    fgcolor = { STATE_TYPE : color, ... }

    The foreground color to use for the widget. This is also the text
    color for most widgets, which will display text.
    
    lightcolor = { STATE_TYPE : color, ... }
    darkcolor = { STATE_TYPE : color, ... }

    Used to create shadow border effects on several widgets (see also
    the draw_border() method). The color values should be a bit brighter
    or darker than the bgcolor values.

    image = { STATE_TYPE : string }

    Pixmap files to use instead of the background color. If the file is
    not supplied or cannot be loaded, the respective bgcolor value is
    used.
    NOTE: The image key-value pair handling is not implemented yet.
    
    font = { 'name' : string, 'size' : integer, 'alias' : integer }

    Widgets, which support the display of text, make use of this
    key-value pair. The 'name' key denotes the font name ('Helvetica')
    or the full path to a font file ('Helvetica.ttf').
    'size' is the font size to use. 'alias' is interpreted as boolean value
    for antialiasing.

    shadow = integer

    The size of the 3D border effect for a widget.

    IMPORTANT: It is important to know, that the Style class only
    supports a two-level hierarchy for styles. Especially the
    copy_style() method is not aware of style entries of more than two
    levels. This means, that a dictionary in a style dictionary is
    possible (as done in the 'font' or the various color style entries),
    but more complex style encapsulations are unlikely to work
    correctly.
    Some legal examples for user defined style entries:

    'ownentry' = 99                        # One level
    'ownentry' = { 'foo' : 1, 'bar' : 2 }  # Two levels: level1[level2]

    This one however is not guaranteed to behave correctly and thus
    should be avoided:

    'ownentry' = { 'foo' : { 'bar' : 1, 'baz' : 2 }, 'morefoo' : { ... }}

    Style files:
    ------------
    A style file is a key-value pair association of style entries for
    widgets. It can be loaded and used by the Style.load() method to set
    specific themes and styles for the widgets. The style files use a
    python syntax and contain key-value pairs of style information for
    the specific widgets. The general syntax looks like follows:

    widgetclassname = { style_entry : { value } }

    An example style file entry for the Button widget class can look
    like the following:

    button = { 'bgcolor' : { STATE_NORMAL : (200, 100, 0) },
               'fgcolor' : { STATE_NORMAL : (255, 0, 0) },
               'shadow' : 5 }

    The above example will set the bgcolor[STATE_NORMAL] color style
    entry for the button widget class to (200, 100, 0), the
    fgcolor[STATE_NORMAL] color style entry to (255, 0, 0) and the
    'shadow' value for the border size to 5.
    Any other value of the style will remain untouched. Loading a style
    while running an application does not have any effect on widgets
    
    * with own styles set via the BaseWidget.get_style() method,
    * already drawn widgets using the default style.
    
    The latter ones need to be refreshed via the set_dirty()/update()
    methods explicitly to make use of the new style.

    Attributes:
    styles  - A dictionary with the style definitions of various elements.
    """

    __slots__ = [ "styles", "_private" ]
    
    def __init__ (self):
        # Initialize the default style.
        self.styles = {
            "default" : { "bgcolor" : { STATE_NORMAL : (234, 228, 223),
                                        STATE_ENTERED : (239, 236, 231),
                                        STATE_ACTIVE : (205, 200, 194),
                                        STATE_INSENSITIVE : (234, 228, 223) },
                          "fgcolor" : { STATE_NORMAL : (0, 0, 0),
                                        STATE_ENTERED : (0, 0, 0),
                                        STATE_ACTIVE : (0, 0, 0),
                                        STATE_INSENSITIVE : (204, 192, 192) },
                          "lightcolor" : { STATE_NORMAL : (245, 245, 245),
                                           STATE_ENTERED : (245, 245, 245),
                                           STATE_ACTIVE : (30, 30, 30),
                                           STATE_INSENSITIVE : (240, 240, 240)
                                           },
                          "darkcolor" : { STATE_NORMAL : (30, 30, 30),
                                          STATE_ENTERED : (30, 30, 30),
                                          STATE_ACTIVE : (245, 245, 245),
                                          STATE_INSENSITIVE : (204, 192, 192)
                                          },
                          "image" : { STATE_NORMAL : None,
                                      STATE_ENTERED : None,
                                      STATE_ACTIVE : None,
                                      STATE_INSENSITIVE : None },
                          "font" : { "name" : None,
                                     "size" : 16,
                                     "alias" : True },
                          "shadow" : 2 }
            }

        self._private = {}
        
        # Used by draw_check().
        self._private["check_size"] = 14
        
        # Load the default style.
        self.load (os.path.join (os.path.dirname (__file__), "default.rc"))

    def get_style (self, cls):
        """S.get_style (...) -> dict
        
	Returns the style for a specific widget class.

        Returns the style for a specific widget class. If no matching
        entry was found, the method searches for the next upper
        entry of the class's __mro__. If it reaches the end of the
        __mro__ list without finding a matching entry, a copy of the
        default style will be created and added to the styles dictionary
        by using the missing key.
        """
        classes = [c.__name__.lower () for c in cls.__mro__]
        for name in classes:
            if name in self.styles:
                return self.styles[name]
        return self.styles.setdefault (cls.__name__.lower (), {})
        
    def get_style_entry (self, cls, style, key, subkey=None):
        """S.get_style_entry (...) -> value

        Gets a style entry from the style dictionary.

        Gets a entry from the style dictionary. If the entry could not
        be found, the method searches for the next upper entry of the
        __mro__. If it reaches the end of the __mro__ list without
        finding a matching entry, it will try to return the entry from
        the 'default' style dictionary.
        """
        deeper = subkey != None
        if key in style:
            if deeper:
                if subkey in style[key]:
                    return style[key][subkey]
            else:
                return style[key]

        classes = [c.__name__.lower () for c in cls.__mro__]
        for name in classes:
            if name in self.styles:
                style = self.styles[name]
                # Found a higher level class style, check it.
                if key in style:
                    if deeper:
                        if subkey in style[key]:
                            return style[key][subkey]
                    else:
                        return style[key]

        # None found, refer to the default.
        if deeper:
            return self.styles["default"][key][subkey]
        return self.styles["default"][key]
    
    def copy_style (self, cls):
        """S.copy_style (...) -> dict

        Creates a plain copy of a specific style.

        Due to the cascading ability of the Style class, an existing
        style will be filled with the entries of the 'default' style
        dictionary which do not exist in it.
        """
        style = copy.deepcopy (self.get_style (cls))
        default = self.styles["default"]
        for key in default:
            if key not in style:
                style[key] = copy.deepcopy (default[key])
            else:
                sub = default[key]
                for subkey in default[key]:
                    style[key].setdefault (subkey, sub[subkey])
        return style
    
    def load (self, file):
        """S.load (...) -> None

        Loads style definitions from a file.

        Loads style definitions from a file and adds them to the
        'styles' attribute. Already set values in this dictionary will
        be overwritten.
        """
        glob_dict = {}
        loc_dict = {}
        execfile (file, glob_dict, loc_dict)
        for key in loc_dict:
            # Skip the Constants import directive.
            if key == "Constants": 
                continue

            # Search the style or create a new one from scratch.
            entry = self.styles.setdefault (key, {})
            # Look up all entries of our style keys and add them to the
            # style.
            widget = loc_dict[key]
            for key in widget:
                if type (widget[key]) == dict:
                    entry[key] = {}
                    for subkey in widget[key]:
                        entry[key][subkey] = widget[key][subkey]
                else:
                    entry[key] = widget[key]

    def create_style_dict (self):
        """Style.create_style_dict () -> dict

	Creates a new style dictionary.

        Creates a new unfilled style dictionary with the most necessary
        entries needed by the Style class specifications.
        """
        style = {
            "bgcolor" : { STATE_NORMAL : (0, 0, 0),
                          STATE_ENTERED : (0, 0, 0),
                          STATE_ACTIVE : (0, 0, 0),
                          STATE_INSENSITIVE : (0, 0, 0) },
            "fgcolor" : { STATE_NORMAL : (0, 0, 0),
                          STATE_ENTERED : (0, 0, 0),
                          STATE_ACTIVE : (0, 0, 0),
                          STATE_INSENSITIVE : (0, 0, 0) },
            "lightcolor" : { STATE_NORMAL : (0, 0, 0),
                             STATE_ENTERED : (0, 0, 0),
                             STATE_ACTIVE : (0, 0, 0),
                             STATE_INSENSITIVE : (0, 0, 0) },
            "darkcolor" : { STATE_NORMAL : (0, 0, 0),
                            STATE_ENTERED : (0, 0, 0),
                            STATE_ACTIVE : (0, 0, 0),
                            STATE_INSENSITIVE : (0, 0, 0) },
            "image" : { STATE_NORMAL : None,
                        STATE_ENTERED : None,
                        STATE_ACTIVE : None,
                        STATE_INSENSITIVE : None },
            "font" : { "name" : None,
                       "size" : 0,
                       "alias" : False },
            "shadow" : 0
            }
        return style

    def draw_rect (self, width, height, state, cls=None, style=None):
        """S.draw_rect (...) -> Surface

        Creates a rectangle surface based on the style information.

        The rectangle will have the passed width and height and will be
        filled with the 'bgcolor'[state] value of the passed style.
        If no style is passed, the method will try to retrieve a style
        using the get_style() method.
        """
        if not style:
            style = self.get_style (cls)
        color = self.get_style_entry (cls, style, "bgcolor", state)
        return Draw.draw_rect (width, height, color)

    def get_border_size (self, cls=None, style=None, bordertype=BORDER_FLAT):
        """S.get_border_size (...) -> int

        Gets the border size for a specific border type and style.

        Gets the size of a border in pixels for the specific border type
        and style. for BORDER_NONE the value will be 0 by
        default. BORDER_FLAT will always return a size of 1.
        The sizes of other border types depend on the passed style.

        If no style is passed, the method will try to retrieve a style
        using the get_style() method.

        Raises a ValueError, if the passed bordertype argument is
        not a value of the BORDER_TYPES tuple.
        """
        if bordertype not in BORDER_TYPES:
            raise ValueError ("bordertype must be a value from BORDER_TYPES")

        if not style:
            style = self.get_style (cls)

        if bordertype == BORDER_FLAT:
            return 1
        elif bordertype in (BORDER_SUNKEN, BORDER_RAISED):
            return self.get_style_entry (cls, style, "shadow")
        elif bordertype in (BORDER_ETCHED_IN, BORDER_ETCHED_OUT):
            return self.get_style_entry (cls, style, "shadow") * 2
        return 0
    
    def draw_border (self, surface, state, cls=None, style=None,
                     bordertype=BORDER_FLAT, padding=0, space=0):
        """S.draw_border (...) -> Surface

        Draws a border on the passed using a specific border type.

        Dependant on the border type, this method will draw a rectangle
        border on the passed surface.
        The 'padding' argument indicates the amount of pixels to leave
        between the outer edges of the surface and the border.
        'space' denotes, how many pixels will be left between each
        border pixel before drawing the next one. A value of 0 thus
        causes the method to draw a solid border while other values will
        draw dashed borders.
        The BORDER_RAISED, BORDER_SUNKEN, BORDER_ETCHED_IN and
        BORDER_ETCHED_OUT border types use the 'lightcolor', 'darkcolor'
        and 'shadow' style entries for drawing, BORDER_FLAT uses the
        'fgcolor' entry.
        
        If no style is passed, the method will try to retrieve a style
        using the get_style() method.
        
        Raises a ValueError, if the passed bordertype argument is
        not a value of the BORDER_TYPES tuple.
        """
        if bordertype not in BORDER_TYPES:
            raise ValueError ("bordertype must be a value from BORDER_TYPES")
        # Do nothing in case, that the border type is none.
        if bordertype == BORDER_NONE:
            return surface 

        if not style:
            style = self.get_style (cls)

        # The spacing for the lines. space == 0 actually means a soldi line,
        # spacing == 1 a dashed one with 1px spaces, etc.
        # Add one pixel for the slicing later on. 
        space += 1
        
        # Maybe pixel3d should be used here, but it does not support 24
        # bit color depths.
        array = pygame.surfarray.array3d (surface)

        # Create the area, the border should surround.
        # We will use the passed padding for it.
        r = surface.get_rect ()
        r.x += padding
        r.y += padding
        r.width -= padding
        r.height -= padding

        # Dependant on the border style, we will care about the used
        # colors. 3D effect such as sunken or raised make use of the
        # light/darkcolor style keys, the flat one uses the fgcolor. If
        # it is a 3D effect, we are going to use the shadow key to
        # determine, how many lines the distinction shall have.
        # 
        # The drawing is done as follows:
        # * First fill the upper row of the (n,m) matrix with the given
        #   color and color only every wanted pixel.
        # * The color the bottom row of the matrix in the same way.
        # * The left column will be colored as well.
        # * The same again with the right column.
        
        if bordertype == BORDER_FLAT:
            color = self.get_style_entry (cls, style, "fgcolor", state)
            array[r.x:r.width:space, r.y] = color
            array[r.x:r.width:space, r.height - 1]= color
            array[r.x, r.y:r.height:space] = color
            array[r.width - 1, r.y:r.height:space]= color

        elif bordertype in (BORDER_SUNKEN, BORDER_RAISED):
            shadow = self.get_style_entry (cls, style, "shadow")
            if shadow < 1:
                return surface # No shadow wanted.
            color1 = self.get_style_entry (cls, style, "lightcolor", state)
            color2 = self.get_style_entry (cls, style, "darkcolor", state)
            if bordertype == BORDER_SUNKEN:
                color1, color2 = color2, color1

            # By default we will create bevel edges, for which the
            # topleft colors take the most place. Thus the bottomleft
            # array slices will be reduced continously.
            for i in xrange (shadow):
                array[r.x + i:r.width - i:space, r.y + i] = color1
                array[r.x + i:r.width - i:space, r.height - (i + 1)] = color2
                array[r.x + i, r.y + i:r.height - i:space] = color1
                array[r.width - (i + 1), r.y + i+1:r.height - i:space] = color2

        elif bordertype == BORDER_ETCHED_IN:
            shadow = self.get_style_entry (cls, style, "shadow")
            if shadow < 1:
                return surface # No shadow wanted.
            color1 = self.get_style_entry (cls, style, "lightcolor", state)
            color2 = self.get_style_entry (cls, style, "darkcolor", state)
            if bordertype == BORDER_ETCHED_OUT:
                color1, color2 = color2, color1
            s = shadow
            # First (inner) rectangle.
            array[r.x + s:r.width:space, r.y + s:r.y + 2 * s] = color1
            array[r.x + s:r.width:space,r.height - s:r.height] = color1
            array[r.x + s:r.x + 2 * s, r.y + s:r.height:space] = color1
            array[r.width - s:r.width, r.y + s:r.height:space] = color1
            # Second (outer) rectangle.
            array[r.x:r.width - s:space, r.y:r.y + s] = color2
            array[r.x:r.width - s:space, r.height - 2*s:r.height - s] = color2
            array[r.x:r.x + s, r.y:r.height - s:space] = color2
            array[r.width - 2*s:r.width - s, r.y:r.height - s:space] = color2

        # Create the surface and return it to the caller.
        return pygame.surfarray.make_surface (array)

    def draw_slider (self, width, height, state, cls=None, style=None):
        """S.draw_slider (...) -> Surface

        Creates a rectangle surface with a grip look.

        TODO: At the moment, this method creates a simple rectangle
        surface with raised border. In future versions it will _really_
        create a surface with a grip look (hopefully).
        """
        if not style:
            style = self.get_style (cls)

        # Create the surface.
        surface = self.draw_rect (width, height, state, cls, style)
        surface = self.draw_border (surface, state, cls, style, BORDER_RAISED)
        return surface
    
    def draw_string (self, text, state, cls=None, style=None):
        """S.draw_string (...) -> Surface

        Creates a string surface based on the style information.

        Creates a transparent string surface from the provided text
        based on the style information. The method makes use of the
        'font' style entry to determine the font and size and uses the
        'fgcolor' style entry for the color.

        If no style is passed, the method will try to retrieve a style
        using the get_style() method.
        """
        if not style:
            style = self.get_style (cls)
        name = self.get_style_entry (cls, style, "font", "name")
        size = self.get_style_entry (cls, style, "font", "size")
        alias = self.get_style_entry (cls, style, "font", "alias")
        color = self.get_style_entry (cls, style, "fgcolor", state)
        return String.draw_string (text, name, size, alias, color)
    
    def draw_string_with_mnemonic (self, text, state, mnemonic, cls=None,
                                   style=None):
        """S.draw_string_with_mnemonic (...) -> Surface

        Creates a string surface with an additional underline.

        This method basically does the same as the draw_string()
        method, but additionally underlines the character specified with
        the 'mnemonic' index argument using the 'fgcolor' style entry..

        If no style is passed, the method will try to retrieve a style
        using the get_style() method.

        TODO: This should be made more flexible to support different
        mnemonic looks.
        """
        if not style:
            style = self.get_style (cls)

        name = self.get_style_entry (cls, style, "font", "name")
        size = self.get_style_entry (cls, style, "font", "size")
        alias = self.get_style_entry (cls, style, "font", "alias")
        fgcolor = self.get_style_entry (cls, style, "fgcolor", state)

        font = String.create_font (name, size)
        surface = String.draw_string (text, name, size, alias, fgcolor)

        left = font.size (text[:mnemonic])
        right = font.size (text[mnemonic + 1:])

        height = surface.get_rect ().height - 2
        width = surface.get_rect ().width
        Draw.draw_line (surface, fgcolor, (left[0], height),
                        (width - right[0], height), 1)
        return surface
    
    def draw_arrow (self, surface, arrowtype, state, cls=None, style=None):
        """S.draw_arrow (...) -> Surface

        Draws an arrow on a surface.
        
        Draws an arrow with on a surface using the passed arrowtype as
        arrow direction. The method uses a third of the surface width
        (or height for ARROW_TOP/ARROW_DOWN) as arrow width and places
        it on the center of the surface. It also uses the 'fgcolor'
        style entry as arrow color.

        If no style is passed, the method will try to retrieve a style
        using the get_style() method.
        
        Raises a ValueError, if the passed arrowtype argument is not a
        value of the ARROW_TYPES tuple.
        """
        if arrowtype not in ARROW_TYPES:
            raise TypeError ("arrowtype must be a value of ARROW_TYPES")
        
        if not style:
            style = self.get_style (cls)

        color = self.get_style_entry (cls, style, "fgcolor", state)
        rect = surface.get_rect ()
        array = pygame.surfarray.array3d (surface)

        if arrowtype in (ARROW_LEFT, ARROW_RIGHT):
            arrow_width = rect.width / 3
            center = rect.centery
            if center % 2 == 0:
                center -= 1
            if arrowtype == ARROW_LEFT:
                for i in xrange (arrow_width):
                    col = arrow_width + i
                    array[col:col + arrow_width - i:1, center + i] = color
                    array[col:col + arrow_width - i:1, center - i] = color
            elif arrowtype == ARROW_RIGHT:
                for i in xrange (arrow_width):
                    col = rect.width - arrow_width - i - 1
                    array[col:col - arrow_width + i:-1, center + i] = color
                    array[col:col - arrow_width + i:-1, center - i] = color

        elif arrowtype in (ARROW_UP, ARROW_DOWN):
            arrow_height = rect.height / 3
            center = rect.centerx
            if center % 2 == 0:
                center -= 1

            if arrowtype == ARROW_UP:
                for i in xrange (arrow_height):
                    row = arrow_height + i
                    array[center + i, row:row + arrow_height - i:1] = color
                    array[center - i, row:row + arrow_height - i:1] = color
            elif arrowtype == ARROW_DOWN:
                for i in xrange (arrow_height):
                    row = rect.height - arrow_height - i - 1
                    array[center + i, row:row - arrow_height + i:-1] = color
                    array[center - i, row:row - arrow_height + i:-1] = color
        
        surface = pygame.surfarray.make_surface (array)
        return surface
    
    def draw_check (self, checked, state, cls=None, style=None):
        """S.draw_check (...) -> Surface

        Creates a surface with a check box.

        Creates a surface with check box using a width and height of 14
        pixels. The method uses a sunken border effect and makes use of
        the 'lightcolor' and 'darkcolor' style entries for the border.
        Dependant on the passed 'state' argument, the method will either
        use fixed color values of

        (255, 255, 255) for the background and
        (0, 0, 0) for the check,

        which is only drawn, if the 'checked' argument evaluates to
        True. If the 'state' argument is set to STATE_INSENSITIVE the
        'bgcolor' and 'fgcolor' style entries are used instead.
        
        If no style is passed, the method will try to retrieve a style
        using the get_style() method.
        """
        if not style:
            style = self.get_style (cls)

        surface = self.draw_rect (self._private["check_size"],
                                  self._private["check_size"], state, cls,
                                  style)

        # Some colors we need.
        bg = (255, 255, 255) # Default background color.
        check = (0, 0, 0)    # Check color.
        sh = (150, 150, 150) # Check shadow to make it look smooth.

        array = pygame.surfarray.array3d (surface)
        # Draw the borders and fill the rest.
        dark = self.get_style_entry (cls, style, "darkcolor",state)
        light = self.get_style_entry (cls, style, "lightcolor", state)
        array[0:2, 0:14] = dark
        array[0:14, 0:2] = dark
        array[12:14, 0:14] = light
        array[0:14, 12:14] = light
        array[0, 12] = dark
        array[12, 0] = dark

        if state == STATE_INSENSITIVE:
            array[2:12, 2:12] = self.get_style_entry (cls, style, "bgcolor",
                                                      state)
            check = self.get_style_entry (cls, style, "fgcolor", state)
            sh = check
        else:
            array[2:12, 2:12] = bg
        
        if checked:
            # Place a check into the drawn box by direct pixel
            # manipulation.
            # TODO: provide a handy matrix for this, so it can be merged
            # and changed quickly.
            #
            #                           11  13
            #     0 1 2 3 4 5 6 7 8 9 10  12  
            #    -----------------------------
            # 0  |* * * * * * * * * * * * * *|
            # 1  |* * * * * * * * * * * * * *|
            # 2  |* * 0 0 0 0 0 0 0 0 0 0 * *|
            # 3  |* * 0 0 0 0 0 0 0 0 # # * *|
            # 4  |* * 0 0 0 0 0 0 0 # # # * *|
            # 5  |* * 0 0 0 0 0 0 # # # 0 * *|
            # 6  |* * 0 0 # # 0 # # # 0 0 * *|
            # 7  |* * 0 # # # 0 # # 0 0 0 * *|
            # 8  |* * 0 0 # # # # # 0 0 0 * *|
            # 9  |* * 0 0 0 # # # 0 0 0 0 * *|
            # 10 |* * 0 0 0 0 0 # 0 0 0 0 * *|
            # 11 |* * 0 0 0 0 0 0 0 0 0 0 * *|
            # 12 |* * * * * * * * * * * * * *|
            # 13 |* * * * * * * * * * * * * *|
            #    -----------------------------
            # * = border shadow
            # 0 = unset
            # # = set with a specific color.
            #
            array[3, 7] = sh
            array[4, 6] = sh
            array[4, 7:9] = check
            array[5, 6] = sh
            array[5, 7:9] = check
            array[5, 9] = sh
            array[6, 7] = sh
            array[6, 8:10] = check
            array[7, 6] = sh
            array[7, 7:11] = check
            array[8, 5:9] = check
            array[9, 4:7] = check
            array[10, 3:6] = check
            array[11, 3:5] = sh
            
        surface = pygame.surfarray.make_surface (array)
        return surface

    def draw_radio (self, checked, state, cls=None, style=None):
        """S.draw_radio (...) -> Surface

        Creates a surface with a radio check box.

        Creates a surface with radio check box using a width and height
        of 14 pixels. The method uses a sunken border effect and makes
        use of the 'lightcolor' and 'darkcolor' style entries for the
        border.  Dependant on the passed 'state' argument, the method
        will either use fixed color values of

        (255, 255, 255) for the background and 
        (0, 0, 0) for the check,

        which is only drawn, if the 'checked' argument evaluates to
        True. If the 'state' argument is set to STATE_INSENSITIVE the
        'bgcolor' and 'fgcolor' style entries are used instead.
        
        If no style is passed, the method will try to retrieve a style
        using the get_style() method.
        """
        if not style:
            style = self.get_style (cls)
        
        surface = self.draw_rect (self._private["check_size"],
                                  self._private["check_size"], state, cls,
                                  style)

        # We need some colors for the radio check.
        sh1 = (0, 0, 0)        # Border topleft.
        sh2 = (150, 150, 150)  # Border shadow top- and bottomleft.
        sh3 = (255, 255, 255)  # Outer border shadow bottomleft.
        bg = (255, 255, 255)   # Background color for the check.
        check = (0, 0, 0)      # Color of the radio check.
        if state == STATE_INSENSITIVE:
            bg = self.get_style_entry (cls, style, "bgcolor", state)
            check = self.get_style_entry (cls, style, "fgcolor", state)
            sh1 = check
            sh2 = self.get_style_entry (cls, style, "fgcolor", state)
            sh3 = (240, 240, 240)

        # The complete radio check will be drawn by manipulating pixels
        # of the box.
        # TODO: provide a handy matrix for this, so it can be merged
        # and changed quickly.
        #                           11  13
        #     0 1 2 3 4 5 6 7 8 9 10  12  
        #    -----------------------------
        # 0  |x x x x x x x x x x x x x x|
        # 1  |x x x x x * * * * x x x x x|
        # 2  |x x x * * s s s s s * x x x|
        # 3  |x x * s s 0 0 0 0 0 s * x x|
        # 4  |x x * s 0 0 0 0 0 0 0 * x x|
        # 5  |x * s 0 0 0 # # # 0 0 0 * x|
        # 6  |x * s 0 0 # # # # # 0 0 * 8|
        # 7  |x * s 0 0 # # # # # 0 0 * 8|
        # 8  |x * s 0 0 # # # # # 0 0 * 8|
        # 9  |x x s 0 0 0 # # # 0 0 0 * 8|
        # 10 |x x * s 0 0 0 0 0 0 0 * 8 x|
        # 11 |x x x * * 0 0 0 0 0 * * 8 x|
        # 12 |x x x x x * * * * * 8 8 x x|
        # 13 |x x x x x x 8 8 8 8 x x x x|
        #    -----------------------------
        # x = default background color
        # * = border shadow (sh2)
        # s = topleft border (sh1)
        # 0 = background color (bg)
        # 8 = border shadow 2 (sh3)
        # # = check color (check)
        #
        array = pygame.surfarray.array3d (surface)
        array[1, 5:9] = sh2
        array[2, 3:5] = sh2
        array[2, 5:10] = sh1
        array[2, 10] = sh2
        array[3:5, 2] = sh2
        array[3, 3:5] = sh1
        array[3:12, 5:10] = bg
        array[3, 10] = sh1
        array[3:5, 11] = sh2
        array[4, 3] = sh1
        array[4:11, 4] = bg
        array[4:11, 10] = bg
        array[5:9, 1] = sh2
        array[5:10, 2] = sh1
        array[5:10, 3] = bg
        array[5:10, 11] = bg
        array[5:10, 12] = sh2
        array[6:10, 13] = sh3
        array[10, 2] = sh2
        array[10, 3] = sh1
        array[10:12, 11] = sh2
        array[10:12, 12] = sh3
        array[11, 3:5] = sh2
        array[11, 10] = sh2
        array[12, 5:10] = sh2
        array[12, 10:12] = sh3
        array[13, 6:10] = sh3

        if checked:
            array[5:10, 6:9] = check
            array[6:9, 5] = check
            array[6:9, 9] = check

        surface = pygame.surfarray.make_surface (array)
        return surface

    def create_caption (self, width, title=None, state=STATE_NORMAL, cls=None,
                        style=None):
        """S.draw_caption (...) -> Surface

        Creates and a caption bar suitable for Window objects.

        Creates a rectangle surface with a flat border and the passed
        'title' text argument. The method uses a fixed color value of
        (124, 153, 173) for the surface.

        The passed 'width' will be ignored, if the size of the title
        text exceeds it. Instead the width of the title text plus an
        additional spacing of 4 pixels will be used.
        The height of the surface relies on the title text height plus
        an additional spacing of 4 pixels.

        If no style is passed, the method will try to retrieve a style
        using the get_style() method.
        """
        if not title:
            title = ""
        if not style:
            style = self.get_style (cls)

        # Create the window title.
        surface_text = self.draw_string (title, state, cls, style)
        rect_text = surface_text.get_rect ()

        # Add two pixels for the border and 2 extra ones for spacing.
        cap_height = rect_text.height + 4
        if width < rect_text.width + 4:
            width = rect_text.width + 4
        
        # Create the complete surface.
        surface = Draw.draw_rect (width, cap_height, (124, 153, 173))
        surface = self.draw_border (surface, state, cls, style, BORDER_FLAT)
        surface.blit (surface_text, (2, 2))
        
        return surface

    def draw_caret (self, surface, x, y, thickness, state, cls=None,
                    style=None):
        """S.draw_caret (...) -> None

        Draws a caret line on a surface.

        Draws a vertical caret line onto the passed surface. The
        position of the caret will be set using the 'x' argument. The
        length of the caret line can be adjusted using the 'y' argument.
        The thickness of the caret line is set by the 'thickness'
        argument. This method makes use of the 'fgcolor' style entry for
        the color of the caret line.

        If no style is passed, the method will try to retrieve a style
        using the get_style() method.
        """
        if not style:
            style = self.get_style (cls)
        rect = surface.get_rect ()
        ax = (rect.topleft[0] + x, rect.topleft[1] + y)
        bx = (rect.bottomleft[0] + x, rect.bottomleft[1] - y)
        Draw.draw_line (surface,
                        self.get_style_entry (cls, style, "fgcolor", state),
                        ax, bx, thickness)

    def draw_label (self, label):
        """S.draw_label (...) -> Surface

        Creates the surface for the passed Label widget.
        """
        cls = label.__class__

        rtext = None
        if label.mnemonic[0] != -1:
            rtext = self.draw_string_with_mnemonic (label.text, label.state,
                                                    label.mnemonic[0], cls,
                                                    label.style)
        else:
            rtext = self.draw_string (label.text, label.state, cls,
                                      label.style)
        
        rect = rtext.get_rect ()
        width = rect.width + 2 * label.padding
        height = rect.height + 2 * label.padding

        # Guarantee size.
        if width < label.size[0]:
            width = label.size[0]
        if height < label.size[1]:
            height = label.size[1]
	font = pygame.font.Font(None, 24)
        #surface = self.draw_rect (width, height, label.state, cls, label.style)
	img = font.render(label.text ,1, (255,255,255,255))
	surface = pygame.Surface ((width, height))
	#img.center = surface.get_rect ().center
        surface.blit (img, img.get_rect())
	#return rtext
        return surface

    def draw_button (self, button):
        """S.draw_button (...) -> Surface

        Creates the surface for the passed Button widget.
        """
	surface = 0
	if button.focus:
		font = pygame.font.Font(None, 26)
		img = font.render(button.child.text ,1, (200,150,55,255))
		surface = pygame.Surface ((img.get_rect().width, img.get_rect().height))
		surface.blit (img, img.get_rect())
		surface.set_colorkey((0,0,0,0))
		return surface
	font = pygame.font.Font(None, 24)
	img = font.render(button.child.text ,1, (255,255,255,255))
	if surface:
		rect = img.get_rect()
		rect.center = surface.get_rect().center
	else:
		surface = pygame.Surface ((img.get_rect().width, img.get_rect().height))
		rect = img.get_rect()
	surface.blit (img, img.get_rect())
	surface.set_colorkey((0,0,0,0))
	return surface
   
    def draw_checkbutton (self, button):
        """S.draw_checkbutton (...) -> Surface

        Creates the surface for the passed CheckButton widget.
        """
        cls = button.__class__

        # Create the absolute sizes of the surface, including the
        # padding.
        width = 2 * button.padding
        height = 2 * button.padding
        if button.child:
            width += button.child.width
            height += button.child.height

        # Create check box
        check = self.draw_check (button.active, button.state, cls,
                                 button.style)
        rect_check = check.get_rect ()

        # The layout looks like:
        #  ----------------
        #  | X | child    |
        #  ----------------
        # Check   Child
        # Thus we have to add a specific spacing between the child and the
        # check. By default we will use a fixed value of 4.
        width += rect_check.width + 4
        if height < rect_check.height:
            # Do not forget to add the padding!
            height = rect_check.height + 2 * button.padding

        # Guarantee size.
        if width < button.size[0]:
            width = button.size[0]
        if height < button.size[1]:
            height = button.size[1]

        # The surface on which both components will be placed.
        surface = self.draw_rect (width, height, button.state, cls,
                                  button.style)
        rect_surface = surface.get_rect ()
        
        if button.child:
            # Draw a dashed border around the child, if the CheckButton
            # has focus.
            dash = button.child.image
            if button.focus:
                dash = self.draw_border (button.child.image, button.state, cls,
                                         button.style, BORDER_FLAT, space=1)

            # Place the child right besides the check, respect the
            # specific padding between the check and child, normal
            # padding _and_ the dashed border.
            button.child.rect.x = rect_check.width + button.padding + 4
            button.child.rect.centery = rect_surface.centery
            surface.blit (dash, button.child.rect)

        # Place the check at the right position.
        rect_check.x = rect_surface.x + button.padding
        rect_check.centery = rect_surface.centery
        surface.blit (check, rect_check)

        return surface

    def draw_entry (self, entry):
        """S.draw_entry (...) -> Surface

        Creates the surface for the passed Entry widget.
        """
        cls = entry.__class__
        border = self.get_border_size (cls, entry.style, BORDER_SUNKEN)

        # Peek the style so we can calculate the font.
        st = entry.style or self.get_style (cls)
        fn = self.get_style_entry (cls, st, "font", "name")
        sz = self.get_style_entry (cls, st, "font", "size")

        font = String.create_font (fn, sz)
        rtext = self.draw_string (entry.text, entry.state, cls, entry.style)

        height = font.get_height () + 2 * (entry.padding + border)
        width = entry.size[0]

        # Guarantee size.
        if height < entry.size[1]:
            height = entry.size[1]

        # The 'inner' surface, which we will use for blitting the text.
        sf_text = self.draw_rect (width - 2 * (entry.padding + border),
                                  height - 2 * (entry.padding + border),
                                  entry.state, cls, entry.style)

        # Main surface.
        surface = self.draw_rect (width, height, entry.state, cls, entry.style)
        surface = self.draw_border (surface, entry.state, cls, entry.style,
                                    BORDER_SUNKEN)

        # We will 'move' the text by adjusting the overhead and blitting
        # with negative values.
        blit_pos = 0
        caret_pos = font.size (entry.text[:entry.caret])[0]
        rect_sftext = sf_text.get_rect ()
        if caret_pos > rect_sftext.width:
            blit_pos = rect_sftext.width - caret_pos - 2

        sf_text.blit (rtext, (blit_pos, 0))

        # Draw caret.
        if entry.focus and entry.caret_visible:
            self.draw_caret (sf_text, blit_pos + caret_pos, 1, 2, entry.state,
                             cls, entry.style)

        rect_sftext.center = surface.get_rect ().center
        surface.blit (sf_text, rect_sftext)

        return surface
    def draw_imagelabel(self, label):
        """S.draw_imagelabel (...) -> Surface

        Creates the surface for the passed ImageLabel widget.
        """
        cls = label.__class__

        rtext = None
        if label.mnemonic[0] != -1:
            rtext = self.draw_string_with_mnemonic (label.text, label.state,
                                                    label.mnemonic[0], cls,
                                                    label.style)
        else:
            rtext = self.draw_string (label.text, label.state, cls,
                                      label.style)
        rect = rtext.get_rect ()
        if label._picture:
            re = label._picture.get_rect ()
            width = re.width
            height = re.height

        # Guarantee size.
        if width < label.size[0]:
            width = label.size[0]
        if height < label.size[1]:
            height = label.size[1]

        surface = self.draw_rect (width, height, label.state, cls, label.style)
        rect_sf = surface.get_rect ()
        if label._picture:
            re = label._picture.get_rect()
            re.center = rect_sf.center
            surface.blit(label._picture, re)
        rect.center = surface.get_rect ().center
        surface.blit (rtext, rect)
        return surface
    
    def draw_imagebutton (self, button):
        """S.draw_imagebutton (button) -> Surface

        Creates the surface for the passed ImageButton widget.
        """
        cls = button.__class__
        border1 = self.get_border_size (cls, button.style, BORDER_RAISED)
        border2 = self.get_border_size (cls, button.style, BORDER_FLAT)

        width = 2 * (button.padding + border1 + border2)
        height = 2 * (button.padding + border1 + border2)
        if button.child:
            width += button.child.width
            height += button.child.height

        if button.picture:
            re = button.picture.get_rect ()
            width += re.width
            if button.child:
                 width += 2 # Add two px to leave between child and image.
            if height < re.height:
                height = re.height + 2 * (button.padding + border1 + border2)

        # Guarantee size.
        if width < button.size[0]:
            width = button.size[0]
        if height < button.size[1]:
            height = button.size[1]
        
        surface = self.draw_rect (width, height, button.state, cls,
                                  button.style)
        surface = self.draw_border (surface, button.state, cls, button.style,
                                    BORDER_RAISED)
        rect_sf = surface.get_rect ()

        if button.picture:
            re = button.picture.get_rect ()
            if button.child:
                re.x = rect_sf.centerx - \
                       (re.width + button.child.rect.width + 2) / 2
                re.centery = rect_sf.centery
            else:
                re.center = rect_sf.center
            surface.blit (button.picture, re)

        # Draw a dashed border around the image, if the button has
        # focus.
        if button.focus:
            surface = self.draw_border (surface, button.state, cls,
                                        button.style, BORDER_FLAT,
                                        border1 + border2, 1)
        if button.child:
            if button.picture:
                re = button.picture.get_rect ()
                button.child.rect.right = rect_sf.centerx + \
                                         (re.width + button.child.rect.width \
                                          + 2) / 2
                button.child.rect.centery = rect_sf.centery
            else:
                button.child.rect.center = rect_sf.center
            surface.blit (button.child.image, button.child.rect)
        return surface

    def draw_radiobutton (self, button):
        """S.draw_radiobutton (button) -> Surface

        Creates the surface for the passed RadioButton widget.
        """
        cls = button.__class__
        
        # Create the absolute sizes of the surface, including the
        # padding and.
        width = 2 * button.padding
        height = 2 * button.padding
        if button.child:
            width += button.child.width
            height += button.child.height

        # Create check box
        check = self.draw_radio (button.active, button.state, cls,
                                 button.style)
        rect_check = check.get_rect ()

        # The layout looks like:
        #  ----------------
        #  | X | child    |
        #  ----------------
        # Check   Child
        # Thus we have to add a specific spacing between the child and the
        # check. By default we will use a fixed value of 4.
        width += rect_check.width + 4
        if height < rect_check.height:
            # Do not forget to add the padding!
            height = rect_check.height + 2 * button.padding

        # Guarantee size.
        if width < button.size[0]:
            width = button.size[0]
        if height < button.size[1]:
            height = button.size[1]

        # The surface on which both components will be placed.
        surface = self.draw_rect (width, height, button.state, cls,
                                  button.style)
        rect_surface = surface.get_rect ()

        if button.child:
            # Draw a dashed border around the child, if the CheckButton
            # has focus.
            dash = button.child.image
            if button.focus:
                dash = self.draw_border (button.child.image, button.state, cls,
                                         button.style, BORDER_FLAT, space=1)

            # Place the child right besides the check, respect the
            # specific padding between the check and child, normal
            # padding _and_ the dashed border.
            button.child.rect.x = rect_check.width + button.padding + 4
            button.child.rect.centery = rect_surface.centery
            surface.blit (dash, button.child.rect)

        # Place the check at the right position.
        rect_check.x = rect_surface.x + button.padding
        rect_check.centery = rect_surface.centery
        surface.blit (check, rect_check)

        return surface

    def draw_progressbar (self, bar):
        """S.draw.progressbar (...) -> Surface

        Creates the surface for the passed ProgressBar widget.
        """
        cls = bar.__class__
        border = self.get_border_size (cls, bar.style, BORDER_SUNKEN)
        st = bar.style or self.get_style (cls)

        # Guarantee size.
        width = bar.size[0]
        height = bar.size[1]
        
        surface = self.draw_rect (width, height, bar.state, cls, bar.style)

        # Status area.
        width -= 2 * border
        height -= 2 * border
        width = int (width * bar.value / 100)

        # Draw the progress.
        sf_progress = Draw.draw_rect (width, height, self.get_style_entry \
                                      (cls, st, "barcolor", bar.state))
        surface.blit (sf_progress, (border, border))

        # Draw and blit the text, if any.
        if bar.text:
            sf_text = self.draw_string (bar.text, bar.state, cls, bar.style)
            re = sf_text.get_rect ()
            re.center = surface.get_rect().center
            surface.blit (sf_text, re)

        surface = self.draw_border (surface, bar.state, cls, bar.style,
                                    BORDER_SUNKEN)
        return surface

    def draw_frame (self, frame):
        """S.draw_frame (...) -> Surface

        Creates the surface for the passed Frame widget.
        """
        cls = frame.__class__
        border = self.get_border_size (cls, frame.style, frame.border)

        width, height = frame.calculate_size ()
        if cls.__name__ == "HFrame":
            frame.dispose_widgets (height)
        elif cls.__name__ == "VFrame":
            frame.dispose_widgets (width)

        # Guarantee correct sizes.
        if width < frame.size[0]:
            width = frame.size[0]
        if height < frame.size[1]:
            height = frame.size[1]

        surface = self.draw_rect (width, height, frame.state, cls, frame.style)

        # Border area.
        pos = 0
        if frame.widget:
            height -= frame.widget.height / 2
            pos = frame.widget.height / 2
        surface_border = self.draw_rect (width, height, frame.state, cls,
                                         frame.style)
        surface_border = self.draw_border (surface_border, frame.state, cls,
                                           frame.style, frame.border)
        surface.blit (surface_border, (0, pos))

        # Draw the children.
        if frame.widget:
            surface.blit (frame.widget.image, (border + frame.padding, 0))
        for widget in frame.children:
            surface.blit (widget.image,
                          (widget.position[0] - frame.position[0],
                           widget.position[1] - frame.position[1]))
        return surface

    def draw_table (self, table):
        """S.draw_table (...) -> Surface

        Creates the surface for the passed Table widget.
        """
        cls = table.__class__

        width, height = table.calculate_size ()
        table.dispose_widgets ()
        surface = self.draw_rect (width, height, table.state, cls, table.style)

        # Draw all children.
        for widget in table.children:
            surface.blit (widget.image,
                          (widget.position[0] - table.position[0],
                           widget.position[1] - table.position[1]))
        return surface

    def draw_scale (self, scale):
        """S.draw_scale (...) -> Surface

        Creates the surface for the passed Scale widget.
        """
        cls = scale.__class__
        border1 = self.get_border_size (cls, scale.style, BORDER_SUNKEN)
        border2 = self.get_border_size (cls, scale.style, BORDER_FLAT)

        # Use a default value for the slider, if not set in the style.
        if cls.__name__ == "VScale":
            slider = (16, 30)
        try:
            st = scale.style or self.get_style (cls)
            slider = self.get_style_entry (cls, st, "slider")
        except KeyError: pass

        width = scale.size[0]
        if width < slider[0]:
            width = slider[0]
        height = scale.size[1]
        if height < slider[1]:
            height = slider[1]

        # Main surface to draw on. We do not want to have any resizing,
        # thus we are doing this in two steps.
        surface = self.draw_rect (width, height, scale.state, cls, scale.style)
        surface = self.draw_border (surface, scale.state, cls, scale.style,
                                    BORDER_SUNKEN)
        rect = surface.get_rect ()

        sf_knob = self.draw_slider (slider[0], slider[1], scale.state, cls,
                                    scale.style)
        if scale.focus:
            sf_knob = self.draw_border (sf_knob, scale.state, cls, scale.style,
                                        BORDER_FLAT, border1 + border2, 1)
        rect_knob = sf_knob.get_rect ()
        if cls.__name__ == "HScale":
            rect_knob.centerx = scale.get_coords_from_value ()
            rect_knob.centery = rect.centery
        elif cls.__name__ == "VScale":
            rect_knob.centerx = rect.centerx
            rect_knob.centery = scale.get_coords_from_value ()
        surface.blit (sf_knob, rect_knob)

        return surface

    def draw_scrollbar (self, scrollbar):
        """S.draw_scrollbar (...) -> Surface

        Creates the surface for the passed ScrollBar widget.
        """
        cls = scrollbar.__class__
        border = self.get_border_size (cls, scrollbar.style, BORDER_SUNKEN)

        # We use a temporary state here, so that just the buttons will
        # have the typical sunken effect.
        tmp_state = scrollbar.state
        if scrollbar.state == STATE_ACTIVE:
            tmp_state = STATE_NORMAL

        # Guarantee size.
        width = scrollbar.size[0]
        height = scrollbar.size[1]

        surface = self.draw_rect (width, height, tmp_state, cls,
                                  scrollbar.style)
        surface = self.draw_border (surface, tmp_state, cls, scrollbar.style,
                                    BORDER_SUNKEN)
        rect = surface.get_rect ()
        
        # Create both buttons.
        bborder = self.get_border_size (cls, scrollbar.style, BORDER_RAISED)
        bwidth = 0
        ar_width = 0
        if cls.__name__ == "HScrollBar":
            bwidth = height - 2 * border
            ar_width = bwidth - bborder
        elif cls.__name__ == "VScrollBar":
            bwidth = width - 2 * border
            ar_width = bwidth - bborder
        
        bstate = tmp_state
        if scrollbar.button_dec:
            bstate = STATE_ACTIVE
        button1 = self.draw_rect (bwidth, bwidth, bstate, cls, scrollbar.style)
        button1 = self.draw_border (button1, bstate, cls, scrollbar.style,
                                    BORDER_RAISED)
        rect_button1 = button1.get_rect ()

        # Draw the arrow.
        arrow = self.draw_rect (ar_width, ar_width, bstate, cls,
                                scrollbar.style)
        if cls.__name__ == "HScrollBar":
            arrow = self.draw_arrow (button1, ARROW_LEFT, bstate, cls,
                                     scrollbar.style)
        elif cls.__name__ == "VScrollBar":
            arrow = self.draw_arrow (button1, ARROW_UP, bstate, cls,
                                     scrollbar.style)
        re = arrow.get_rect ()
        re.center = rect_button1.center
        button1.blit (arrow, re)

        if cls.__name__ == "HScrollBar":
            rect_button1.x = border
            rect_button1.centery = rect.centery
            surface.blit (button1, rect_button1)
        elif cls.__name__ == "VScrollBar":
            rect_button1.y = border
            rect_button1.centerx = rect.centerx
            surface.blit (button1, rect_button1)
        
        bstate = tmp_state
        if scrollbar.button_inc:
            bstate = STATE_ACTIVE
        button2 = self.draw_rect (bwidth, bwidth, bstate, cls, scrollbar.style)
        button2 = self.draw_border (button2, bstate, cls, scrollbar.style,
                                    BORDER_RAISED)
        rect_button2 = button2.get_rect ()

        # Draw the arrow.
        arrow = self.draw_rect (ar_width, ar_width, bstate, cls,
                                scrollbar.style)

        if cls.__name__ == "HScrollBar":
            arrow = self.draw_arrow (button2, ARROW_RIGHT, bstate, cls,
                                     scrollbar.style)
        elif cls.__name__ == "VScrollBar":
            arrow = self.draw_arrow (button2, ARROW_DOWN, bstate, cls,
                                     scrollbar.style)
        re = arrow.get_rect ()
        re.center = rect_button2.center
        button2.blit (arrow, re)

        if cls.__name__ == "HScrollBar":
            rect_button2.x = rect.width - bwidth - border
            rect_button2.centery = rect.centery
            surface.blit (button2, rect_button2)
        elif cls.__name__ == "VScrollBar":
            rect_button2.y = rect.height - bwidth - border
            rect_button2.centerx = rect.centerx
            surface.blit (button2, rect_button2)

        # Create the slider.
        slider_size = scrollbar.get_slider_size ()
        if slider_size > 0:
            if cls.__name__ == "HScrollBar":
                sl = self.draw_slider (slider_size, bwidth, tmp_state, cls,
                                       scrollbar.style)
                rect = sl.get_rect ()
                rect.centerx = scrollbar.get_coords_from_value ()
                rect.centery = surface.get_rect ().centery
            elif cls.__name__ == "VScrollBar":
                sl = self.draw_slider (bwidth, slider_size, tmp_state, cls,
                                       scrollbar.style)
                rect = sl.get_rect ()
                rect.centery = scrollbar.get_coords_from_value ()
                rect.centerx = surface.get_rect ().centerx
            surface.blit (sl, rect)
        return surface

    def draw_scrolledwindow (self, window):
        """S.draw_scrolledwindow (...) -> Surface

        Creates the Surface for the passed ScrolledWindow widget.
        """
        cls = window.__class__
        border = self.get_border_size (cls, window.style, BORDER_SUNKEN)

        # Guarantee correct sizes.
        width = window.size[0]
        height = window.size[1]

        if window.child:
            window.child.update ()
        vscroll, hscroll = window.update_scrollbars (border)

        surface = self.draw_rect (width, height, window.state, cls,
                                  window.style)

        # Create the surface for the child.
        width, height = window.get_visible_area ()

        # The get_visible_area() method removes the drawn border!
        width += 2 * border
        height += 2 * border
        surface_w = self.draw_rect (width, height, window.state, cls,
                                    window.style)

        # Set the widget at the correct coordinates.
        if window.child:
            rect = window.child.rect
            rect.x = - window.hscrollbar.value + border + window.padding
            rect.y = - window.vscrollbar.value + border + window.padding
            window.child.position = rect.x + window.position[0], \
                                    window.position[1] + rect.y
            window.child.dirty = True # Enforce recreation.
            window.child.update ()
            surface_w.blit (window.child.image, rect)
        surface_w = self.draw_border (surface_w, window.state, cls,
                                       window.style, BORDER_SUNKEN)

        if hscroll:
            window.hscrollbar.position = window.position[0], \
                                         window.position[1] + height
            window.hscrollbar.update ()
            surface.blit (window.hscrollbar.image, (0, height))
        if vscroll:
            window.vscrollbar.position = window.position[0] + width, \
                                         window.position[1]
            window.vscrollbar.update ()
            surface.blit (window.vscrollbar.image, (width, 0))

        # Readjust the event area of the child.
        window.recalculate_child_rect ()
        surface.blit (surface_w, (0, 0))

        return surface
