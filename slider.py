import tkinter as tk

class Slider:
    def __init__(self, parent, text, defaultValue):
        self.label = tk.Label(parent, text = text)

        self.value = tk.DoubleVar()
        self.slider = tk.Scale(parent, variable = self.value, from_ = 0, to = 256, resolution = 1, orient = "horizontal")
        self.slider.bind("<ButtonRelease-1>", self.selectionChanged)

        self.value.set(defaultValue)
        self.draw()

    def draw(self):
        self.label.pack(anchor = tk.CENTER)
        self.slider.pack(anchor = tk.CENTER)

    def selectionChanged(self, event):
        selection = "Value = " + str(self.value.get())

    def getValue(self):
        return self.value.get()
