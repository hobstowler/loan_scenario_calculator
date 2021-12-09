# Author: Hobs Towler
# Date: 12/1/2021
# Description:

from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from main import *
from income import *
from dataload import *
from Forms import *


class LeftPanel:
    def __init__(self, parent: tk.Tk):
        self.frame = tk.Frame(parent, name="leftpanel")
        self.frame.grid(column=0, row=0)

        # drawer variables
        self.loans = []
        self.jobs = []
        self.expenses = []
        self.taxes = []
        self.scenarios = []

        # nav menu variables
        self._nav_label = None
        self._context = "loan"
        self._context_vars = {
            "scenario": ["Select a Scenario.", self.scenarios],
            "job": ["Select a Job.", self.jobs],
            "loan": ["Select a Loan.", self.loans],
            "expense": ["Select an Expense.", self.expenses],
            "tax": ["Select a Tax Bracket", self.taxes]
        }

        # bottom menu variables
        self._del_button = None

        # instantiate major components
        self._nav_menu = self.create_nav_menu()
        self._drawer = self.create_drawer()
        self._bottom_menu = self.create_bottom_menu()

        #self.set_context(2)

    def create_nav_menu(self):
        """
        Creates the menu for the left panel. Allows switching between different finance objects.
        :return: The Frame object representing the navigation menu.
        """
        nav_menu = tk.Frame(self.frame, name="nav_menu", width=25, height=500)
        nav_menu.grid(column=0, row=0, sticky=N + W + S + E, rowspan=2, pady=(20, 0))
        for i in range(5):
            nav_menu.rowconfigure(i, weight=1)

        # Create the buttons to switch between different contexts in Left Panel
        b1 = ttk.Button(nav_menu, name="scenario", text="Scenarios", width=10)
        b1.pack(fill="y")
        b1.bind("<Button-1>", lambda t=0: self.set_context(t))
        b2 = ttk.Button(nav_menu, name="job", text="Jobs", width=10)
        b2.pack(fill="y")
        b2.bind("<Button-1>", lambda t=1: self.set_context(t))
        b3 = ttk.Button(nav_menu, name="loan", text="Loans", width=10)
        b3.pack(fill="y")
        b3.bind("<Button-1>", lambda t=2: self.set_context(t))
        b4 = ttk.Button(nav_menu, name="expense", text="Expenses", width=10)
        b4.pack(fill="y")
        b4.bind("<Button-1>", lambda t=3: self.set_context(t))
        b5 = ttk.Button(nav_menu, name="tax", text="Tax Brackets", width=10)
        b5.pack(fill="y")
        b5.bind("<Button-1>", lambda t=4: self.set_context(t))

        return nav_menu

    def create_drawer(self):
        self._nav_label = tk.Label(self.frame, name="nav_label", text=self._context_vars[self._context])
        self._nav_label.grid(column=1, row=0, columnspan=5)

        left_drawer = tk.Frame(self.frame, borderwidth=2, relief='sunken', width=300, height=500)
        left_drawer.grid(column=1, row=1, sticky=N + W + S + E)
        left_drawer.grid_propagate(False)

        return left_drawer

    def create_bottom_menu(self):
        frame = tk.Frame(self.frame, name="left_bottom_menu", width=300, height=50)
        frame.grid(column=1, row=2, sticky=N + W + S + E)

        for i in range(3):
            frame.columnconfigure(i, weight=1)

        # Buttons for the bottom menu. Edit, New, and Delete.
        tk.Button(frame, name="new_item", text="New...", command=lambda: self.new()) \
            .grid(column=0, row=0, sticky=W+E)
        tk.Button(frame, name="edit_item", text="Edit...", command=lambda: self.edit()) \
            .grid(column=1, row=0, sticky=W+E)
        self._del_button = tk.Button(frame, name="delete_item", text="Delete...", state="disabled", command=lambda: self.delete())
        self._del_button.grid(column=2, row=0, sticky=W+E)
        tk.Checkbutton(frame, name="delete_check", command=lambda: self.toggle_delete()).grid(column=3, row=0)

        return frame

    def toggle_delete(self):
        if self._del_button['state'] == "disabled":
            self._del_button['state'] = "active"
        else:
            self._del_button['state'] = "disabled"

    def set_context(self, context):
        self._context = context.widget.winfo_name()
        self._nav_label['text'] = self._context_vars.get(self._context)[0]

    def get_context(self) -> int:
        return self._context

    def refresh_drawer(self):
        for c in self._drawer:
            c.destroy()
        self.draw_drawer(self._context_vars.get(self.get_context()[1]), self._drawer)

    def draw_drawer(self, fin_list: list, root: tk.Frame):
        pass

    #TODO figure out how to disable the left panel
    def new(self):
        mid_panel.populate(self.get_context())

    #TODO disable left panel
    def edit(self):
        pass

    def delete(self):
        pass


class MidPanel:
    def __init__(self, parent: tk.Tk):
        self._forms = None
        panel = tk.Frame(parent)
        self.frame = panel
        panel.grid(column=1, row=0, sticky=N+S)

        self._label = StringVar()
        detail_label = tk.Label(panel, name="detail_label", textvariable=self._label, width=20)
        detail_label.grid(column=0, row=0, sticky=N+S+W+E, pady=(1, 0))
        detail_label.grid_propagate(False)
        self._label.set("DETAIL")

        self.detail_panel = tk.Frame(panel, name="detail_panel", borderwidth=2, relief='sunken', width=300, height=500)
        self.detail_panel.grid(column=0, row=1, sticky=N+E+S+W)
        self.detail_panel.grid_propagate(False)

        self._formvars = {}

    def populate(self, context: str, obj=None):
        for c in self.detail_panel.winfo_children():
            c.destroy()
            self._forms = None
            #TODO make this save?
            self._formvars.clear()

        panel = self.detail_panel
        if obj is None:
            self._forms = DetailForm()

        form = self._forms.get_form(context)
        self._label.set(form[0])
        for i in range(1, len(form)):
            for j in range(0, len(form[i])):
                tk_type = form[i][j][0]
                text = form[i][j][1]
                name = form[i][j][2]
                col_span = form[i][j][3]
                if tk_type == "Label":
                    tk.Label(panel, text=text, name=name)\
                        .grid(row=i, column=j, columnspan=col_span)
                elif tk_type == "Entry":
                    s = StringVar()
                    self._formvars.update({name: s})
                    e = ttk.Entry(panel, textvariable=s, name=name)
                    e.bind("<FocusOut>", lambda t=name: self.callback(t))
                    e.grid(row=i, column=j, columnspan=col_span, sticky=W+E)
                elif tk_type == "CheckButton":
                    var = IntVar()
                    var.set(0)
                    self._formvars.update({name: var})
                    check = ttk.Checkbutton(panel, text=text, name=name, variable=var, onvalue=1, offvalue=0)
                    check.grid(row=i, column=j, columnspan=col_span)
                elif tk_type == "Space":
                    tk.Frame(panel, height=10).grid(row=i, column=j, columnspan=col_span)
                elif tk_type == "Combo":
                    combo = ttk.Combobox(panel, text=text)
                    combo.grid(row=i, column=j, columnspan=col_span, sticky=W+E)
                    combo['values'] = form[i][j][4]
        for c in panel.winfo_children():
            c.grid(pady=(1, 1))

        print(self._formvars)

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
        ttk.Button(bMenu, text="Cancel", command=lambda: self.cancel()).grid(column=1, row=0, sticky=W + E)
        ttk.Button(bMenu, text="Save", command=lambda: self.save()).grid(column=3, row=0, sticky=W + E)

    def callback(self, t: str):
        text = t.widget.winfo_name()
        s_var = self._formvars.get(text)
        #print(s_var.get())
        if isinstance(s_var, StringVar):
            print(s_var.get())

    def cancel(self):
        self.clear()
        self._label.set("")

    def save(self):
        pass

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

        stat_panel = tk.Frame(panel, borderwidth=2, relief='ridge', width=500, height=550)
        stat_panel.grid(column=0, row=0, rowspan=2, sticky=N+S)


# declare global variables

# create the root
root = Tk()
root.title("Loan Calculator")

# create the three main panels.
left_panel = LeftPanel(root)
mid_panel = MidPanel(root)
right_panel = RightPanel(root)

# load the data
load_loans()
load_jobs()
load_expenses()
load_incomes()
load_scenarios()

#def print_hierarchy(w, depth=0):
    #print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    #for i in w.winfo_children():
        #print_hierarchy(i, depth+1)
#print_hierarchy(root)

root.mainloop()
