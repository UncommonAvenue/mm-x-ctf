# $Id: Constants.py,v 1.22 2005/09/13 08:36:11 marcusva Exp $
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

"""Constants used by the ocempgui widgets module."""

import pygame.locals

# State constants.
STATE_NORMAL =      0
STATE_ENTERED =     1
STATE_ACTIVE =      2
STATE_INSENSITIVE = 3
STATE_TYPES = (STATE_NORMAL, STATE_ENTERED, STATE_ACTIVE, STATE_INSENSITIVE)

# Signal constants, native.
SIG_KEYDOWN =   pygame.locals.KEYDOWN
SIG_KEYUP =     pygame.locals.KEYUP
SIG_MOUSEDOWN = pygame.locals.MOUSEBUTTONDOWN
SIG_MOUSEMOVE = pygame.locals.MOUSEMOTION
SIG_MOUSEUP =   pygame.locals.MOUSEBUTTONUP
SIG_TICK =      intern ("ticked")

# Signal constants, raised by the widgets.
SIG_ACTIVATE =     intern ("activate")
SIG_CLICKED =      intern ("clicked")
SIG_FOCUS =        intern ("focus")
SIG_INPUT =        intern ("input")
SIG_TOGGLED =      intern ("toggled")
SIG_VALCHANGE =    intern ("value-change")
SIG_SELECTCHANGE = intern ("selection-change")
SIG_LISTCHANGE =   intern ("list-change")

# Srolling behaviour widget widgets, which support it.
SCROLL_NEVER =  0
SCROLL_AUTO =   1
SCROLL_ALWAYS = 2
SCROLL_TYPES = (SCROLL_NEVER, SCROLL_AUTO, SCROLL_ALWAYS)

# Selection modes.
SELECTION_NONE =     0
SELECTION_SINGLE =   1
SELECTION_MULTIPLE = 2
SELECTION_TYPES = (SELECTION_NONE, SELECTION_SINGLE, SELECTION_MULTIPLE)

# Border types.
BORDER_NONE =       0
BORDER_FLAT =       1
BORDER_SUNKEN =     2
BORDER_RAISED =     3
BORDER_ETCHED_IN =  4
BORDER_ETCHED_OUT = 5
BORDER_TYPES = (BORDER_NONE, BORDER_FLAT, BORDER_SUNKEN, BORDER_RAISED,
                BORDER_ETCHED_IN, BORDER_ETCHED_OUT)

# Arrow types.
ARROW_UP =    0
ARROW_DOWN =  1
ARROW_LEFT =  2
ARROW_RIGHT = 3
ARROW_TYPES = (ARROW_UP, ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT)

# Alignment types.
ALIGN_NONE =   0
ALIGN_TOP =    1 << 0
ALIGN_BOTTOM = 1 << 1
ALIGN_LEFT =   1 << 2
ALIGN_RIGHT =  1 << 3
ALIGN_TYPES = (ALIGN_NONE, ALIGN_TOP, ALIGN_BOTTOM, ALIGN_LEFT, ALIGN_RIGHT)
