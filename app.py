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
            "l_sel": "lightblue2",
            "l_hover": "lightblue1",
            'l_active_hover': 'lightblue3',
            "b_reset": "SystemButtonFace",
            "b_sel": 'medium turquoise',
            'b_hover': 'turquoise',
            'b_active_hover': 'dark turquoise'
        }


class LeftPanel:
    def __init__(self, root: tk.Tk, fin_vars: dict):
        """
        Initializes the Left Panel for the app. Creates a navigation menu, drawer, and bottom menu for the drawer.
        :param root: The root for the application.
        :param fin_vars: The financial objects from the loaded data.
        """
        self._root = root
        self._fin_vars = fin_vars

        self.frame = tk.Frame(self._root, name="leftpanel")
        self.frame.grid(column=0, row=0)

        # drawer variables
        self._fin_obj_selection = None

        # nav menu variables
        self._nav_menu = tk.Frame(self.frame, name="nav_menu", width=25, height=600)
        self._nav_menu.grid(column=0, row=0, sticky=N + W + S + E, rowspan=2, pady=(25, 0))
        self._nav_menu_elements = [
            self.NavLabel("scenarios"),
            self.NavButton(Scenario, "Select a Scenario.", self, fin_vars.get("scenarios")),
            self.NavLabel("income"),
            self.NavButton("jobs", "Select a Job.", self, fin_vars.get("jobs")),
            self.NavButton("assets", "Select an Asset.", self, fin_vars.get("assets")),
            self.NavLabel("loans"),
            self.NavButton("mortgage", "Select a Mortgage.", self, fin_vars.get("mortgages")),
            self.NavButton("student", "Select a Student Loan.", self, fin_vars.get("student loans")),
            self.NavButton("auto", "Select an Auto Loan.", self, fin_vars.get("auto loans")),
            self.NavButton("personal", "Select a Personal Loan.", self, fin_vars.get("loans")),
            self.NavLabel("expenses"),
            self.NavButton("expenses", "Select an Expense.", self, fin_vars.get("expenses")),
            self.NavButton("taxes", "Select a Tax Bracket.", self, fin_vars.get("taxes"))
        ]
        self._nav_selection = self._nav_menu_elements[3]

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
        self._bottom_menu = self.BottomMenu(self)
        self._bottom_menu.create(self.frame)
        #self._mid_panel = None

        # Populates the drawer with the initial context
        #self.populate_list()
        #self._active = True
        self.populate_nav_menu()
        self._nav_selection.click()

        #TODO implement scroll bar. may need to be part of the refresh

    class NavLabel:
        """Text label on the top-level navigation menu."""
        def __init__(self, label: str):
            """
            Initializes the label object.
            :param label: Label string.
            """
            # super.__init__()
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
            super().__init__(label.__str__())
            self.detail = detail
            self._fin_list = fin_objects
            self._parent = parent
            self._active = False

        def activate(self, active=True) -> None:
            """
            Activates the button. Behavior when button is clicked.
            :param active:
            """
            self._active = active

        def click(self, e=None) -> None:
            """
            Called when button is clicked on.
            """
            self.activate()
            self._parent.new_context(self, self._fin_list)

        # TODO move into LeftPanel and pass key string instead?
        def get_fin_list(self) -> list:
            """
            Gets the list of financial objects associates with this Nav Button.
            :return:
            """
            return self._fin_list

        def enter(self, e):
            """
            Called when cursor moves over button. Changes background to hover color.
            :param e: The event.
            """
            button = e.widget
            if self._active:
                button['bg'] = colors.get('b_active_hover')
            else:
                button['bg'] = colors.get('b_hover')

        def leave(self, e):
            """
            Called when cursor leaves button. Changes background back to normal colors.
            :param e: The event.
            :return:
            """
            button = e.widget
            if self._active:
                button['bg'] = colors.get('b_sel')
            else:
                button['bg'] = colors.get('b_reset')

        def get_gui(self, root: tk.Frame) -> tk.Button:
            """
            Creates the Navigation button with Tkinter widgets.
            :param root: The root widget.
            """
            button = tk.Button(root, text=self.label.capitalize(), width=10)
            button.pack()
            button.bind("<Button-1>", self.click)
            button.bind("<Enter>", self.enter)
            button.bind("<Leave>", self.leave)
            if self._active:
                button['bg'] = colors.get('b_sel')
            else:
                button['bg'] = colors.get('b_reset')

            return button

    class BottomMenu:
        """Class representing the bottom menu with controls for editing, deleting, and creating new items."""
        def __init__(self, parent):
            """
            Initializes the bottom menu.
            :param parent: The parent LeftPanel object.
            """
            self._parent = parent
            self._del_button = None
            self._check_var = None

        def new(self) -> None:
            """
            Called when clicking new button. Passthrough to create a new Finance Object with parent LeftPanel.
            """
            self._parent.new_fin_object()

        def edit(self) -> None:
            """
            Called when clicking edit button. Passthrough to edit the select Finance Object with parent LeftPanel.
            """
            self._parent.edit_selected_fin_object()

        def delete(self):
            """
            Called when clicking the
            :return:
            """
            self._parent.delete_selected_fin_object()

        def toggle_delete(self):
            if self._del_button['state'] == "disabled":
                self._del_button['state'] = "active"
            else:
                self._del_button['state'] = "disabled"

        def reset(self):
            self._del_button['state'] = "disabled"
            if self._check_var is not None:
                self._check_var.set(0)

        @staticmethod
        def enter(e):
            """
            Called when cursor moves over button. Changes background to hover color.
            :param e: The event.
            """
            button = e.widget
            if button['state'] != 'disabled':
                button['bg'] = colors.get('b_hover')

        def leave(self, e):
            """
            Called when cursor leaves button. Changes background back to normal colors.
            :param e: The event.
            :return:
            """
            button = e.widget
            button['bg'] = colors.get('b_reset')

        def create(self, root):
            frame = tk.Frame(root, name="left_bottom_menu", width=300, height=50)
            frame.grid(column=1, row=2, sticky=N + W + S + E)

            for i in range(3):
                frame.columnconfigure(i, weight=1)

            # Buttons for the bottom menu. Edit, New, and Delete.
            tk.Button(frame, text="New", command=lambda: self.new()).grid(column=0, row=0, sticky=W + E)
            tk.Button(frame, text="Edit", command=lambda: self.edit()).grid(column=1, row=0, sticky=W + E)
            self._del_button = tk.Button(frame, text="Delete", state="disabled", command=lambda: self.delete())
            self._del_button.grid(column=2, row=0, sticky=W + E)
            self._check_var = tk.IntVar()
            self._check_var.set(0)
            tk.Checkbutton(frame, variable=self._check_var, command=lambda: self.toggle_delete())\
                .grid(column=3, row=0)

            for c in frame.winfo_children():
                if c.winfo_class() == "Button":
                    c.bind("<Enter>", self.enter)
                    c.bind("<Leave>", self.leave)

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
        self._bottom_menu.reset()
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

    #TODO implement
    def populate_new(self):
        self._nav_selection
        self.populate_editable()

    def delete_selected_fin_object(self):
        if self._fin_obj_selection is not None:
            self._nav_selection.get_fin_list().remove(self._fin_obj_selection)
            self._fin_obj_selection = None
            self.populate_list(refresh=True)

    def edit_selected_fin_object(self):
        if self._fin_obj_selection is not None:
            self.populate_editable(self._fin_obj_selection)


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
        'jobs': [Job('Data Analyst II', 'Cerner Corporation'), Job('Data Analyst I', 'Cerner Corporation')],
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
