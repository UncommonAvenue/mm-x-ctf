# $Id: __init__.py,v 1.26 2005/09/08 15:45:57 marcusva Exp $
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

"""Widget subsystem of OcempGUI. This module contains various classes
to create and use graphical user interface elements in a pygame
application. All provided classes are fully accessible and support
various attributes and methods to make them suitable for a GUI driven
program."""

# Initialize the widget subsystem.
import base
base.init ()

import Constants
from Style import Style

# Basic widgets.
from BaseWidget import BaseWidget
from Button import Button
from CheckButton import CheckButton
from Entry import Entry
from ImageButton import ImageButton
from Label import Label,ImageLabel
from ProgressBar import ProgressBar
from RadioButton import RadioButton
from Scale import HScale, VScale
from ScrollBar import HScrollBar, VScrollBar
from ToggleButton import ToggleButton
from Keysym import Keysym

# Container widgets.
from Bin import Bin
from ScrolledWindow import ScrolledWindow
from ScrolledList import ScrolledList
from Container import Container
from Table import Table
from Frame import HFrame, VFrame
from Window import Window
from DialogWindow import DialogWindow

# Event and render system.
from Renderer import Renderer, MenuRenderer

# Other modules.
# from ocempgui.widgets.components import *
