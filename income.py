# Author: Hobs Towler
# Date: 12/1/2021
# Description:
import json
import locale
import tkinter as tk
from tkinter import *

from misc import *


class FinanceObj:
    """
    A generic financial object. Can include expenses, loans, and jobs.
    """
    asset_category_list = ['stocks', 'property', 'misc']
    expense_category_list = ['utilities', 'subscriptions', 'groceries']
    label_list = ['streaming', 'tv']

    def __init__(self, app, name: str, desc: str) -> None:
        """
        Initializes the financial object with a name and description.
        :param name: The name of the object. Used in display functions
        :param desc: The longer form description of the object.
        """
        self._app = app
        self._data = {
            'name': 3,
            'desc': desc
        }
        self._assumptions = {}
        self._active = False
        self._form_vars = {}
        self.button_hover_message = f"Click to populate a list of {self.__str__()}s."

    @staticmethod
    def __str__() -> str:
        """
        Returns a string representation of the class.
        :return: The string representation.
        """
        return f'Finance Object'

    @classmethod
    def button_hover_message(cls) -> str:
        """
        Returns a message when the navigation button object is hovered over.
        :return: The hover message.
        """
        return f"Click to populate a list of {cls.__str__()}."

    @classmethod
    def list_hover_message(cls) -> str:
        """
        Returns a message when the list button object is hovered over.
        :return: The hover message.
        """
        return f"Left click to see more detail. Right click to edit."

    def get_jsonification(self) -> dict:
        """
        Returns a dict representing the object that can be easily jsonified.
        :return: The dict representing the object.
        """
        jsonification = {
            'name': self._data.get('name'),
            'desc': self._data.get('desc'),
            'data': self._data,
            'assumptions': self._assumptions
        }
        return json.dumps(jsonification)

    def name(self) -> str:
        """
        Gets the name of the object.
        :return: The name.
        """
        return self._data.get('name')

    def desc(self) -> str:
        """
        Gets the description of the object.
        :return: The description.
        """
        return self._data.get('desc')

    def get_data(self) -> dict:
        """
        Returns the data dictionary associated with this object.
        :return: The data dict.
        """
        return self._data

    def get_assumptions(self) -> dict:
        """
        Returns the dict of underlying assumptions associated with this object.
        :return: The underlying assumptions dict.
        """
        return self._assumptions

    def data(self, key: str) -> (float, int, str):
        """
        Gets the value from the data dict.
        :param key: the key value for the data.
        :return: The value for the given key.
        """
        return self._data.get(key)

    def assume(self, key: str) -> (float, int, str):
        """
        Gets the value from the assumptions dict.
        :param key: the key value for the assumption.
        :return: The value of the assumption for given key.
        """
        return self._assumptions.get(key)

    def type(self) -> str:
        """
        Returns the type of Finance Object.
        :return: The object type as string.
        """
        return type(self).__name__

    def activate(self, active=True) -> None:
        """
        Activate the Finance Object.
        :param active: sets the active indicator. True by default.
        """
        self._active = active

    def left_click(self) -> None:
        """
        Passthrough method for a left click on the list button. Populates the detail panel with additional information.
        :param parent: The App object.
        """
        self._app.populate_detail(self)
        self._active = True
        self._app.populate_list(refresh=True)

    def right_click(self) -> None:
        """
        Passthrough method for a right click on the list button. Populates the editable view for the object.
        :param parent: The App object.
        """
        self._app.populate_editable(self)

    def cancel(self):
        """
        Method for a cancel of the Bottom Menu. Repopulates the list with the current context.
        :param parent: The App object.
        """
        self._app.populate_list(refresh=True)

    # TODO validate input is correct
    def save(self, key):
        """
        Saves a given key/value pair in the data dict. Called when changing focus in an editable view.
        :param key: The key value in the data dict.
        :param parent: The App object.
        """
        f_var = self._form_vars.get(key)
        self._data.update({key: f_var.get()})
        self._app.populate_editable(self)

    def copy(self):
        new_fin_obj = self.__class__(self._app, '', '')
        new_fin_obj.get_data().update(self.get_data().copy())
        new_fin_obj.get_data().update({'name': f'Copy of {self.data("name")}'})
        self._app.copy_existing_fin_object(new_fin_obj)
        self._app.populate_info(f'Successfully copied "{self.data("name")}"!')

    def save_all(self):
        """
        Save all key value pairs based on the current form_vars values.
        :param parent: The App object.
        """
        for key in self._form_vars:
            self._data.update({key: self._form_vars.get(key).get()})
        self._app.save_fin_obj(self)

        self._app.populate_list(refresh=True)
        self._app.populate_detail(self)
        self._app.populate_info(f'Successfully saved "{self.data("name")}"!')

    def refresh_detail(self, *args):
        self._app.populate_detail(self)

    # TODO implement
    @staticmethod
    def validate_string(string: str) -> bool:
        pass

    @staticmethod
    def validate_integer(number: int) -> bool:
        pass

    @staticmethod
    def validate_float(number: float):
        pass

    # TODO make standalone methods in app?
    def tk_line_break(self, root, index) -> int:
        """
        Creates a blank Label to serve as a space between rows.
        :param root: The tk root object.
        :param index: The current row index.
        :return: The incremented index.
        """
        tk.Label(root, text="").grid(column=0, row=index)

        return index + 1

    def tk_line(self, root, index, column=0, colspan=1, thickness=2, padding=0, color='black') -> int:
        """
        Creates a line using a colored tk Frame widget.
        :param root: The tk root widget.
        :param index: The current row index.
        :param colspan: The column span for tk grid.
        :param thickness: The thickness/height of the line.
        :param padding: horizontal padding/margin for the line.
        :param color: The color of the line.
        :return: The incremented index.
        """
        line = tk.Frame(root, height=thickness)
        line.grid(column=column, row=index, columnspan=colspan, padx=padding, sticky=W+E)
        line['bg'] = color

        return index + 1

    def tk_list_pair(self, text_1, text_2, root, index):
        tk.Label(root, text=text_1, anchor='e').grid(column=0, row=index, sticky=W + E)
        tk.Label(root, text=text_2, anchor='e').grid(column=1, row=index, sticky=W + E)
        return index + 1

    def tk_checkbox(self, key, text, root, index, additional_info: str = None) -> int:
        """

        :param key:
        :param text:
        :param root:
        :param parent:
        :param index:
        :param additional_info:
        :return:
        """

        return index + 1

    def tk_float_entry(self, key, text, root, index, additional_info: str = None) -> int:
        """
        Creates an editable tk Entry widget with label and supplemental information.
        :param key: The key for the data dict.
        :param text: The label text.
        :param root: The tk root.
        :param index: The current row index.
        :param additional_info: Supplemental label information.
        :return: The incremented index.
        """
        val = self.data(key)
        s_var = tk.DoubleVar()
        s_var.set(val)
        self._form_vars.update({key: s_var})

        tk.Label(root, text=text, anchor='e').grid(column=0, row=index, sticky=W + E, padx=(0, 2))
        entry = tk.Entry(root, name=key, textvariable=s_var)
        col_span = 2
        if additional_info is not None:
            col_span = 1
            tk.Label(root, text=additional_info, anchor='e').grid(column=2, row=index, columnspan=col_span,
                                                                  sticky=W + E)
        entry.grid(column=1, row=index, columnspan=col_span, sticky=W + E)
        entry.bind("<FocusOut>", lambda e, k=key: self.save(k))

        return index + 1

    def tk_string_entry(self, key, text, root, index, additional_info: str = None) -> int:
        """
        Creates an editable tk Entry widget with label and supplemental information.
        :param key: The key for the data dict.
        :param text: The label text.
        :param root: The tk root.
        :param index: The current row index.
        :param additional_info: Supplemental label information.
        :return: The incremented index.
        """
        val = self.data(key)
        s_var = tk.StringVar()
        s_var.set(val)
        self._form_vars.update({key: s_var})

        tk.Label(root, text=text, anchor='e').grid(column=0, row=index, sticky=W + E, padx=(0, 2))
        entry = tk.Entry(root, name=key, textvariable=s_var)
        col_span = 2
        if additional_info is not None:
            col_span = 1
            tk.Label(root, text=additional_info, anchor='e').grid(column=2, row=index, columnspan=col_span,
                                                                  sticky=W + E)
        entry.grid(column=1, row=index, columnspan=col_span, sticky=W + E)
        entry.bind("<FocusOut>", lambda e, k=key: self.save(k))

        return index + 1

    def tk_editable_dropdown(self, key, text, values, root, index) -> int:
        """
        Creates an editable tk dropdown widget with label.
        :param key: The key for the data dict.
        :param text: Text for the label.
        :param values: Values for the dropdown list.
        :param root: The tk root object.
        :param parent: The App object.
        :param index: The current row index.
        :return: Returns the incremented row index.
        """
        s_var = StringVar()
        s_var.set(self.data(key))
        self._form_vars.update({key: s_var})

        dropdown = tk.OptionMenu(root, s_var, *values)
        tk.Label(root, text=text, anchor='e').grid(column=0, row=index, sticky=W + E, padx=(0, 2))
        dropdown.grid(column=1, row=index, columnspan=2, sticky=W + E)
        s_var.trace('w', lambda e, f, g, k=key: self.save(k))

        return index + 1

    def launch_assumption_window(self) -> None:
        """
        Launches a new window to allow editing of underlying assumptions for the Finance Object.
        :param parent: The App object.
        """
        root = self._app.get_root()
        AssumptionsWindow(root, self._app, self)

    def list_button_enter(self, e) -> None:
        """
        Called when cursor enters the list button widget. Changes styling of the widget.
        :param parent: The App object.
        :param e: The cursor event.
        """
        if e.widget.winfo_class() == 'Frame':
            widget = e.widget
        else:
            parent_name = e.widget.winfo_parent()
            widget = e.widget._nametowidget(parent_name)

        if self._active:
            widget['bg'] = Style.color('l_active_hover')
            for c in widget.winfo_children():
                c['bg'] = Style.color('l_active_hover')
        else:
            widget['bg'] = Style.color('l_hover')
            for c in widget.winfo_children():
                c['bg'] = Style.color('l_hover')
        self._app.populate_info(self.list_hover_message())

    def list_button_leave(self, e) -> None:
        """
        Called when cursor leaves the list button. Changes styling of widget.
        :param parent: The App object.
        :param e: The cursor event.
        """
        if e.widget.winfo_class() == 'Frame':
            widget = e.widget
        else:
            parent_name = e.widget.winfo_parent()
            widget = e.widget._nametowidget(parent_name)

        if self._active:
            widget['bg'] = Style.color('l_sel')
            for c in widget.winfo_children():
                c['bg'] = Style.color('l_sel')
        else:
            widget['bg'] = Style.color('l_reset')
            for c in widget.winfo_children():
                c['bg'] = Style.color('l_reset')
        self._app.populate_info("")

    def get_list_button(self, root, name=None, desc=None) -> None:
        """
        Builds and returns a list button representation of this object using tkinter widgets.
        :param root: The root frame used to build the editable view.
        :param parent: The parent LeftPanel. Used for callbacks and lambda functions.
        :param name: Used in the header, can be changed from default by calling child class.
        :param desc: Used in the header, can be changed from default by calling child class.
        """
        if name is None:
            name = self.data('name')
        if desc is None:
            desc = self.data('desc')
        frame = tk.Frame(root, borderwidth=2, relief='groove', height=40)
        frame.pack(fill="x", ipady=2)
        frame.bind("<Button-1>", lambda e: self.left_click())

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        name = tk.Label(frame, text=name, justify=LEFT, anchor="w", foreground=Style.color('fin_type'))
        name.grid(column=0, row=0, sticky=W)
        f_type = tk.Label(frame, text=self.type(), justify=RIGHT, anchor="e", foreground=Style.color("t_type"))
        f_type.grid(column=1, row=0, sticky=E)
        desc = tk.Label(frame, text=desc, justify=LEFT, anchor="w")
        desc.grid(column=0, row=1, sticky=W, columnspan=2)

        frame.bind("<Button-1>", lambda e: self.left_click())
        frame.bind("<Button-3>", lambda e: self.right_click())
        frame.bind("<Enter>", lambda e: self.list_button_enter(e))
        frame.bind("<Leave>", lambda e: self.list_button_leave(e))
        for c in frame.winfo_children():
            c.bind("<Button-1>", lambda e: self.left_click())
            c.bind("<Button-3>", lambda e: self.right_click())
            c.bind("<Enter>", lambda e: self.list_button_enter(e))
            # c.bind("<Leave>", self.list_leave)
            if self._active:
                c['bg'] = Style.color("b_sel")

        if self._active:
            frame['bg'] = Style.color("b_sel")

    def get_listable(self, root):
        pass

    def get_editable(self, root, name: str = None, desc: str = None) -> tuple:
        """
        Builds an editable view for a FinanceObj in the left drawer. Typically called when user clicks edit or right-
        clicks an item in the drawer.
        :param root: The root frame used to build the editable view.
        :param name: Used in the header, can be changed from default by calling child class.
        :param desc: Used in the header, can be changed from default by calling child class.
        :return: Returns the frame and current index to be used in inherited calls.
        """
        index = 0
        if name is None:
            name = "Name"
        if desc is None:
            desc = "Description"

        frame = tk.Frame(root)
        frame.pack(fill='both', padx=10, pady=10)
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=2)
        frame.columnconfigure(2, weight=2)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=0)

        top_buttons = tk.Frame(frame)
        top_buttons.grid(column=0, row=index, columnspan=3, sticky=E)

        copy = tk.Label(top_buttons, text='Copy')
        copy.grid(column=0, row=0)
        copy.bind('<Button-1>', lambda e: self.copy())
        save = tk.Button(top_buttons, text='Save')
        save.grid(column=1, row=0)
        save.bind('<Button-1>', lambda e: self.save_all())
        cancel = tk.Button(top_buttons, text='X ', anchor='e')
        cancel.grid(column=2, row=0)
        cancel.bind('<Button-1>', lambda e: self.cancel())
        index += 1

        assumptions_button = tk.Button(frame, text='Assumptions')
        assumptions_button.grid(column=2, row=index)
        assumptions_button.bind('<Button-1>', lambda e: self.launch_assumption_window())
        if len(self._assumptions) < 1:
            assumptions_button['state'] = 'disabled'
        index += 1

        index = self.tk_line_break(frame, index)
        index = self.tk_string_entry('name', name, frame, index)
        index = self.tk_string_entry('desc', desc, frame, index)

        return frame, index

    def get_detail(self, root, name: str = None, desc: str = None) -> tuple:
        """
        Builds the tk Frame layout for the detailed panel. Typically called when a user left clicks from the list.
        :param desc:
        :param name:
        :param root: The root Tk Frame of the detail panel.
        :return: Returns the frame and information panels to be used for inherited calls.
        """
        if name is None:
            name = self.name()
        if desc is None:
            desc = self.desc()

        frame = tk.Frame(root)
        frame.pack(fill=BOTH)
        frame.pack_propagate(True)
        frame.grid_propagate(True)

        # Top title banner
        title = tk.Frame(frame, width=700)
        title.pack(fill=X, expand=True, padx=10, pady=(15, 0))
        title.grid_propagate(True)
        title.pack_propagate(False)
        title.columnconfigure(0, weight=1)

        t1 = tk.Label(title, text=name, font=('bold', 14), anchor='w')
        t1.grid(column=0, row=0, sticky=W+E)
        t1['fg'] = Style.color('detail title')
        t2 = tk.Label(title, text=desc, font=('bold', 12), anchor='w')
        t2.grid(column=0, row=1, sticky=W+E)
        t2['fg'] = Style.color('detail subtitle')
        self.tk_line(title, 2, padding=0)

        return frame


# TODO add support for different assets like 401k, IRA, houses, bank accounts
class Assets(FinanceObj):
    def __init__(self, app, name: str, desc: str = ""):
        super().__init__(app, name, desc)
        self._data.update({
            'category': "",
            'label': ""
        })
        self._assets = []

    @staticmethod
    def __str__():
        return f'Assets'

    def get_jsonification(self) -> dict:
        """
        Returns a dict representing the Assets object that can be easily jsonified.
        :return: The dict representing the Assets.
        """
        jsonification = super().get_jsonification()

        asset_list = []
        for asset in self._assets:
            asset_list.append(asset.get_jsonification())
        jsonification.update({'expense list': asset_list})

    def get_assets(self):
        return self._assets

    def get_total(self):
        """
        Returns the total of all assets.
        :return: The total dollar value for assets.
        """
        total = 0
        for asset in self._assets:
            total += asset.amount
        return round(total, 2)

    def launch_asset_window(self):
        root = self._app.get_root()
        AssetWindow(root, self._app, self)

    def get_editable(self, root, name: str = None, desc: str = None) -> tuple:
        """
        Builds an editable view for a FinanceObj in the left drawer. Typically called when user clicks edit or right-
        clicks an item in the drawer.
        :param root: The root frame used to build the editable view.
        :param parent: The parent LeftPanel. Used for callbacks and lambda functions.
        :param name: Used in the header, can be changed from default by calling child class.
        :param desc: Used in the header, can be changed from default by calling child class.
        :return: Returns the frame and current index to be used in inherited calls.
        """
        frame, index = super().get_editable(root, name)
        index = self.tk_line_break(frame, index)

        # Labels and Categories
        cat_list = super().asset_category_list
        cat_list.sort()
        index = self.tk_editable_dropdown('category', 'Category', cat_list, frame, index)
        index = self.tk_float_entry('label', 'Labels', frame, index)
        index = self.tk_line_break(frame, index)

        # Individual Assets
        total = self.get_total()
        tk.Label(frame, text=f'${total:,}', anchor='e').grid(column=1, row=index, sticky=W+E)
        asset_button = tk.Button(frame, text='Edit Assets')
        asset_button.grid(column=2, row=index, columnspan=2, sticky=W + E)
        asset_button.bind("<Button-1>", lambda e: self.launch_asset_window())
        index += 1

        return frame, index

    def get_detail(self, root) -> tuple:
        frame = super().get_detail(root)

        category = tk.Frame(frame)
        category.pack(fill=X, padx=10, pady=(15, 15))
        category.pack_propagate(False)
        category.grid_propagate(True)

        cat = tk.Label(category, text=f'Category: {self.data("category")}', font=('bold', 12), anchor='w')
        cat.grid(column=0, row=0, sticky=W+E)
        labels = tk.Label(category, text=f'Labels: {self.data("label")}', font=('bold', 10), anchor='w')
        labels.grid(column=0, row=1, sticky=W+E)

        main = tk.Frame(frame)
        main.pack(fill=BOTH, padx=10)
        main.pack_propagate(False)
        main.grid_propagate(True)

        tk.Label(main, text='Description').grid(column=0, row=0, sticky=W+E)
        tk.Label(main, text='Value').grid(column=1, row=0, sticky=W+E)

        index = 1
        for asset in self._assets:
            tk.Label(main, text=asset.desc).grid(column=0, row=index, sticky=W+E)
            tk.Label(main, text=f'${asset.amount:,}').grid(column=1, row=index, sticky=W+E)
            index += 1

        index = self.tk_line(main, index, colspan=2)
        tk.Label(main, text='Total').grid(column=0, row=index, sticky=W+E, pady=(10, 0))
        tk.Label(main, text=f'${self.get_total():,}').grid(column=1, row=index, sticky=W+E, pady=(10, 0))

        return frame


# TODO assert instead of if statements
# TODO add support for yearly expenses
class Expenses(FinanceObj):
    """
    An object that can keep track of monthly expenses and provide a total amount.
    """

    def __init__(self, app, name: str, desc: str = "") -> None:
        """
        Initializes the Expenses object with a name, description, and dictionary of expenses.
        """
        super().__init__(app, name, desc)
        self._data.update({
            'category': "",
            'label': ""
        })
        self._expenses = []

    @staticmethod
    def __str__():
        return f'Expenses'

    # TODO implement
    def get_jsonification(self) -> dict:
        """
        Returns a dict representing the Assets object that can be easily jsonified.
        :return: The dict representing the Assets.
        """
        jsonification = super().get_jsonification()

        expense_list = []
        for expense in self._expenses:
            expense_list.append(expense.get_jsonification())
        jsonification.update({'expense list': expense_list})

        return jsonification

    def get_labels(self) -> list:
        """
        Returns all labels in list form that are associated with this instance of the expense object.
        :return: Labels in list format.
        """
        raw_labels = self.data('label')
        labels = raw_labels.split(',')
        for label in labels:
            label = label.strip()

        return labels

    def get_expenses(self) -> list:
        """
        Returns the dictionary of expenses.
        :return: The expenses.
        """
        return self._expenses

    def get_total(self) -> float:
        """
        Returns the total of all expenses.
        :return: The total monthly expenditure.
        """
        total = 0
        for expense in self._expenses:
            total += expense.amount
        return round(total, 2)

    def launch_expense_window(self):
        root = self._app.get_root()
        ExpenseWindow(root, self._app, self)

    def get_editable(self, root, name: str = None, desc: str = None) -> tuple:
        """
        Builds an editable view for a FinanceObj in the left drawer. Typically called when user clicks edit or right-
        clicks an item in the drawer.
        :param root: The root frame used to build the editable view.
        :param name: Used in the header, can be changed from default by calling child class.
        :param desc: Used in the header, can be changed from default by calling child class.
        :return: Returns the frame and current index to be used in inherited calls.
        """
        frame, index = super().get_editable(root, name)
        index = self.tk_line_break(frame, index)

        # Labels and Categories
        cat_list = super().expense_category_list
        cat_list.sort()
        index = self.tk_editable_dropdown('category', 'Category', cat_list, frame, index)
        index = self.tk_float_entry('label', 'Labels', frame, index)
        index = self.tk_line_break(frame, index)

        # Individual Expenses
        total = self.get_total()
        tk.Label(frame, text=f'${total:,}', anchor='e').grid(column=1, row=index, sticky=W+E)
        expense_button = tk.Button(frame, text='Edit Expenses')
        expense_button.grid(column=2, row=index, columnspan=2, sticky=W + E)
        expense_button.bind("<Button-1>", lambda e: self.launch_expense_window())
        index += 1

        return frame, index

    def get_detail(self, root) -> tuple:
        frame = super().get_detail(root)

        category = tk.Frame(frame)
        category.pack(fill=X, padx=10, pady=(15, 15))
        category.pack_propagate(False)
        category.grid_propagate(True)

        cat = tk.Label(category, text=f'Category: {self.data("category")}', font=('bold', 12), anchor='w')
        cat.grid(column=0, row=0, sticky=W+E)
        labels = tk.Label(category, text=f'Labels: {self.data("label")}', font=('bold', 10), anchor='w')
        labels.grid(column=0, row=1, sticky=W+E)

        main = tk.Frame(frame)
        main.pack(fill=BOTH, padx=10)
        main.pack_propagate(False)
        main.grid_propagate(True)

        tk.Label(main, text='Description').grid(column=0, row=0, sticky=W+E)
        tk.Label(main, text='Amount').grid(column=1, row=0, sticky=W+E)

        index = 1
        for expense in self._expenses:
            tk.Label(main, text=expense.desc).grid(column=0, row=index, sticky=W+E)
            tk.Label(main, text=f'${expense.amount:,}').grid(column=1, row=index, sticky=W+E)
            index += 1

        index = self.tk_line(main, index, colspan=2)
        tk.Label(main, text='Total').grid(column=0, row=index, sticky=W+E, pady=(10, 0))
        tk.Label(main, text=f'${self.get_total():,}').grid(column=1, row=index, sticky=W+E, pady=(10, 0))

        return frame


class Income(FinanceObj):
    def __init__(self, app, name, desc=""):
        super(Income, self).__init__(app, name, desc)

    @staticmethod
    def __str__():
        return f'Income'


class TaxBracket(FinanceObj):
    """
    Represents a tax bracket for income. Includes methods for getting the taxed amount and effective tax rate.
    """

    def __init__(self, app, name: str, desc: str = "") -> None:
        super().__init__(app, name, desc)
        self._brackets = []
        self._data.update({
            'state': '',
            'locality': '',
            'status': 'Single',
            'type': 'Federal',
            'standard deduction': 24000
        })

        self._valid_types = ["Federal", "State", "Local"]
        self._valid_status = ["Single", "Married, Joint", "Married, Separate", "Head of Household"]

    @staticmethod
    def __str__():
        return f'Tax Brackets'

    def define_brackets(self, brackets):
        """
        Allows you to define multiple ranges in the bracket at once. Input must be a two dimensional list with two
        elements for each range: upper limit of the range and tax rate for the range.
        :param brackets: A two dimensional list of brackets
        :return: Nothing.
        """
        if len(brackets) < 1:
            return

        self._brackets = []
        for b in brackets:
            if len(b) == 2:
                self.add_range(b[0], b[1])

    def get_brackets(self) -> list:
        return self._brackets

    def add_range(self, upper_range: (int, float), rate: (int, float)):
        """
        Adds a range and associated rate to the tax bracket. Method will check to see if the range is already in the
        list and replace the rate if it does. Passing 'None' for the upper range will be equivalent to the highest tax
        bracket.
        :param upper_range: The upper limit of the range being added.
        :param rate: The tax rate for that range
        :return: Nothing
        """
        if upper_range == None:
            upper_range = 1000000000
        if not isinstance(upper_range, (int, float)) or not isinstance(rate, (int, float)):
            return
        index = self._get_range(upper_range)
        if index is None:
            self._brackets.append([upper_range, rate / 100])
            self._brackets.sort()
        else:
            self._brackets[index] = [upper_range, rate / 100]

    def rem_range(self, upper_range: (int, float)):
        """
        Removes a bracket range if it exists.
        :param upper_range: The range to be removed.
        :return: True if there was a bracket to be removed.
        """
        index = None
        for r in self._brackets:
            if r[0] == upper_range:
                index = self._brackets.index(r)
        if index is not None:
            del self._brackets[index]
            return True
        return False

    def _get_range(self, upper_range):
        """
        Internal method to check if a range already exists in the list.
        :param upper_range: The upper range to be checked.
        :return: the index of the range if it already exists in the list.
        """
        for r in self._brackets:
            if r[0] == upper_range:
                return self._brackets.index(r)
        return None

    def calculate_taxed_amount(self, income) -> tuple:
        """
        Calculates the total taxed amount and the effective tax rate for a given income.
        :param income: The yearly income to be taxed
        :return: A list of the taxed amount and the effective rate.
        """
        if len(self._brackets) == 0:
            return 0

        taxed_amount = 0
        for i in range(0, len(self._brackets)):
            if i == 0:
                if income >= self._brackets[i].upper:
                    amount = (self._brackets[i].upper * self._brackets[i].rate / 100)
                    taxed_amount += amount
                else:
                    amount = income * self._brackets[i].rate / 100
                    taxed_amount += amount
            else:
                lower_range = self._brackets[i - 1].upper + 0.01
                upper_range = self._brackets[i].upper
                if income >= upper_range:
                    amount = (upper_range - lower_range) * self._brackets[i].rate / 100
                    taxed_amount += amount
                elif income < upper_range and income > lower_range:
                    amount = (income - lower_range) * self._brackets[i].rate / 100
                    taxed_amount += amount

        taxed_amount = taxed_amount
        effective_rate = round(100 * taxed_amount / income, 4)

        return taxed_amount, effective_rate

    def launch_bracket_editor(self):
        root = self._app.get_root()
        BracketWindow(root, self._app, self)

    def get_editable(self, root) -> tuple:
        """
        Builds an editable view for a FinanceObj in the left drawer. Typically called when user clicks edit or right-
        clicks an item in the drawer.
        :param root: The root frame used to build the editable view.
        :param parent: The parent LeftPanel. Used for callbacks and lambda functions.
        :param name: Used in the header, can be changed from default by calling child class.
        :param desc: Used in the header, can be changed from default by calling child class.
        :return: Returns the frame and current index to be used in inherited calls.
        """
        frame, index = super().get_editable(root)
        index = self.tk_line_break(frame, index)

        index = self.tk_editable_dropdown('type', 'Type', self._valid_types, frame, index)

        if self.data('type').capitalize() == 'State':
            index = self.tk_float_entry('state', "State", frame, index)
        elif self.data('type').capitalize() == 'Local':
            index = self.tk_float_entry('locality', "Locality", frame, index)

        index = self.tk_editable_dropdown('status', 'Filing Status:', self._valid_status, frame, index)
        index = self.tk_line_break(frame, index)

        brackets = tk.Button(frame, text="Define Brackets")
        brackets.grid(column=2, row=index, columnspan=2, sticky=W + E)
        brackets.bind("<Button-1>", lambda e: self.launch_bracket_editor())

        return frame, index

    def get_list_button(self, root):
        name = self.data('type')
        desc = self.data('status')
        super().get_list_button(root, name, desc)

    def get_detail(self, root):
        frame = super().get_detail(root)

        summary_panel = tk.Frame(frame, width=700)
        summary_panel.pack(fill=X, expand=True, padx=10, pady=(15, 0))
        summary_panel.columnconfigure(0, weight=1)

        type_text = f'{self.data("type")}, {self.data("status")}'
        type_status = tk.Label(summary_panel, text=type_text, anchor='w', font=11)
        type_status.grid(column=0, row=0, sticky=W+E)
        if self.data('type').capitalize() == 'State':
            state = tk.Label(summary_panel, text=f'State: {self.data("state")}', anchor='w', font=10)
            state.grid(row=1, column=0, sticky=W+E)
        elif self.data('type').capitalize() == 'Local':
            local = tk.Label(summary_panel, text=f'Locality: {self.data("locality")}', anchor='w', font=10)
            local.grid(row=1, column=0, sticky=W+E)
        self.tk_line(summary_panel, 2, padding=0, thickness=1)

        bracket_panel = tk.Frame(frame)
        bracket_panel.pack(fill=BOTH, padx=10, pady=15)
        index = 0
        index = self.tk_list_pair('Rate', "Taxable Range", bracket_panel, index)
        index = self.tk_line(bracket_panel, index, colspan=2, padding=0)
        for i in range(len(self._brackets)):
            if i != 0:
                prev_bracket = self._brackets[i-1]
            else:
                prev_bracket = Bracket(0, -0.01)
            bracket = self._brackets[i]
            bounds = f'${prev_bracket.upper + 0.01:,} to {bracket.upper:,}'
            index = self.tk_list_pair(f'{bracket.rate}%', bounds, bracket_panel, index)


class Job(FinanceObj):
    """Represents a job."""

    def __init__(self, app, title: str, company: str = "") -> None:
        """
        Initializes the Job object with a title and description. Income and retirement contribution rates are optional.
        :param title: The job title.
        :param company: Brief description of the job.
        """
        super().__init__(app, title, company)

        self._data.update({
            'income': 3500,
            '401k rate': 12,
            'roth rate': 3,
            'pay frequency': 'Bi-Weekly'
        })
        self._assumptions.update({
            'social security rate': 6.2,
            'social security cap': 147000,
            'medicare tax rate': 1.45,
            'employer match': 6,
            'employer match rate': 50
        })

        self._taxes = []
        self._pre_tax_deductions = Expenses(app, 'pre tax')
        self._post_tax_deductions = Expenses(app, 'post tax')

        self._valid_pay_frequency = ['Weekly', 'Bi-Weekly', 'Semimonthly', 'Monthly', 'Quarterly', 'Annually']
        self._num_pay_periods = {
            'Weekly': 52,
            'Bi-Weekly': 26,
            'Semimonthly': 24,
            'Monthly': 12,
            'Quarterly': 4,
            'Annually': 1
        }
        self._breakdowns = ['Annual', 'Monthly']
        self._breakdown = StringVar()
        self._breakdown.set("Annual")
        self._breakdown.trace('w', self.refresh_detail)

        self.button_hover_message = f"Click to populate a list of {self.__str__()}s."

    @staticmethod
    def __str__():
        return f'Jobs'

    # TODO implement
    def get_jsonification(self) -> dict:
        """
        Returns a dict representing the object that can be easily jsonified.
        :return: The dict representing the object.
        """
        pass

    def get_annual_income(self) -> (int, float):
        """
        Returns the annual income based on base salary and pay periods.
        :return: The annual income.
        """
        return self.get_pay_periods() * self.data('income')

    def get_pay_periods(self):
        """
        Returns the number of pay periods based on pay frequency. Used to calculate annual ammounts.
        :return: The number of pay periods.
        """
        return self._num_pay_periods.get(self.data('pay frequency'))

    def get_401k_amount(self) -> (int, float):
        return round(self.data('401k rate') * self.get_annual_income() / 100, 2)

    def get_roth_amount(self):
        return round(self.data('roth rate') * self.get_annual_income() / 100, 2)

    def get_pretax_income(self) -> (int, float):
        """
        Returns the net amount before taxes and post tax deductions are applied.
        :return: The pre tax annual income.
        """
        income = self.get_annual_income()
        total_deduction = 0
        total_deduction += self.get_401k_amount()
        total_deduction += self._pre_tax_deductions.get_total() * self.get_pay_periods()

        return income - total_deduction

    def get_taxed_amounts(self):
        income = self.get_annual_income()
        federal = 0
        state = 0
        local = 0

        for tax in self._taxes:
            amount, rate = tax.calculate_taxed_amount(income)
            type = tax.data('type')
            if type == 'Federal':
                federal += amount
            elif type == 'State':
                state += amount
            elif type == 'Local':
                local += amount

        return federal, state, local

    def get_posttax_income(self) -> (int, float):
        """
        Returns the net annual amount after taxes and deductions.
        :return: The net annual income.
        """
        income = self.get_pretax_income()
        taxed_amount = 0
        total_deduction = 0

        federal, state, local = self.get_taxed_amounts()
        taxed_amount += federal
        taxed_amount += state
        taxed_amount += local
        total_deduction += self._post_tax_deductions.get_total() * self.get_pay_periods()

        taxed_amount += self.get_social_security_taxed_amount()
        taxed_amount += self.get_medicare_taxed_amount()
        taxed_amount += self.get_roth_amount()

        return round(income - taxed_amount - total_deduction, 2)

    # TODO calculate employer responsibility
    def get_social_security_taxed_amount(self):
        cap = self.assume('social security cap')
        rate = self.assume('social security rate') / 100
        income = self.get_annual_income()

        if income <= cap:
            return rate * income
        else:
            return rate * cap

    # TODO calculate employer responsibility
    def get_medicare_taxed_amount(self):
        rate = self.assume('medicare tax rate') / 100
        income = self.get_annual_income()
        return rate * income

    def launch_deduction_selector(self, expense):
        root = self._app.get_root()
        ExpenseSelector(root, self._app, expense)

    def launch_tax_selector(self):
        root = self._app.get_root()
        TaxSelector(root, self._app, self._taxes)

    def get_editable(self, root) -> tuple:
        """
        Builds an editable view for a FinanceObj in the left drawer. Typically called when user clicks edit or right-
        clicks an item in the drawer.
        :param root: The root frame used to build the editable view.
        :param parent: The parent LeftPanel. Used for callbacks and lambda functions.
        :param name: Used in the header, can be changed from default by calling child class.
        :param desc: Used in the header, can be changed from default by calling child class.
        :return: Returns the frame and current index to be used in inherited calls.
        """
        frame, index = super().get_editable(root, name="Title", desc="Company")
        index = self.tk_line_break(frame, index)

        # Pay frequency and income section
        index = self.tk_editable_dropdown('pay frequency', 'Pay Frequency', self._valid_pay_frequency,
                                          frame, index)
        pay_freq = self.data('pay frequency')
        pay_periods = 'x ' + str(self.get_pay_periods())
        index = self.tk_float_entry('income', 'Income (' + pay_freq + ')',
                                    frame, index, pay_periods)
        tk.Label(frame, text=f'= ${round(self.data("income") * self.get_pay_periods(), 2):,}', anchor='e') \
            .grid(column=2, row=index, columnspan=2, sticky=W + E)
        index += 1
        index = self.tk_line_break(frame, index)

        # Retirement accounts section
        retirement = f'  ${self.get_401k_amount():,}'
        roth = f'  ${self.get_roth_amount():,}'
        index = self.tk_float_entry('401k rate', '401k Contribution', frame, index, retirement)
        index = self.tk_float_entry('roth rate', 'Roth Contribution', frame, index, roth)
        tk.Label(frame, text=f'= ${round(self.get_401k_amount() + self.get_roth_amount(), 2):,}', anchor='e') \
            .grid(column=2, row=index, columnspan=2, sticky=W + E)
        index += 1
        index = self.tk_line_break(frame, index)

        # Tax brackets section
        bracket_button = tk.Button(frame, text="Tax Brackets")
        bracket_button.grid(column=2, row=index, columnspan=2, sticky=W + E)
        bracket_button.bind("<Button-1>", lambda e: self.launch_tax_selector())
        index += 1

        # Pre tax deductions section
        pre_tax_amount = self._pre_tax_deductions.get_total()
        tk.Label(frame, text=f"${pre_tax_amount:,}", anchor='e').grid(column=1, row=index, sticky=W + E)
        pre_tax_button = tk.Button(frame, text="Pre Tax Deductions")
        pre_tax_button.grid(column=2, row=index, columnspan=2, sticky=W + E)
        pre_tax_button.bind("<Button-1>",
                            lambda e, d=self._pre_tax_deductions: self.launch_deduction_selector(d))
        index += 1

        # Post tax deductions section
        post_tax_amount = self._post_tax_deductions.get_total()
        tk.Label(frame, text=f"${post_tax_amount:,}", anchor='e').grid(column=1, row=index, sticky=W + E)
        post_tax_button = tk.Button(frame, text="Post Tax Deductions")
        post_tax_button.grid(column=2, row=index, columnspan=2, sticky=W + E)
        post_tax_button.bind("<Button-1>",
                             lambda e, d=self._post_tax_deductions: self.launch_deduction_selector(d))
        index += 1

        return frame, index

    def get_detail(self, root, name: str = None, desc: str = None) -> tuple:
        frame = super().get_detail(root)

        monthly_factor = 1

        breakdown = tk.Frame(frame)
        breakdown.pack(fill=X, padx=10, pady=15)
        breakdown.columnconfigure(0, weight=1)
        breakdown.columnconfigure(1, weight=1)

        income = tk.Frame(breakdown, height=200)
        income.grid(column=0, row=0, sticky=W+E)

        index = 0
        tk.Label(income, text="Income Breakdown", anchor='w')\
            .grid(column=0, row=index, columnspan=2, sticky=W+E)
        time_period = tk.OptionMenu(income, self._breakdown, *self._breakdowns)
        time_period.grid(column=2, row=index, columnspan=2, sticky=W+E)
        index += 1
        index = self.tk_line(income, index, colspan=4)
        index = self.tk_line_break(income, index)

        # Gross Income
        income_per = locale.currency(self.data('income'), grouping=True)
        annual_income = locale.currency(self.get_annual_income(), grouping=True)

        tk.Label(income, text="Income per pay period:", anchor='e')\
            .grid(column=0, row=index, columnspan=3, sticky=W+E)
        tk.Label(income, text=f"{income_per}", anchor='e').grid(column=3, row=index, sticky=W+E)
        index += 1

        tk.Label(income, text=f"Pay periods ({self.data('pay frequency')}):", anchor='e')\
            .grid(column=0, row=index, columnspan=3, sticky=W+E)
        tk.Label(income, text=f"x {monthly_factor}", anchor='e').grid(column=3, row=index, sticky=W+E)
        index += 1

        index = self.tk_line(income, index, column=3)

        if self._breakdown.get() == "Monthly":
            annual_income = locale.currency(self.get_annual_income() / 12, grouping=True)
            tk.Label(income, text="Average Monthly Income:", anchor='e')\
                .grid(column=0, row=index, columnspan=3, sticky=W+E)
            tk.Label(income, text=f"{annual_income}", anchor='e').grid(column=3, row=index, sticky=W+E)
        else:
            tk.Label(income, text="Annual Gross Income:", anchor='e')\
                .grid(column=0, row=index, columnspan=3, sticky=W+E)
            tk.Label(income, text=f"{annual_income}", anchor='e').grid(column=3, row=index, sticky=W+E)
        index += 1

        index = self.tk_line_break(income, index)

        # Pre Tax Net Income
        if self._breakdown.get() == "Monthly":
            monthly_factor = monthly_factor / 12

        pre_tax_amount = locale.currency(self._pre_tax_deductions.get_total() * monthly_factor, grouping=True)
        pre_tax_retirement = locale.currency(self.get_401k_amount() * monthly_factor, grouping=True)
        pre_tax_income = locale.currency(self.get_pretax_income() * monthly_factor, grouping=True)

        tk.Label(income, text="Pre-Tax Deductions:", anchor='e') \
            .grid(column=0, row=index, columnspan=3, sticky=W + E)
        tk.Label(income, text=f"- {pre_tax_amount}", anchor='e').grid(column=3, row=index, sticky=W + E)
        index += 1

        tk.Label(income, text="401k Contributions:", anchor='e') \
            .grid(column=0, row=index, columnspan=3, sticky=W + E)
        tk.Label(income, text=f"- {pre_tax_retirement}", anchor='e').grid(column=3, row=index, sticky=W + E)
        index += 1

        index = self.tk_line(income, index, column=3)
        tk.Label(income, text=f"{pre_tax_income}").grid(column=3, row=index, sticky=W + E)
        index += 1

        index = self.tk_line_break(income, index)

        # Post Tax Net Income

        post_tax_amount = locale.currency(self._post_tax_deductions.get_total() * monthly_factor, grouping=True)
        post_tax_retirement = locale.currency(self.get_roth_amount() * monthly_factor, grouping=True)
        federal, state, local = self.get_taxed_amounts()
        federal = locale.currency(federal * monthly_factor, grouping=True)
        state = locale.currency(state * monthly_factor, grouping=True)
        local = locale.currency(local * monthly_factor, grouping=True) if local != 0 else 0
        social_security = locale.currency(self.get_social_security_taxed_amount() * monthly_factor, grouping=True)
        medicare = locale.currency(self.get_medicare_taxed_amount() * monthly_factor, grouping=True)
        post_tax_income = locale.currency(self.get_posttax_income() * monthly_factor, grouping=True)

        tk.Label(income, text="Post-Tax Deductions:", anchor='e') \
            .grid(column=0, row=index, columnspan=3, sticky=W + E)
        tk.Label(income, text=f"- {post_tax_amount}", anchor='e').grid(column=3, row=index, sticky=W + E)
        index += 1

        tk.Label(income, text="Roth Contributions:", anchor='e') \
            .grid(column=0, row=index, columnspan=3, sticky=W + E)
        tk.Label(income, text=f"- {post_tax_retirement}", anchor='e').grid(column=3, row=index, sticky=W + E)
        index += 1

        tk.Label(income, text="Federal Withholding:", anchor='e') \
            .grid(column=0, row=index, columnspan=3, sticky=W + E)
        tk.Label(income, text=f"- {federal}", anchor='e').grid(column=3, row=index, sticky=W + E)
        index += 1

        tk.Label(income, text="State Withholding:", anchor='e') \
            .grid(column=0, row=index, columnspan=3, sticky=W + E)
        tk.Label(income, text=f"- {state}", anchor='e').grid(column=3, row=index, sticky=W + E)
        index += 1

        if local != 0:
            tk.Label(income, text="Local Withholding:", anchor='e') \
                .grid(column=0, row=index, columnspan=3, sticky=W + E)
            tk.Label(income, text=f"- {local}", anchor='e').grid(column=3, row=index, sticky=W + E)
            index += 1

        tk.Label(income, text="Social Security Tax:", anchor='e') \
            .grid(column=0, row=index, columnspan=3, sticky=W + E)
        tk.Label(income, text=f"- {social_security}", anchor='e').grid(column=3, row=index, sticky=W + E)
        index += 1

        tk.Label(income, text="Medicare Tax:", anchor='e') \
            .grid(column=0, row=index, columnspan=3, sticky=W + E)
        tk.Label(income, text=f"- {medicare}", anchor='e').grid(column=3, row=index, sticky=W + E)
        index += 1

        index = self.tk_line(income, index, column=3)
        tk.Label(income, text=f"{post_tax_income}", anchor='e').grid(column=3, row=index, sticky=W + E)
        index += 1

        index = self.tk_line_break(income, index)

        retirement = tk.Frame(breakdown, height=200)
        retirement.grid(column=1, row=0, sticky=W+E)

        return frame
