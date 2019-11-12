import tkinter as tk
import tkinter.ttk as ttk


class RadioNeighBoundMenu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_1 = tk.Label(self, text="Neighborhood", width=26)
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
        self.radioOptMoore.grid(row=1, column=0, sticky=tk.W)
        self.radioOptNeumann.grid(row=2, column=0, sticky=tk.W)

        self.separator_1 = ttk.Separator(self, orient=tk.VERTICAL)
        self.separator_1.grid(row=0, column=1, rowspan=3, sticky=tk.N+tk.S)

        self.label_2 = tk.Label(self, text="Boundary", width=26)
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


class SizeGrainMenu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seedNumVar = tk.IntVar(self)
        self.seedNumVar.set(3)
        self.labelSeed = tk.Label(self, text="Seed number:", width=26)
        self.labelSeed.grid(row=0, column=0, sticky=tk.W)
        self.seedEntry = tk.Entry(self, textvariable=self.seedNumVar)
        self.seedEntry.grid(row=0, column=1, sticky=tk.W)

        self.widthNumVar = tk.IntVar(self)
        self.widthNumVar.set(50)
        self.labelWidth = tk.Label(self, text="Width:", width=26)
        self.labelWidth.grid(row=1, column=0, sticky=tk.W)
        self.WidthEntry = tk.Entry(self, textvariable=self.widthNumVar)
        self.WidthEntry.grid(row=1, column=1, sticky=tk.W)

        self.heightNumVar = tk.IntVar(self)
        self.heightNumVar.set(100)
        self.labelHeight = tk.Label(self, text="Height:", width=26)
        self.labelHeight.grid(row=2, column=0, sticky=tk.W)
        self.heightEntry = tk.Entry(self, textvariable=self.heightNumVar)
        self.heightEntry.grid(row=2, column=1, sticky=tk.W)


class Menu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.seedBtn = tk.Button(self, text="Seed", width=8)
        self.seedBtn.grid(row=0, column=0)

        self.startStopBtn = tk.Button(self, text='Start/Stop', width=8)
        self.startStopBtn.grid(row=0, column=1)

        self.loadBtn = tk.Button(self, text='Load', width=8)
        self.loadBtn.grid(row=0, column=2)

        self.saveBtn = tk.Button(self, text='Save', width=8)
        self.saveBtn.grid(row=0, column=3)

        self.separator_0 = ttk.Separator(self)
        self.separator_0.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.E)

        self.radioMenu = RadioNeighBoundMenu(self)
        self.radioMenu.grid(row=2, column=0, columnspan=4, sticky=tk.W+tk.E)

        self.separator_1 = ttk.Separator(self)
        self.separator_1.grid(row=3, column=0, columnspan=4, sticky=tk.W+tk.E)

        self.sizeGrainMenu = SizeGrainMenu(self)
        self.sizeGrainMenu.grid(row=4, column=0, columnspan=4, sticky=tk.W+tk.E)

        self.startStopBtn.bind('<Button-1>', self.startStopBtnAction)


    def startStopBtnAction(self, event):
        return True

if __name__ == '__main__':
    root = tk.Tk()
    menu = Menu(root)
    menu.grid(row=0, column=0, sticky=tk.N + tk.W + tk.S + tk.E)
    root.mainloop()
