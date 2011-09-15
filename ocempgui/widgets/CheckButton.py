# $Id: CheckButton.py,v 1.8 2005/09/12 12:43:43 marcusva Exp $
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

"""A button widget with a check box."""

from ToggleButton import ToggleButton
from Constants import *
import base

class CheckButton (ToggleButton):
    """CheckButton (text) -> CheckButton

    Creates a new CheckButton widget with the supplied text.

    The CheckButton widget has the same functionality as the
    ToggleButton widget, but uses a different look. It places a small
    check box besides its Label, which displays the state of the
    CheckButton.
    
    Default action (invoked by activate()):
    See the ToggleButton class.
    
    Mnemonic action (invoked by activate_mnemonic()):
    See the ToggleButton class.
    """
    def __init__ (self, text):
        ToggleButton.__init__ (self, text)

    def draw (self):
        """C.draw () -> Surface

        Draws the CheckButton surface and returns it.

        Creates the visible surface of the CheckButton and returns it to
        the caller.
        """
        if self.child:
            self.child.update ()
        return base.GlobalStyle.draw_checkbutton (self)
