# Author: Hobs Towler
# Date: 12/7/2021
# Description:

class DetailForm:
    def __init__(self):
        self._forms = []
        self.create_forms()

    def create_forms(self):
        # Scenarios Form
        self._forms.append(["Scenario Editor",
                            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
                            [["Label", "Description", "", 1], ["Entry", "", "", 2]],
                            [["", "", "", 3]]
                            ])
        # Jobs Form
        self._forms.append(["Job Editor",
                            [["Label", "Title", "", 1], ["Entry", "", "", 2]],
                            [["Label", "Company", "", 1], ["Entry", "", "", 2]],
                            [["", "", "", 3]],
                            [["Label", "Salary", "", 1], ["Entry", "", "", 2]]
                            ])
        # Loans Form
        self._forms.append(["Loan Editor",
                            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
                            [["", "", "", 3]],
                            [["Label", "Loan Amount", "", 1], ["Entry", "", "", 2]],
                            [["Label", "Down Payment", "", 1], ["Entry", "", "", 1],
                             ["CheckButton", "Percentage", "", 1]],
                            [["Label", "Rate", "", 1], ["Entry", "", "", 2]],
                            [["", "", "", 3]]
                            ])
        # Expenses Form
        self._forms.append(["Expense Editor",
                            [["Label", "Name", "", 1], ["Entry", "", "", 2]],
                            [["Label", "Description", "", 1], ["Entry", "", "", 2]],
                            [["", "", "", 3]]
                            ])

    def get_form(self, context) -> list:
        return self._forms[context]
