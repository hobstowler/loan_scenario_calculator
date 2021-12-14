# Author: Hobs Towler
# Date: 12/1/2021
# Description:

from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from main import *
from income import *
from dataload import *
from forms import *


class LeftPanel:
    def __init__(self, parent: tk.Tk):
        self.frame = tk.Frame(parent, name="leftpanel")
        self.frame.grid(column=0, row=0)

        # drawer variables
        self.loans = [
            Loan("Test Loan", "Test Loan Description"), Mortgage("A Second Loan", "This Loan is a Mortgage"),
            Mortgage("A Ssdfgecond Loan", "This Loan is a Mortgage"),
            Mortgage("A Ssdfgecond Loan", "This Loan is a Mortgage"),
            Mortgage("A Secsdfgond Lodsehssdgfn", "This Loan is a Mortgage"),
            Mortgage("A Ssdfgecaerond Loan", "This Loan is a Mortgage"),
            Mortgage("A Sssdfdfgecond Loan", "This Loan is a Mortgage"),
            Mortgage("A Secsdfsdfgsdgond Lodsehssdgfn", "This Loan is a Mortgage"),
            Mortgage("A Ssdfggsdecond Loan", "This Loan is a Mortgage"),
            Mortgage("A sdfgsdf Loan", "This Loan is a Mortgage"),
            Mortgage("A Secsdfgsdffdfgsdfggond Lodsehssdgfn", "This Loan is a Mortgage"),
            Mortgage("A sdfgan", "This Loan is a Mortgage"),
            Mortgage("A Ssdfsfgsgecond Loan", "This Loan is a Mortgage"),
            Mortgage("A Secsdfgond Lodsehssdgfn", "This Loan is a Mortgage"),
            Mortgage("A Ssdfgsdfgsfgecond Loan", "This Loan is a Mortgage"),
            Mortgage("A Ssdfdsfdgfgsdgecond Loan", "This Loan is a Mortgage"),
            Mortgage("A Secsdfgond Lodsehssdgfn", "This Loan is a Mortgage")
        ]
        self.jobs = [Job("First Job", "it sucks")]
        self.expenses = []
        self.taxes = []
        self.scenarios = []
        self._selection = None

        # nav menu variables
        self._nav_label = None
        self._context = "loans"
        self._context_vars = {
            "scenarios": ["Select a Scenario", self.scenarios],
            "jobs": ["Select a Job", self.jobs],
            "loans": ["Select a Loan", self.loans],
            "expenses": ["Select an Expense", self.expenses],
            "taxes": ["Select a Tax Bracket", self.taxes]
        }
        self._colors = {
            "t_type": "navy",
            "t_name": "red",
            "b_sel": "green",
            "b_reset": "SystemButtonFace"
        }

        # bottom menu variables
        self._del_button = None

        # instantiate major components
        self._nav_menu = self.create_nav_menu()
        self._drawer = None
        self._bottom_menu = None
        self._mid_panel = None
        self.create_drawer()
        self.create_bottom_menu()

        #TODO implement scroll bar. may need to be part of the refresh
        self._drawer.configure(scrollregion=self._drawer.bbox("all"))

    def create_nav_menu(self) -> Frame:
        """
        Creates the menu for the left panel. Allows switching between different finance objects.
        :return: The Frame object representing the navigation menu.
        """
        nav_menu = tk.Frame(self.frame, name="nav_menu", width=25, height=500)
        nav_menu.grid(column=0, row=0, sticky=N + W + S + E, rowspan=2, pady=(20, 0))

        for name in self._context_vars.keys():
            button = tk.Button(nav_menu, name=name, text=name.capitalize(), width=10)
            button.pack(fill="y")
            button.bind("<Button-1>", lambda e: self.set_context(e))
            if name == self._context:
                self._context = button
                button.configure(bg=self._colors.get("b_sel"))

        return nav_menu

    #TODO clean up flow.
    def create_drawer(self) -> None:
        self._nav_label = tk.Label(self.frame, name="nav_label", text=self._context_vars.get(self.get_context())[0])
        self._nav_label.grid(column=1, row=0, columnspan=5)

        left_drawer = tk.Canvas(self.frame, borderwidth=2, relief='sunken', width=300, height=500)
        left_drawer.grid(column=1, row=1, sticky=N + W + S + E)
        left_drawer.grid_propagate(False)
        left_drawer.pack_propagate(False)

        scroll = tk.Scrollbar(self.frame, command=left_drawer.yview())
        scroll.grid(column=2, row=1, sticky=N+S)
        left_drawer.configure(yscrollcommand=scroll.set)

        self._drawer = left_drawer
        fin_list = self._context_vars.get(self.get_context())
        self.draw_drawer(fin_list[1])

    def refresh_drawer(self) -> None:
        for c in self._drawer.winfo_children():
            c.destroy()
        fin_list = self._context_vars.get(self.get_context())[1]
        self.draw_drawer(fin_list)

    def draw_drawer(self, fin_list: list) -> None:
        if fin_list is None:
            return
        for list_item in fin_list:
            self.create_drawer_button(list_item)

    #TODO flesh out
    def create_drawer_button(self, item: FinanceObj):
        frame = tk.Frame(self._drawer, borderwidth=2, relief='groove', name=item.name().lower(), height=40, width=300)
        frame.pack(fill="x", ipady=2, ipadx=2)
        frame.bind("<Button-1>", lambda e, i=item, f=frame: self.b_click(i,f))

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        name = tk.Label(frame, text=item.name(), justify=LEFT, anchor="w", foreground=self._colors.get("t_name"))
        name.grid(column=0, row=0, sticky=W)
        f_type = tk.Label(frame, text=item.type(), justify=RIGHT, anchor="e", foreground=self._colors.get("t_type"))
        f_type.grid(column=1, row=0, sticky=E)
        desc = tk.Label(frame, text=item.desc(), justify=LEFT, anchor="w")
        desc.grid(column=0, row=1, sticky=W, columnspan=2)

        for c in frame.winfo_children():
            c.bind("<Button-1>", lambda e, i=item, f=frame: self.b_click(i,f))

    def b_click(self, fin_obj, button: Frame):
        if self._selection is not None:
            self.recolor_button(self._selection, self._colors.get("b_reset"))
        if button is None:
            return
        self.recolor_button(button, self._colors.get("b_sel"))
        self._selection = button
        self._mid_panel.populate(False, fin_obj)

    def recolor_button(self, component, color: str):
        component.configure(bg=color)
        for c in component.winfo_children():
            c.configure(bg=color)

    def create_bottom_menu(self):
        frame = tk.Frame(self.frame, name="left_bottom_menu", width=300, height=50)
        frame.grid(column=1, row=2, sticky=N + W + S + E)
        self._bottom_menu = frame

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

    def toggle_delete(self):
        if self._del_button['state'] == "disabled":
            self._del_button['state'] = "active"
        else:
            self._del_button['state'] = "disabled"

    def set_context(self, event):
        widget = event.widget
        context = widget.winfo_name()
        if context == self.get_context():
            return
        self.recolor_button(self._context, self._colors.get("b_reset"))
        self.recolor_button(widget, self._colors.get("b_sel"))
        self._selection = None
        self._context = widget
        self._nav_label['text'] = self._context_vars.get(self.get_context())[0]
        self.refresh_drawer()

    def get_context(self) -> str:
        return self._context.winfo_name()

    #TODO figure out how to disable the left panel
    def new(self):
        self._mid_panel.populate(True)

    #TODO disable left panel
    def edit(self):
        self._mid_panel.activate()

    def delete(self):
        pass

    # Can this be done iteratively?
    def add_fin_obj(self, fin_obj: FinanceObj):
        if isinstance(fin_obj, Loan):
            fin_list = self._context_vars.get("loans")[1]
        elif isinstance(fin_obj, Job):
            fin_list = self._context_vars.get("jobs")[1]
        elif isinstance(fin_obj, Expenses):
            fin_list = self._context_vars.get("expenses")[1]
        elif isinstance(fin_obj, TaxBracket):
            fin_list = self._context_vars.get("taxes")[1]
        elif isinstance(fin_obj, Scenario):
            fin_list = self._context_vars.get("scenarios")[1]

        if fin_obj not in fin_list:
            fin_list.append(fin_obj)

        self.refresh_drawer()

    def set_mid_panel(self, mid: Frame) -> None:
        self._mid_panel = mid


class MidPanel:
    def __init__(self, parent: tk.Tk):
        self._form = None
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
        self._bottom_menu = None
        self._left_panel = None

        self._form_vars = {}

    def create_new_form(self) -> DetailForm:
        context = self._left_panel.get_context()
        if context == "scenarios":
            return DetailForm(Scenario("new scenario", "new scenario"))
        if context == "loans":
            return DetailForm(Loan("new loan", "new loan"))
        if context == "jobs":
            return DetailForm(Job("new job", "new job"))
        if context == "expenses":
            return DetailForm(Expenses("new expense list", "new expense list"))
        if context == "taxes":
            return DetailForm(TaxBracket("new tax bracket", "new tax bracket"))

    def reset_panel(self):
        for c in self.detail_panel.winfo_children():
            c.destroy()
            self._form = None
            self._form_vars.clear()

    def populate(self, active=False, obj=None):
        self.reset_panel()
        context = self._left_panel.get_context()

        panel = self.detail_panel
        if obj is None:
            self._form = self.create_new_form()
            obj = self._form.get_fin_obj()
        else:
            self._form = DetailForm(obj)

        #TODO make type-based
        form = self._form.get_form(context)

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
                    if name == "name":
                        s.set(obj.name())
                    elif name == "desc":
                        s.set(obj.desc())
                    else:
                        s.set(obj.get_data().get(name))
                    self._form_vars.update({name: s})
                    e = ttk.Entry(panel, textvariable=s, name=name)
                    e.bind("<FocusOut>", lambda e, t=name: self.send_change(t))
                    e.grid(row=i, column=j, columnspan=col_span, sticky=W+E)
                elif tk_type == "CheckButton":
                    var = IntVar()
                    var.set(0)
                    self._form_vars.update({name: var})
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
            if not active and c.winfo_class() != "Frame":
                c['state'] = "disabled"

        self.show_bottom_menu(active)

    def show_bottom_menu(self, active: bool = False):
        """
        "Shows" the bottom menu in the middle panel by creating it.
        :return: None
        """
        b_menu = tk.Frame(self.frame, name="bottom_menu")
        b_menu.grid(column=0, row=2, sticky=N + W + S + E)
        for i in range(5):
            b_menu.columnconfigure(i, weight=1)
            if i % 2 == 0:
                # add padding frames between the two buttons
                tk.Frame(b_menu).grid(column=i, row=0)
        ttk.Button(b_menu, text="Cancel", command=lambda: self.cancel()).grid(column=1, row=0, sticky=W + E)
        ttk.Button(b_menu, text="Save", command=lambda: self.save()).grid(column=3, row=0, sticky=W + E)
        for c in b_menu.winfo_children():
            if not active and c.winfo_class() != "Frame":
                c['state'] = "disabled"

        self._bottom_menu = b_menu

    def activate(self, active=True):
        if self._bottom_menu is None:
            return
        if active:
            for c in self._bottom_menu.winfo_children():
                if c.winfo_class() != "Frame":
                    c['state'] = "active"
            for c in self.detail_panel.winfo_children():
                if c.winfo_class() != "Frame":
                    c['state'] = "active"

    def send_change(self, key: str):
        s_var = self._form_vars.get(key).get()
        print(key)
        self._form.save_data({key: s_var})

    def cancel(self):
        self.clear()
        self._label.set("")

    def save(self):
        if self._form is None:
            return
        for k in self._form_vars.keys():
            self.send_change(k)
        self._left_panel.add_fin_obj(self._form.get_fin_obj())
        self.reset_panel()

    def hide_bottom_menu(self):
        """
        Usually called by clear(). "Hides" the bottom menu for the middle panel by destroying the frame.
        :return: None
        """
        self._bottom_menu.destroy()
        self._bottom_menu = None

    def clear(self):
        """
        Clears the context from the middle panel.
        :return: None
        """
        for c in self.detail_panel.winfo_children():
            c.destroy()
        self.hide_bottom_menu()

    def set_left_panel(self, left: Frame) -> None:
        self._left_panel = left


# TODO implement!
class RightPanel:
    def __init__(self, parent: tk.Tk):
        panel = tk.Frame(parent)
        panel.grid(column=2, row=0, sticky=N+S)

        stat_panel = tk.Frame(panel, borderwidth=2, relief='ridge', width=500, height=550)
        stat_panel.grid(column=0, row=0, rowspan=2, sticky=N+S)


def main():
    # create the root
    root = Tk()
    root.title("Loan Calculator")

    # create the three main panels.
    left_panel = LeftPanel(root)
    mid_panel = MidPanel(root)
    right_panel = RightPanel(root)
    left_panel.set_mid_panel(mid_panel)
    mid_panel.set_left_panel(left_panel)

    # load the data
    load_loans()
    load_jobs()
    load_expenses()
    load_incomes()
    load_scenarios()

    root.mainloop()

main()


