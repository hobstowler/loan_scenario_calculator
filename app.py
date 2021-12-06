# Author: Hobs Towler
# Date: 12/1/2021
# Description:

from tkinter import *
from tkinter import ttk
from main import *
from income import *
from dataload import *

def change_to_scenario():
    #d_label.set("Scenario")
    print("SCENARIOS")


def change_to_loans():
    #d_label.set("Loans")
    print("LOANS")


def change_to_jobs():
    #d_label.set("Jobs")
    print("JOBS")


def change_to_expenses():
    #d_label.set("Expenses")
    print("EXPENSES")


def open_scenario():
    pass

def open_loan():
    pass

def open_job():
    pass

def open_expense():
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

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0)

left_pane = ttk.Frame(mainframe)
left_pane.grid(column=0, row=0)
middle_pane = ttk.Frame(mainframe)
middle_pane.grid(column=1, row=0)
right_pane = ttk.Frame(mainframe)
right_pane.grid(column=2, row=0)

nav_menu = ttk.Frame(left_pane, width=300, height=50, padding=8)
nav_menu.grid(column=0, row=0, sticky=(N,W,S,E), pady=4, padx=2)
left_drawer = ttk.Frame(left_pane, borderwidth=2, relief='sunken', width=300, height=500, padding=6)
left_drawer.grid(column=0, row=1)

detail_label = ttk.Frame(middle_pane, borderwidth=2, relief='ridge', width=300, height=50, padding=6)
detail_label.grid(column=0, row=0)
d_label = StringVar()
dd_label = ttk.Label(detail_label)
dd_label.grid(column=0, row=0)
d_label.set("DETAIL")
dd_label['textvariable'] = d_label
detail_panel = ttk.Frame(middle_pane, width=300, height=500, padding=6)
detail_panel.grid(column=0, row=1)

stat_panel = ttk.Frame(right_pane, borderwidth=2, relief='ridge', width=500, height=550, padding=6)
stat_panel.grid(column=0, row=0, rowspan=2)


scenario_button = ttk.Button(nav_menu, text="Scenarios", width=10, command=change_to_scenario).grid(column=0, row=0)
job_button = ttk.Button(nav_menu, text="Jobs", width=10, command=change_to_jobs).grid(column=2, row=0)
loan_button = ttk.Button(nav_menu, text="Loans", width=10, command=change_to_loans).grid(column=3, row=0)
expense_button = ttk.Button(nav_menu, text="Expenses", width=10, command=change_to_expenses).grid(column=4, row=0)




root.mainloop()
