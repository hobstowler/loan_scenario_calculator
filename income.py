# Author: Hobs Towler
# Date: 12/1/2021
# Description:
import json
import tkinter as tk
from tkinter import *

from misc import *


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
        self._assumptions = {}
        self._active = False
        self._form_vars = {}
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
        return self._data

    def get_assumptions(self) -> dict:
        return self._assumptions

    def data(self, key: str):
        """
        Gets the value from the data dict.
        :return: The value for the given key.
        """
        return self._data.get(key)

    def assume(self, key: str):
        return self._assumptions.get(key)

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

    #TODO validate input is correct
    def save(self, key, parent):
        f_var = self._form_vars.get(key)
        val = f_var.get()
        if isinstance(f_var, StringVar):
            print("it's a string")
        elif isinstance(f_var, DoubleVar):
            print("it's a float")
        self._data.update({key: val})
        parent.populate_editable(self)

    def save_all(self, parent):
        for key in self._form_vars:
            print('saving:', key)
            self._data.update({key: self._form_vars.get(key).get()})
        parent.save_fin_obj(self)

        parent.populate_list(refresh=True)

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
        tk.Label(root, text="").grid(column=0, row=index)

        return index + 1

    def tk_editable_entry(self, key, text, root, parent, index, additional_info: str = None):
        val = self.data(key)
        if val is None:
            raise ValueError
        elif isinstance(val, int) or isinstance(val, float):
            s_var = tk.DoubleVar()
        else:
            s_var = tk.StringVar()
        s_var.set(val)
        self._form_vars.update({key: s_var})

        tk.Label(root, text=text, anchor='e').grid(column=1, row=index, sticky=W + E, padx=(0, 2))
        entry = tk.Entry(root, name=key, textvariable=s_var)
        col_span = 2
        if additional_info is not None:
            col_span = 1
            tk.Label(root, text=additional_info, anchor='e').grid(column=3, row=index, columnspan=col_span, sticky=W + E)
        entry.grid(column=2, row=index, columnspan=col_span, sticky=W + E)
        entry.bind("<FocusOut>", lambda e, k=key, p=parent: self.save(k, p))

        return index + 1

    def tk_editable_dropdown(self, key, text, values, root, parent, index) -> int:
        s_var = StringVar()
        s_var.set(self.data(key))
        self._form_vars.update({key: s_var})

        dropdown = tk.OptionMenu(root, s_var, *values)
        tk.Label(root, text=text, anchor='e').grid(column=1, row=index, sticky=W + E, padx=(0, 2))
        dropdown.grid(column=2, row=index, columnspan=2, sticky=W + E)
        s_var.trace('w', lambda e, f, g, k=key, p=parent: self.save(k, p))

        return index + 1

    def launch_assumption_window(self, parent):
        root = parent.get_root()
        AssumptionsWindow(root, parent, self)

    def list_button_enter(self, parent, e):
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
        parent.populate_info(self.list_hover_message())

    def list_button_leave(self, parent, e):
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
        parent.populate_info("")

    def get_list_button(self, root, parent, name=None, desc=None):
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

        frame.bind("<Button-1>", lambda e, p=parent: self.left_click(p))
        frame.bind("<Button-3>", lambda e, p=parent: self.right_click(p))
        frame.bind("<Enter>", lambda e, p=parent: self.list_button_enter(p, e))
        frame.bind("<Leave>", lambda e, p=parent: self.list_button_leave(p, e))
        for c in frame.winfo_children():
            c.bind("<Button-1>", lambda e, p=parent: self.left_click(p))
            c.bind("<Button-3>", lambda e, p=parent: self.right_click(p))
            c.bind("<Enter>", lambda e, p=parent: self.list_button_enter(p, e))
            #c.bind("<Leave>", self.list_leave)
            if self._active:
                c['bg'] = Style.color("b_sel")

        if self._active:
            frame['bg'] = Style.color("b_sel")

    def get_editable(self, root, parent, name: str = None, desc: str = None) -> tuple:
        """
        Builds an editable view for a FinanceObj in the left drawer. Typically called when user clicks edit or right-
        clicks an item in the drawer.
        :param root: The root frame used to build the editable view.
        :param parent: The parent LeftPanel. Used for callbacks and lambda functions.
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
        frame.pack(fill='both')
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=2)
        frame.columnconfigure(2, weight=2)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=0)

        save = tk.Button(frame, text='Save')
        save.grid(column=3, row=index)
        save.bind('<Button-1>', lambda e, p=parent: self.save_all(p))
        cancel = tk.Button(frame, text='X', anchor='e')
        cancel.grid(column=4, row=index)
        cancel.bind('<Button-1>', lambda e, p=parent: self.cancel(p))
        index += 1
        assumptions_button = tk.Button(frame, text='Assumptions')
        assumptions_button.grid(column=3, row=index, columnspan=2)
        assumptions_button.bind('<Button-1>', lambda e, p=parent: self.launch_assumption_window(p))
        if len(self._assumptions) < 1:
            assumptions_button['state'] = 'disabled'
        index += 1

        index = self.tk_line_break(frame, index)
        index = self.tk_editable_entry('name', name, frame, parent, index)
        index = self.tk_editable_entry('desc', desc, frame, parent, index)

        return frame, index

    def get_detail(self, root, parent) -> tuple:
        """
        Builds the tk Frame layout for the detailed panel. Typically called when a user left clicks from the list.
        :param root: The root Tk Frame of the detail panel.
        :param parent: The LeftPanel object. Used for callbacks and lambda functions
        :return: Returns the frame and information panels to be used for inherited calls.
        """
        frame = tk.Frame(root)
        frame.pack(fill='both')
        frame.pack_propagate(False)
        frame.grid_propagate(False)

        # TOP INFORMATION BANNER
        information = tk.Frame(root, width=700, height=49)
        information.grid(column=0, row=0, columnspan=7, sticky=W+E, pady=(0, 3))
        information.grid_propagate(False)

        name = tk.Label(information, text=self.name(), font=('bold', 13))
        name.grid(column=0, row=0, sticky=W)
        desc = tk.Label(information, text=self.desc())
        desc.grid(column=0, row=1, sticky=W)

        information['bg'] = Style.color('bg_header')
        for c in information.winfo_children():
            c['bg'] = Style.color('bg_header')

        return frame, information


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
        self._expenses = []

    @staticmethod
    def __str__():
        return f'Expenses'

    # TODO implement
    def get_jsonification(self) -> dict:
        jsonification = super().get_jsonification()

        expense_list = []
        for expense in self._expenses:
            expense_list.append(expense.get_jsonification())
        jsonification.update({'expense list': expense_list})

        return jsonification

    def add_expense(self, new_expense: Expense):
        if new_expense not in self._expenses:
            self._expenses.append(new_expense)

    def remove_expense(self, expense):
        if expense in self._expenses:
            self._expenses.remove(expense)

    def reset(self) -> None:
        """
        Clears all of the expenses.
        :return: Nothing.
        """
        self._expenses.clear()

    def get_expenses(self) -> list:
        """
        Returns the dictionary of expenses.
        :return: The expenses.
        """
        return self._expenses

    def get_expense_total(self) -> float:
        """
        Returns the total of all expenses.
        :return: The total monthly expenditure.
        """
        total = 0
        for expense in self._expenses:
            total += expense.amount
        return round(total, 2)

    def launch_expense_window(self, parent):
        root = parent.get_root()
        ExpenseWindow(root, parent, self)

    def get_editable(self, root, parent, name: str = None, desc: str = None) -> tuple:
        frame, index = super().get_editable(root, parent, name)

        index = self.tk_line_break(frame, index)

        expense_button = tk.Button(frame, text='Edit Expenses')
        expense_button.grid(column=2, row=index, columnspan=2, sticky=W+E)
        expense_button.bind("<Button-1>", lambda e, p=parent: self.launch_expense_window(p))
        index += 1

        return frame, index


class Income(FinanceObj):
    def __init__(self, name, desc=""):
        super(Income, self).__init__(name, desc)

    @staticmethod
    def __str__():
        return f'Income'


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

    def launch_bracket_editor(self, parent):
        root = parent.get_root()
        BracketWindow(root, parent, self)

    def get_editable(self, root, parent) -> tuple:
        frame, index = super().get_editable(root, parent)

        index = self.tk_editable_dropdown('type', 'Type', self._valid_types, frame, parent, index)
        if self.data('type').capitalize() == 'State':
            index = self.tk_editable_entry('state', "State", frame, parent, index)
        elif self.data('type').capitalize() == 'Local':
            index = self.tk_editable_entry('locality', "Locality", frame, parent, index)
        index = self.tk_editable_dropdown('filing status', 'Filing Status', self._valid_status, frame, parent, index)

        brackets = tk.Button(frame, text="Define Brackets")
        brackets.grid(column=2, row=index, columnspan=2, sticky=W+E)
        brackets.bind("<Button-1>", lambda e, p=parent: self.launch_bracket_editor(p))

        return frame, index

    def get_list_button(self, root, parent):
        name = self.data('type')
        desc = self.data('status')
        super().get_list_button(root, parent, name, desc)


class Job(FinanceObj):
    """Represents a job."""
    def __init__(self, title: str, company: str = "") -> None:
        """
        Initializes the Job object with a title and description. Income and retirement contribution rates are optional.
        :param title: The job title.
        :param company: Brief description of the job.
        """
        super().__init__(title, company)

        self._data.update({
            'income': 30000,
            '401k rate': 4,
            'roth rate': 4,
            'pay frequency': 'Weekly'
        })
        self._assumptions.update({
            'social security rate': 6.2,
            'social security cap': 147000,
            'medicate tax rate': 1.45
        })

        self._taxes = []
        self._pre_tax_deductions = Expenses('pre tax')
        self._post_tax_deductions = Expenses('post tax')

        self._valid_pay_frequency = ['Weekly', 'Bi-Weekly', 'Semimonthly', 'Monthly', 'Quarterly', 'Annually']
        self._num_pay_periods = {
            'Weekly': 52,
            'Bi-Weekly': 26,
            'Semimonthly': 24,
            'Monthly': 12,
            'Quarterly': 4,
            'Annually': 1
        }

        self.button_hover_message = f"Click to populate a list of {self.__str__()}s."

    @staticmethod
    def __str__():
        return f'Jobs'

    # TODO implement
    def get_jsonification(self) -> dict:
        pass

    def get_annual_income(self) -> (int, float):
        return self.get_pay_periods() * self.data('income')

    def get_pay_periods(self):
        """
        Returns the number of pay periods based on pay frequency. Used to calculate annual ammounts.
        :return: The number of pay periods.
        """
        return self._num_pay_periods.get(self.data('pay frequency'))

    def get_401k_amount(self) -> (int, float):
        return round(self.data('401k rate') * self.data('income') / 100, 2)

    def get_roth_amount(self):
        return round(self.data('roth rate') * self.data('income') / 100, 2)

    def get_pretax_income(self) -> (int, float):
        """
        Returns the net amount before taxes and post tax deductions are applied.
        :return: The pre tax annual income.
        """
        income = self.data('income')
        total_deduction = 0
        total_deduction += self.get_401k_amount()
        for deduction in self._pre_tax_deductions:
            total_deduction += deduction.amount

        return round(income - total_deduction, 2)

    def get_posttax_income(self) -> (int, float):
        """
        Returns the net annual amount after taxes and deductions.
        :return: The net annual income.
        """
        income = self.get_pretax_income()
        taxed_amount = 0
        total_deduction = 0

        for tax in self._taxes:
            taxed_amount += tax.calculate_taxed_amount(income)
        for deduction in self._post_tax_deductions:
            total_deduction += deduction.amount
        taxed_amount += self.get_social_security_taxed_amount()
        taxed_amount += self.get_medicare_taxed_amount()
        taxed_amount += self.get_roth_amount()

        return round(income - taxed_amount - total_deduction, 2)

    # TODO calculate employer responsibility
    def get_social_security_taxed_amount(self):
        cap = self.assume('social security cap')
        rate = self.assume('social security rate')
        income = self.get_annual_income()
        if income <= cap:
            return rate * income / 100
        else:
            return rate * cap / 100

    # TODO calculate employer responsibility
    def get_medicare_taxed_amount(self):
        rate = self.assume('medicare tax rate')
        income = self.data('income')
        return rate * income / 100

    def launch_deduction_selector(self, parent, expense):
        root = parent.get_root()
        ExpenseSelector(root, parent, expense)

    def launch_tax_selector(self, parent):
        root = parent.get_root()
        TaxSelector(root, parent, self._taxes)

    def get_editable(self, root, parent) -> tuple:
        frame, index = super().get_editable(root, parent, name="Title", desc="Company")
        index = self.tk_line_break(frame, index)

        index = self.tk_editable_dropdown('pay frequency', 'Pay Frequency', self._valid_pay_frequency,
                                          frame, parent, index)
        pay_freq = self.data('pay frequency')
        pay_periods = 'x ' + str(self.get_pay_periods())
        index = self.tk_editable_entry('income', 'Income (' + pay_freq + ')',
                                       frame, parent, index, pay_periods)
        tk.Label(frame, text=f'= ${round(self.data("income") * self.get_pay_periods(),2):,}', anchor='e')\
            .grid(column=2, row=index, columnspan=2, sticky=W+E)
        index += 1
        index = self.tk_line_break(frame, index)

        retirement = f'  ${self.get_401k_amount():,}'
        roth = f'  ${self.get_roth_amount():,}'
        index = self.tk_editable_entry('401k rate', '401k Contribution', frame, parent, index, retirement)
        index = self.tk_editable_entry('roth rate', 'Roth Contribution', frame, parent, index, roth)
        tk.Label(frame, text=f'= ${round(self.get_401k_amount() + self.get_roth_amount(),2):,}', anchor='e')\
            .grid(column=2, row=index, columnspan=2, sticky=W+E)
        index += 1
        index = self.tk_line_break(frame, index)

        bracket_button = tk.Button(frame, text="Tax Brackets")
        bracket_button.grid(column=2, row=index, columnspan=2, sticky=W + E)
        bracket_button.bind("<Button-1>", lambda e, p=parent: self.launch_tax_selector(p))
        index += 1

        pre_tax_amount = self._pre_tax_deductions.get_expense_total()
        tk.Label(frame, text=f"${pre_tax_amount:,}", anchor='e').grid(column=1, row=index, sticky=W+E)
        pre_tax_button = tk.Button(frame, text="Pre Tax Deductions")
        pre_tax_button.grid(column=2, row=index, columnspan=2, sticky=W + E)
        pre_tax_button.bind("<Button-1>",
                            lambda e, p=parent, d=self._pre_tax_deductions: self.launch_deduction_selector(p, d))
        index += 1

        post_tax_amount = self._post_tax_deductions.get_expense_total()
        tk.Label(frame, text=f"${post_tax_amount:,}", anchor='e').grid(column=1, row=index, sticky=W + E)
        post_tax_button = tk.Button(frame, text="Post Tax Deductions")
        post_tax_button.grid(column=2, row=index, columnspan=2, sticky=W + E)
        post_tax_button.bind("<Button-1>",
                             lambda e, p=parent, d=self._post_tax_deductions: self.launch_deduction_selector(p, d))
        index += 1

        return frame, index


#TODO add support for assets like 401k, IRA, houses, bank accounts
class Assets(FinanceObj):
    def __init__(self, name: str, desc: str = ""):
        self._assets = []
        super().__init__(name, desc)

    @staticmethod
    def __str__():
        return f'Assets'

    def get_assets(self):
        return self._assets

    def launch_asset_window(self, parent):
        root = parent.get_root()
        AssetWindow(root, parent, self)

    def get_editable(self, root, parent, name: str = None, desc: str = None) -> tuple:
        frame, index = super().get_editable(root, parent, name)

        index = self.tk_line_break(frame, index)

        expense_button = tk.Button(frame, text='Edit Assets')
        expense_button.grid(column=2, row=index, columnspan=2, sticky=W+E)
        expense_button.bind("<Button-1>", lambda e, p=parent: self.launch_asset_window(p))
        index += 1

        return frame, index

