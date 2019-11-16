import tkinter as tk
import tkinter.ttk as ttk
import sys
import os
import asyncio
import threading
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../../'))

import cellular_automaton.core as core
import cellular_automaton.gui as gui

class Main:
    def __init__(self):
        gui_root = tk.Tk()

        self._controller = core.MainController()

        body = gui.Body(self._controller, gui_root)
        body.grid(row=0, column=0, sticky=tk.N + tk.W + tk.S + tk.E)
        body.columnconfigure(0, weight=0)
        body.reset()
        body.update()

        separator = ttk.Separator(gui_root, orient=tk.VERTICAL)
        separator.grid(row=0, column=1, sticky=tk.N + tk.S)

        view = gui.View(gui_root)
        view.grid(row=0, column=2, sticky=tk.N + tk.W + tk.S + tk.E)
        view.columnconfigure(0, weight=1)
        view.rowconfigure(0, weight=1)
        view.update(next(self._controller.array_generator()))

        gui_root.columnconfigure(0, weight=0)
        gui_root.columnconfigure(2, weight=1)
        gui_root.rowconfigure(0, weight=1)

        self._view = view
        self._gui_root = gui_root
        self._view_thread = None
        self._on = True
        self._on_lock = threading.Lock()

    async def _view_async_loop(self):
        arrays = self._controller.array_generator()
        while True:
            self._controller.first_control_gate()
            self._controller.second_control_gate()
            with self._on_lock:
                if not self._on:
                    break
            array = next(arrays)
            self._view.update(array)
            await asyncio.sleep(self._controller.get_delay())

    def _view_main_loop(self):
        asyncio.run(self._view_async_loop())

    def main(self):
        self._view_thread = threading.Thread(target=self._view_main_loop)
        self._view_thread.start()
        self._gui_root.mainloop()
        with self._on_lock:
            self._on = False
        self._controller.open_gate()
        self._view_thread.join()
        return 0

if __name__ == '__main__':
    main = Main()
    exit(main.main())
