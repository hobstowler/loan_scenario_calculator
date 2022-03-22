# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import tkinter as tk
from tkinter import N, W, S, E, RIGHT

from income import FinanceObj, Job, Assets, Expenses, TaxBracket
from loans import Loan, Mortgage, Student, Auto, Personal
from scenario import Scenario

colors = {
            "l_sel": "lightblue2",
            "l_hover": "lightblue1",
            'l_active_hover': 'lightblue3',
            "b_reset": "SystemButtonFace",
            "b_sel": 'medium turquoise',
            'b_hover': 'turquoise',
            'b_active_hover': 'dark turquoise',
            'fin_type': 'red',
            'save_button': 'green',
            'save_button_hover': 'darkgreen'
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
            self.NavButton(Job, "Select a Job.", self, fin_vars.get("jobs")),
            self.NavButton(Assets, "Select an Asset.", self, fin_vars.get("assets")),
            self.NavLabel("loans"),
            self.NavButton(Mortgage, "Select a Mortgage.", self, fin_vars.get("mortgages")),
            self.NavButton(Student, "Select a Student Loan.", self, fin_vars.get("student loans")),
            self.NavButton(Auto, "Select an Auto Loan.", self, fin_vars.get("auto loans")),
            self.NavButton(Personal, "Select a Personal Loan.", self, fin_vars.get("loans")),
            self.NavLabel("expenses"),
            self.NavButton(Expenses, "Select an Expense.", self, fin_vars.get("expenses")),
            self.NavButton(TaxBracket, "Select a Tax Bracket.", self, fin_vars.get("taxes"))
        ]
        self._nav_selection = self._nav_menu_elements[3]

        self._nav_text = tk.StringVar()
        self._nav_text.set(self._nav_selection.detail + " Right click to modify.")
        self._nav_label = tk.Label(self.frame, name="nav_label", textvariable=self._nav_text)
        self._nav_label.grid(column=1, row=0, columnspan=5, sticky=N+S+W+E, pady=(1, 0))
        self._nav_label.grid_propagate(False)

        # instantiate major components
        self._detail_panel = None
        self._info_panel = None
        self._drawer = tk.Canvas(self.frame, borderwidth=2, relief='groove', width=300, height=600)
        self._drawer.grid(column=1, row=1, sticky=N + W + S + E)
        self._drawer.pack_propagate(False)
        self._bottom_menu = self.BottomMenu(self)
        self._bottom_menu.create(self.frame)
        #self._mid_panel = None

        # Populates the drawer with the initial context
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
            self._fin_obj = label
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
            self._parent.new_context(self)

        # TODO move into LeftPanel and pass key as string instead?
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
            self._parent.populate_info(self._fin_obj.button_hover_message())

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
            self._parent.populate_info("")

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
            self._parent.populate_new()

        def edit(self) -> None:
            """
            Called when clicking edit button. Passthrough to edit the select Finance Object with parent LeftPanel.
            """
            self._parent.edit_selected_fin_object()

        def delete(self) -> None:
            """
            Called when clicking the
            :return:
            """
            self._parent.delete_selected_fin_object()

        def toggle_delete(self) -> None:
            """
            Toggles the delete button on or off when the checkbutton is selected.
            """
            if self._del_button['state'] == "disabled":
                self._del_button['state'] = "active"
            else:
                self._del_button['state'] = "disabled"

        def reset(self) -> None:
            """
            Resets the delete button when changing contexts (new nav menu selection) in LeftPanel.
            """
            self._del_button['state'] = "disabled"
            if self._check_var is not None:
                self._check_var.set(0)

        def create(self, root) -> None:
            """
            Creates the bottom menu using Tkinter widgets.
            :param root: The root frame.
            """
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
            tk.Checkbutton(frame, variable=self._check_var, command=lambda: self.toggle_delete()).grid(column=3, row=0)

            for c in frame.winfo_children():
                if c.winfo_class() == "Button":
                    c.bind("<Enter>", self.enter)
                    c.bind("<Leave>", self.leave)

        @staticmethod
        def enter(e):
            """
            Called when cursor moves over button. Changes background to hover color.
            :param e: The event.
            """
            button = e.widget
            if button['state'] != 'disabled':
                button['bg'] = colors.get('b_hover')

        @staticmethod
        def leave(e):
            """
            Called when cursor leaves button. Changes background back to normal colors.
            :param e: The event.
            """
            button = e.widget
            button['bg'] = colors.get('b_reset')

    #TODO implement saving and loading using JSONs
    def save_all(self):
        pass

    def save_fin_obj(self, fin_obj):
        fin_list = self._nav_selection.get_fin_list()
        print(fin_list)
        if fin_obj not in fin_list:
            fin_list.append(fin_obj)
        self.populate_list(refresh=True)

    def load_all(self):
        pass

    def set_detail_panel(self, panel) -> None:
        self._detail_panel = panel

    def set_info_panel(self, panel) -> None:
        self._info_panel = panel

    def get_root(self) -> tk.Tk:
        return self._root

    # TODO streamline so that Navbutton holds the dict key instead of the list
    def new_context(self, clicked: NavButton) -> None:
        """
        Called when a Navigation button is clicked. Loads the list of FinanceObjs in the drawer and activates
        necessary elements.
        :param clicked: The clicked navigation button.
        """
        # Clear previous selection.
        if self._fin_obj_selection is not None:
            self._fin_obj_selection.activate(False)
            self._fin_obj_selection = None

        self._nav_selection.activate(False)
        self._nav_selection = clicked
        self._nav_selection.activate()
        self._nav_text.set(clicked.detail + " Right click to modify.")

        # refresh to update gui with any active elements
        self._bottom_menu.reset()
        self.populate_nav_menu()
        self.populate_list(clicked.get_fin_list())

    def populate_nav_menu(self) -> None:
        """
        Destroys all child widgets in the navigation menu and repopulates them to bring in updated activation elements.
        """
        for c in self._nav_menu.winfo_children():
            c.destroy()

        for item in self._nav_menu_elements:
            item.get_gui(self._nav_menu)

    def populate_list(self, fin_list: list = None, refresh=False) -> None:
        """
        Populates the drawer with a list of all financial objects of the given context. Called when a navigation button
        is selected or when a FinanceObj in the list activates (is clicked on).
        :param fin_list: The list of fin objects used to populate the list.
        :param refresh: Indicates whether the list is being refreshed or not. If it is, the existing selection is used.
        """
        for c in self._drawer.winfo_children():
            c.destroy()
        if not refresh:
            if self._detail_panel is not None:
                blank_out = True if self._fin_obj_selection is None else False
                self._detail_panel.reset(blank_out)
            if fin_list is None:
                return
        else:
            fin_list = self._nav_selection.get_fin_list()

        for fin_obj in fin_list:
            fin_obj.get_list_button(self._drawer, self)

    def populate_editable(self, fin_object: FinanceObj) -> None:
        """
        Populates the editable view for a selected FinanceObj. Called on right click or clicking the edit button from
        the Bottom Menu.
        :param fin_object: The selected FinanceObj.
        """
        for c in self._drawer.winfo_children():
            c.destroy()
        self._bottom_menu.reset()

        fin_object.get_editable(self._drawer, self)

    def populate_detail(self, fin_object: FinanceObj) -> None:
        """
        Populates the detail window from a finance object selection in the list.
        :param fin_object: The selected Finance Object.
        """
        if self._fin_obj_selection is not None:
            if fin_object != self._fin_obj_selection:
                self._fin_obj_selection.activate(False)
                self._fin_obj_selection = fin_object
        else:
            self._fin_obj_selection = fin_object
        self._detail_panel.reset()
        fin_object.get_detail(self._detail_panel.get_frame(), self)

    def populate_new(self):
        """
        Populated the editable with a new finance object of the type selected in the navigation bar.
        """
        if self._fin_obj_selection is not None:
            self._fin_obj_selection.activate(False)
        new_obj = self._nav_selection._fin_obj('name', 'desc')      # gets the static class and creates a new instance.
        self.populate_editable(new_obj)

    def populate_info(self, message):
        if self._info_panel is None:
            return
        self._info_panel.message(message)

    def delete_selected_fin_object(self):
        """
        Deletes the selected Finance Object in the list view.
        """
        if self._fin_obj_selection is not None:
            self._nav_selection.get_fin_list().remove(self._fin_obj_selection)
            self._fin_obj_selection = None
            self.populate_list(refresh=True)

    def edit_selected_fin_object(self):
        if self._fin_obj_selection is not None:
            self.populate_editable(self._fin_obj_selection)


# TODO implement!
class DetailPanel:
    """
    Class representing a panel to display detailed information about Financial Objects.
    """
    def __init__(self, root: tk.Tk):
        """
        Initializes the Detail Panel
        :param root: Root window tk object.
        """
        self._frame = tk.Frame(root, borderwidth=2, relief='ridge', width=700, height=600)
        self._frame.grid(column=2, row=0, sticky=N + S)
        self._frame.pack_propagate(False)
        self._frame.grid_propagate(False)

        self.reset(True)

    def get_frame(self) -> tk.Frame:
        """
        Returns the base tk.Frame object related to this panel.
        :return: The tk.Frame object.
        """
        return self._frame

    def reset(self, blank=False) -> None:
        """
        Resets the panel and displays a helpful message if the panel is to remain blank until next user input.
        :param blank: Whether the panel will remain blank after the current operations.
        """
        for c in self._frame.winfo_children():
            c.destroy()

        if blank:
            nothing = tk.Label(self._frame, text="Click on something in the drawer to see detailed information.")
            nothing.pack(expand=True)


class InfoPanel:
    """
    Class representing an informational panel in the bottom right of the screen.
    """
    def __init__(self, root: tk.Tk) -> None:
        """
        Initializes the information panel.
        :param root: The root tk window.
        """
        self._frame = tk.Frame(root, height=15)
        self._frame.grid(column=0, row=1, columnspan=3, sticky=W+E)
        self._frame.pack_propagate(False)

        self._info = tk.StringVar()
        self._info.set("Testing information panel...")
        label = tk.Label(self._frame, textvariable=self._info)
        label.pack(side=RIGHT)

    def message(self, message: str) -> None:
        """
        Sets the message in the info panel.
        :param message: The message to be set.
        """
        self._info.set(message)

    def clear(self) -> None:
        """
        Clears the message.
        """
        self.message("")


def main():
    # create the root
    root = tk.Tk()
    root.title("Loan Calculator")
    root.tk_setPalette(background='#fff')

    # load the data
    fin_vars = {
        'scenarios': [Scenario('test scenario', 'scenario description')],
        'jobs': [Job('Data Analyst II', 'Cerner Corporation'), Job('Data Analyst I', 'Cerner Corporation')],
        'assets': [],
        'mortgages': [Mortgage('7129 Grand Ave', 'Kansas City, MO 64114')],
        'student loans': [Student('Virginia Tech', 'BA in English Literature')],
        'loans': [Loan('test loan', 'test description')],
        'taxes': []
    }

    # create the main panels.
    left_panel = LeftPanel(root, fin_vars)
    right_panel = DetailPanel(root)
    info_panel = InfoPanel(root)

    #set panel relationships
    left_panel.set_detail_panel(right_panel)
    left_panel.set_info_panel(info_panel)

    root.mainloop()


if __name__ == "__main__":
    main()
