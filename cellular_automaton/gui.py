import tkinter as tk

class Menu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.startStopBtn = tk.Button(self, text='Start/Stop')
        self.startStopBtn.grid(row=0, column=0)
        self.startStopBtn.bind('<Button-1>', self.startStopBtnAction)

        self.loadBtn = tk.Button(self, text='Load')
        self.loadBtn.grid(row=0, column=1)

        self.saveBtn = tk.Button(self, text='Save')
        self.saveBtn.grid(row=0, column=2)

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
        self.radioOptMoore.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        self.radioOptNeumann.grid(row=2, column=0, columnspan=3, sticky=tk.W)

    def startStopBtnAction(self):
        return True

if __name__ == '__main__':
    root = tk.Tk()
    menu = Menu(root)
    menu.grid(row=0, column=0, sticky=tk.N + tk.W + tk.S + tk.E)
    root.mainloop()
