# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, W, S, E

from dataload import save_all
from forms import DetailForm
from income import FinanceObj, Job, TaxBracket
from loans import Loan, Mortgage, Student
from scenario import Scenario

colors = {
            "t_type": "navy",
            "t_name": "red",
            "b_sel": "green",
            "b_reset": "SystemButtonFace"
        }


class NavLabel:
    """Text label on the top-level navigation menu."""
    def __init__(self, label: str):
        """
        Initializes the label object.
        :param label: Label string.
        """
        #super.__init__()
        self.label = label

    def get_gui(self, root: tk.Frame) -> None:
        """
        Creates the visual using tkinter Label.
        :param root: The parent frame.
        :return: Nothing
        """
        label = tk.Label(root, width=13, text=self.label.capitalize(), anchor='w')
        label.pack()


class NavButton(NavLabel):
    """Button on the top-level navigation menu."""
    def __init__(self, label: FinanceObj, detail: str, parent, fin_objects: list):
        super(NavButton, self).__init__(label.__str__())
        print(repr(label))
        print("test:", label.__str__())
        self.detail = detail
        self._fin_list = fin_objects
        self._parent = parent
        self._active = False

    def activate(self, active=True) -> None:
        """
        Activates the button. Behaviour when button is selected.
        :param active:
        :return:
        """
        self._active = active

    def click(self):
        self._active = True
        self._parent.new_context(self, self._fin_list)

    def get_fin_list(self) -> list:
        return self._fin_list

    def get_gui(self, root: tk.Frame):
        button = tk.Button(root, text=self.label.capitalize(), width=10)
        button.pack()
        button.bind("<Button-1>", lambda e: self.click())
        if self._active:
            button['bg'] = colors.get('b_sel')
        else:
            button['bg'] = colors.get('b_reset')

        return button


class BottomMenu():
    def __init__(self, parent):
        self._parent = parent
        self._del_button = None

    def new(self) -> None:
        pass
        #if not self._active:
        #    return
        #self.drawer_button_click(None, None)
        #self._mid_panel.populate_list()
        #self._mid_panel.activate()
        #self.activate("disabled")

    def edit(self) -> None:
        pass
        #if not self._active:
        #    return
        #if self._drawer_button_sel is None:
        #    print("nothing is selected")
        #    return
        #self._mid_panel.activate()
        #self.activate("disabled")

    def delete(self):
        pass
        #self._drawer_button_sel

    def toggle_delete(self):
        if self._del_button['state'] == "disabled":
            self._del_button['state'] = "active"
        else:
            self._del_button['state'] = "disabled"

    def reset(self):
        self._del_button['state'] = "disabled"

    def create(self, root):
        bottom_menu = tk.Frame(root, name="left_bottom_menu", width=300, height=50)
        bottom_menu.grid(column=1, row=2, sticky=N + W + S + E)

        for i in range(3):
            bottom_menu.columnconfigure(i, weight=1)

        # Buttons for the bottom menu. Edit, New, and Delete.
        tk.Button(bottom_menu, name="new_item", text="New...", command=lambda: self.new()) \
            .grid(column=0, row=0, sticky=W + E)
        tk.Button(bottom_menu, name="edit_item", text="Edit...", command=lambda: self.edit()) \
            .grid(column=1, row=0, sticky=W + E)
        self._del_button = tk.Button(bottom_menu, name="delete_item", text="Delete...", state="disabled",
                                     command=lambda: self.delete())
        self._del_button.grid(column=2, row=0, sticky=W + E)
        tk.Checkbutton(bottom_menu, name="delete_check", command=lambda: self.toggle_delete()).grid(column=3, row=0)


class LeftPanel:
    def __init__(self, root: tk.Tk, fin_vars: dict):
        """
        Initializes the Left Panel for the app. Creates a navigation menu, drawer, and bottom menu for the drawer.
        :param root: The root for the application.
        :param fin_vars: The financial objects from the loaded data.
        """
        self._root = root
        self.frame = tk.Frame(self._root, name="leftpanel")
        self.frame.grid(column=0, row=0)

        # drawer variables
        self._fin_obj_selection = None

        # nav menu variables
        self._nav_menu = tk.Frame(self.frame, name="nav_menu", width=25, height=600)
        self._nav_menu.grid(column=0, row=0, sticky=N + W + S + E, rowspan=2, pady=(25, 0))
        self._nav_menu_elements = [
            NavLabel("scenarios"),
            NavButton(Scenario, "Select a Scenario.", self, fin_vars.get("scenarios")),
            NavLabel("income"),
            NavButton("jobs", "Select a Job.", self, fin_vars.get("jobs")),
            NavButton("assets", "Select an Asset.", self, fin_vars.get("assets")),
            NavLabel("loans"),
            NavButton("mortgage", "Select a Mortgage.", self, fin_vars.get("mortgages")),
            NavButton("student", "Select a Student Loan.", self, fin_vars.get("student loans")),
            NavButton("auto", "Select an Auto Loan.", self, fin_vars.get("auto loans")),
            NavButton("personal", "Select a Personal Loan.", self, fin_vars.get("loans")),
            NavLabel("expenses"),
            NavButton("expenses", "Select an Expense.", self, fin_vars.get("expenses")),
            NavButton("taxes", "Select a Tax Bracket.", self, fin_vars.get("taxes"))
        ]
        self._nav_selection = self._nav_menu_elements[3]
        #self._nav_selection._active = True

        self._nav_text = tk.StringVar()
        self._nav_text.set(self._nav_selection.detail + " Right click to modify.")
        self._nav_label = tk.Label(self.frame, name="nav_label", textvariable=self._nav_text)
        self._nav_label.grid(column=1, row=0, columnspan=5, sticky=N+S+W+E, pady=(1, 0))
        self._nav_label.grid_propagate(False)

        # instantiate major components
        self._detail_panel = None
        self._drawer = tk.Canvas(self.frame, borderwidth=2, relief='groove', width=300, height=600)
        self._drawer.grid(column=1, row=1, sticky=N + W + S + E)
        self._drawer.pack_propagate(False)
        self._bottom_menu = BottomMenu(self)
        self._bottom_menu.create(self.frame)
        #self._mid_panel = None

        # Populates the drawer with the initial context
        #self.populate_list()
        #self._active = True
        self.populate_nav_menu()
        self._nav_selection.click()

        #TODO implement scroll bar. may need to be part of the refresh

    def set_detail_panel(self, panel) -> None:
        self._detail_panel = panel

    def get_root(self) -> tk.Tk:
        return self._root

    def new_context(self, clicked: NavButton, fin_list: list):
        print("new context")
        if self._fin_obj_selection is not None:
            print("clear fin obj")
            self._fin_obj_selection.activate(False)
            self._fin_obj_selection = None
        self._nav_selection.activate(False)
        self._nav_selection = clicked
        self._nav_selection.activate()
        self._nav_text.set(clicked.detail + " Right click to modify.")
        self.populate_nav_menu()
        self.populate_list(clicked.get_fin_list())

    def populate_nav_menu(self) -> None:
        for c in self._nav_menu.winfo_children():
            c.destroy()

        for item in self._nav_menu_elements:
            item.get_gui(self._nav_menu)

    def populate_list(self, fin_list: list = None, refresh=False) -> None:
        """
        Populates the drawer with a list of all financial objects of the given context. Called when context changes or
        when returning from mid panel.
        :return: Nothing.
        """
        if self._detail_panel is not None and not refresh:
            self._detail_panel.reset()
        for c in self._drawer.winfo_children():
            c.destroy()

        if not refresh:
            if fin_list is None:
                return
        else:
            print("refreshing")
            fin_list = self._nav_selection.get_fin_list()

        for fin_obj in fin_list:
            fin_obj.get_list_button(self._drawer, self)

    # TODO break populate_list in two to simplify flow. remove Mid Panel altogether and move two a two panel flow
    def populate_editable(self, fin_object: FinanceObj, active=False):
        for c in self._drawer.winfo_children():
            c.destroy()

        fin_object.get_editable(self._drawer, self)

    def populate_detail(self, fin_object: FinanceObj):
        if self._fin_obj_selection is not None:
            if fin_object != self._fin_obj_selection:
                self._fin_obj_selection.activate(False)
                self._fin_obj_selection = fin_object
        else:
            self._fin_obj_selection = fin_object
        self._detail_panel.reset()
        fin_object.get_detail(self._detail_panel.get_frame(), self)

    def populate_new(self):
        self._nav_selection
        self.populate_editable()

    def drawer_button_click(self, fin_obj, button: tk.Frame) -> None:
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


# TODO implement!
class RightPanel:
    def __init__(self, root: tk.Tk):
        self._frame = tk.Frame(root, borderwidth=2, relief='ridge', width=600, height=600)
        self._frame.grid(column=2, row=0, sticky=N + S)
        self._frame.pack_propagate(False)

        #stat_panel = tk.Frame(self._frame, borderwidth=2, relief='ridge', width=500, height=550)
        #stat_panel.grid(column=0, row=0, rowspan=2, sticky=N+S)

    def get_frame(self) -> tk.Frame:
        return self._frame

    def reset(self) -> None:
        for c in self._frame.winfo_children():
            c.destroy()


def main():
    # create the root
    root = tk.Tk()
    root.title("Loan Calculator")

    # load the data
    #fin_vars = load_all()
    #save_all(fin_vars)
    fin_vars = {
        'scenarios': [Scenario('test scenario', 'scenario description')],
        'jobs': [Job('Data Analyst II', 'Cerner Corporation'),Job('Data Analyst I', 'Cerner Corporation')],
        'assets': [],
        'mortgages': [Mortgage('7129 Grand Ave', 'Kansas City, MO 64114')],
        'student loans': [Student('Virginia Tech', 'BA in English Literature')],
        'loans': [Loan('test loan', 'test description')]
    }

    # create the three main panels.
    left_panel = LeftPanel(root, fin_vars)
    #mid_panel = MidPanel(root)
    right_panel = RightPanel(root)

    #set panel relationships
    left_panel.set_detail_panel(right_panel)

    root.mainloop()

if __name__ == "__main__":
    main()
