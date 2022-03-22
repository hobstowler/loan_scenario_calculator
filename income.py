# Author: Hobs Towler
# Date: 12/1/2021
# Description:
import json
import tkinter as tk
from tkinter import *

colors = {
            "l_sel": "lightblue2",
            "l_hover": "lightblue1",
            'l_active_hover': 'lightblue3',
            "l_reset": "SystemButtonFace",
            "b_reset": "SystemButtonFace",
            "b_sel": 'medium turquoise',
            'b_hover': 'turquoise',
            'b_active_hover': 'dark turquoise',
            'fin_type': 'red',
            'bg_header': 'cadetblue'
        }


class FinanceObj:
    """
    A generic financial object. Can include expenses, loans, and jobs.
    """
    def __init__(self, name: str, desc: str) -> None:
        """
        Initializes the financial object with a name and description.
        :param name: The name of the object. Used in display functions
        :param desc: The longer form description of the object.
        """
        self._data = {
            'name': name,
            'desc': desc
        }
        self._active = False
        self._form_strings = {}
        self.button_hover_message = f"Click to populate a list of {self.__str__()}s."

    @staticmethod
    def __str__():
        return f'Finance Object'

    @classmethod
    def button_hover_message(cls):
        return f"Click to populate a list of {cls.__str__()}."

    @classmethod
    def list_hover_message(cls):
        return f"Left click to see more detail. Right click to edit."

    def get_jsonification(self) -> dict:
        jsonification = {
            'name': self._data.get('name'),
            'desc': self._data.get('desc'),
            'data': self._data
        }
        return json.dumps(jsonification)

    def set_name(self, new_name: str) -> bool:
        """
        Sets a new name for the object. Returns true if the operation is successful.
        :param new_name: The new name.
        :return: True if successful.
        """
        if isinstance(new_name, str):
            self._name = new_name
            return True
        else:
            return False

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

    def data(self, key: str) -> dict:
        """
        Gets the data dict from this object.
        :return: The dict of data for the object.
        """
        return self._data.get(key)

    def type(self) -> str:
        return type(self).__name__

    def activate(self, active=True):
        self._active = active

    def left_click(self, parent):
        parent.populate_detail(self)
        self._active = True
        parent.populate_list(refresh=True)

    def right_click(self, parent):
        parent.populate_editable(self)

    def cancel(self, parent):
        parent.populate_list(refresh=True)

    def save(self, key, parent):
        print('saving:', key)
        self._data.update({key: self._form_strings.get(key).get()})
        parent.populate_editable(self)

    def save_all(self, parent):
        for key in self._form_strings:
            print('saving:', key)
            self._data.update({key: self._form_strings.get(key).get()})
        parent.save_fin_obj(self)

        parent.populate_list(refresh=True)

    def validate_string(self) -> bool:
        pass

    def validate_integer(self) -> bool:
        pass

    # TODO make standalone methods in app
    def tk_line_break(self, root, index) -> int:
        tk.Label(root, text="").grid(column=0, row=index)
        return index + 1

    def tk_editable_string_pair(self, key, text, root, parent, index):
        s_var = tk.StringVar()
        s_var.set(self._data.get(key))
        self._form_strings.update({key: s_var})
        tk.Label(root, text=text, anchor='e').grid(column=1, row=index, sticky=W + E, padx=(0, 2))
        entry = tk.Entry(root, name=key, textvariable=s_var)
        entry.grid(column=2, row=index, columnspan=2, sticky=W + E)
        entry.bind("<FocusOut>", lambda e, k=key, p=parent: self.save(k, p))
        return index + 1

    def tk_editable_int_pair(self, key, text, root, parent, index):
        s_var = tk.IntVar()
        s_var.set(self.data(key))
        self._form_strings.update({key: s_var})
        tk.Label(root, text=text, anchor='e').grid(column=1, row=index, sticky=W + E, padx=(0, 2))
        entry = tk.Entry(root, name=key, textvariable=s_var)
        entry.grid(column=2, row=index, columnspan=2, sticky=W + E)
        entry.bind("<FocusOut>", lambda e, k=key, p=parent: self.save(k, p))
        return index + 1

    def tk_editable_float_pair(self, key, text, root, parent, index):
        s_var = tk.DoubleVar()
        s_var.set(self.data(key))
        self._form_strings.update({key: s_var})
        tk.Label(root, text=text, anchor='e').grid(column=1, row=index, sticky=W + E, padx=(0, 2))
        entry = tk.Entry(root, name=key, textvariable=s_var)
        entry.grid(column=2, row=index, columnspan=2, sticky=W + E)
        entry.bind("<FocusOut>", lambda e, k=key, p=parent: self.save(k, p))
        return index + 1

    def tk_editable_dropdown(self, key, text, values, root, parent, index) -> int:
        s_var = StringVar()
        s_var.set(self.data(key))
        self._form_strings.update({key: s_var})
        dropdown = tk.OptionMenu(root, s_var, *values)
        tk.Label(root, text=text, anchor='e').grid(column=1, row=index, sticky=W + E, padx=(0, 2))
        dropdown.grid(column=2, row=index, columnspan=2, sticky=W + E)
        s_var.trace('w', lambda e, f, g, k=key, p=parent: self.save(k, p))

        return index + 1

    def list_enter(self, parent, e):
        if e.widget.winfo_class() == 'Frame':
            widget = e.widget
        else:
            parent_name = e.widget.winfo_parent()
            widget = e.widget._nametowidget(parent_name)

        if self._active:
            widget['bg'] = colors.get('l_active_hover')
            for c in widget.winfo_children():
                c['bg'] = colors.get('l_active_hover')
        else:
            widget['bg'] = colors.get('l_hover')
            for c in widget.winfo_children():
                c['bg'] = colors.get('l_hover')
        parent.populate_info(self.list_hover_message())


    def list_leave(self, parent, e):
        if e.widget.winfo_class() == 'Frame':
            widget = e.widget
        else:
            parent_name = e.widget.winfo_parent()
            widget = e.widget._nametowidget(parent_name)

        if self._active:
            widget['bg'] = colors.get('l_sel')
            for c in widget.winfo_children():
                c['bg'] = colors.get('l_sel')
        else:
            widget['bg'] = colors.get('l_reset')
            for c in widget.winfo_children():
                c['bg'] = colors.get('l_reset')
        parent.populate_info("")

    def get_list_button(self, root, parent, name=None, desc=None):
        if name is None:
            name = self.data('name')
        if desc is None:
            desc = self.data('desc')
        frame = tk.Frame(root, borderwidth=2, relief='groove', height=40)
        frame.pack(fill="x", ipady=2)
        frame.bind("<Button-1>", lambda e: self.left_click())
        #TODO Move to JSON for data load to allow changes to main attributes

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        name = tk.Label(frame, text=name, justify=LEFT, anchor="w", foreground=colors.get('fin_type'))
        name.grid(column=0, row=0, sticky=W)
        f_type = tk.Label(frame, text=self.type(), justify=RIGHT, anchor="e", foreground=colors.get("t_type"))
        f_type.grid(column=1, row=0, sticky=E)
        desc = tk.Label(frame, text=desc, justify=LEFT, anchor="w")
        desc.grid(column=0, row=1, sticky=W, columnspan=2)

        frame.bind("<Button-1>", lambda e, p=parent: self.left_click(p))
        frame.bind("<Button-3>", lambda e, p=parent: self.right_click(p))
        frame.bind("<Enter>", lambda e, p=parent: self.list_enter(p, e))
        frame.bind("<Leave>", lambda e, p=parent: self.list_leave(p, e))
        for c in frame.winfo_children():
            c.bind("<Button-1>", lambda e, p=parent: self.left_click(p))
            c.bind("<Button-3>", lambda e, p=parent: self.right_click(p))
            c.bind("<Enter>", lambda e, p=parent: self.list_enter(p, e))
            #c.bind("<Leave>", self.list_leave)
            if self._active:
                c['bg'] = colors.get("b_sel")

        if self._active:
            frame['bg'] = colors.get("b_sel")

    def get_editable(self, root, parent, name: str = None, desc: str = None):
        index = 0
        if name is None:
            name = "Name"
        if desc is None:
            desc = "Description"

        frame = tk.Frame(root)
        frame.pack(fill='both')
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)
        frame.columnconfigure(2, weight=4)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)

        save = tk.Button(frame, text='Save')
        save.grid(column=3, row=index)
        save.bind('<Button-1>', lambda e, p=parent: self.save_all(p))
        cancel = tk.Button(frame, text='X', anchor='e')
        cancel.grid(column=4, row=index)
        cancel.bind('<Button-1>', lambda e, p=parent: self.cancel(p))
        index += 1

        index = self.tk_line_break(frame, index)
        index = self.tk_editable_string_pair('name', name, frame, parent, index)
        index = self.tk_editable_string_pair('desc', desc, frame, parent, index)

        return frame, index

    def get_detail(self, root, parent):
        frame = tk.Frame(root)
        frame.pack(fill='both')
        frame.pack_propagate(False)
        frame.grid_propagate(False)

        # TOP INFORMATION BANNER
        information = tk.Frame(root, width=700, height=49)
        information.grid(column=0, row=0, columnspan=7, sticky=W+E, pady=(0, 3))
        information.grid_propagate(False)

        name = tk.Label(information, text=self.name() + ", " + self.desc(), font=('bold', 13))
        name.grid(column=0, row=0, sticky=W)

        information['bg'] = colors.get('bg_header')
        for c in information.winfo_children():
            c['bg'] = colors.get('bg_header')

        return frame, information


class InvalidExpenseType(Exception):
    pass


class Expense:
    def __init__(self, amount: (int, float), type: str):
        self.amount = amount
        if type.lower() not in ["annual", "monthly", "daily"]:
            self.type = type
        else:
            raise InvalidExpenseType("Type must be 'annual', 'monthly', or 'daily'.")


#TODO assert instead of if statements
#TODO add support for yearly expenses
class Expenses(FinanceObj):
    """
    An object that can keep track of monthly expenses and provide a total amount.
    """
    def __init__(self, name: str, desc: str = "") -> None:
        """
        Initializes the Expenses object with a name, description, and dictionary of expenses.
        """
        super(Expenses, self).__init__(name, desc)
        self._expenses = {}
        self._yearly_expenses = {}

    @staticmethod
    def __str__():
        return f'Expenses'

    # TODO implement
    def get_jsonification(self) -> dict:
        jsonification = super().get_jsonification()

    def add(self, label: str, amount: (int, float)) -> bool:
        """
        Adds an expense with a label and monthly amount.
        :param label: The label for the expense.
        :param amount: The monthly amount
        :return: Nothing.
        """
        if isinstance(label, str) and isinstance(amount, (int, float)):
            self._expenses.update({label.capitalize(): round(amount, 2)})
            return True
        return False

    def rem(self, label: str) -> bool:
        """
        Removes an expense.
        :param label: The label of the expense to be removed
        :return: True if removal was successful. False if key does not exist in dictionary.
        """
        if label in self._expenses:
            del self._expenses[label]
            return True
        return False

    def reset(self) -> None:
        """
        Clears all of the expenses.
        :return: Nothing.
        """
        self._expenses.clear()

    def all(self) -> dict:
        """
        Returns the dictionary of expenses.
        :return: The expenses.
        """
        return self._expenses

    def total(self) -> float:
        """
        Returns the total of all expenses.
        :return: The total monthly expenditure.
        """
        total = 0
        for e in self._expenses:
            total += self._expenses.get(e)
        return round(total, 2)

    def change_label(self, old_label: str, new_label: str) -> bool:
        """
        Changes the label for an expense.
        :param old_label: the old label.
        :param new_label: the new label.
        :return: True if successful.
        """
        if old_label in self._expenses:
            self.add(new_label, self._expenses.get(old_label))
            self.rem(old_label)
            return True
        return False


class Income(FinanceObj):
    def __init__(self, name, desc=""):
        super(Income, self).__init__(name, desc)

    @staticmethod
    def __str__():
        return f'Income'


class Bracket:
    def __init__(self, rate, lower, upper):
        self.rate = rate
        self.lower = lower
        self.upper = upper


class BracketWindow:
    def __init__(self, root, tax_bracket):
        self._bracket = tax_bracket

        self._rate = tk.DoubleVar()
        self._lower = tk.DoubleVar()
        self._upper = tk.DoubleVar()

        window = tk.Toplevel(root)
        window.title(f"Define Tax Bracket: {tax_bracket.data('name')}")
        window.grid_propagate(True)
        self._frame = tk.Frame(window)
        self._frame.grid(column=0, row=0)
        self.populate()
        self._root = root

    def new_bracket(self):
        pass

    def delete_bracket(self):
        pass

    def populate(self):
        pass

    def exit(self):
        self._frame.winfo_toplevel().destroy()


class TaxBracket(FinanceObj):
    """
    Represents a tax bracket for income. Includes methods for getting the taxed amount and effective tax rate.
    """
    def __init__(self, name: str, desc: str="") -> None:
        super(TaxBracket, self).__init__(name, desc)
        self._brackets = []
        self._data.update({
            'state': '',
            'locality': '',
            'filing status': 'Single',
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
            self._brackets.append([upper_range, rate/100])
            self._brackets.sort()
        else:
            self._brackets[index] = [upper_range, rate/100]

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

    def calculate_taxed_amount(self, income):
        """
        Calculates the total taxed amount and the effective tax rate for a given income.
        :param income: The yearly income to be taxed
        :return: A list of the taxed amount and the effective rate.
        """
        if len(self._brackets) == 0:
            return None

        taxed_amount = 0
        if self._tax_type.capitalize() == "Federal":
            income -= self._standard_deduction

            # Social Security Amount
            if income < 147000:
                taxed_amount += income * 0.062
            else:
                taxed_amount += 147000 * 0.062

            # Medicare Amount
            if income < 200000:
                taxed_amount += income * 0.0145
            else:
                taxed_amount += ((200000 * 0.0145) + ((income - 200000) * 0.0235))

        for i in range(0, len(self._brackets)):
            if i == 0:
                if income >= self._brackets[i][0]:
                    taxed_amount += self._brackets[i][0] * self._brackets[i][1]
                else:
                    taxed_amount += income * self._brackets[i][1]
            else:
                lower_range = self._brackets[i-1][0]
                upper_range = self._brackets[i][0]
                if income >= upper_range:
                    taxed_amount += (upper_range - lower_range) * self._brackets[i][1]
                elif income < upper_range and income > lower_range:
                    taxed_amount += (income - lower_range) * self._brackets[i][1]
        
        return [round(taxed_amount, 2), round(100 * taxed_amount / income, 4)]

    def get_editable(self, root, parent):
        frame, index = super().get_editable(root, parent)

        index = self.tk_editable_dropdown('type', 'Type', self._valid_types, frame, parent, index)
        if self.data('type').capitalize() == 'State':
            index = self.tk_editable_string_pair('state', "State", frame, parent, index)
        elif self.data('type').capitalize() == 'Local':
            index = self.tk_editable_string_pair('locality', "Locality", frame, parent, index)
        index = self.tk_editable_dropdown('filing status', 'Filing Status', self._valid_status, frame, parent, index)

        return frame, index

    def get_list_button(self, root, parent):
        name = self.data('type')
        desc = self.data('status')
        super().get_list_button(root, parent, name, desc)



class Job(FinanceObj):
    """Represents a job."""
    def __init__(self,
                 title: str,
                 desc: str = "",
                 income: (int, float) = 30000,
                 rate_401k: float = 0,
                 rate_roth: float = 0
                 ) -> None:
        """
        Initializes the Job object with a title and description. Income and retirement contribution rates are optional.
        :param title: The job title.
        :param desc: Brief description of the job.
        :param income: Annual salary for the job
        :param rate_401k: 401k contribution rate.
        :param rate_roth: roth contribution rate.
        """
        super().__init__(title, desc)

        self._data.update({
            'income': income,
            '401k rate': rate_401k,
            'roth rate': rate_roth,
            'pay frequency': 'Weekly'
        })
        self._income = income
        self._401k_rate = rate_401k
        self._roth_rate = rate_roth

        self._taxes = []
        self._pre_tax_deductions = Expenses('pre tax')
        self._post_tax_deductions = Expenses('post tax')

        self._valid_pay_frequency = ['Hourly', 'Weekly', 'Bi-Weekly', 'Monthly', 'Annually']
        self.button_hover_message = f"Click to populate a list of {self.__str__()}s."

    @staticmethod
    def __str__():
        return f'Jobs'

    def get_gross_income(self) -> (int, float):
        """
        Returns the annual amount earned before taxes and deductions like retirement and health insurance.
        :return: Gross income earned.
        """
        return self._income

    def get_pretax_income(self) -> (int, float):
        """
        Returns the net amount before taxes and post tax deductions are applied.
        :return: The pre tax annual income.
        """
        income = self._income

        if len(self._pre_tax_deductions) == 0:
            return income

        income = income * (1 - self._401k_rate)
        income -= self._pre_tax_deductions.total()

        return income

    def get_posttax_income(self) -> (int, float):
        """
        Returns the net annual amount after taxes and deductions.
        :return: The net annual income.
        """
        income = self.get_pretax_income()
        taxed_amount = 0
        deducted_amount = 0

        for tax in self._taxes:
            taxed_amount += tax.calculate_taxed_amount(income)
        deducted_amount = self._post_tax_deductions.amount()

        income = income * (1 - self._roth_rate)
        income -= (taxed_amount + deducted_amount)

        return income

    def set_401k(self, rate):
        self._401k_rate = rate

    def set_roth(self, rate):
        self._roth_rate = rate

    def add_tax_bracket(self, tax: TaxBracket):
        if tax not in self._tax_bracket:
            self._taxes.append(tax)
            return True
        return False

    def get_editable(self, root, parent) -> tuple:
        frame, index = super().get_editable(root, parent, name="Title", desc="Company")

        index = self.tk_line_break(frame, index)
        index = self.tk_editable_string_pair('income', 'Income', frame, parent, index)
        index = self.tk_editable_dropdown('pay frequency', 'Pay Frequency', self._valid_pay_frequency,
                                          self.data('pay frequency'), frame, parent, index)
        index = self.tk_editable_float_pair('401k rate', '401k Contribution %', frame, parent, index)
        index = self.tk_editable_float_pair('roth rate', 'Roth Contribution %', frame, parent, index)

        tk.Label(frame).grid(column=1, row=9)
        tk.Button(frame, text="Tax Brackets").grid(column=2, row=10, sticky=W + E)
        tk.Button(frame, text="Pre Tax Deductions").grid(column=2, row=11, sticky=W + E)
        tk.Button(frame, text="Post Tax Deductions").grid(column=2, row=12, sticky=W + E)
        index += 1


#TODO add support for assets like 401k, IRA, houses, bank accounts
class Assets(FinanceObj):
    def __init__(self):
        pass

    @staticmethod
    def __str__():
        return f'Assets'

