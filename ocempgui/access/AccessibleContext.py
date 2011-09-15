# $Id: AccessibleContext.py,v 1.2 2005/08/31 08:17:29 marcusva Exp $
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

"""Context class for accessibility aware objects. The class contains
needed methods and attributes to provide a basic set of information
about an object."""

class AccessibleContext (object):
    """AccessibleContext () -> AccessibleContext

    An accessibility information provider class.

    The AccessibleContext class provides a minimum set of information
    an accessible object must return. Those information include the
    object name and description, its current state and its relation to
    other objects like parents or children.

    Dependant on the object further information can be provided through
    the various AccessibleContext methods.

    TODO: example implementation

    Attributes:
    name        - The name of the object.
    description - Description of the object.
    """
    def __init__ (self):
        self.name = None
        self.description = None

    def get_accessible_action (self):
        """A.get_accessible_action () -> AccessibleAction

        Gets the AccessibleAction for the object.

        Gets the actions the object can perform. Those can be mouse
        clicks, keyboard actions and more.

        TODO: more details.
        """
        raise NotImplementedError
