# $Id: Table.py,v 1.19 2005/09/12 12:43:43 marcusva Exp $
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

"""Widget class, which places its children in a table grid"""

from Container import Container
from Constants import *
import base

class Table (Container):
    """Table (rows, cols) -> Table

    A container widget, which packs its children in a table like manner.

    The Table class is a layout container, which packs it children in a
    regular, table like manner and allows each widget to be aligned
    within its table cell. The table uses a 0-based (Null-based)
    indexing, which means, that if 4 rows are created, they can be
    accessed using a row value ranging from 0 to 3. The same applies to
    the columns.

    The Table provides read-only 'columns' and 'rows' attributes, which
    are the amount of columns and rows within that Table.
    
    totalr = table.rows
    totalc = table.columns

    To access the children of the Table the 'grid' attribute can be
    used. It is a dictionary containing the widgets as values. To access
    a widget, a tuple containing the row and column is used as the
    dictionary key.

    widget = table.grid[(0, 3)]
    widget = table.grid[(7, 0)]

    The above examples will get the widget located at the first row,
    fourth column (0, 3) and the eighth row, first column (7, 0).

    The layout for each widget within the table can be set individually
    using the set_align() method. Alignments can be combined, which
    means, that a ALIGN_TOP | ALIGN_LEFT would align the widget at the
    topleft corner of its cell.

    However, not every alignment make sense, so a ALIGN_TOP | ALIGN_BOTTOM
    would cause the widget to be placed at the bottom. The priority
    order for the alignment follows. The lower the value, the higher the
    priority.

    Alignment      Priority
    -----------------------
    ALIGN_BOTTOM      0
    ALIGN_TOP         1
    ALIGN_LEFT        0
    ALIGN_RIGHT       1
    ALIGN_NONE        1
    
    Default action (invoked by activate()):
    None
    
    Mnemonic action (invoked by activate_mnemonic()):
    None
    
    Attributes:
    columns  - The column amount of the Table.
    rows     - The row amount of the Table.
    grid     - Grid to hold the children of the Table.
    """
    def __init__ (self, rows, cols):
        Container.__init__ (self)
        if (type (rows) != int) or (type (cols) != int):
            raise TypeError ("Arguments must be positive integers")
        if (rows <= 0) or (cols <= 0):
            raise ValueError ("Arguments must be positive integers")
        self._cols = cols
        self._rows = rows

        # The grid for the children.
        self._grid = {}
        for i in xrange (self._rows):
            for j in xrange (self._cols):
                self._grid[(i, j)] = None # None means unused, !None is used.

        # Grid for the layout.
        self._layout = {}
        for i in xrange (self._rows):
            for j in xrange (self._cols):
                self._layout[(i, j)] = ALIGN_NONE

        # Width and height grids.
        self._colwidth = {}
        self._rowheight = {}
        for i in xrange (self._cols):
            self._colwidth[i] = 0
        for i in xrange (self._rows):
            self._rowheight[i] = 0

    def add_child (self, row, col, widget):
        """T.add_child (...) -> None

        Adds a widget into the cell located at (row, col) of the Table.

        Raises a ValueError, if the passed row and col arguments are not
        within the cell range of the Table.
        Raises an Exception, if the cell at the passed row and col
        coordinates is already occupied.
        """
        if (row, col) not in self.grid:
            raise ValueError ("Cell (%d, %d) out of range" % (row, col))
        if self.grid[(row, col)] != None:
            raise Exception ("Cell (%d, %d) already occupied" % (row, col))

        Container.add_child (self, widget)
        self.grid[(row, col)] = widget

    def remove_child (self, widget):
        """T.remove_widget (...) -> None

        Removes a widget from the Table.
        """
        Container.remove_child (self, widget)
        for i in xrange (self._rows):
            for j in xrange (self._cols):
                if self.grid[(i, j)] == widget:
                    self.grid[(i, j)] = None

    def set_focus (self, focus=True):
        """T.set_focus (focus=True) -> None

        Overrides the set_focus() behaviour for the Table.

        The Table class is not focusable by default. It is a layout
        class for other widgets, so it does not need to get the input
        focus and thus it will return false without doing anything.
        """
        return False

    def set_align (self, row, col, align=ALIGN_NONE):
        """T.set_align (...) -> None

        Sets the alignment for a specific cell.

        Raises a ValueError, if the passed row and col arguments are not
        within the rows and columns of the Table.
        """
        # TODO: Add check for the align types.
        if (row, col) not in self._layout:
            raise ValueError ("Cell (%d, %d) out of range" % (row, col))
        self._layout[(row, col)] = align
        self.dirty = True
    
    def destroy (self):
        """T.destroy () -> None

        Destroys the Table and all its children and shedules them for
        deletion by the renderer.
        """
        Container.destroy (self)
        del self._grid
        del self._layout
        del self._colwidth
        del self._rowheight
        
    def calculate_size (self):
        """T.calculate_size () -> int, int

        Calculates the size needed by the children.

        Calculates the size needed by the children and returns the
        resulting width and height.
        """
        for i in xrange (self._cols):
            self._colwidth[i] = 0
        for i in xrange (self._rows):
            self._rowheight[i] = 0

        # Fill the width and height grids with correct values.
        for row in xrange (self._rows):
            actheight = 0
            for col in xrange (self._cols):
                widget = self.grid[(row, col)]
                if not widget: # No child here.
                    continue
                widget.update ()
                cw = widget.width
                ch = widget.height
                if self._colwidth[col] < cw:
                    self._colwidth[col] = cw + self.spacing
                if actheight < (ch + self.spacing):
                    actheight = ch + self.spacing

            if self._rowheight[row] < actheight:
                self._rowheight[row] = actheight
        
        width = 0
        height = 0
        height = reduce (lambda x, y: x + y, self._rowheight.values (), height)
        height += 2 * self.padding - self.spacing
        width = reduce (lambda x, y: x + y, self._colwidth.values (), width)
        width += 2 * self.padding - self.spacing
        return width, height
    
    def dispose_widgets (self):
        """T._dispose_widgets (...) -> None

        Sets the children to their correct positions within the Table.
        """
        # Move all widgets to their correct position.
        x = self.position[0] + self.padding
        y = self.position[1] + self.padding
        for row in xrange (self._rows):
            for col in xrange (self._cols):
                widget = self.grid[(row, col)]
                if not widget: # no child here
                    x += self._colwidth[col]
                    continue
                # Dependant on the cell layout, move the widget to the
                # desired position.
                align = self._layout[(row, col)]
                # Default align is centered.
                posx = x + (self._colwidth[col] - widget.width -
                            self.spacing) / 2
                posy = y + (self._rowheight[row] - widget.height -
                            self.spacing) / 2
                if align & ALIGN_LEFT:
                    posx = x
                elif align & ALIGN_RIGHT:
                    posx = x + self._colwidth[col] - widget.width - \
                           self.spacing
                if align & ALIGN_TOP:
                    posy = y
                elif align & ALIGN_BOTTOM:
                    posy = y + self._rowheight[row] - widget.height - \
                           self.spacing
                widget.position = posx, posy
                widget.update ()
                x += self._colwidth[col]

            y += self._rowheight[row]
            x = self.position[0] + self.padding

    def draw (self):
        """T.draw () -> Surface

        Draws the Table surface and returns it.

        Creates the visible surface of the Table and returns it to the
        caller.
        """
        return base.GlobalStyle.draw_table (self)

    columns = property (lambda self: self._cols,
                        doc = "The column amount of the Table.")
    rows = property (lambda self: self._rows,
                     doc = "The row amount of the Table.")
    grid = property (lambda self: self._grid, doc = "The grid of the Table.")
