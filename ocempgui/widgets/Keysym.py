from BaseWidget import BaseWidget
from Entry import Entry
from Editable import Editable
from Constants import *
import base

class Keysym(Entry):
    """Keysym()-> Keysym

    Creates a Keysym entry for recording getting a key

    Keysym is an Entry that holds only one key at a time
    """

    def __init__(self):
        Entry.__init__(self, "")
        self.value = 0

    def notify (self, event):
        """E.notify (...) -> None

        Notifies the Editable about an event.
        """
        if not self.sensitive:
            return

        if event.signal == SIG_MOUSEDOWN:
            if self.eventarea.collidepoint (event.data.pos):
                self.run_signal_handlers (SIG_MOUSEDOWN)
                if (event.data.button == 1):
                    self.activate ()

        # The next few events are only available, if the entry is focused.
        if self.focus:
            # Blinking caret.
            # TODO: TICK events are not the best idea to use here.
            if event.signal == SIG_TICK:
                if self._counter == 50:
                    self._caret_visible = not self._caret_visible
                    self._counter = 0
                    self.dirty = True
                self._counter += 1
            
            elif event.signal == SIG_KEYDOWN:
                if base.debug: print "Editable.KEYDOWN"
                self.run_signal_handlers (SIG_KEYDOWN, event.data)
                self._input (event.data)
                self._counter = 0

        BaseWidget.notify (self, event)

    def _input (self, event):
        """E._input (...) -> None

        Receives the SIG_KEYDOWN events and updates the text.
        """
        if event.key == pygame.locals.K_ESCAPE:
            if self.editable:
                self._text = self._temp # Undo text input.
                # TODO: Maybe SIG_INPUT should be raise only, if there
                # were changes in the text.
                if base.debug: print "Editable.INPUT"
                self.run_signal_handlers (SIG_INPUT)
                self._caret = 0 # Reset caret.
            self.focus = False

        elif event.key == pygame.locals.K_RETURN:
            if self.editable:
                if base.debug: print "Editable.INPUT"
                # TODO: Maybe SIG_INPUT should be raise only, if there
                # were changed in the text.
                self.run_signal_handlers (SIG_INPUT)
                self._caret = 0 # Reset caret.
            self.focus = False

        # Go the start (home) of the text.
        elif event.key == pygame.locals.K_HOME:
            self._caret = 0

        # Go to the end (end) of the text.
        elif event.key == pygame.locals.K_END:
            self._caret = len (self._text)

        # The next statements directly influence the text, thus we
        # have to check, if it is editable or not.
        elif self.editable:
            # Delete at the position (delete).
            if event.key == pygame.locals.K_DELETE:
                if self._caret < len (self._text):
                    self._text = self._text[:self._caret] + \
                                 self._text[self._caret + 1:]

            # Delete backwards (backspace).
            elif event.key == pygame.locals.K_BACKSPACE:
                if self._caret > 0:
                    self._text = self._text[:self._caret - 1] + \
                                 self._text[self._caret:]
                    self._caret -= 1

            # Joystick buttons
            elif event.type == pygame.locals.JOYBUTTONDOWN:
                self._text = str(event.key)
                self.value = event.key

            # Any other case is okay, so show it.
            else:
                self._text =  pygame.key.name(event.key)
                self.value = event.key
                
        self.dirty = True


