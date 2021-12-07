# Author: Hobs Towler
# Date: 12/7/2021
# Description:

class DetailForm:
    def __init__(self):
        self._forms = []

        self._forms.append([]) # Scenarios Form
        self._forms.append([]) # Jobs Form
        self._forms.append([]) # Loans Form
        self._forms.append([]) # Expenses Form

    def get_form(self, context) -> list:
        return self._forms[context]
