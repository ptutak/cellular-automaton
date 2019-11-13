from time import sleep
import cellular_automaton.gui as gui

class TestMenu:
    def test_start_stop_action(self):
        ui = gui.Menu(None)
        assert ui.startStopBtnAction(None)
