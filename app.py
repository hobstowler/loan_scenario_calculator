# Author: Hobs Towler
# Date: 12/1/2021
# Description:

from tkinter import *
from tkinter import ttk
from main import *
from income import *


def load_scenarios() -> list:
    """
    Imports scenarios from the Scenarios folder.
    :return:
    """
    pass


def load_expenses() -> list:
    pass


def load_jobs() -> list:
    pass


def load_incomes() -> list:
    pass


def load_loans() -> list:
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


loans = load_loans()
jobs = load_jobs()
expenses = load_expenses()
incomes = load_incomes()
scenarios = load_scenarios()

root = Tk()
root.title("test")

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

ttk.Label(mainframe, text="feet2").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
feet_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()
