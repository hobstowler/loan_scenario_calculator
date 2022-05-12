
from tkinter import *
from misc import *
import json


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
            'name': name,
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
        val = f_var.get()
        if isinstance(f_var, StringVar):
            print("it's a string")
        elif isinstance(f_var, DoubleVar):
            print("it's a float")
        self._data.update({key: val})
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
        Label(root, text="").grid(column=0, row=index)

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
        line = Frame(root, height=thickness)
        line.grid(column=column, row=index, columnspan=colspan, padx=padding, sticky=W+E)
        line['bg'] = color

        return index + 1

    def tk_list_pair(self, text_1,
                     text_2,
                     root,
                     index,
                     col_span=0,
                     anchor='e',
                     color=None,
                     highlight_color=None):
        first = Label(root, text=text_1, anchor=anchor)
        first.grid(column=0, columnspan=col_span, row=index, sticky=W + E)
        second = Label(root, text=text_2, anchor='e')
        second.grid(column=col_span, row=index, sticky=W + E)
        if color:
            first['fg'] = color
        if highlight_color:
            second['fg'] = highlight_color

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
        # TODO implement
        return index + 1

    def tk_editable_entry(self, key, text, root, index, additional_info: str = None) -> int:
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
        if val is None:
            raise ValueError
        elif isinstance(val, int) or isinstance(val, float):
            s_var = DoubleVar()
            # TODO format numbers
        else:
            s_var = StringVar()
        s_var.set(val)
        self._form_vars.update({key: s_var})

        Label(root, text=text, anchor='e').grid(column=0, row=index, sticky=W + E, padx=(0, 2))
        entry = Entry(root, name=key, textvariable=s_var)
        col_span = 2
        if additional_info is not None:
            col_span = 1
            Label(root, text=additional_info, anchor='e').grid(column=2, row=index, columnspan=col_span,
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

        dropdown = OptionMenu(root, s_var, *values)
        Label(root, text=text, anchor='e').grid(column=0, row=index, sticky=W + E, padx=(0, 2))
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
        frame = Frame(root, borderwidth=2, relief='groove', height=40)
        frame.pack(fill="x", ipady=2)
        frame.bind("<Button-1>", lambda e: self.left_click())

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        name = Label(frame, text=name, justify=LEFT, anchor="w", foreground=Style.color('fin_type'))
        name.grid(column=0, row=0, sticky=W)
        f_type = Label(frame, text=self.type(), justify=RIGHT, anchor="e", foreground=Style.color("t_type"))
        f_type.grid(column=1, row=0, sticky=E)
        desc = Label(frame, text=desc, justify=LEFT, anchor="w")
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

        frame = Frame(root)
        frame.pack(fill='both', padx=10, pady=10)
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=2)
        frame.columnconfigure(2, weight=2)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=0)

        top_buttons = Frame(frame)
        top_buttons.grid(column=0, row=index, columnspan=3, sticky=E)

        copy = Label(top_buttons, text='Copy')
        copy.grid(column=0, row=0)
        copy.bind('<Button-1>', lambda e: self.copy())
        save = Button(top_buttons, text='Save')
        save.grid(column=1, row=0)
        save.bind('<Button-1>', lambda e: self.save_all())
        cancel = Button(top_buttons, text='X ', anchor='e')
        cancel.grid(column=2, row=0)
        cancel.bind('<Button-1>', lambda e: self.cancel())
        index += 1

        assumptions_button = Button(frame, text='Assumptions')
        assumptions_button.grid(column=2, row=index)
        assumptions_button.bind('<Button-1>', lambda e: self.launch_assumption_window())
        if len(self._assumptions) < 1:
            assumptions_button['state'] = 'disabled'
        index += 1

        index = self.tk_line_break(frame, index)
        index = self.tk_editable_entry('name', name, frame, index)
        index = self.tk_editable_entry('desc', desc, frame, index)

        return frame, index

    def get_detail(self, root, name: str = None, desc: str = None) -> tuple:
        """
        Builds the tk Frame layout for the detailed panel. Typically called when a user left clicks from the list.
        :param desc:
        :param name:
        :param root: The root Tk Frame of the detail panel.
        :return: Returns the frame and information panels to be used for inherited calls.
        """
        name = self.name() if name is None else name
        desc = self.desc() if desc is None else desc

        frame = Frame(root)
        frame.pack(fill=BOTH)
        frame.pack_propagate(True)
        frame.grid_propagate(True)

        # Top title banner
        title = Frame(frame, width=700)
        title.pack(fill=X, padx=10, pady=(15, 0))
        title.grid_propagate(True)
        title.pack_propagate(False)
        title.columnconfigure(0, weight=1)

        t1 = Label(title, text=name, font=('bold', 14), anchor='w')
        t1.grid(column=0, row=0, sticky=W+E)
        t1['fg'] = Style.color('detail title')
        t2 = Label(title, text=desc, font=('bold', 12), anchor='w')
        t2.grid(column=0, row=1, sticky=W+E)
        t2['fg'] = Style.color('detail subtitle')
        self.tk_line(title, 2, padding=0)

        return frame