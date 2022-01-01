# Author: Hobs Towler
# Date: 12/7/2021
# Description:

from income import *
from loans import *
from tkinter import *
from dataload import *


class DetailForm:
    """
    Provides a template for editing Finance Objects in the app window. Also handles data transfer from app to Object
    and from Object to app.
    """
    def __init__(self, fin_obj: FinanceObj = None) -> None:
        self._forms = {}
        self._fin_obj = fin_obj
        self.create_forms()

        #self.parse(thing)

    #TODO forms by type
    def create_forms(self) -> None:
        """
        TYPE | LABEL | ID | COLUMN SPAN | MISC
        :return:
        """
        # Scenarios Form
        self._forms.update({"scenarios": [
            "Scenario Editor",
            [["Label", "Name", "", 1], ["Entry", "", "name", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "desc", 2]],
            [["Space", "", "", 3]],
            [["Button", "Jobs", "jobs", 1]],
            [["Space", "", "", 3]],
            [["Button", "Incomes", "incomes", 1]],
            [["Space", "", "", 3]],
            [["Button", "Expenses", "expenses", 1]],
            [["Space", "", "", 3]],
            [["Button", "Mortgages", "mortgages", 1]],
            [["Space", "", "", 3]],
            [["Button", "Loans", "loans", 1]],
            [["Space", "", "", 3]],
            [["Button", "Tax Brackets", "tax_brackets", 1]]

        ]})
        # Jobs Form
        self._forms.update({"jobs": [
            "Job Editor",
            [["Label", "Name", "", 1], ["Entry", "", "name", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "desc", 2]],
            [["Space", "", "", 3]],
            [["Label", "Salary", "", 1], ["Entry", "", "salary", 2]],
            [["Label", "Pay Frequency", "", 1], ["Combo", "", "salary_freq", 2,
                                                 ["Annual", "Monthly", "Bi-Weekly", "Weekly", "Hourly"], 0]],
            [["Space", "", "", 3]],
            [["Label", "401k Contribution", "", 1], ["Entry", "", "401k", 2]],
            [["Label", "Roth 401k Contribution", "", 1], ["Entry", "", "roth_401k", 2]],
            [["Space", "", "", 3]],
            [["Label", "Deductions", "", 1]],
            [["Button", "Pre-Tax Deductions", "pre_tax_expenses", 1],
             ["Button", "Post-Tax Deductions", "post_tax_expenses", 1]],
            [["Space", "", "", 3]],
            [["Button", "Tax Brackets", "tax_brackets", 1]]
        ]})
        # Loans Form
        self._forms.update({"loans": [
            "Loan Editor",
            [["Label", "Name", "", 1], ["Entry", "", "name", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "desc", 2]],
            [["Label", "Loan Type", "", 1], ["Combo", "", "loan type", 2, ["Mortgage", "Auto", "Personal"], -1]],
            [["Space", "", "", 3]],
            [["Label", "Total Amount", "", 1], ["Entry", "", "total", 2]],
            [["Label", "Down Payment", "", 1], ["Entry", "", "down payment", 1], ["CheckButton", "Percentage", "", 1]],
            [["Label", "Principal", "", 1], ["Entry", "", "principal", 2]],
            [["Label", "Rate", "", 1], ["Entry", "", "rate", 2]],
            [["Label", "Term", "", 1], ["Entry", "", "length", 1], ["CheckButton", "Years", "l_years", 1]],
            [["Space", "", "", 3]]
        ]})
        # Mortgage Form
        self._forms.update({"mortgages": [

        ]})
        # Auto Loan Form
        self._forms.update({"auto loans": [

        ]})
        # Expenses Form
        self._forms.update({"expenses": [
            "Expense Editor",
            [["Label", "Name", "", 1], ["Entry", "", "name", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "desc", 2]],
            [["Space", "", "", 3]]
        ]})
        # Tax Brackets Form
        self._forms.update({"taxes": [
            "Tax Bracket Editor",
            [["Label", "Name", "", 1], ["Entry", "", "name", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "desc", 2]],
            [["Space", "", "", 3]]
        ]})

    def get_form(self, context) -> list:
        return self._forms[context]

    def get_fin_obj(self) -> FinanceObj:
        return self._fin_obj

    def update_fin_obj(self, context: str, data: dict):
        for key in data.keys():
            val = data.get(key)
            if key == "name" and self._fin_obj.name() != val:
                print(data.get(key))
                self._fin_obj.set_name(val)
            elif key == "desc" and self._fin_obj.desc() != val:
                self._fin_obj.set_desc(val)
            else:
                self._fin_obj.get_data().update({key: val})

