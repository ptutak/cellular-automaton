from time import sleep
import cellular_automaton.gui as gui
import numpy as np
from unittest.mock import patch, MagicMock


class TestView:
    def test_update(self):
        view = gui.View(np.zeros((3,3), dtype=np.int32))
        view.panel = MagicMock()
        with patch('cellular_automaton.gui.ImageTk') as mocked_image:
            view.update(np.zeros((4, 4), dtype=np.int32))
        assert mocked_image.mock_calls[0]
