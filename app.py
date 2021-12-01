# Author: Hobs Towler
# Date: 12/1/2021
# Description:

from tkinter import *
from tkinter import ttk
from main import *
from income import *


def import_scenarios():
    """
    Imports scenarios from the Scenarios folder.
    :return:
    """
    pass

def import_expenses():
    pass


def import_jobs():
    pass


def import_incomes():
    pass


def import_loans():
    pass


def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass


class MenuBar:
    def __init__(self, root):
        pass

class MainPanel:
    def __init__(self, root):
        pass

class Context:
    pass

class Stats(Context):
    pass

class LoanDetail(Context):
    pass

root = Tk()
root.title("test")

scene = Scenario()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
feet_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()
