# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import tkinter as tk
from tkinter import N, W, S, E, RIGHT, ttk

from income import FinanceObj, Job, Assets, Expenses, TaxBracket
from loans import Loan, Mortgage, Student, Auto, Personal
from misc import Style, Bracket
from scenario import Scenario


class App:
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

        #TODO implement scroll bar. may need to be part of the refresh

    def launch(self):
        fin_vars = self._fin_vars
        root = self._root
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
            self.NavLabel("loans"),
            self.NavButton(Mortgage, "Select a Mortgage.", self, fin_vars.get("mortgages")),
            self.NavButton(Student, "Select a Student Loan.", self, fin_vars.get("student loans")),
            self.NavButton(Auto, "Select an Auto Loan.", self, fin_vars.get("auto loans")),
            self.NavButton(Personal, "Select a Personal Loan.", self, fin_vars.get("loans")),
            self.NavLabel("misc"),
            self.NavButton(Assets, "Select an Asset.", self, fin_vars.get("assets")),
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
        self._detail_panel = self.DetailPanel(root)
        self._info_panel = self.InfoPanel(root)
        self._drawer = tk.Canvas(self.frame, borderwidth=2, relief='groove', width=300, height=600)
        self._drawer.grid(column=1, row=1, sticky=N + W + S + E)
        self._drawer.pack_propagate(False)
        self._bottom_menu = self.BottomMenu(self)
        self._bottom_menu.create(self.frame)

        # Populates the drawer with the initial context
        self.populate_nav_menu()
        self._nav_selection.click()

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
        def __init__(self, label, detail: str, parent, fin_objects: list):
            super().__init__(label.__str__())
            if fin_objects is None:
                fin_objects = []
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
                button['bg'] = Style.color('b_active_hover')
            else:
                button['bg'] = Style.color('b_hover')
            self._parent.populate_info(self._fin_obj.button_hover_message())

        def leave(self, e):
            """
            Called when cursor leaves button. Changes background back to normal colors.
            :param e: The event.
            :return:
            """
            button = e.widget
            if self._active:
                button['bg'] = Style.color('b_sel')
            else:
                button['bg'] = Style.color('b_reset')
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
                button['bg'] = Style.color('b_sel')
            else:
                button['bg'] = Style.color('b_reset')

            return button

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
            self._frame.grid(column=0, row=1, columnspan=3, sticky=W + E)
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
            self._parent.create_new_fin_object()

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
                button['bg'] = Style.color('b_hover')

        @staticmethod
        def leave(e):
            """
            Called when cursor leaves button. Changes background back to normal colors.
            :param e: The event.
            """
            button = e.widget
            button['bg'] = Style.color('b_reset')

    #TODO implement saving and loading using JSONs
    def save_all(self):
        pass

    def load_all(self):
        pass

    def save_fin_obj(self, fin_obj):
        """
        Saves a new Finance Object when returning from the New dialogue evoked from the bottom menu button.
        :param fin_obj: The new Finance Object.
        """
        fin_list = self._nav_selection.get_fin_list()
        if fin_obj not in fin_list:
            fin_list.append(fin_obj)
        self.populate_list(refresh=True)

    def get_fin_vars(self, key: str = None) -> list:
        """
        Return the list finance objects of a given type based on key.
        :param key: The key in the key value pair of finance objects in list.
        :return: a list of finance object for given key.
        """
        if key is None:
            return self._fin_vars
        else:
            fin_vars = self._fin_vars.get(key)
            if fin_vars is None:
                fin_vars = []
                self._fin_vars.update({key: fin_vars})
            return fin_vars

    def get_root(self) -> tk.Tk:
        """
        Returns the root tk widget for the application.
        :return: The root tk widget.
        """
        return self._root

    #   Methods for changing out views
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

        if fin_list is None or len(fin_list) == 0:
            self._nav_text.set("")
            nothing = tk.Label(self._drawer, text="Nothing to see here... Try adding something new.")
            nothing.pack(expand=True)
        else:
            for fin_obj in fin_list:
                fin_obj.get_list_button(self._drawer)

    def populate_editable(self, fin_object: FinanceObj) -> None:
        """
        Populates the editable view for a selected FinanceObj. Called on right click or clicking the edit button from
        the Bottom Menu.
        :param fin_object: The selected FinanceObj.
        """
        for c in self._drawer.winfo_children():
            c.destroy()
        self._bottom_menu.reset()

        fin_object.get_editable(self._drawer)

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
        fin_object.get_detail(self._detail_panel.get_frame())

    def populate_info(self, message) -> None:
        """
        Pushes a message to the information panel in the bottom right-hand corner.
        :param message: The message being pushed.
        """
        if self._info_panel is None:
            return
        self._info_panel.message(message)

    #   Bottom Menu Pass-through Functions
    def create_new_fin_object(self):
        """
        Populated the editable with a new finance object of the type selected in the navigation bar. Called by the
        bottom menu new button.
        """
        if self._fin_obj_selection is not None:
            self._fin_obj_selection.activate(False)
        new_obj = self._nav_selection._fin_obj(self, 'name', 'desc')      # gets the static class and creates a new instance.
        self.populate_editable(new_obj)

    def copy_existing_fin_object(self, fin_obj):
        if self._fin_obj_selection is not None:
            self._fin_obj_selection.activate(False)
        self.populate_editable(fin_obj)

    def delete_selected_fin_object(self) -> None:
        """
        Deletes the selected Finance Object in the list view. Called by bottom menu button.
        """
        if self._fin_obj_selection is not None:
            self._nav_selection.get_fin_list().remove(self._fin_obj_selection)
            self._fin_obj_selection = None
            self.populate_list(refresh=True)

    def edit_selected_fin_object(self) -> None:
        """
        Passthrough function to create the editable view for an existing, selected fin object. Called by bottom menu
        button.
        """
        if self._fin_obj_selection is not None:
            self.populate_editable(self._fin_obj_selection)


def main():
    # create the root
    root = tk.Tk()
    #root.overrideredirect(True)
    #title_bar = tk.Frame(root, bg='#2e2e2e', relief='raised', bd=2, highlightthickness=0)
    root.title("Loan Calculator")
    root.tk_setPalette(background='#fff')

    # load the data
    fin_vars = {}

    # create the main panels.
    app = App(root, fin_vars)
    federal_single = TaxBracket(app, 'Federal', 'Single Filer')
    brackets = federal_single.get_brackets()
    brackets.append(Bracket(10, 9950))
    brackets.append(Bracket(12, 40525))
    brackets.append(Bracket(22, 86375))
    brackets.append(Bracket(24, 164925))
    brackets.append(Bracket(32, 209425))
    brackets.append(Bracket(35, 523600))
    brackets.append(Bracket(37, 1000000000))

    federal_married = TaxBracket(app, 'Federal', 'Married Filing Jointly')
    federal_married.get_data().update({'status': "Married, Joint"})
    brackets = federal_married.get_brackets()
    brackets.append(Bracket(10, 19900))
    brackets.append(Bracket(12, 81050))
    brackets.append(Bracket(22, 172750))
    brackets.append(Bracket(24, 329850))
    brackets.append(Bracket(32, 418850))
    brackets.append(Bracket(35, 628300))
    brackets.append(Bracket(37, 1000000000))

    fin_vars.update({
        'scenarios': [Scenario(app, 'test scenario', 'scenario description')],
        'jobs': [Job(app, 'Data Analyst II', 'Cerner Corporation'), Job(app, 'Data Analyst I', 'Cerner Corporation')],
        'assets': [Assets(app, 'test', "A new Asset")],
        'expenses': [Expenses(app, 'exp', 'Test Expense')],
        'mortgages': [Mortgage(app, '7129 Grand Ave', 'Kansas City, MO 64114')],
        'student loans': [Student(app, 'Virginia Tech', 'BA in English Literature')],
        'loans': [Loan(app, 'test loan', 'test description')],
        'taxes': [federal_single, federal_married]
    })
    app.launch()
    #right_panel = DetailPanel(root)
    #info_panel = InfoPanel(root)

    #set panel relationships
    #left_panel.set_detail_panel(right_panel)
    #left_panel.set_info_panel(info_panel)

    root.mainloop()


if __name__ == "__main__":
    main()
