import csv
import tkinter as tk
from tkinter import ttk
from math import sin, pi


import matplotlib
import matplotlib.pyplot as pyplot
matplotlib.use('TkAgg')


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def preodic_function(t):
    return int(128 + 126 * sin(pi / 16 * t))


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(__file__)

        self.btn_start = ttk.Button(self, text="Start", command=self.command_start)
        self.btn_start.pack()
        self.btn_stop = ttk.Button(self, text="Stop", command=self.command_stop)
        self.btn_stop.pack()
        self.btn_export = ttk.Button(self, text="Export", command=self.command_export)
        self.btn_export.pack()

        self.canvas = tk.Canvas(self)
        self.oval = self.canvas.create_oval(20, 20, 200, 100, fill='grey')
        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.figure = pyplot.figure(1)
        canvas = FigureCanvasTkAgg(self.figure, master=self)
        plot_widget = canvas.get_tk_widget()
        plot_widget.pack()

        self.tick = 0
        self.ticks = []
        self.running = False

    def command_start(self):
        self.running = True
        self.update()

    def command_stop(self):
        self.running = False

    def command_export(self):
        with open('export.csv', 'w') as f:
            writer = csv.DictWriter(f, ['t', 'x'])
            writer.writeheader()
            for elem in self.ticks:
                writer.writerow({'t': elem[0], 'x': elem[1]})

    def recolor_oval(self, color):
        self.canvas.itemconfig(self.oval, fill=color)

    def redraw_graph(self):
        self.ticks.append((self.tick, preodic_function(self.tick)))
        pyplot.plot([elem[0] for elem in self.ticks],
                    [elem[1] for elem in self.ticks],
                    'b-')
        self.figure.canvas.draw()

    def update(self):
        if not self.running:
            return
        de = ("%02x" % 255)
        re = ("%02x" % (256 - preodic_function(self.tick) % 256))
        we = ("%02x" % 255)
        ge = "#"
        color = ge + de + re + we

        self.tick = self.tick + 1

        self.recolor_oval(color)
        self.redraw_graph()

        self.after(100, self.update)


if __name__ == '__main__':
    window = Application()
    window.mainloop()
