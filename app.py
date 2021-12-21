# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import tkinter as tk
import tkinter.ttk as ttk
from main import *
from income import *
from dataload import *
from forms import *


class LeftPanel:
    def __init__(self, parent: tk.Tk, fin_vars: dict):
        self.frame = tk.Frame(parent, name="leftpanel")
        self.frame.grid(column=0, row=0)

        # drawer variables
        self._drawer_button_sel = None
        # self._selected_fin_obj = None

        # nav menu variables
        self._nav_button_sel = "loans"
        self._context_vars = {
            "scenarios": ["Select a Scenario", fin_vars.get("scenarios")],
            "jobs": ["Select a Job", fin_vars.get("jobs")],
            "loans": ["Select a Loan", fin_vars.get("loans")],
            "expenses": ["Select an Expense", fin_vars.get("expenses")],
            "taxes": ["Select a Tax Bracket", fin_vars.get("taxes")]
        }
        self._colors = {
            "t_type": "navy",
            "t_name": "red",
            "b_sel": "green",
            "b_reset": "SystemButtonFace"
        }
        self._nav_label = tk.Label(self.frame, name="nav_label", text=self._context_vars.get(self._nav_button_sel)[0])
        self._nav_label.grid(column=1, row=0, columnspan=5)

        # bottom menu variables
        self._del_button = None

        # instantiate major components
        self._nav_menu = self.create_nav_menu()
        self._drawer = self.create_drawer()
        self._bottom_menu = self.create_bottom_menu()
        self._mid_panel = None

        # Populates the drawer with the initial context
        self.populate()

        #TODO implement scroll bar. may need to be part of the refresh

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
            button.bind("<Button-1>", lambda e, w=button: self.set_context(w))
            if name == self._nav_button_sel:
                self._nav_button_sel = button
                button['bg'] = self._colors.get("b_sel")

        return nav_menu

    #TODO clean up flow.
    def create_drawer(self) -> Canvas:
        """
        Creates a scrollable drawer that will hold the different items based on selected scenario. Loans, incomes, scenarios,
        taxes, expenses, for example.
        :return: itself, a tk.Canvas object.
        """
        parent = tk.Canvas(self.frame, borderwidth=2, relief='sunken', width=300, height=500)
        parent.grid(column=1, row=1, sticky=N + W + S + E)
        parent.grid_propagate(False)
        parent.pack_propagate(False)

        scroll = tk.Scrollbar(self.frame, command=parent.yview())
        scroll.grid(column=2, row=1, sticky=N+S)
        parent.configure(yscrollcommand=scroll.set)

        return parent

    def create_bottom_menu(self):
        """
        Creates the bottom menu for the drawer. Has buttons to manipulate items in the drawer: New, Edit, and Delete.
        :return: itself, a tk.Frame object.
        """
        parent = tk.Frame(self.frame, name="left_bottom_menu", width=300, height=50)
        parent.grid(column=1, row=2, sticky=N + W + S + E)

        for i in range(3):
            parent.columnconfigure(i, weight=1)

        # Buttons for the bottom menu. Edit, New, and Delete.
        tk.Button(parent, name="new_item", text="New...", command=lambda: self.new()) \
            .grid(column=0, row=0, sticky=W+E)
        tk.Button(parent, name="edit_item", text="Edit...", command=lambda: self.edit()) \
            .grid(column=1, row=0, sticky=W+E)
        self._del_button = tk.Button(parent, name="delete_item", text="Delete...", state="disabled", command=lambda: self.delete())
        self._del_button.grid(column=2, row=0, sticky=W+E)
        tk.Checkbutton(parent, name="delete_check", command=lambda: self.toggle_delete()).grid(column=3, row=0)

        return parent

    def populate(self) -> None:
        """
        Populates the drawer with a list of all financial objects of the given context. Called when context changes.
        :return: Nothing.
        """
        for c in self._drawer.winfo_children():
            c.destroy()
        fin_list = self._context_vars.get(self.get_context())[1]
        if fin_list is None:
            return
        for item in fin_list:
            frame = tk.Frame(self._drawer, borderwidth=2, relief='groove', name=item.name().lower(), height=40, width=300)
            frame.pack(fill="x", ipady=2, ipadx=2)
            frame.bind("<Button-1>", lambda e, i=item, f=frame: self.drawer_button_click(i, f))

            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)

            name = tk.Label(frame, text=item.name(), justify=LEFT, anchor="w", foreground=self._colors.get("t_name"))
            name.grid(column=0, row=0, sticky=W)
            f_type = tk.Label(frame, text=item.type(), justify=RIGHT, anchor="e", foreground=self._colors.get("t_type"))
            f_type.grid(column=1, row=0, sticky=E)
            desc = tk.Label(frame, text=item.desc(), justify=LEFT, anchor="w")
            desc.grid(column=0, row=1, sticky=W, columnspan=2)

            for c in frame.winfo_children():
                c.bind("<Button-1>", lambda e, i=item, f=frame: self.drawer_button_click(i, f))

        self._drawer.configure(scrollregion=self._drawer.bbox("all"))

    def drawer_button_click(self, fin_obj, button: Frame) -> None:
        """
        Called when a button in the drawer is clicked. Can be expanded to do specific things based on the type of fin
        object passed, but currently opens the form editor in a disabled mode when clicked.
        :param fin_obj: The financial object contained in the button.
        :param button: The Frame representing the button.
        :return: Nothing.
        """
        if self._drawer_button_sel is not None:
            self.recolor_widget_bg(self._drawer_button_sel, self._colors.get("b_reset"))
        if button is None:
            return
        self.recolor_widget_bg(button, self._colors.get("b_sel"))
        self._drawer_button_sel = button
        self._mid_panel.populate(False, fin_obj)

    def recolor_widget_bg(self, widget, color: str) -> None:
        """
        Changes the background color of the widget.
        :param widget: The widget whose background color will change.
        :param color: The new background color.
        :return: Nothing.
        """
        widget['bg'] = color
        for c in widget.winfo_children():
            c['bg'] = color

    def toggle_delete(self) -> None:
        """
        Toggles the delete button active state.
        :return: Nothing.
        """
        if self._del_button['state'] == "disabled":
            self._del_button['state'] = "active"
        else:
            self._del_button['state'] = "disabled"

    def set_context(self, widget: tk.Button):
        if widget.winfo_name() == self.get_context() or widget['state'] == "disabled":
            return

        # resets the current selection and sets the selected color for the new selection
        self.recolor_widget_bg(self._nav_button_sel, self._colors.get("b_reset"))
        self.recolor_widget_bg(widget, self._colors.get("b_sel"))

        self._drawer_button_sel = None
        self._nav_button_sel = widget
        self._nav_label['text'] = self._context_vars.get(widget.winfo_name())[0]
        self._mid_panel.reset_panel()
        self.populate()

    def get_context(self) -> str:
        return self._nav_button_sel.winfo_name()

    def new(self):
        self.drawer_button_click(None, None)
        self._mid_panel.populate(True)
        self.activate_nav_menu()
        self.activate_drawer()

    # TODO button color does not come back on active state
    def activate_nav_menu(self, state="disabled"):
        for c in self._nav_menu.winfo_children():
            if isinstance(c, tk.Button):
                c['state'] = state

    def activate_drawer(self, state="disabled"):
        for c in self._drawer.winfo_children():
            if not isinstance(c, tk.Frame):
                c['state'] = state

    #TODO disable left panel
    def edit(self):
        if self._drawer_button_sel is None:
            print("nothing is selected")
            return
        self._mid_panel.activate()
        self.activate_nav_menu()

    def delete(self):
        self._drawer_button_sel

    # Can this be done iteratively?
    def add_fin_obj(self, fin_obj: FinanceObj) -> None:
        """
        Adds a financial object to the appropriate list. Called when saving a new object.
        :param fin_obj: The new financial object to be added to the list.
        :return: Nothing.
        """
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

        self.populate()

    def set_mid_panel(self, mid: Frame) -> None:
        """
        Used during initialization of app to set a reference to the mid panel.
        :param mid: The mid panel for the application.
        :return: Nothing.
        """
        self._mid_panel = mid


class MidPanel:
    def __init__(self, parent: tk.Tk):
        self._form = None
        self.frame = tk.Frame(parent)
        self.frame.grid(column=1, row=0, sticky=N+S)

        self._label = StringVar()
        detail_label = tk.Label(self.frame, name="detail_label", textvariable=self._label, width=20)
        detail_label.grid(column=0, row=0, sticky=N+S+W+E, pady=(1, 0))
        detail_label.grid_propagate(False)
        self._label.set("DETAIL")

        self.detail_panel = tk.Frame(self.frame, name="detail_panel", borderwidth=2, relief='sunken', width=300, height=500)
        self.detail_panel.grid(column=0, row=1, sticky=N+E+S+W)
        self.detail_panel.grid_propagate(False)
        self._bottom_menu = None
        self._left_panel = None

        # buffer for changes on form.
        self._form_buffer = {}

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

    def create_bottom_menu(self, active: bool = False):
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
        tk.Button(b_menu, text="Cancel", width=7, command=lambda: self.cancel()).grid(column=1, row=0, sticky=W + E)
        tk.Button(b_menu, text="Save", width=7, command=lambda: self.save()).grid(column=3, row=0, sticky=W + E)
        for c in b_menu.winfo_children():
            if not active and c.winfo_class() != "Frame":
                c['state'] = "disabled"

        self._bottom_menu = b_menu

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
                    self._form_vars.update({name: s})
                    combo = ttk.Combobox(panel, text=text)
                    combo.grid(row=i, column=j, columnspan=col_span, sticky=W+E)
                    combo['values'] = form[i][j][4]
        for c in panel.winfo_children():
            c.grid(pady=(1, 1))
            if not active and c.winfo_class() != "Frame":
                c['state'] = "disabled"

        self.create_bottom_menu(active)

    def reset_panel(self):
        for c in self.detail_panel.winfo_children():
            c.destroy()
            self._form = None
            self._form_vars.clear()

    def activate(self, state="active") -> None:
        """
        Used to activate the mid panel to allow editing of the loaded form.
        :param state: active by default.
        :return: Nothing.
        """
        if self._bottom_menu is None:
            return
        for c in self._bottom_menu.winfo_children():
            if c.winfo_class() != "Frame":
                c['state'] = state
        for c in self.detail_panel.winfo_children():
            if c.winfo_class() != "Frame":
                c['state'] = state

    def send_change(self, key: str):
        s_var = self._form_vars.get(key).get()
        self._form_buffer.update({key: s_var})
        #self._form.update_fin_obj(self._left_panel.get_context(), {key: s_var})

    def cancel(self):
        self.clear()
        self._label.set("")
        self._left_panel.activate_nav_menu("active")
        self._left_panel.drawer_button_click(None, None)


    #TODO change this to call into fin objects update method and send the buffered changes.
    def save(self):
        if self._form is None:
            return
        for k in self._form_vars.keys():
            self.send_change(k)
        self._left_panel.add_fin_obj(self._form.get_fin_obj())
        self.reset_panel()
        self._left_panel.activate_nav_menu("active")

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
        """
        Used during initialization of the app to set a reference to the left panel.
        :param left: The left panel for the app.
        :return: Nothing.
        """
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

    vars = load_all()

    # create the three main panels.
    left_panel = LeftPanel(root, vars)
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


