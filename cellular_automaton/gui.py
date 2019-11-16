import asyncio
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import threading
from time import sleep
from PIL import Image, ImageTk


class RadioNeighBoundMenu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_1 = tk.Label(self, text="Neighborhood")
        self.label_1.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.neighborhoodVar = tk.StringVar(self)
        self.neighborhoodVar.set("Moore")
        self.radioOptMoore = tk.Radiobutton(
            self,
            text="Moore",
            variable=self.neighborhoodVar,
            value="Moore")
        self.radioOptNeumann = tk.Radiobutton(
            self,
            text="Neumann",
            variable=self.neighborhoodVar,
            value="Neumann")
        self.radioOptHexagonalLeft = tk.Radiobutton(
            self,
            text="hexagonal-left",
            variable=self.neighborhoodVar,
            value="hexagonal-left"
        )
        self.radioOptHexagonalRight = tk.Radiobutton(
            self,
            text="hexagonal-right",
            variable=self.neighborhoodVar,
            value="hexagonal-right"
        )
        self.radioOptHexagonalRandom = tk.Radiobutton(
            self,
            text="hexagonal-random",
            variable=self.neighborhoodVar,
            value="hexagonal-random"
        )
        self.radioOptPentagonalLeft = tk.Radiobutton(
            self,
            text="pentagonal-left",
            variable=self.neighborhoodVar,
            value="pentagonal-left"
        )
        self.radioOptPentagonalRight = tk.Radiobutton(
            self,
            text="pentagonal-right",
            variable=self.neighborhoodVar,
            value="pentagonal-right"
        )
        self.radioOptPentagonalRandom = tk.Radiobutton(
            self,
            text="pentagonal-random",
            variable=self.neighborhoodVar,
            value="pentagonal-random"
        )
        self.radioOptMoore.grid(row=1, column=0, sticky=tk.W)
        self.radioOptNeumann.grid(row=2, column=0, sticky=tk.W)
        self.radioOptHexagonalLeft.grid(row=3, column=0, sticky=tk.W)
        self.radioOptHexagonalRight.grid(row=4, column=0, sticky=tk.W)
        self.radioOptHexagonalRandom.grid(row=5, column=0, sticky=tk.W)
        self.radioOptPentagonalLeft.grid(row=6, column=0, sticky=tk.W)
        self.radioOptPentagonalRight.grid(row=7, column=0, sticky=tk.W)
        self.radioOptPentagonalRandom.grid(row=8, column=0, sticky=tk.W)
        self.separator_1 = ttk.Separator(self, orient=tk.VERTICAL)
        self.separator_1.grid(row=0, column=1, rowspan=9, sticky=tk.N+tk.S)

        self.label_2 = tk.Label(self, text="Boundary")
        self.label_2.grid(row=0, column=2, sticky=tk.W+tk.E)

        self.boundaryVar = tk.StringVar(self)
        self.boundaryVar.set("periodic")
        self.radioOptPeriodic = tk.Radiobutton(
            self,
            text="periodic",
            variable=self.boundaryVar,
            value="periodic"
        )
        self.radioOptAbsorb = tk.Radiobutton(
            self,
            text="absorb",
            variable=self.boundaryVar,
            value="absorb"
        )
        self.radioOptPeriodic.grid(row=1, column=2, sticky=tk.W)
        self.radioOptAbsorb.grid(row=2, column=2, sticky=tk.W)

        self.delayVar = tk.DoubleVar(self)
        self.delayVar.set(0.2)
        self.label_3 = tk.Label(self, text="Delay:")
        self.label_3.grid(row=9, column=0, sticky=tk.W)
        self.delayEntry = tk.Entry(self, textvariable=self.delayVar)
        self.delayEntry.grid(row=9, column=2, sticky=tk.W)



class SizeGrainMenu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.seedNumVar = tk.IntVar(self)
        self.seedNumVar.set(3)
        self.labelSeed = tk.Label(self, text="Seed number:")
        self.labelSeed.grid(row=0, column=0, sticky=tk.W)
        self.seedEntry = tk.Entry(self, textvariable=self.seedNumVar)
        self.seedEntry.grid(row=0, column=1, sticky=tk.W)

        self.widthNumVar = tk.IntVar(self)
        self.widthNumVar.set(100)
        self.labelWidth = tk.Label(self, text="Width:")
        self.labelWidth.grid(row=1, column=0, sticky=tk.W)
        self.WidthEntry = tk.Entry(self, textvariable=self.widthNumVar)
        self.WidthEntry.grid(row=1, column=1, sticky=tk.W)

        self.heightNumVar = tk.IntVar(self)
        self.heightNumVar.set(50)
        self.labelHeight = tk.Label(self, text="Height:")
        self.labelHeight.grid(row=2, column=0, sticky=tk.W)
        self.heightEntry = tk.Entry(self, textvariable=self.heightNumVar)
        self.heightEntry.grid(row=2, column=1, sticky=tk.W)


class Menu(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self._controller = controller

        self.startStopBtn = tk.Button(self, text='Start/Stop', width=8)
        self.startStopBtn.grid(row=0, column=0)
        self.startStopBtn.bind('<Button-1>', self.startStopBtnAction)

        self.loadBtn = tk.Button(self, text='Load', width=8)
        self.loadBtn.grid(row=0, column=1)
        self.loadBtn.bind('<Button-1>', self.loadBtnAction)

        self.saveBtn = tk.Button(self, text='Save', width=8)
        self.saveBtn.grid(row=0, column=2)
        self.saveBtn.bind('<Button-1>', self.saveBtnAction)

        self.nextStepBtn = tk.Button(self, text="Next Step", width=8)
        self.nextStepBtn.grid(row=1, column=0)
        self.nextStepBtn.bind('<Button-1>', self.nextStepBtnAction)

        self.updateBtn = tk.Button(self, text="Update Solver", width=8)
        self.updateBtn.grid(row=1, column=1)
        self.updateBtn.bind('<Button-1>', self.updateBtnAction)

        self.resetBtn = tk.Button(self, text="Reset", width=8)
        self.resetBtn.grid(row=1, column=2)
        self.resetBtn.bind('<Button-1>', self.resetBtnAction)

    def nextStepBtnAction(self, event):
        self._controller.next_step()

    def startStopBtnAction(self, event):
        self._controller.start_stop()

    def updateBtnAction(self, event):
        self._controller.update()

    def resetBtnAction(self, event):
        self._controller.reset()

    def saveBtnAction(self, event):
        self._controller.save()

    def loadBtnAction(self, event):
        self._controller.load()


class Body(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = controller
        self.menu = Menu(self)
        self.menu.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.menu.columnconfigure(0, weight=1)
        self.menu.columnconfigure(1, weight=1)
        self.menu.columnconfigure(2, weight=1)

        self.separator_0 = ttk.Separator(self)
        self.separator_0.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.radioMenu = RadioNeighBoundMenu(self)
        self.radioMenu.grid(row=2, column=0, sticky=tk.W+tk.E)
        self.radioMenu.columnconfigure(0, weight=1)
        self.radioMenu.columnconfigure(2, weight=1)
        self.separator_1 = ttk.Separator(self)
        self.separator_1.grid(row=3, column=0, sticky=tk.W+tk.E)

        self.sizeGrainMenu = SizeGrainMenu(self)
        self.sizeGrainMenu.grid(row=4, column=0, sticky=tk.W+tk.E)
        self.sizeGrainMenu.columnconfigure(0, weight=1)
        self.sizeGrainMenu.columnconfigure(1, weight=1)

    def start_stop(self):
        self._controller.start_stop()

    def reset(self):
        seed_number = self.sizeGrainMenu.seedNumVar.get()
        height = self.sizeGrainMenu.heightNumVar.get()
        width = self.sizeGrainMenu.widthNumVar.get()
        self._controller.reset(height, width, seed_number)
        self._controller.start_stop()
        self._controller.start_stop()

    def update(self):
        boundary = self.radioMenu.boundaryVar.get()
        neighborhood = self.radioMenu.neighborhoodVar.get()
        delay = self.radioMenu.delayVar.get()
        self._controller.update_solver(neighborhood, boundary)
        self._controller.update_delay(delay)

    def next_step(self):
        self._controller.next_step()

    def save(self):
        files = [('CSV', '*.csv')]
        filename = filedialog.asksaveasfilename(filetypes=files)
        if filename:
            self._controller.save(filename)

    def load(self):
        files = [('CSV', '*.csv')]
        filename = filedialog.askopenfilename(filetypes=files)
        if filename:
            self._controller.load(filename)
        self._controller.next_step()


class View(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._image = None
        self.panel = tk.Label(self)
        self.panel.grid(row=0, column=0)

    def update(self, array):
        image = Image.fromarray(array, 'CMYK')
        image = image.resize((image.width*3, image.height*3))
        self._image = ImageTk.PhotoImage(image=image)
        self.panel.configure(image=self._image)
