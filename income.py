# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

colors = {
            "t_type": "navy",
            "t_name": "red",
            "b_sel": "green",
            "b_reset": "SystemButtonFace"
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
        self._data = {}
        self._data.update({'name': name})
        self._data.update({'desc': desc})
        self._active = False
        self._form_strings = {}

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

    def set_desc(self, new_desc: str) -> bool:
        """
        Sets a new description for the object. Returns true if the operation is successful.
        :param new_desc: The new description.
        :return: True if successful.
        """
        if isinstance(new_desc, str):
            self._desc = new_desc
            print("success")
            return True
        else:
            return False

    def desc(self) -> str:
        """
        Gets the description of the object.
        :return: The description.
        """
        return self._data.get('desc')

    def get_data(self) -> dict:
        return self._data

    def set_data(self, data: dict) -> None:
        self._data = data

    def type(self) -> str:
        return type(self).__name__

    def update(self, data: dict):
        for k in data.keys():
            if k == "name":
                self._name = data.get(k)
            elif k == "desc":
                self._desc = data.get(k)
            else:
                self._data.update({k: data.get(k)})

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

    def save(self):
        pass

    def get_list_button(self, root, parent):
        frame = tk.Frame(root, borderwidth=2, relief='groove', height=40)
        frame.pack(fill="x", ipady=2)
        frame.bind("<Button-1>", lambda e: self.left_click())
        #TODO Move to JSON for data load to allow changes to main attributes

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        name = tk.Label(frame, text=self._data.get('name'), justify=LEFT, anchor="w", foreground=colors.get("t_name"))
        name.grid(column=0, row=0, sticky=W)
        f_type = tk.Label(frame, text=self.type(), justify=RIGHT, anchor="e", foreground=colors.get("t_type"))
        f_type.grid(column=1, row=0, sticky=E)
        desc = tk.Label(frame, text=self._data.get('desc'), justify=LEFT, anchor="w")
        desc.grid(column=0, row=1, sticky=W, columnspan=2)

        frame.bind("<Button-1>", lambda e, w=parent: self.left_click(w))
        frame.bind("<Button-3>", lambda e, w=parent: self.right_click(w))
        for c in frame.winfo_children():
            c.bind("<Button-1>", lambda e, w=parent: self.left_click(w))
            c.bind("<Button-3>", lambda e, w=parent: self.right_click(w))
            if self._active:
                c['bg'] = colors.get("b_sel")

        if self._active:
            frame['bg'] = colors.get("b_sel")

    def get_editable(self, root, parent, name: str = None, desc: str = None):
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

        cancel = tk.Button(frame, text='X', anchor='e')
        cancel.grid(column=4, row=0)
        cancel.bind('<Button-1>', lambda e, w=parent: self.cancel(w))

        key = 'name'
        value = self._data.get(key)
        s_var = StringVar()
        s_var.set(value)
        self._form_strings.update({key: s_var})
        tk.Label(frame, text=name, anchor='e').grid(column=1, row=1)
        tk.Entry(frame, name=key, textvariable=s_var).grid(column=2, row=1, columnspan=2, sticky=W+E)

        key = 'desc'
        value = self._data.get(key)
        s_var = StringVar()
        s_var.set(value)
        self._form_strings.update({key: s_var})
        tk.Label(frame, text=desc, anchor='e').grid(column=1, row=2)
        tk.Entry(frame, name=key, textvariable=s_var).grid(column=2, row=2, columnspan=2, sticky=W+E)
        return frame

    def get_detail(self, root, parent):
        pass


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


class TaxBracket(FinanceObj):
    """
    Represents a tax bracket for income. Includes methods for getting the taxed amount and effective tax rate.
    """
    def __init__(self, name: str, desc: str="") -> None:
        super(TaxBracket, self).__init__(name, desc)
        self._brackets = []
        self._label = ""
        self._state = ""
        self._status = ""
        self._tax_type = "FEDERAL"
        self._standard_deduction = 24000

        self._valid_types = ["STATE", "FEDERAL", "LOCAL"]
        self._valid_status = ["SINGLE", "MARRIED, JOINT", "MARRIED, SEPARATE", "HEAD OF HOUSEHOLD"]

    def change_label(self, new_label):
        """
        Changes the display label of the tax type.
        :param new_label: the new label.
        :return: Nothing.
        """
        if new_label.isalpha():
            self._label = new_label.capitalize

    def label(self):
        """
        Returns the display label for the tax bracket
        :return: the tax bracket label.
        """
        return self._label

    def tax_type(self):
        """
        Returns the tax type: Federal, State, or Local.
        :return: The tax type
        """
        return self._tax_type

    def change_state(self, new_state):
        """
        Change the geographic state that the tax bracket applies to.
        :param new_state: The new state.
        :return: Nothing.
        """
        if new_state.isalpha():
            self._state = new_state

    def get_state(self):
        """
        Gets the geographic state that the tax bracket applies to.
        :return: The geographic state.
        """
        return self._state

    def change_status(self, new_status):
        """
        Changes the filing status for this tax bracket.
        :param new_status: The new filing status.
        :return: Nothing.
        """
        new_status = new_status.upper()
        if new_status in self._valid_status:
            self._status = new_status

    def get_status(self):
        """
        Returns the filing status for this tax bracket.
        :return: The filing status for the tax bracket.
        """
        return self._status

    def set_standard_deduction(self, standard__deduction):
        self._standard_deduction = standard__deduction

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
        if self._tax_type == "FEDERAL":
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
        super(Job, self).__init__(title, desc)

        self._income = income
        self._401k_rate = rate_401k
        self._roth_rate = rate_roth

        self._taxes = []
        self._pre_tax_deductions = Expenses('pre tax')
        self._post_tax_deductions = Expenses('post tax')

        self._valid_pay_frequency = ['Hourly', 'Weekly', 'Bi-Weekly', 'Monthly', 'Annually']

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

    def get_editable(self, root, parent):
        frame = super().get_editable(root, parent, name="Title", desc="Company")

        tk.Label(frame).grid(column=1, row=4)

        income_string = StringVar()
        income_string.set(str(self._income))
        tk.Label(frame, text="Income", anchor='e').grid(column=1, row=5)
        tk.Entry(frame, name='income', textvariable=income_string).grid(column=2, row=5, columnspan=2, sticky=W + E)

        pay_vals = self._valid_pay_frequency
        pay_freq_string = StringVar()
        pay_freq_string.set(pay_vals[4])
        pay_freq = tk.OptionMenu(frame, pay_freq_string, *pay_vals)
        tk.Label(frame, text="Pay Frequency", anchor='e').grid(column=1, row=6)
        pay_freq.grid(column=2, row=6, columnspan=2, sticky=W + E)

        retirement_string = StringVar()
        retirement_string.set(self._401k_rate)
        tk.Label(frame, text="401k Contribution", anchor='e').grid(column=1, row=7)
        tk.Entry(frame, name='401k', textvariable=retirement_string).grid(column=2, row=7, columnspan=2, sticky=W + E)

        roth_string = StringVar()
        roth_string.set(self._401k_rate)
        tk.Label(frame, text="Roth Contribution", anchor='e').grid(column=1, row=8)
        tk.Entry(frame, name='roth', textvariable=roth_string).grid(column=2, row=8, columnspan=2, sticky=W + E)

        tk.Label(frame).grid(column=1, row=9)
        tk.Button(frame, text="Tax Brackets").grid(column=2, row=10, sticky=W + E)
        tk.Button(frame, text="Pre Tax Deductions").grid(column=2, row=11, sticky=W + E)
        tk.Button(frame, text="Post Tax Deductions").grid(column=2, row=12, sticky=W + E)


#TODO add support for assets like 401k, IRA, houses, bank accounts
class Assets(FinanceObj):
    def __init__(self):
        pass

