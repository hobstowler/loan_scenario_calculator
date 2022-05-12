# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import locale
from tkinter import *

from financeObj import FinanceObj
from misc import *


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
        index = self.tk_editable_entry('label', 'Labels', frame, index)
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
        return total

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
        index = self.tk_editable_entry('label', 'Labels', frame, index)
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
        print('income', income)
        if len(self._brackets) == 0:
            return 0

        taxed_amount = 0
        for i in range(0, len(self._brackets)):
            print("rate:", self._brackets[i].rate)
            print("upper:", self._brackets[i].upper)
            if i == 0:
                if income >= self._brackets[i].upper:
                    amount = (self._brackets[i].upper * self._brackets[i].rate / 100)
                    print(amount)
                    taxed_amount += amount
                else:
                    amount = income * self._brackets[i].rate / 100
                    print(amount)
                    taxed_amount += amount
            else:
                lower_range = self._brackets[i - 1].upper + 0.01
                upper_range = self._brackets[i].upper
                if income >= upper_range:
                    amount = (upper_range - lower_range) * self._brackets[i].rate / 100
                    print(amount)
                    taxed_amount += amount
                elif income < upper_range and income > lower_range:
                    amount = (income - lower_range) * self._brackets[i].rate / 100
                    print('upper:', upper_range, 'lower:', lower_range)
                    print(amount)
                    taxed_amount += amount

        taxed_amount = round(taxed_amount, 2)
        print(taxed_amount)
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
            index = self.tk_editable_entry('state', "State", frame, index)
        elif self.data('type').capitalize() == 'Local':
            index = self.tk_editable_entry('locality', "Locality", frame, index)

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
        self._breakdowns = ['Annual', 'Monthly', 'Per Pay Period']
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

    def get_annual_401k_amount(self, annual: bool = True) -> float:
        income = self.get_annual_income() if annual else self.data('income')
        return self.data('401k rate') * income / 100

    def get_annual_roth_amount(self, annual: bool = True):
        income = self.get_annual_income() if annual else self.data('income')
        return self.data('roth rate') * income / 100

    def get_pretax_income(self, annual: bool = True) -> float:
        """
        Returns the net amount before taxes and post tax deductions are applied.
        :return: The pre tax annual income.
        """
        income = self.get_annual_income()
        total_deduction = 0
        total_deduction += self.get_annual_401k_amount()
        total_deduction += self._pre_tax_deductions.get_total()

        return income - total_deduction

    def get_annual_post_tax_income(self) -> (int, float):
        """
        Returns the net annual amount after taxes and deductions.
        :return: The net annual income.
        """
        income = self.get_pretax_income()
        taxed_amount = 0
        total_deduction = 0

        federal, state, local = self.get_annual_taxed_amounts()
        taxed_amount += federal
        taxed_amount += state
        taxed_amount += local
        total_deduction += self._post_tax_deductions.get_total()

        taxed_amount += self.get_annual_social_security()
        taxed_amount += self.get_annual_medicare()
        taxed_amount += self.get_annual_roth_amount()

        return income - taxed_amount - total_deduction

    def get_annual_taxed_amounts(self):
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

    # TODO calculate employer responsibility
    def get_annual_social_security(self):
        cap = self.assume('social security cap')
        rate = self.assume('social security rate') / 100
        income = self.get_annual_income()
        pay_periods = self.get_pay_periods()
        if income <= cap:
            return round((rate * income) / pay_periods, 2)
        else:
            return round((rate * cap) / pay_periods, 2)

    # TODO calculate employer responsibility
    def get_annual_medicare(self):
        rate = self.assume('medicare tax rate') / 100
        income = self.data('income')
        return round(rate * income, 2)

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
        index = self.tk_editable_entry('income', 'Income (' + pay_freq + ')', frame, index, pay_periods)
        tk.Label(frame, text=f'= ${round(self.data("income") * self.get_pay_periods(), 2):,}', anchor='e') \
            .grid(column=2, row=index, columnspan=2, sticky=W + E)
        index += 1
        index = self.tk_line_break(frame, index)

        # Retirement accounts section
        retirement = f'  ${self.get_annual_401k_amount():,}'
        roth = f'  ${self.get_annual_roth_amount():,}'
        index = self.tk_editable_entry('401k rate', '401k Contribution', frame, index, retirement)
        index = self.tk_editable_entry('roth rate', 'Roth Contribution', frame, index, roth)
        tk.Label(frame, text=f'= ${round(self.get_annual_401k_amount() + self.get_annual_roth_amount(), 2):,}', anchor='e') \
            .grid(column=2, row=index, columnspan=2, sticky=W + E)
        index += 1
        index = self.tk_line_break(frame, index)

        # Tax brackets section
        bracket_button = tk.Button(frame, text="Tax Brackets")
        bracket_button.grid(column=1, row=index, columnspan=2, sticky=W + E)
        bracket_button.bind("<Button-1>", lambda e: self.launch_tax_selector())
        index += 1

        # Pre tax deductions section
        pre_tax_amount = self._pre_tax_deductions.get_total()
        tk.Label(frame, text=f"${pre_tax_amount:,}", anchor='e').grid(column=0, row=index, sticky=W + E)
        pre_tax_button = tk.Button(frame, text="Pre Tax Deductions")
        pre_tax_button.grid(column=1, row=index, columnspan=2, sticky=W + E)
        pre_tax_button.bind("<Button-1>",
                            lambda e, d=self._pre_tax_deductions: self.launch_deduction_selector(d))
        index += 1

        # Post tax deductions section
        post_tax_amount = self._post_tax_deductions.get_total()
        tk.Label(frame, text=f"${post_tax_amount:,}", anchor='e').grid(column=0, row=index, sticky=W + E)
        post_tax_button = tk.Button(frame, text="Post Tax Deductions")
        post_tax_button.grid(column=1, row=index, columnspan=2, sticky=W + E)
        post_tax_button.bind("<Button-1>",
                             lambda e, d=self._post_tax_deductions: self.launch_deduction_selector(d))
        index += 1

        return frame, index

    def get_detail(self, root, name: str = None, desc: str = None) -> tuple:
        frame = super().get_detail(root)


        breakdown = tk.Frame(frame)
        breakdown.pack(fill=X, padx=10, pady=(30, 15))
        breakdown.columnconfigure(0, weight=1)
        breakdown.columnconfigure(1, weight=1)

        income = tk.Frame(breakdown, height=200)
        income.grid(column=0, row=1, sticky=W+E)

        self.get_detailed_income(income)

        retirement = tk.Frame(breakdown, height=200)
        retirement.grid(column=1, row=1, sticky=N+W+E)

        self.get_detailed_retirement(retirement)

        return frame

    def get_detailed_income(self, root):
        pay_periods = self.get_pay_periods()
        breakdown = self._breakdown.get()

        # Header and dropdown
        index = 0
        tk.Label(root, text="Income Breakdown", anchor='w', font=('bold', 11)) \
            .grid(column=0, row=index, columnspan=2, sticky=W + E)
        index += 1
        index = self.tk_line(root, index, colspan=4)
        time_period = tk.OptionMenu(root, self._breakdown, *self._breakdowns)
        time_period.grid(column=0, row=index, columnspan=2, sticky=W + E)
        index += 1
        index = self.tk_line_break(root, index)

        # Gross Income Section
        income_per = locale.currency(self.data('income'), grouping=True)
        annual_income = locale.currency(self.get_annual_income(), grouping=True)

        index = self.tk_list_pair("Income per pay period:", f"{income_per}", root, index, 3)
        index = self.tk_list_pair(f"Pay periods ({self.data('pay frequency')}):", f"x {pay_periods}", root, index, 3)
        index = self.tk_line(root, index, column=3)
        if breakdown == "Monthly":
            annual_income = locale.currency(self.get_annual_income() / 12, grouping=True)
            index = self.tk_list_pair("Average Monthly Income:", f"{annual_income}", root, index, 3)
        else:
            index = self.tk_list_pair("Annual Gross Income:", f"{annual_income}", root, index, 3)
        index = self.tk_line_break(root, index)

        if breakdown == "Monthly":
            pay_periods = 12
        if breakdown == "Annual":
            pay_periods = 1

        # Pre Tax Net Income
        pre_tax_amount = locale.currency(self._pre_tax_deductions.get_total() / pay_periods, grouping=True)
        pre_tax_retirement = locale.currency(self.get_annual_401k_amount() / pay_periods, grouping=True)
        pre_tax_income = locale.currency(self.get_pretax_income() / pay_periods, grouping=True)

        index = self.tk_list_pair("Pre-Tax Deductions:", f"- {pre_tax_amount}", root, index, 3)
        index = self.tk_list_pair("401k Contributions:", f"- {pre_tax_retirement}", root, index, 3)
        index = self.tk_line(root, index, column=3)
        index = self.tk_list_pair("", f"{pre_tax_income}", root, index, 3)
        index = self.tk_line_break(root, index)

        # Post Tax Net Income
        post_tax_amount = locale.currency(self._post_tax_deductions.get_total() / pay_periods, grouping=True)
        post_tax_retirement = locale.currency(self.get_annual_roth_amount() / pay_periods, grouping=True)
        federal, state, local = self.get_annual_taxed_amounts()
        federal /= pay_periods
        state /= pay_periods
        local /= pay_periods

        federal = locale.currency(federal, grouping=True)
        state = locale.currency(state, grouping=True)
        local = locale.currency(local, grouping=True) if local != 0 else None
        social_security = locale.currency(self.get_annual_social_security() / pay_periods, grouping=True)
        medicare = locale.currency(self.get_annual_medicare() / pay_periods, grouping=True)
        post_tax_income = locale.currency(self.get_annual_post_tax_income() / pay_periods, grouping=True)

        index = self.tk_list_pair("Post-Tax Deductions:", f"- {post_tax_amount}", root, index, 3)
        index = self.tk_list_pair("Roth Contributions:", f"- {post_tax_retirement}", root, index, 3)
        index = self.tk_list_pair("Federal Withholding:", f"- {federal}", root, index, 3)
        index = self.tk_list_pair("State Withholding:", f"- {state}", root, index, 3)

        if local:
            index = self.tk_list_pair("Local Withholding:", f"- {local}", root, index, 3)

        index = self.tk_list_pair("Social Security Tax:", f"- {social_security}", root, index, 3)
        index = self.tk_list_pair("Medicare Tax:", f"- {medicare}", root, index, 3)
        index = self.tk_line(root, index, column=3)
        index = self.tk_list_pair("", f"{post_tax_income}", root, index, 3)

        index = self.tk_line_break(root, index)

    def get_detailed_retirement(self, root):
        pay_periods = self.get_pay_periods()
        annual_income = self.get_annual_income()
        roth_rate = self.data('roth rate')
        rate = self.data('401k rate')
        breakdown = self._breakdown.get()

        employer_match = self.assume('employer match')
        employer_per_check = annual_income * employer_match / 100 / self.get_pay_periods()
        employer_per_check = locale.currency(employer_per_check, grouping=True)
        employer_match_rate = self.assume('employer match rate')
        total_contribution_percent = rate + roth_rate
        contribution_intro = f'Your employer matches {employer_match_rate}% on {employer_match}% of your ' \
                             f'contributions. This works out to an extra {employer_per_check} per paycheck.'
        cont_mess_body = ""

        # Set pay period modifier and labels for breakdown based on current breakdown variable value
        if breakdown == "Per Pay Period":
            cont_label = f"Your 401k Contributions ({rate}%):"
            cont_roth_label = f"Your Roth Contributions ({roth_rate}%):"
            cont_employer_label = f"Your Employer's Contribution " \
                                  f"({int(employer_match_rate * employer_match / 100)}%):"
        elif breakdown == "Monthly":
            pay_periods = 12
            cont_label = f"Your Average Monthly 401k Contributions ({rate}%):"
            cont_roth_label = f"Your Average Monthly Roth Contributions ({roth_rate}%):"
            cont_employer_label = f"Your Employer's Average Monthly Contribution " \
                                  f"({employer_match_rate}% on {employer_match}%):"
        else:
            pay_periods = 1
            cont_label = f"Your Annual 401k Contributions ({rate}%):"
            cont_roth_label = f"Your Annual Roth Contributions ({roth_rate}%):"
            cont_employer_label = f"Your Employer's Annual Contribution " \
                                  f"({int(employer_match_rate * employer_match / 100)}%):"

        cont_diff = None
        cont_additional = None
        if total_contribution_percent < employer_match:
            cont_employer_amount = annual_income * total_contribution_percent * employer_match_rate / pay_periods / 10000
            cont_max_employer = annual_income * employer_match * employer_match_rate / pay_periods / 10000
            cont_diff = cont_max_employer - cont_employer_amount
            cont_additional = (employer_match - total_contribution_percent) / 100 * self.data('income') / pay_periods
            cont_mess_body = f'Your total contributions are less than what your employer matches on. Raise your' \
                                   f' total contribution rate to {employer_match}% to avoid losing out on your ' \
                                   f'employer\'s matching contributions to your retirement account.'
        elif total_contribution_percent >= employer_match:
            cont_employer_amount = annual_income * employer_match * employer_match_rate / pay_periods / 10000
            cont_mess_body = f'You\'re getting the full benefit of your employer\'s matching contribution. ' \
                                   f'Excellent! Contributions above your current rate won\'t be matched by your ' \
                                   f'employer, but you might consider contributing more anyways.'

        index = 0
        tk.Label(root, text="Retirement Summary Breakdown", anchor='w', font=('bold', 11)) \
            .grid(column=0, row=index, columnspan=2, sticky=W + E)
        index += 1
        index = self.tk_line(root, index, colspan=4)
        index = self.tk_line_break(root, index)

        cont_intro = tk.Label(root, text=contribution_intro, anchor='w', wraplength=400, justify=LEFT)
        cont_intro.grid(column=0, row=index, columnspan=4, sticky=W+E)
        index += 1

        index = self.tk_line_break(root, index)

        cont_mess = tk.Label(root, text=cont_mess_body, anchor='w', wraplength=400, justify=LEFT)
        cont_mess.grid(column=0, row=index, columnspan=4, sticky=W+E)
        index += 1

        index = self.tk_line_break(root, index)

        contribution_401k = self.get_annual_401k_amount() / pay_periods
        contribution_roth = self.get_annual_roth_amount() / pay_periods
        total = cont_employer_amount + contribution_roth + contribution_401k

        contribution_401k = locale.currency(contribution_401k, grouping=True)
        contribution_roth = locale.currency(self.get_annual_roth_amount() / pay_periods, grouping=True)
        cont_employer_amount = locale.currency(cont_employer_amount, grouping=True)

        index = self.tk_list_pair('Retirement Contributions:', '', root, index, 3, anchor='w', color='green')
        index = self.tk_line(root, index, colspan=4, padding=0)
        index = self.tk_list_pair(cont_label, f'{contribution_401k}',
                                  root, index, 3, highlight_color='blue')
        index = self.tk_list_pair(cont_roth_label, f'{contribution_roth}',
                                  root, index, 3, highlight_color='blue')
        index = self.tk_list_pair(cont_employer_label, f'{cont_employer_amount}',
                                  root, index, 3, highlight_color='blue')
        index = self.tk_line(root, index, column=3)
        index = self.tk_list_pair('', f'{locale.currency(total, grouping=True)}', root, index, 3, highlight_color='green')

        if cont_diff:
            diff_total = total + cont_diff + cont_additional
            cont_diff = locale.currency(cont_diff, grouping=True)
            cont_additional = locale.currency(cont_additional, grouping=True)
            diff_total = locale.currency(diff_total, grouping=True)

            index = self.tk_line_break(root, index)
            index = self.tk_list_pair('Lost Potential Contributions:', '', root, index, 3, anchor='w', color='red')
            index = self.tk_line(root, index, colspan=4, padding=0)
            index = self.tk_list_pair('Additional Employer Contribution:', f'{cont_diff}',
                                      root, index, 3, highlight_color='red')
            index = self.tk_list_pair('Additional Personal Contribution:', f'{cont_additional}',
                                      root, index, 3, highlight_color='red')
            index = self.tk_list_pair('Total:', f'{diff_total}',
                                      root, index, 3, highlight_color='red')

