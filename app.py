# Author: Hobs Towler
# Date: 12/1/2021
# Description:
import tkinter
from tkinter import *
import tkinter as tk
from main import *
from income import *
from dataload import *


def open_scenario():
    pass

def open_loan():
    pass

def open_job():
    pass

def open_expense():
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

        self._scenario_text = "Pick a Scenario."
        self._job_text = "Pick a Job."
        self._loan_text = "Pick a Loan."
        self._expense_text = "Pick an Expense."
        self._context_text = [self._scenario_text, self._job_text, self._loan_text, self._expense_text]
        self._context = 2

        for i in range(4):
            nav_menu.columnconfigure(i, weight=1)

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

    def set_context(self, context: int):
        self._label['text'] = self._context_text[context]
        self._context = context

    def get_context(self) -> int:
        return self._context


class BottomMenu:
    def __init__(self, parent: tk.Frame) -> None:
        frame = tk.Frame(parent, name="left_bottom_menu", width=300, height=50)
        frame.grid(column=0, row=2, sticky=N + W + S + E)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        # Buttons for the bottom menu. Edit, New, and Delete.
        tk.Button(frame, name="edit_item", text="Edit...", command=edit_item) \
            .grid(column=0, row=0, sticky=W + E)
        tk.Button(frame, name="new_item", text="New...", command=lambda: mid_panel.populate(left_panel.nav().get_context())) \
            .grid(column=1, row=0, sticky=W + E)
        self._del_button = tk.Button(frame, name="delete_item", text="Delete...", state="disabled", command=delete_item)
        self._del_button.grid(column=2, row=0, sticky=W + E)
        tk.Checkbutton(frame, name="delete_check", command=lambda: self.toggle_delete()).grid(column=3, row=0)

    def toggle_delete(self):
        if self._del_button['state'] == "disabled":
            self._del_button['state'] = "active"
        else:
            self._del_button['state'] = "disabled"


class LeftPanel:
    def __init__(self, parent: tk.Tk):
        panel = tk.Frame(parent)
        self.frame = panel
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
        self.frame = panel
        panel.grid(column=1, row=0, sticky=N+S)

        self._label = StringVar()
        detail_label = tk.Label(panel, name="detail_label", textvariable=self._label, width=20)
        detail_label.grid(column=0, row=0, sticky=N+S+W+E, pady=(26, 0))
        detail_label.grid_propagate(False)
        self._label.set("DETAIL")

        self.detail_panel = tk.Frame(panel, name="detail_panel", borderwidth=2, relief='sunken',width=300, height=500)
        self.detail_panel.grid(column=0, row=1, sticky=N+E+S+W)
        self.detail_panel.grid_propagate(False)

    # TODO make this form-based
    def populate(self, context: int):
        for c in self.detail_panel.winfo_children():
            c.destroy()
        if context == 0:
            return
        if context == 1:
            return
        if context == 2:
            self.pop_loan()
        if context == 3:
            return

    def pop_loan(self):
        panel = self.detail_panel
        tk.Label(panel, text="Name").grid(column=0, row=0)
        tk.Entry(panel, width=20).grid(column=1, row=0)

        tk.Label(panel, text="Loan Amount").grid(column=0, row=1)
        loan_amount = StringVar()
        loan_amount.set("test")
        tk.Entry(panel, width=20, textvariable=loan_amount).grid(column=1, row=1)

        tk.Label(panel, text="Down Payment").grid(column=0, row=2)
        tk.Entry(panel, width=20).grid(column=1, row=2)
        tk.Checkbutton(panel, name="down_percent", text="Percentage").grid(column=2,row=2)

        tk.Label(panel, text="Rate").grid(column=0, row=3)
        tk.Entry(panel, width=20).grid(column=1, row=3)
        self.show_bottom_menu()

    def show_bottom_menu(self):
        """
        "Shows" the bottom menu in the middle panel by creating it.
        :return: None
        """
        bMenu = tk.Frame(self.frame, name="bottom_menu")
        bMenu.grid(column=0, row=2, sticky=N + W + S + E)
        for i in range(5):
            bMenu.columnconfigure(i, weight=1)
            if i % 2 == 0:
                #add padding frames between the two buttons
                tk.Frame(bMenu).grid(column=i, row=0)
        tk.Button(bMenu, text="Cancel", command=lambda: self.clear()).grid(column=1, row=0, sticky=W + E)
        tk.Button(bMenu, text="Save").grid(column=3, row=0, sticky=W + E)

    def hide_bottom_menu(self):
        """
        Usually called by clear(). "Hides" the bottom menu for the middle panel by destroying the frame.
        :return: None
        """
        for c in self.frame.winfo_children():
            if c.winfo_name() == "bottom_menu":
                c.destroy()

    def clear(self):
        """
        Clears the context from the middle panel.
        :return: None
        """
        for c in self.detail_panel.winfo_children():
            c.destroy()
        self.hide_bottom_menu()



class RightPanel:
    def __init__(self, parent: tk.Tk):
        panel = tk.Frame(parent)
        panel.grid(column=2, row=0)

        stat_panel = tk.Frame(panel, borderwidth=2, relief='ridge', width=500, height=550)
        stat_panel.grid(column=0, row=0, rowspan=2)


def _create_left_drawer(root, context: str="none") -> tk.Frame:
    left_drawer = tk.Frame(root, borderwidth=2, relief='sunken', width=300, height=500)
    left_drawer.grid(column=0, row=1, sticky=N+W+S+E)
    left_drawer.grid_propagate(False)

    return left_drawer


# declare global variables
buttons = {}
labels = {}

# load the data
loans = load_loans()
jobs = load_jobs()
expenses = load_expenses()
incomes = load_incomes()
scenarios = load_scenarios()

# create the root
root = Tk()
root.title("Loan Calculator")

# create the three main panels.
left_panel = LeftPanel(root)
mid_panel = MidPanel(root)
right_panel = RightPanel(root)

#def print_hierarchy(w, depth=0):
    #print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    #for i in w.winfo_children():
        #print_hierarchy(i, depth+1)
#print_hierarchy(root)

root.mainloop()
