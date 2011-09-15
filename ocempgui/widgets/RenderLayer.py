# $Id: RenderLayer.py,v 1.12 2005/09/15 23:37:55 marcusva Exp $
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

# After spending hours of trying to understand the group/layer pitfalls, I
# found a layering renderer made by S.J. Brown with a PD license, which fits
# my needs.
# The original one can be found here:
# http://sjbrown.ezide.com/games/writing-games.html

"""A layered sprite renderer group based on RenderUpdates."""

from pygame.sprite import RenderUpdates
import base

class RenderLayer (RenderUpdates):
    """RenderLayer () -> RenderLayer

    Creates a pygame renderer based on the RenderUpdates renderer.

    This renderer supports a 3-dimensional effect by adding a z-Axis
    order using the 'depth' property of attached sprites.
    """
    def __init__ (self, sprite=()):
        super (RenderLayer, self).__init__ (sprite)
        self.sprite_depths = []
    
    def add_internal (self, sprite):
        """RenderLayer.add_internal (...) -> None
        """
        if sprite in self.spritedict:
            return
        RenderUpdates.add_internal (self, sprite)

        if sprite.depth == 0:
            self.sprite_depths.insert (0, sprite)
        else:
            success = False
            for i in range (len (self.sprite_depths) - 1):
                candidate = self.sprite_depths[i]
                if sprite.depth < candidate.depth:
                    self.sprite_depths.insert (i, sprite)
                    success = True
                    break
            if not success:
                self.sprite_depths.append (sprite)

    def add (self, *sprites):
        """RenderLayer.add (...) -> None
        """
        for sprite in sprites:
            has = self.spritedict.has_key
            if hasattr (sprite, '_spritegroup'):
                for sprite in sprite.sprites ():
                    if not has (sprite):
                        self.add_internal (sprite)
                        sprite.add_internal (self)
            else:
                try:
                    len (sprite) #see if its a sequence
                except (TypeError, AttributeError):
                    if not has (sprite):
                        self.add_internal (sprite)
                        sprite.add_internal (self)
                    else:
                        for sprite in sprite:
                            if not has (sprite):
                                self.add_internal (sprite)
                                sprite.add_internal (self)

    def add_top (self, sprite):
        """RenderLayer.add_top (...) -> None
        """
        pos = len (self.sprite_depths) - 1
        if pos >= 0:
            top = self.sprite_depths[pos]
            sprite.depth = top.depth + 1
        self.add (sprite)

    def remove_internal (self, sprite):
        """RenderLayer.remove_internal (...) -> None
        """
        RenderUpdates.remove_internal (self, sprite)
        self.sprite_depths.remove (sprite)

    def draw (self, surface):
        """R.draw (...) -> list

        Draws all sprites on the passed surface.

        Draws all sprites on the passed surface.
        """
        spritedict = self.spritedict
        dirty = self.lostsprites
        dirty_append = dirty.append
        self.lostsprites = []
        for sprite in self.sprite_depths:
            r = spritedict[sprite]
            newrect = surface.blit (sprite.image, sprite.rect)
            if r == 0:
                dirty_append (newrect)
            else:
                if newrect.colliderect (r):
                    dirty_append (newrect.union (r))
                else:
                    dirty_append (newrect)
                    dirty_append (r)
            spritedict[sprite] = newrect
        return dirty

    def update (self, *args):
        """RenderLayer.update (...) -> None
        """
        depth = 0
        dirty = False
        if args:
            k = self.spritedict.keys ()
            for sprite in k:
                depth = sprite.depth
                sprite.update (args)
                if depth != sprite.depth:
                    dirty = True
        else:
            k = self.spritedict.keys ()
            for sprite in k:
                depth = sprite.depth
                sprite.update ()
                if depth != sprite.depth:
                    dirty = True
        if dirty:
            if base.debug: print "Reordering sprites..."
            fn = lambda x, y: cmp (x.depth, y.depth)
            self.sprite_depths.sort (fn)

    def get_depths (self):
        """R.get_depths () -> list

        Gets a list with the depths of the attached widgets.
        """
        depths = []
        for sprite in self.spritedict.keys ():
            if sprite.depth not in depths:
                depths.append (sprite.depth)
        return depths
