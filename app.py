# Author: Hobs Towler
# Date: 12/1/2021
# Description:
import tkinter
from tkinter import *
import tkinter as tk
from main import *
from income import *
from dataload import *




def change_to_scenario():
    change_label("Pick a Scenario", "nav_menu")
    button = get_button("scenario_button", "nav_menu")


def change_to_loans():
    change_label("Pick a Loan", "nav_menu")
    button = get_button("loan_button", "nav_menu")


def change_to_jobs():
    change_label("Pick a Job", "nav_menu")
    button = get_button("job_button", "nav_menu")


def change_to_expenses():
    change_label("Pick an Expense", "nav_menu")
    button = get_button("expense_button", "nav_menu")


def get_button(button_name: str, context: str) -> tk.Button:
    for b in buttons.get(context):
        if b.winfo_name() == button_name:
            return b


def change_label(label_text: str, context: str) -> None:
    for c in labels.get(context).winfo_children():
        if c.winfo_class() == "Label":
            c['text'] = label_text


def update_buttons(parent: tk.Frame) -> None:
    temp_list = []
    for x in parent.winfo_children():
        temp_list.append(x)
    buttons.update({parent.winfo_name(): temp_list})


def open_scenario():
    pass

def open_loan():
    pass

def open_job():
    pass

def open_expense():
    pass

def create_new():
    pass

def edit_item():
    pass

def delete_item():
    pass

class Context:
    pass

class Stats(Context):
    pass

class LoanDetail(Context):
    pass


class NavMenu:
    def __init__(self, parent: tk.Frame):
        nav_menu = tk.Frame(parent, name="nav_menu", width=300, height=30)
        nav_menu.grid(column=0, row=0, sticky=N+W+S+E, pady=(0, 0), padx=0)

        nav_menu.columnconfigure(0, weight=1)
        nav_menu.columnconfigure(1, weight=1)
        nav_menu.columnconfigure(2, weight=1)
        nav_menu.columnconfigure(3, weight=1)

        self._scenario_text = "Pick a Scenario."
        self._job_text = "Pick a Job."
        self._loan_text = "Pick a Loan."
        self._expense_text = "Pick an Expense."
        self._context_text = [self._scenario_text, self._job_text, self._loan_text, self._expense_text]

        tk.Button(nav_menu, name="scenario_button", text="Scenarios", width=8, command=lambda: self.set_context(0))\
            .grid(column=0, row=0, sticky=W+E)
        tk.Button(nav_menu, name="job_button", text="Jobs", width=8, command=lambda: self.set_context(1))\
            .grid(column=1, row=0, sticky=W+E)
        tk.Button(nav_menu, name="loan_button", text="Loans", width=8, command=lambda: self.set_context(2))\
            .grid(column=2, row=0, sticky=W+E)
        tk.Button(nav_menu, name="expense_button", text="Expenses", width=8, command=lambda: self.set_context(3))\
            .grid(column=3, row=0, sticky=W+E)

        self._label = tk.Label(nav_menu, name="nav_label", text=self._context_text[0])
        self._label.grid(column=0, row=1, columnspan=4)

        update_buttons(nav_menu)
        labels.update({"nav_menu": nav_menu})

    def set_context(self, context: int):
        self._label['text'] = self._context_text[context]


class BottomMenu:
    def __init__(self, parent: tk.Frame) -> None:
        frame = tk.Frame(parent, name="left_botttom_menu", width=300, height=50)
        frame.grid(column=0, row=2, sticky=N + W + S + E)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        # Buttons for the bottom menu. Edit, New, and Delete.
        tk.Button(frame, name="edit_item", text="Edit...", command=edit_item) \
            .grid(column=0, row=0, sticky=W + E)
        tk.Button(frame, name="new_item", text="New...", command=create_new) \
            .grid(column=1, row=0, sticky=W + E)
        tk.Button(frame, name="delete_item", text="Delete...", state="disabled", command=delete_item) \
            .grid(column=2, row=0, sticky=W + E)
        tk.Checkbutton(frame, name="delete_check").grid(column=3, row=0)

        # add buttons to global dictionary variable
        update_buttons(frame)


class LeftPanel:
    def __init__(self, parent: tk.Tk):
        panel = tk.Frame(parent)
        panel.grid(column=0, row=0)
        self._nav_menu = NavMenu(panel)
        _create_left_drawer(panel)
        self._bottom_menu = BottomMenu(panel)

    def nav(self) -> NavMenu:
        return self._nav_menu

    def bottom(self) -> BottomMenu:
        return self._bottom_menu


class MidPanel:
    def __init__(self, parent: tk.Tk):
        panel = tk.Frame(parent)
        panel.grid(column=1, row=0, sticky=N+S)

        detail_label = tk.Frame(panel, name="detail_label", width=300, height=100)
        detail_label.grid(column=0, row=0, sticky=N+S, pady=(26,0), rowspan=2)
        d_label = StringVar()
        dd_label = tk.Label(detail_label)
        dd_label.grid(column=0, row=0)
        d_label.set("DETAIL")
        dd_label['textvariable'] = d_label
        detail_panel = tk.Frame(panel, width=300, height=500)
        detail_panel.grid(column=0, row=2)


class RightPanel:
    def __init__(self, parent: tk.Tk):
        panel = tk.Frame(parent)
        panel.grid(column=2, row=0)

        stat_panel = tk.Frame(panel, borderwidth=2, relief='ridge', width=500, height=550)
        stat_panel.grid(column=0, row=0, rowspan=2)


def _create_left_drawer(root, context: str="none") -> tk.Frame:
    left_drawer = tk.Frame(root, borderwidth=2, relief='sunken', width=300, height=500)
    left_drawer.grid(column=0, row=1, sticky=N+W+S+E)

    return left_drawer





allow_delete = False
loans = load_loans()
jobs = load_jobs()
expenses = load_expenses()
incomes = load_incomes()
scenarios = load_scenarios()
buttons = {}
labels = {}

#create the root
root = Tk()
root.title("Loan Calculator")

#create the three main panels.
left_panel = LeftPanel(root)
mid_panel = MidPanel(root)
right_panel = RightPanel(root)









def print_hierarchy(w, depth=0):
    #print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfo_children():
        print_hierarchy(i, depth+1)
print_hierarchy(root)


root.mainloop()
