# Author: Hobs Towler
# Date: 12/1/2021
# Description:
import tkinter
from tkinter import *
import tkinter as tk
from main import *
from income import *
from dataload import *
from Forms import *


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


class LeftPanel:
    def __init__(self, parent: tk.Tk):
        self.frame = tk.Frame(parent)
        self.frame.grid(column=0, row=0)

        # nav menu variables
        self._nav_label = None
        self._context = 2
        self._context_text = [
            "Pick a Scenario.",
            "Pick a Job.",
            "Pick a Loan.",
            "Pick an Expense."
        ]

        # drawer variables

        # bottom menu variables
        self._del_button = None

        # instantiate major components
        self._nav_menu = self.create_nav_menu()
        self._drawer = self.create_drawer()
        self._bottom_menu = self.create_bottom_menu()

    def create_nav_menu(self):
        nav_menu = tk.Frame(self.frame, name="nav_menu", width=300, height=30)
        nav_menu.grid(column=0, row=0, sticky=N + W + S + E, pady=(0, 0), padx=0)
        for i in range(4):
            nav_menu.columnconfigure(i, weight=1)

        tk.Button(nav_menu, name="scenario_button", text="Scenarios", width=8, command=lambda: self.set_context(0)) \
            .grid(column=0, row=0, sticky=W + E)
        tk.Button(nav_menu, name="job_button", text="Jobs", width=8, command=lambda: self.set_context(1)) \
            .grid(column=1, row=0, sticky=W + E)
        tk.Button(nav_menu, name="loan_button", text="Loans", width=8, command=lambda: self.set_context(2)) \
            .grid(column=2, row=0, sticky=W + E)
        tk.Button(nav_menu, name="expense_button", text="Expenses", width=8, command=lambda: self.set_context(3)) \
            .grid(column=3, row=0, sticky=W + E)


        self._nav_label = tk.Label(nav_menu, name="nav_label", text=self._context_text[self._context])
        self._nav_label.grid(column=0, row=1, columnspan=4)

        return nav_menu

    def create_drawer(self):
        left_drawer = tk.Frame(self.frame, borderwidth=2, relief='sunken', width=300, height=500)
        left_drawer.grid(column=0, row=1, sticky=N + W + S + E)
        left_drawer.grid_propagate(False)

        return left_drawer

    def create_bottom_menu(self):
        frame = tk.Frame(self.frame, name="left_bottom_menu", width=300, height=50)
        frame.grid(column=0, row=2, sticky=N + W + S + E)

        for i in range(3):
            frame.columnconfigure(i, weight=1)

        # Buttons for the bottom menu. Edit, New, and Delete.
        tk.Button(frame, name="edit_item", text="Edit...", command=edit_item) \
            .grid(column=0, row=0, sticky=W+E)
        tk.Button(frame, name="new_item", text="New...",
                  command=lambda: mid_panel.populate(self.get_context())) \
            .grid(column=1, row=0, sticky=W+E)
        self._del_button = tk.Button(frame, name="delete_item", text="Delete...", state="disabled", command=delete_item)
        self._del_button.grid(column=2, row=0, sticky=W+E)
        tk.Checkbutton(frame, name="delete_check", command=lambda: self.toggle_delete()).grid(column=3, row=0)

        return frame

    def toggle_delete(self):
        if self._del_button['state'] == "disabled":
            self._del_button['state'] = "active"
        else:
            self._del_button['state'] = "disabled"

    def set_context(self, context: int):
        self._nav_label['text'] = self._context_text[context]
        self._context = context

    def get_context(self) -> int:
        return self._context


class MidPanel:
    def __init__(self, parent: tk.Tk):
        self._forms = DetailForm()
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

    def populate(self, context: int):
        for c in self.detail_panel.winfo_children():
            c.destroy()
        panel = self.detail_panel
        form = self._forms.get_form(context)
        self._label.set(form[0])
        for i in range(1, len(form)):
            for j in range(0, len(form[i])):
                type = form[i][j][0]
                text = form[i][j][1]
                name = form[i][j][2]
                col_span = form[i][j][3]
                if type == "Label":
                    tk.Label(panel, text=text).grid(row=i, column=j, columnspan=col_span)
                if type == "Entry":
                    tk.Entry(panel, text=text).grid(row=i, column=j, columnspan=col_span, sticky=W+E)
                if type == "CheckButton":
                    tk.Checkbutton(panel, text=text).grid(row=i, column=j, columnspan=col_span)
                if type == "":
                    tk.Frame(panel, height=10).grid(row=i, column=j, columnspan=col_span)

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
        tk.Button(bMenu, text="Close", command=lambda: self.clear()).grid(column=1, row=0, sticky=W + E)
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
        panel.grid(column=2, row=0, sticky=N+S)

        stat_panel = tk.Frame(panel, borderwidth=2, relief='ridge', width=500, height=573)
        stat_panel.grid(column=0, row=0, rowspan=2, sticky=N+S)


# declare global variables

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
