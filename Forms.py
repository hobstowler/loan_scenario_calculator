# Author: Hobs Towler
# Date: 12/7/2021
# Description:

from income import *
from loans import *
from tkinter import *

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
        # Scenarios Form
        self._forms.update({"scenario": [
            "Scenario Editor",
            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "", 2]],
            [["Space", "", "", 3]]
        ]})
        # Jobs Form
        self._forms.update({"job": [
            "Job Editor",
            [["Label", "Title", "", 1], ["Entry", "", "", 2]],
            [["Label", "Company", "", 1], ["Entry", "", "", 2]],
            [["Space", "", "", 3]],
            [["Label", "Salary", "", 1], ["Entry", "", "", 2]]
        ]})
        # Loans Form
        self._forms.update({"loan": [
            "Loan Editor",
            [["Label", "Name", "", 1], ["Entry", "", "name", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "desc", 2]],
            [["Label", "Loan Type", "", 1], ["Combo", "", "loan type", 2, ["Mortgage", "Auto", "Personal"]]],
            [["Space", "", "", 3]],
            [["Label", "Total Amount", "", 1], ["Entry", "", "total", 2]],
            [["Label", "Down Payment", "", 1], ["Entry", "", "down payment", 1], ["CheckButton", "Percentage", "", 1]],
            [["Label", "Principal", "", 1], ["Entry", "", "principal", 2]],
            [["Label", "Rate", "", 1], ["Entry", "", "rate", 2]],
            [["Label", "Term", "", 1], ["Entry", "", "length", 1], ["CheckButton", "Years", "l_years", 1]],
            [["Space", "", "", 3]]
        ]})
        # Mortgage Form
        self._forms.update({"mortgage": [

        ]})
        # Auto Loan Form
        self._forms.update({"auto": [

        ]})
        # Expenses Form
        self._forms.update({"expense": [
            "Expense Editor",
            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "", 2]],
            [["Space", "", "", 3]]
        ]})
        # Tax Brackets Form
        self._forms.update({"tax": [
            "Tax Bracket Editor",
            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "", 2]],
        ]})

    def get_form(self, context) -> list:
        return self._forms[context]

    def save(self):
        pass

    def parse_data(self, data: dict = None):
        if data is None:
            return
        fin_data = self._fin_obj.get_data()
        for key in data:
            if key == "name":
                self._fin_obj.set_name(data.get(key))
            elif key == "desc":
                self._fin_obj.set_desc(data.get(key))
            else:
                fin_data.update({key: data.get(key)})

