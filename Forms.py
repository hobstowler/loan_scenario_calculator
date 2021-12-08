# Author: Hobs Towler
# Date: 12/7/2021
# Description:

from income import *
from loans import *

class DetailForm:
    def __init__(self, thing=None) -> None:
        self._forms = []
        self.create_forms()
        self._name = ""
        self._type = ""
        self._amount = ""
        self._down = ""
        self._rate = ""

        self.parse(thing)

    #TODO forms by type
    def create_forms(self) -> None:
        # Scenarios Form
        self._forms.append([
            "Scenario Editor",
            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "", 2]],
            [["Space", "", "", 3]]
            ])
        # Jobs Form
        self._forms.append([
            "Job Editor",
            [["Label", "Title", "", 1], ["Entry", "", "", 2]],
            [["Label", "Company", "", 1], ["Entry", "", "", 2]],
            [["Space", "", "", 3]],
            [["Label", "Salary", "", 1], ["Entry", "", "", 2]]
            ])
        # Loans Form
        self._forms.append([
            "Loan Editor",
            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
            [["Label", "Loan Type", "", 1], ["Combo", "", "", 2, ["Mortgage", "Auto", "Personal"]]],
            [["Space", "", "", 3]],
            [["Label", "Loan Amount", "", 1], ["Entry", "", "", 2]],
            [["Label", "Down Payment", "", 1], ["Entry", "", "", 1], ["CheckButton", "Percentage", "", 1]],
            [["Label", "Rate", "", 1], ["Entry", "", "", 2]],
            [["Space", "", "", 3]]
            ])
        # Expenses Form
        self._forms.append([
            "Expense Editor",
            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "", 2]],
            [["Space", "", "", 3]]
            ])
        # Tax Brackets Form
        self._forms.append([
            "Tax Bracket Editor",
            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
            [["Label", "Description", "", 1], ["Entry", "", "", 2]],
        ])

    def get_form(self, context) -> list:
        return self._forms[context]

    def save(self):
        pass

    def parse(self, thing=None):
        if thing == None:
            return
        if isinstance(thing, Mortgage):
            return
        if isinstance(thing, Auto):
            return
        if isinstance(thing, Loan):
            return
        if isinstance(thing, Job):
            return
        if isinstance(thing, Expenses):
            return
        if isinstance(thing, TaxBracket):
            return

