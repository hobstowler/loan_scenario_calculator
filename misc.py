# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 3/11/2022
# Description:
import tkinter
import tkinter as tk
from tkinter import E, W


class Expense:
    """
    Class representing a monthly expense.
    """
    def __init__(self, desc: str, amount: (int, float)) -> None:
        """
        Initializes the Expense object with a description and an amount
        :param desc:
        :param amount:
        """
        self.amount = amount
        self.desc = desc

    def get_jsonification(self) -> dict:
        """
        Returns a dict representing the Expense object that can be easily jsonified.
        :return: The dict representing the Expense.
        """
        jsonification = {
            'amount': self.amount,
            'desc': self.desc
        }
        return jsonification


class Asset(Expense):
    def __init__(self, desc: str, amount: (int, float)) -> None:
        super().__init__(desc, amount)


class Bracket:
    """
    Class representing a single tax bracket.
    """
    def __init__(self, rate: float, upper: (float, int)) -> None:
        """
        Initializes The bracket with a rate and upper range.
        :param rate: The tax rate for this range.
        :param upper: The upper taxable limit for this range.
        """
        self.rate = rate
        self.upper = upper

    def get_jsonification(self) -> dict:
        """
        Returns a JSON-friendly version of this bracket.
        :return: A dict object representing this object.
        """
        jsonification = {
            'rate': self.rate,
            'upper': self.upper
        }
        return jsonification


class ExtraPayment:
    """Class representing an extra payment on a loan. Has a defined start, length, and amount."""
    def __init__(self, start_month, length, amount):
        """
        Initializes the extra payment with a start month, length, and amount.
        :param start_month: The month that extra payments start occurring.
        :param length: The number of months that extra payments will be made.
        :param amount: The amount of extra money paid in each installment.
        """
        self.start = start_month
        self.length = length
        self.end = start_month + length
        self.amount = amount

    def get_jsonification(self) -> dict:
        """
        Returns a JSON-friendly version of this bracket.
        :return: A dict object representing this object.
        """
        jsonification = {
            'start': self.start,
            'length': self.length,
            'end': self.end,
            'amount': self.amount
        }
        return jsonification


class Window:
    def __init__(self, root, parent, fin_obj, title=None):
        self._fin_obj = fin_obj
        self._parent = parent

        self._window = tk.Toplevel(root)
        self._window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self._window.title(title)
        self._window.grid_propagate(True)
        self._frame = tk.Frame(self._window)
        self._frame.grid(column=0, row=0, padx=15, pady=15)
        self.populate()
        self._root = root

    def on_exit(self):
        self._parent.populate_editable(self._fin_obj)
        self._window.destroy()

    def populate(self):
        pass


class ExpenseWindow(Window):
    def __init__(self, root, parent, expense):
        title = f"Define Tax Bracket: {expense.data('name')}"

        self._desc = tk.StringVar()
        self._amount = tk.DoubleVar()

        super().__init__(root, parent, expense, title)

    def new_expense(self):
        new_expense = Expense(self._desc.get(), self._amount.get())
        expense_list = self._fin_obj.get_expenses()

        if new_expense not in expense_list:
            expense_list.append(new_expense)
        self._desc.set("")
        self._amount.set(0)

        self.populate()

    def delete_expense(self, expense):
        expense_list = self._fin_obj.get_expenses()
        if expense in expense_list:
            expense_list.remove(expense)

        self.populate()

    def populate(self):
        for c in self._frame.winfo_children():
            c.destroy()

        frame = self._frame
        expense_list = self._fin_obj.get_expenses()

        tk.Label(frame, text=self._fin_obj.name().title()).grid(column=0, row=0, columnspan=6)
        tk.Label(frame, text="").grid(column=0, row=1)

        tk.Label(frame, text='Expense Description').grid(column=0, row=2, columnspan=4)
        tk.Entry(frame, textvariable=self._desc).grid(column=0, row=3, columnspan=4)
        tk.Label(frame, text='Monthly Amount').grid(column=4, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._amount).grid(column=4, row=3, columnspan=2)
        add_button = tk.Button(frame, text='Add', width=6)
        add_button.grid(column=6, row=3, sticky=W + E)
        add_button.bind("<Button-1>", lambda e: self.new_expense())

        last = 6
        for i in range(len(expense_list)):
            tk.Label(frame, text=expense_list[i].desc, anchor='w').grid(column=0, row=6 + i, columnspan=2, sticky=W + E)
            tk.Label(frame, text=expense_list[i].amount, anchor='w').grid(column=4, row=6 + i, columnspan=2, sticky=W + E)
            del_button = tk.Button(frame, text="Delete", width=6)
            del_button.bind("<Button-1>", lambda e, p=expense_list[i]: self.delete_expense(p))
            del_button.grid(column=6, row=6 + i, columnspan=2, sticky=W + E)
            last += 1


class AssetWindow(Window):
    def __init__(self, root, parent, asset):
        title = f"Define Tax Bracket: {asset.data('name')}"

        self._desc = tk.StringVar()
        self._amount = tk.DoubleVar()

        super().__init__(root, parent, asset, title)

    def new_expense(self):
        new_asset = Asset(self._desc.get(), self._amount.get())
        asset_list = self._fin_obj.get_assets()

        if new_asset not in asset_list:
            asset_list.append(new_asset)
        self._desc.set("")
        self._amount.set(0)

        self.populate()

    def delete_expense(self, asset):
        asset_list = self._fin_obj.get_assets()
        if asset in asset_list:
            asset_list.remove(asset)

        self.populate()

    def populate(self):
        for c in self._frame.winfo_children():
            c.destroy()

        frame = self._frame
        asset_list = self._fin_obj.get_assets()

        tk.Label(frame, text=self._fin_obj.name().title()).grid(column=0, row=0, columnspan=6)
        tk.Label(frame, text="").grid(column=0, row=1)

        tk.Label(frame, text='Description').grid(column=0, row=2, columnspan=4)
        tk.Entry(frame, textvariable=self._desc).grid(column=0, row=3, columnspan=4)
        tk.Label(frame, text='Asset Value').grid(column=4, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._amount).grid(column=4, row=3, columnspan=2)
        add_button = tk.Button(frame, text='Add', width=6)
        add_button.grid(column=6, row=3, sticky=W + E)
        add_button.bind("<Button-1>", lambda e: self.new_expense())

        last = 6
        for i in range(len(asset_list)):
            tk.Label(frame, text=asset_list[i].desc, anchor='w').grid(column=0, row=6 + i, columnspan=2, sticky=W + E)
            tk.Label(frame, text=asset_list[i].amount, anchor='w').grid(column=4, row=6 + i, columnspan=2, sticky=W + E)
            del_button = tk.Button(frame, text="Delete", width=6)
            del_button.bind("<Button-1>", lambda e, p=asset_list[i]: self.delete_expense(p))
            del_button.grid(column=6, row=6 + i, columnspan=2, sticky=W + E)
            last += 1


# TODO support for infinite upper range
class BracketWindow(Window):
    """
    Class representing a window to add and delete brackets.
    """
    def __init__(self, root, parent, tax_bracket) -> None:
        """
        Initializes the BracketWindow with tk root object and a tax bracket object.
        :param root: The tk Root window.
        :param tax_bracket: The calling tax bracket.
        """
        title = f"Define Tax Bracket: {tax_bracket.data('name')}"

        self._rate = tk.DoubleVar()
        self._upper = tk.DoubleVar()

        super().__init__(root, parent, tax_bracket, title)

    def new_bracket(self) -> None:
        """
        Adds a new bracket to the Tax Bracket.
        """
        # todo logic for a valid bracket--cannot overlap
        # todo blank out on click/focus to prevent weird errors with leading zeros
        new_bracket = Bracket(self._rate.get(), self._upper.get())
        bracket_list = self._fin_obj.get_brackets()
        if new_bracket not in bracket_list:
            bracket_list.append(new_bracket)
            bracket_list.sort(key=lambda x: x.upper)
        self._rate.set(0.0)
        self._upper.set(0.0)
        self.populate()

    def delete_bracket(self, bracket) -> None:
        bracket_list = self._fin_obj.get_brackets()
        if bracket in bracket_list:
            bracket_list.remove(bracket)
        self.populate()

    def populate(self) -> None:
        for c in self._frame.winfo_children():
            c.destroy()

        frame = self._frame
        bracket_list = self._fin_obj.get_brackets()

        tk.Label(frame, text=self._fin_obj.name().title()).grid(column=0, row=0, columnspan=6)
        tk.Label(frame, text="").grid(column=0, row=1)

        tk.Label(frame, text='Tax Rate').grid(column=0, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._rate).grid(column=0, row=3, columnspan=2)
        tk.Label(frame, text='Upper Range').grid(column=2, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._upper).grid(column=2, row=3, columnspan=2)
        add_button = tk.Button(frame, text='Add', width=6)
        add_button.grid(column=6, row=3, sticky=W+E)
        add_button.bind("<Button-1>", lambda e: self.new_bracket())

        last = 6
        for i in range(len(bracket_list)):
            if i == 0:
                lower = 0
            else:
                lower = bracket_list[i-1].upper + 1
            upper = f'${lower:,} to ${bracket_list[i].upper:,}'

            tk.Label(frame, text=f'{bracket_list[i].rate}%').grid(column=0, row=6 + i, columnspan=2, sticky=W + E)
            tk.Label(frame, text=upper).grid(column=2, row=6 + i, columnspan=2, sticky=W + E)
            del_button = tk.Button(frame, text="Delete", width=6)
            del_button.bind("<Button-1>", lambda e, p=bracket_list[i]: self.delete_extra_payment(p))
            del_button.grid(column=6, row=6 + i, columnspan=2, sticky=W + E)
            last += 1


class ExtraPaymentWindow(Window):
    """
    Class representing a window interface for adding new and removing existing ExtraPayments from a Loan.
    """
    def __init__(self, root, parent, loan):
        title = "Add Extra Payments"
        self._loan = loan
        self._parent = parent

        self._start = tk.IntVar()
        self._duration = tk.IntVar()
        self._amount = tk.IntVar()
        super().__init__(root, parent, loan, title)

    def new_extra_payment(self):
        extra_payments = self._fin_obj.get_extra_payments()
        try:
            if self._start.get() == 0 or self._duration.get() == 0 or self._amount.get() == 0:
                ErrorBox(self._root, "invalid inputs")
            else:
                new_extra_payment = ExtraPayment(self._start.get(), self._duration.get(), self._amount.get())
                extra_payments.append(new_extra_payment)
            self.populate()
        except tkinter.TclError:
            ErrorBox(self._root, "invalid inputs")
        self._start.set(0)
        self._duration.set(0)
        self._amount.set(0)

    def delete_extra_payment(self, extra_payment):
        extra_payments = self._fin_obj.get_extra_payments()
        if extra_payment in extra_payments:
            extra_payments.remove(extra_payment)
        self.populate()

    def populate(self):
        for c in self._frame.winfo_children():
            c.destroy()

        frame = self._frame
        extra_payments = self._loan.get_extra_payments()

        tk.Label(frame, text=self._loan.name().title()).grid(column=0, row=0, columnspan=6)
        tk.Label(frame, text="").grid(column=0, row=1)

        tk.Label(frame, text="Start Month").grid(column=0, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._start).grid(column=0, row=3, columnspan=2)
        tk.Label(frame, text="Duration").grid(column=2, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._duration).grid(column=2, row=3, columnspan=2)
        tk.Label(frame, text="Amount").grid(column=4, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._amount).grid(column=4, row=3, columnspan=2)
        add_button = tk.Button(frame, text='Add', width=6)
        add_button.grid(column=6, row=3, sticky=W+E)
        add_button.bind("<Button-1>", lambda e: self.new_extra_payment())

        last = 6
        for i in range(len(extra_payments)):
            tk.Label(frame, text=extra_payments[i].start).grid(column=0, row=6+i, columnspan=2, sticky=W+E)
            tk.Label(frame, text=extra_payments[i].length).grid(column=2, row=6+i, columnspan=2, sticky=W+E)
            tk.Label(frame, text=extra_payments[i].amount).grid(column=4, row=6+i, columnspan=2, sticky=W+E)
            del_button = tk.Button(frame, text="Delete", width=6)
            del_button.bind("<Button-1>", lambda e, p=extra_payments[i]: self.delete_extra_payment(p))
            del_button.grid(column=6, row=6+i, columnspan=2, sticky=W+E)
            last += 1


class AssumptionsWindow(Window):
    def __init__(self, root, parent, fin_obj):
        self._form_vars = {}
        super().__init__(root, parent, fin_obj)
        self._window.title(f"Define Assumptions for {self._fin_obj.data('name')}")

    def save(self, key):
        assumptions = self._fin_obj.get_assumptions()
        assumptions.update({key: self._form_vars.get(key).get()})

    def save_all(self):
        assumptions = self._fin_obj.get_assumptions()
        for key in assumptions.keys():
            self.save(key)

    def populate(self):
        for c in self._frame.winfo_children():
            c.destroy()

        index = 0
        frame = self._frame
        assumptions = self._fin_obj.get_assumptions()
        for key, value in assumptions.items():
            if isinstance(value, float) or isinstance(value, int):
                a_var = tk.DoubleVar()
            else:
                a_var = tk.StringVar()
            a_var.set(value)
            self._form_vars.update({key: a_var})
            tk.Label(frame, text=str(key).title(), anchor='e').grid(column=0, row=index, columnspan=2, sticky=W+E)
            entry = tk.Entry(frame, textvariable=a_var)
            entry.grid(column=2, row=index, columnspan=2, sticky=W+E)
            entry.bind("<FocusOut>", lambda e, k=key: self.save(k))
            index += 1

    def on_exit(self):
        self.save_all()
        super().on_exit()


class Selector(Window):
    def __init__(self, root, parent, selection_list):
        self._selection_list = selection_list
        super().__init__(root, parent, None)

    def on_exit(self):
        self._window.destroy()


class ExpenseSelector(Selector):
    def __init__(self, root, parent, expenses):
        self._all_expenses: list = parent.get_fin_vars('expenses')
        self._expenses: list = expenses.get_expenses()
        super().__init__(root, parent, expenses)

    def add_remove_expense(self, expense, check_var):
        val = check_var.get()
        if val == 1:
            if expense not in self._expenses:
                self._taxes.append(expense)
        else:
            if expense in self._expenses:
                self._taxes.remove(expense)

    def populate(self):
        for c in self._frame.winfo_children():
            c.destroy()

        index = 0
        frame = self._frame
        for expense in self._all_expenses:
            label = f"{expense.name()} | {expense.desc()}"
            tk.Label(frame, text=label).grid(row=index, column=0, sticky=W+E)
            check_var = tk.IntVar()
            if expense in self._expenses:
                check_var.set(1)
            else:
                check_var.set(0)
            check = tk.Checkbutton(frame, variable=check_var,
                                   command=lambda v=check_var, e=expense: self.add_remove_expense(e, v))
            check.grid(row=index, column=1)
            index += 1


class TaxSelector(Selector):
    def __init__(self, root, parent, taxes: list):
        self._all_taxes: list = parent.get_fin_vars('taxes')
        self._taxes: list = taxes
        super().__init__(root, parent, taxes)

    def add_remove_tax(self, tax, check_var):
        val = check_var.get()
        if val == 1:
            if tax not in self._taxes:
                self._taxes.append(tax)
        else:
            if tax in self._taxes:
                self._taxes.remove(tax)

    def populate(self):
        for c in self._frame.winfo_children():
            c.destroy()

        index = 0
        frame = self._frame
        for tax in self._all_taxes:
            label = f"{tax.name()} | {tax.desc()}"
            tk.Label(frame, text=label).grid(row=index, column=0, sticky=W+E)
            check_var = tk.IntVar()
            if tax in self._taxes:
                check_var.set(1)
            else:
                check_var.set(0)
            check = tk.Checkbutton(frame, variable=check_var,
                                   command=lambda v=check_var, t=tax: self.add_remove_tax(t, v))
            check.grid(row=index, column=1)
            index += 1


class ErrorBox:
    def __init__(self, root, message: str):
        window = tk.Toplevel(root)
        window.title('error')
        window.grid_propagate(True)
        window.geometry('200x100')
        tk.Label(window, text="").grid(column=0, row=0)
        tk.Label(window, text=message).grid(column=1, row=1)
        tk.Label(window, text="").grid(column=2, row=2)


class Style:
    colors = {
        "l_sel": "lightblue2",
        "l_hover": "lightblue1",
        'l_active_hover': 'lightblue3',
        "b_reset": "#fff",
        "b_sel": 'medium turquoise',
        'b_hover': 'turquoise',
        'b_active_hover': 'dark turquoise',
        'fin_type': 'red',
        'save_button': 'green',
        'save_button_hover': 'darkgreen',
        'detail title': 'darkblue',
        'detail subtitle': 'blue'
    }

    @classmethod
    def color(cls, color_string: str):
        color = cls.colors.get(color_string)
        if color is None:
            color = cls.colors.get('b_reset')
        return color
