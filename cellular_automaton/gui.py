import asyncio
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import threading
from time import sleep
from PIL import Image, ImageTk


class NeighborhoodRadioMenu(tk.Frame):
    def __init__(self, state_solver_var, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stateSolverVar = state_solver_var
        self.stateOptSimple = tk.Radiobutton(
            self,
            text="Simple State",
            variable=state_solver_var,
            value="simple-random-standard"
        )
        self.stateOptSimple.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.columnconfigure(0, weight=1)
        self.label = tk.Label(self, text="Neighborhood")
        self.label.grid(row=1, column=0, sticky=tk.W+tk.E)

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
        self.radioOptMoore.grid(row=2, column=0, sticky=tk.W)
        self.radioOptNeumann.grid(row=3, column=0, sticky=tk.W)
        self.radioOptHexagonalLeft.grid(row=4, column=0, sticky=tk.W)
        self.radioOptHexagonalRight.grid(row=5, column=0, sticky=tk.W)
        self.radioOptHexagonalRandom.grid(row=6, column=0, sticky=tk.W)
        self.radioOptPentagonalLeft.grid(row=7, column=0, sticky=tk.W)
        self.radioOptPentagonalRight.grid(row=8, column=0, sticky=tk.W)
        self.radioOptPentagonalRandom.grid(row=9, column=0, sticky=tk.W)

    def disable(self):
        self.radioOptMoore.configure(state='disable')
        self.radioOptNeumann.configure(state='disable')
        self.radioOptHexagonalLeft.configure(state='disable')
        self.radioOptHexagonalRight.configure(state='disable')
        self.radioOptHexagonalRandom.configure(state='disable')
        self.radioOptPentagonalLeft.configure(state='disable')
        self.radioOptPentagonalRight.configure(state='disable')
        self.radioOptPentagonalRandom.configure(state='disable')

    def enable(self):
        self.radioOptMoore.configure(state='normal')
        self.radioOptNeumann.configure(state='normal')
        self.radioOptHexagonalLeft.configure(state='normal')
        self.radioOptHexagonalRight.configure(state='normal')
        self.radioOptHexagonalRandom.configure(state='normal')
        self.radioOptPentagonalLeft.configure(state='normal')
        self.radioOptPentagonalRight.configure(state='normal')
        self.radioOptPentagonalRandom.configure(state='normal')


class BoundaryRadioMenu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = tk.Label(self, text="Boundary")
        self.label.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.columnconfigure(0, weight=1)

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
        self.radioOptPeriodic.grid(row=1, column=0, sticky=tk.W)
        self.radioOptAbsorb.grid(row=2, column=0, sticky=tk.W)


class StateRadioMenu(tk.Frame):
    def __init__(self, state_solver_var, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.stateSolverVar = state_solver_var
        self.stateOptGrainCurv = tk.Radiobutton(
            self,
            text="Grain Curvature State",
            variable=self.stateSolverVar,
            value="grain-curvature-probability"
        )
        self.stateOptGrainCurv.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.stateGrainProbabilityVar = tk.DoubleVar(self)
        self.stateGrainProbabilityVar.set(0.5)
        self.stateEntryGrainCurv = tk.Entry(
            self,
            textvariable=self.stateGrainProbabilityVar,
        )
        self.stateEntryGrainCurv.grid(row=1, column=0, sticky=tk.W)

    def disable(self):
        self.stateEntryGrainCurv.configure(state='disabled')

    def enable(self):
        self.stateEntryGrainCurv.configure(state='normal')


class RadioNeighBoundMenu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.stateSolverVar = tk.StringVar(self)
        self.stateSolverVar.set("simple-random-standard")
        self.stateSolverVar.trace_variable('w', self.disable_unused_entries)

        self.neighborhoodMenu = NeighborhoodRadioMenu(self.stateSolverVar, self)
        self.neighborhoodMenu.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.separator_1 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator_1.grid(row=1, column=0, rowspan=1, sticky=tk.W+tk.E)
        self.stateRadioMenu = StateRadioMenu(self.stateSolverVar, self)
        self.stateRadioMenu.grid(row=2, column=0, sticky=tk.W+tk.E)
        self.stateRadioMenu.disable()
        self.separator_2 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator_2.grid(row=3, column=0, rowspan=1, sticky=tk.W+tk.E)
        self.boundaryMenu = BoundaryRadioMenu(self)
        self.boundaryMenu.grid(row=4, column=0, sticky=tk.W+tk.E)
        self.separator_3 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator_3.grid(row=5, column=0, rowspan=1, sticky=tk.W+tk.E)

        self.delayVar = tk.DoubleVar(self)
        self.delayVar.set(0.2)
        self.delayLabel = tk.Label(self, text="Delay:")
        self.delayLabel.grid(row=6, column=0, sticky=tk.W+tk.E)
        self.delayEntry = tk.Entry(self, textvariable=self.delayVar)
        self.delayEntry.grid(row=7, column=0, sticky=tk.W)

    def get_boundary(self):
        return self.boundaryMenu.boundaryVar.get()

    def get_delay(self):
        return self.delayVar.get()

    def get_neighborhood(self):
        return self.neighborhoodMenu.neighborhoodVar.get()

    def get_state_solver(self):
        return self.stateSolverVar.get()

    def get_state_solver_probability(self):
        return self.stateRadioMenu.stateGrainProbabilityVar.get()

    def disable_unused_entries(self, *args):
        state_solver = self.stateSolverVar.get()
        if state_solver == 'simple-random-standard':
            self.stateRadioMenu.disable()
            self.neighborhoodMenu.enable()
        elif state_solver == 'grain-curvature-probability':
            self.stateRadioMenu.enable()
            self.neighborhoodMenu.disable()

class SizeGrainMenu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.seedNumVar = tk.IntVar(self)
        self.seedNumVar.set(3)
        self.labelSeed = tk.Label(self, text="Seed number:")
        self.labelSeed.grid(row=0, column=0, sticky=tk.W)
        self.seedEntry = tk.Entry(self, textvariable=self.seedNumVar)
        self.seedEntry.grid(row=0, column=1, sticky=tk.E)

        self.widthNumVar = tk.IntVar(self)
        self.widthNumVar.set(100)
        self.labelWidth = tk.Label(self, text="Width:")
        self.labelWidth.grid(row=1, column=0, sticky=tk.W)
        self.WidthEntry = tk.Entry(self, textvariable=self.widthNumVar)
        self.WidthEntry.grid(row=1, column=1, sticky=tk.E)

        self.heightNumVar = tk.IntVar(self)
        self.heightNumVar.set(50)
        self.labelHeight = tk.Label(self, text="Height:")
        self.labelHeight.grid(row=2, column=0, sticky=tk.W)
        self.heightEntry = tk.Entry(self, textvariable=self.heightNumVar)
        self.heightEntry.grid(row=2, column=1, sticky=tk.E)


class Menu(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self._controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.startStopBtn = tk.Button(self, text='Start/Stop', command=self.startStopBtnAction, width=8)
        self.startStopBtn.grid(row=0, column=0)

        self.loadBtn = tk.Button(self, text='Load', command=self.loadBtnAction, width=8)
        self.loadBtn.grid(row=0, column=1)

        self.saveBtn = tk.Button(self, text='Save', command=self.saveBtnAction, width=8)
        self.saveBtn.grid(row=0, column=2)

        self.nextStepBtn = tk.Button(self, text="Next Step", command=self.nextStepBtnAction, width=8)
        self.nextStepBtn.grid(row=1, column=0)

        self.updateBtn = tk.Button(self, text="Update Solver", command=self.updateBtnAction, width=12)
        self.updateBtn.grid(row=1, column=1)

        self.resetBtn = tk.Button(self, text="Reset", command=self.resetBtnAction, width=8)
        self.resetBtn.grid(row=1, column=2)

    def nextStepBtnAction(self):
        self._controller.next_step()

    def startStopBtnAction(self):
        self._controller.start_stop()

    def updateBtnAction(self):
        self._controller.update()

    def resetBtnAction(self):
        self._controller.reset()

    def saveBtnAction(self):
        self._controller.save()

    def loadBtnAction(self):
        self._controller.load()


class Inclusions(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self.inclusionNumVar = tk.IntVar(self)
        self.inclusionNumVar.set(3)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.labelInclusion = tk.Label(self, text="Inclusion number:")
        self.labelInclusion.grid(row=0, column=0, sticky=tk.W)
        self.inclusionEntry = tk.Entry(self, textvariable=self.inclusionNumVar)
        self.inclusionEntry.grid(row=0, column=1, sticky=tk.E)

        self.inclusionMinRadiusVar = tk.IntVar(self)
        self.inclusionMinRadiusVar.set(1)
        self.inclusionMinRadiusLabel = tk.Label(self, text="Inclusion min radius:")
        self.inclusionMinRadiusLabel.grid(row=1, column=0, sticky=tk.W)
        self.inclusionMinRadiusEntry = tk.Entry(self, textvariable=self.inclusionMinRadiusVar)
        self.inclusionMinRadiusEntry.grid(row=1, column=1, sticky=tk.E)

        self.inclusionMaxRadiusVar = tk.IntVar(self)
        self.inclusionMaxRadiusVar.set(2)
        self.inclusionMaxRadiusLabel = tk.Label(self, text="Inclusion max radius:")
        self.inclusionMaxRadiusLabel.grid(row=2, column=0, sticky=tk.W)
        self.inclusionMaxRadiusEntry = tk.Entry(self, textvariable=self.inclusionMaxRadiusVar)
        self.inclusionMaxRadiusEntry.grid(row=2, column=1, sticky=tk.E)


class ResetMenu(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self._controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.resetLabel = tk.Label(self, text="Reset options")
        self.resetLabel.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E)
        self.sizeGrainMenu = SizeGrainMenu(self)
        self.sizeGrainMenu.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E)
        self.inclusionMenu = Inclusions(self)
        self.inclusionMenu.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E)

        self.clearButton = tk.Button(self, text="Clear", command=self.clearBtnAction)
        self.clearButton.grid(row=3, column=0, sticky=tk.W+tk.E)

        self.clearSelectedButton = tk.Button(self, text="Clear selected", command=self.clearSelectedBtnAction)
        self.clearSelectedButton.grid(row=4, column=0, sticky=tk.W+tk.E)

        self.reseedButton = tk.Button(self, text="Reseed", command=self.reseedBtnAction)
        self.reseedButton.grid(row=3, column=1, sticky=tk.W+tk.E)

    def clearBtnAction(self):
        self._controller.clear()

    def clearSelectedBtnAction(self):
        self._controller.clear_selected()

    def reseedBtnAction(self):
        self._controller.reseed()

    def getResetValues(self):
        inclusion_min_radius = self.inclusionMenu.inclusionMinRadiusVar.get()
        inclusion_max_radius = self.inclusionMenu.inclusionMaxRadiusVar.get()
        if inclusion_max_radius < inclusion_min_radius:
            self.inclusionMenu.inclusionMaxRadiusVar.set(inclusion_min_radius)
            inclusion_max_radius = inclusion_min_radius
        values = {
            "seed_number": self.sizeGrainMenu.seedNumVar.get(),
            "height": self.sizeGrainMenu.heightNumVar.get(),
            "width": self.sizeGrainMenu.widthNumVar.get(),
            "inclusion_number": self.inclusionMenu.inclusionNumVar.get(),
            "inclusion_min_radius": inclusion_min_radius,
            "inclusion_max_radius": inclusion_max_radius
        }
        return values


class Body(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = controller
        self.menu = Menu(self)
        self.menu.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.separator_0 = ttk.Separator(self)
        self.separator_0.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.radioMenu = RadioNeighBoundMenu(self)
        self.radioMenu.grid(row=2, column=0, sticky=tk.W+tk.E)

        self.separator_1 = ttk.Separator(self)
        self.separator_1.grid(row=3, column=0, sticky=tk.W+tk.E)

        self.resetMenu = ResetMenu(self)
        self.resetMenu.grid(row=3, column=0, sticky=tk.W+tk.E)

    def start_stop(self):
        self._controller.start_stop()

    def clear(self):
        pass

    def clear_selected(self):
        pass

    def reseed(self):
        pass

    def reset(self):
        values = self.resetMenu.getResetValues()
        self._controller.reset(
            values['height'],
            values['width'],
            values['seed_number'],
            values['inclusion_number'],
            values['inclusion_min_radius'],
            values['inclusion_max_radius'])
        self._controller.next_step()

    def update(self):
        boundary = self.radioMenu.get_boundary()
        neighborhood = self.radioMenu.get_neighborhood()
        delay = self.radioMenu.get_delay()
        state_solver = self.radioMenu.get_state_solver()
        if state_solver == "grain-curvature-probability":
            probability = self.radioMenu.get_state_solver_probability()
            state_solver += ":" + str(probability)
        self._controller.update_solver(neighborhood, boundary, state_solver)
        self._controller.update_delay(delay)

    def next_step(self):
        self._controller.next_step()

    def save(self):
        files = [('CSV', '*.csv'), ('PNG', '*.png')]
        filename = filedialog.asksaveasfilename(filetypes=files)
        if filename:
            self._controller.save(filename)

    def load(self):
        files = [('CSV', '*.csv')]
        filename = filedialog.askopenfilename(filetypes=files)
        if filename:
            self._controller.load(filename)



class View(tk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._image = None
        self._array = None
        self._controller = controller
        self._panel = tk.Label(self)
        self._panel.grid(row=0, column=0)
        self._panel.bind('<Button-1>', self.image_click)
        self._info = tk.Label(self, text="Grain id's selected:")
        self._info.grid(row=1, column=0, sticky=tk.W)
        self._grain_selected = tk.Label(self, text="")
        self._grain_selected.grid(row=2, column=0, sticky=tk.W)

    def image_click(self, event):
        print(event.x, event.y)

    def update(self, array):
        self._array = array
        image = Image.fromarray(array, 'CMYK')
        image = image.resize((image.width*3, image.height*3))
        self._image = ImageTk.PhotoImage(image=image)
        self._panel.configure(image=self._image)
