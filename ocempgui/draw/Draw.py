# $Id: Draw.py,v 1.9 2005/09/02 20:52:08 marcusva Exp $
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

"""Simple drawing operations for geometric primitives."""

import pygame

def draw_line (surface, color, a, b, width=1):
    """draw_line (...) -> Rect

    Draws a line on a surface.

    The 'color' argument needs to match the pygame color style. 'a' and
    'b' are sequences of the x- and y-coordinate on the surface and
    'width' denotes the width of the line in pixels.  The return value
    is the bounding box of the affected area.
    
    The following example would draw a horizontal black line on the
    specified surface (the surface must be big enough):

    draw_line (surface, (0, 0, 0), (5, 5), (5, 10))
    
    Note: This function is just a wrapper around pygame.draw.line() and
    thus all documentation about it can be applied to this function,
    too.
    """
    return pygame.draw.line (surface, color, a, b, width)

def draw_triangle (surface, color, a, b, c, width=0):
    """draw_triangle (...) -> Rect

    Draws a triangle with the vertices a, b, c on a surface.

    The 'color' argument needs to match the pygame color style. 'a',
    'b', 'c' are sequences of the x- and y-coordinates of the three
    vertices on th surface. 'width' denotes the width of lines in pixels
    or, if set to 0, fills the triangle with the passed color. The
    return value is the bounding box of the affected area.

    The following example would draw a white, filled triangle on the
    specified surface:

    draw_triangle (surface, (255, 255, 255), (5, 1), (1, 5), (10, 5))
    
    Note: This function is a wrapper around pygame.draw.polygon() with a
    fixed three point list and thus all documentation about it can be
    applied to this function, too.
    """
    return pygame.draw.polygon (surface, color, [a, b, c], width)

def draw_rect (width, height, color=None):
    """draw_rect (...) -> Surface

    Creates a rectangle surface.
    
    Creates a pygame.Surface with the size of 'width' and 'height' and
    fills it with the given background color 'color', which needs to
    match the pygame color style. If no color is provided, the surface
    will be left unfilled.

    The following example creates a red square surface:

    draw_rect (10, 10, (255, 0, 0))

    Note: This method calls pygame.Surface() to create the surface, but
    does not provide any values for the flags, depth or masks, which can
    be applied in the pygame.Surface() call. It uses the default values
    given by pygame. If this is not wanted, it is recommended to
    override this function, where necessary.
    """
    surface = pygame.Surface ((width, height))
    if color:
        surface.fill (color)
    return surface
