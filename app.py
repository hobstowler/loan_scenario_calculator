# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import tkinter as tk
import tkinter.ttk as ttk
from scenario import *
from income import *
from dataload import *
from forms import *

colors = {
            "t_type": "navy",
            "t_name": "red",
            "b_sel": "green",
            "b_reset": "SystemButtonFace"
        }


class NavLabel():
    def __init__(self, label: str, detail: str):
        #super.__init__()
        self.label = label
        self.detail = detail

    def get_gui(self, frame: tk.Frame):
        label = tk.Label(frame, text=self.label.capitalize(), justify=LEFT)
        label.pack()


class NavButton(NavLabel):
    def __init__(self, label: str, detail: str, parent, fin_objects: list):
        super(NavButton, self).__init__(label, detail)
        self._fin_list = fin_objects
        self._parent = parent
        self._active = False

    def deactivate(self):
        self._active = False

    def click(self):
        self._active = True
        self._parent.new_context(self, self._fin_list)

    def get_fin_list(self) -> list:
        return self._fin_list

    def get_gui(self, frame: tk.Frame):
        button = tk.Button(frame, text=self.label.capitalize(), width=10)
        button.pack(fill="y")
        button.bind("<Button-1>", lambda e: self.click())
        if self._active:
            button['bg'] = colors.get('b_sel')
        else:
            button['bg'] = colors.get('b_reset')

        return button


class LeftPanel:
    def __init__(self, parent: tk.Tk, fin_vars: dict):
        """
        Initializes the Left Panel for the app. Creates a navigation menu, drawer, and bottom menu for the drawer.
        :param parent: The root for the application.
        :param fin_vars: The financial objects from the loaded data.
        """
        self.frame = tk.Frame(parent, name="leftpanel")
        self.frame.grid(column=0, row=0)

        # drawer variables
        self._drawer_button_sel = None
        # self._selected_fin_obj = None

        # nav menu variables
        self._nav_menu = tk.Frame(self.frame, name="nav_menu", width=25, height=500)
        self._nav_menu.grid(column=0, row=0, sticky=N + W + S + E, rowspan=2, pady=(25, 0))
        self._nav_menu_elements = [
            NavLabel("scenarios", None),
            NavButton("scenarios", "Select a Scenario", self, fin_vars.get("scenarios")),
            NavLabel("income", None),
            NavButton("jobs", "Select a Job", self, fin_vars.get("jobs")),
            NavButton("assets", "Select an Asset", self, fin_vars.get("assets")),
            NavLabel("loans", None),
            NavButton("mortgages", "Select a Mortgage", self, fin_vars.get("loans")),
            NavButton("student", "Select a Student Loan", self, fin_vars.get("loans")),
            NavButton("auto", "Select an Auto Loan", self, fin_vars.get("loans")),
            NavButton("personal", "Select a Personal Loan", self, fin_vars.get("loans")),
            NavLabel("expenses", None),
            NavButton("expenses", "Select an Expense", self, fin_vars.get("expenses")),
            NavButton("taxes", "Select a Tax Bracket", self, fin_vars.get("taxes"))
        ]
        self._nav_selection = self._nav_menu_elements[3]
        self._nav_selection._active = True

        self._nav_text = StringVar()
        self._nav_text.set(self._nav_selection.detail)
        self._nav_label = tk.Label(self.frame, name="nav_label", textvariable=self._nav_text)
        self._nav_label.grid(column=1, row=0, columnspan=5, sticky=N+S+W+E, pady=(1,0))
        self._nav_label.grid_propagate(False)

        # bottom menu variables
        self._del_button = None

        # instantiate major components
        self._nav_menu = tk.Frame(self.frame, name="nav_menu", width=25, height=500)
        self._nav_menu.grid(column=0, row=0, sticky=N + W + S + E, rowspan=2, pady=(25, 0))

        self._drawer = tk.Canvas(self.frame, borderwidth=2, relief='groove', width=300, height=500)
        self._drawer.grid(column=1, row=1, sticky=N + W + S + E)
        self._drawer.pack_propagate(False)
        #self._bottom_menu = self.create_bottom_menu()
        #self._mid_panel = None

        # Populates the drawer with the initial context
        #self.populate_list()
        #self._active = True
        self.populate_nav_menu()

        #TODO implement scroll bar. may need to be part of the refresh

    def new_context(self, clicked: NavButton, fin_list: list):
        self._nav_selection.deactivate()
        self._nav_selection = clicked
        self._nav_text.set(clicked.detail)
        self.populate_nav_menu()
        self.populate_list(clicked.get_fin_list())

    def populate_nav_menu(self) -> None:
        for c in self._nav_menu.winfo_children():
            c.destroy()

        for item in self._nav_menu_elements:
            item.get_gui(self._nav_menu)

    #TODO clean up flow.
    def create_drawer(self) -> Canvas:
        """
        Creates a scrollable drawer that will hold the different items based on selected scenario. Loans, incomes, scenarios,
        taxes, expenses, for example. Called once at start.
        :return: itself, a tk.Canvas object.
        """
        parent = tk.Canvas(self.frame, borderwidth=2, relief='groove', width=300, height=500)
        parent.grid(column=1, row=1, sticky=N + W + S + E)
        parent.pack_propagate(False)

        #scroll = tk.Scrollbar(self.frame, command=parent.yview())
        #scroll.grid(column=2, row=1, sticky=N+S)
        #parent.configure(yscrollcommand=scroll.set)

        return parent

    def create_bottom_menu(self):
        """
        Creates the bottom menu for the drawer. Has buttons to manipulate items in the drawer: New, Edit, and Delete.
        Called once at start.
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

    def populate_list(self, fin_objects: list = None) -> None:
        """
        Populates the drawer with a list of all financial objects of the given context. Called when context changes or
        when returning from mid panel.
        :return: Nothing.
        """
        self._drawer_button_sel = None
        for c in self._drawer.winfo_children():
            c.destroy()
        fin_list = fin_objects
        if fin_list is None:
            return
        for item in fin_list:
            frame = tk.Frame(self._drawer, borderwidth=2, relief='groove', name=item.name().lower(), height=40)
            frame.pack(fill="x", ipady=2, ipadx=2)
            frame.bind("<Button-1>", lambda e, i=item, f=frame: self.drawer_button_click(i, f))

            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)

            name = tk.Label(frame, text=item.name(), justify=LEFT, anchor="w", foreground=colors.get("t_name"))
            name.grid(column=0, row=0, sticky=W)
            f_type = tk.Label(frame, text=item.type(), justify=RIGHT, anchor="e", foreground=colors.get("t_type"))
            f_type.grid(column=1, row=0, sticky=E)
            desc = tk.Label(frame, text=item.desc(), justify=LEFT, anchor="w")
            desc.grid(column=0, row=1, sticky=W, columnspan=2)

            for c in frame.winfo_children():
                c.bind("<Button-1>", lambda e, i=item, f=frame: self.drawer_button_click(i, f))

        self._drawer.configure(scrollregion=(0,0,300,len(fin_list*44)))

    # TODO break populate_list in two to simplify flow. remove Mid Panel altogether and move two a two panel flow
    def populate_editable(self, fin_object: FinanceObj):
        pass

    def drawer_button_click(self, fin_obj, button: Frame) -> None:
        """
        Called when a button in the drawer is clicked. Can be expanded to do specific things based on the type of fin
        object passed, but currently opens the form editor in a disabled mode when clicked.
        :param fin_obj: The financial object contained in the button.
        :param button: The Frame representing the button.
        :return: Nothing.
        """
        if not self._active:
            return
        if self._drawer_button_sel is not None:
            self.recolor_widget_bg(self._drawer_button_sel, self._colors.get("b_reset"))
        if button is None:
            return
        self.recolor_widget_bg(button, self._colors.get("b_sel"))
        self._drawer_button_sel = button
        self._mid_panel.populate_list(fin_obj)
        self.reset_delete_button()

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

    def set_context(self, widget: tk.Button) -> None:
        """
        Sets the context for the Left Panel view. Called when button on Nav Menu is clicked.
        :param widget: The button that was clicked.
        :return: Nothing
        """
        if not self._active:
            return
        if widget.winfo_name() == self.get_context() or widget['state'] == "disabled":
            return

        # resets the current selection and sets the selected color for the new selection
        self.recolor_widget_bg(self._nav_button_sel, self._colors.get("b_reset"))
        self.recolor_widget_bg(widget, self._colors.get("b_sel"))

        # clean up variables
        self._drawer_button_sel = None
        self._nav_button_sel = widget
        self._nav_label['text'] = self._context_vars.get(widget.winfo_name())[0]
        self._mid_panel.reset_panel()
        self.populate_list()
        self.reset_delete_button()

    def get_context(self) -> str:
        """
        Returns the current view context of the Left Panel.
        :return: The current context.
        """
        return self._nav_button_sel.winfo_name()

    def new(self) -> None:
        """
        Method called when the "New" button is clicked in the Left Panel
        :return: Nothing.
        """
        if not self._active:
            return
        self.drawer_button_click(None, None)
        self._mid_panel.populate_list()
        self._mid_panel.activate()
        self.activate("disabled")

    def edit(self) -> None:
        """
        Method called when the "Edit" button is clicked in the Left Panel
        :return: Nothing
        """
        if not self._active:
            return
        if self._drawer_button_sel is None:
            print("nothing is selected")
            return
        self._mid_panel.activate()
        self.activate("disabled")

    def delete(self):
        self._drawer_button_sel

    def toggle_delete(self) -> None:
        """
        Toggles the delete button active state.
        :return: Nothing.
        """
        if not self._active:
            self.reset_delete_button()
            return
        if self._del_button['state'] == "disabled":
            self._del_button['state'] = "active"
        else:
            self._del_button['state'] = "disabled"

    def reset_delete_button(self, state="disabled") -> None:
        """
        Sets the state of the delete button. Disabled by default.
        :param state: The state to change to. Disabled by default.
        :return: None
        """
        self._del_button['state'] = state
        for c in self._bottom_menu.winfo_children():
            if c.winfo_class() == "Checkbutton":
                c.deselect() if state == "disabled" else c.select()

    def activate(self, state="active") -> None:
        """
        Activates/Deactivates the Left Panel. Typically called when focus is returned from editing or new fin obj flow.
        :param state: The new state of the window.
        :return: Nothing.
        """
        if state == "active":
            self._active = True
        else:
            self._active = False

        for c in self._nav_menu.winfo_children():
            if isinstance(c, tk.Button):
                c['state'] = state
        for c in self._drawer.winfo_children():
            if not isinstance(c, tk.Frame):
                c['state'] = state
            else:
                for fc in c.winfo_children():
                    fc['state'] = state
        for c in self._bottom_menu.winfo_children():
            c['state'] = state

        self.reset_delete_button()

    # TODO Can this be done iteratively?
    def add_fin_obj(self, fin_obj: FinanceObj) -> None:
        """
        Adds a financial object to the appropriate list. Called when saving a new object.
        :param fin_obj: The new financial object to be added to the list.
        :return: Nothing.
        """
        context = ""
        if isinstance(fin_obj, Loan):
            context = "loans"
        elif isinstance(fin_obj, Job):
            context = "jobs"
        elif isinstance(fin_obj, Expenses):
            context = "expenses"
        elif isinstance(fin_obj, TaxBracket):
            context = "taxes"
        elif isinstance(fin_obj, Scenario):
            context = "scenarios"

        fin_list = self._context_vars.get(context)[1]
        if fin_obj not in fin_list:
            fin_list.append(fin_obj)

        save_all({context: fin_list})


        self.populate_list()

    def set_mid_panel(self, mid: Frame) -> None:
        """
        Used during initialization of app to set a reference to the mid panel.
        :param mid: The mid panel for the application.
        :return: Nothing.
        """
        self._mid_panel = mid


class MidPanel:
    """
    Represents the Middle Panel of the applications. Used to display detailed information about a selected financial
    object and is also used to edit those objects.
    """
    def __init__(self, parent: tk.Tk):
        """
        Initializes the Middle Panel.
        :param parent: The root of the window.
        """
        self._form = None
        self.frame = tk.Frame(parent)
        self.frame.grid(column=1, row=0, sticky=N+S)

        self._label = StringVar()
        detail_label = tk.Label(self.frame, name="detail_label", textvariable=self._label, width=20)
        detail_label.grid(column=0, row=0, sticky=N+S+W+E, pady=(1, 0))
        detail_label.grid_propagate(False)
        self._label.set("")

        self.detail_panel = tk.Frame(self.frame, name="detail_panel", borderwidth=2, relief='groove', width=300, height=500)
        self.detail_panel.grid(column=0, row=1, sticky=N+E+S+W)
        self.detail_panel.grid_propagate(False)
        self._bottom_menu = None
        self._left_panel = None
        self._right_panel = None

        # buffer for changes on form.
        self._form_buffer = {}

        self._form_vars = {}

    # TODO there is a better way to do this.
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

    def populate_list(self, obj=None) -> None:
        """
        Populates the middle panel with a form corresponding to the selected financial object on the left panel.
        :param active: If true, the panel loads in an editable state.
        :param obj: Used to differentiate between a new object and existing. None if new object.
        :return: Nothing.
        """
        print("populating")
        self.reset_panel(False)
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
                    e.bind("<FocusOut>", lambda e, t=name: self.buffer_change(t))
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
                    s = StringVar()
                    s_var = obj.get_data().get(name)
                    index = form[i][j][5]
                    if s_var is None and index >= 0:
                        s_var = form[i][j][4][index]
                    s.set(s_var)
                    self._form_vars.update({name: s})
                    combo = ttk.Combobox(panel, text=text, textvariable=s)
                    combo.grid(row=i, column=j, columnspan=col_span, sticky=W+E)
                    combo['values'] = form[i][j][4]
                elif tk_type == "Button":
                    button = tk.Button(panel, text=text)
                    button.grid(row=i, column=j, columnspan=col_span, sticky=W+E)
        panel.columnconfigure(0, weight=0)
        panel.columnconfigure(1, weight=2)
        panel.columnconfigure(2, weight=1)
        for c in panel.winfo_children():
            c.grid(pady=(1, 1))
            if c.winfo_class() != "Frame":
                c['state'] = "disabled"

        self.create_bottom_menu()

    def reset_panel(self, clear=True) -> None:
        """
        Resets the middle panel. If the panel should be empty at the end, clear should be True.
        :param clear: Determines whether to fully clear the panel or not.
        :return: Nothing
        """
        print("reset_panel")
        for c in self.detail_panel.winfo_children():
            c.destroy()
        self._form = None
        self._form_vars.clear()
        self._form_buffer = {}
        if clear:
            self._left_panel.activate()
            self._left_panel.populate_list()
            self.destroy_bottom_menu()
            self._label.set("")

    def activate(self, state="active") -> None:
        """
        Used to activate the mid panel to allow editing of the loaded form.
        :param state: active by default.
        :return: Nothing.
        """
        print("activate mid panel")
        if self._bottom_menu is None:
            print("nothing is selected")
            return
        for c in self._bottom_menu.winfo_children():
            if c.winfo_class() != "Frame":
                c['state'] = state
        for c in self.detail_panel.winfo_children():
            if c.winfo_class() != "Frame":
                c['state'] = state

    def buffer_change(self, key: str) -> None:
        """
        Sends a form change to a buffer dict. When save is clicked, buffer writes out to the financial object and saves
        to file.
        :param key: The name of the field used as the key.
        :return: Nothing.
        """
        print("send change:", key)
        s_var = str(self._form_vars.get(key).get())
        if s_var.isnumeric():
            if len(s_var) > 0 and s_var == "0":
                pass
        self._form_buffer.update({key: s_var})
        #self._form.update_fin_obj(self._left_panel.get_context(), {key: s_var})

    def cancel(self) -> None:
        """
        Cancel button for the mid panel. Resets the form and leaves it blank.
        :return: Nothing.
        """
        print("cancel")
        self.reset_panel()


    #TODO change this to call into fin objects update method and send the buffered changes.
    def save(self) -> None:
        """
        Save button for the mid panel. Writes all buffer data to the financial object and clears the panel.
        :return: Nothing.
        """
        print("save")
        if self._form is None:
            return
        for k in self._form_vars.keys():
            self.buffer_change(k)
        fin_obj = self._form.get_fin_obj()
        fin_obj.update(self._form_buffer)
        self._left_panel.add_fin_obj(fin_obj)
        self.reset_panel()

    def destroy_bottom_menu(self):
        """
        Usually called by clear(). "Hides" the bottom menu for the middle panel by destroying the frame.
        :return: None
        """
        print("hide bottom menu")
        if self._bottom_menu is None:
            return
        self._bottom_menu.destroy()
        self._bottom_menu = None

    def set_left_panel(self, left: Frame) -> None:
        """
        Used during initialization of the app to set a reference to the left panel.
        :param left: The left panel for the app.
        :return: Nothing.
        """
        self._left_panel = left

    def set_right_panel(self, right: Frame) -> None:
        """
        Used during initialization of the app to set a reference to the right panel.
        :param right: The right panel for the app.
        :return: Nothing.
        """
        self._right_panel = right


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

    # load the data
    fin_vars = load_all()

    # create the three main panels.
    left_panel = LeftPanel(root, fin_vars)
    mid_panel = MidPanel(root)
    right_panel = RightPanel(root)

    #set panel relationships
    left_panel.set_mid_panel(mid_panel)
    mid_panel.set_left_panel(left_panel)
    mid_panel.set_right_panel(right_panel)

    root.mainloop()

if __name__ == "__main__":
    main()
