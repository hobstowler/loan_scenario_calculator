# Author: Hobs Towler
# Date: 12/1/2021
# Description:

from loans import *
from income import *

class Scenario(FinanceObj):
    def __init__(self, name, desc="") -> None:
        super(Scenario, self).__init__(name, desc)
        self._jobs = set({})
        self._incomes = set({})
        self._expenses = set({})
        self._loans = set({})
        self._tax_bracket = set({})

    def add_job(self, job: Job) -> bool:
        if job not in self._jobs:
            self._jobs.add(job)
            return True
        return False

    def add_income(self, income: Income) -> bool:
        if income not in self._incomes:
            self._incomes.add(income)
            return True
        return False

    def add_expense(self, expense: Expenses) -> bool:
        if expense not in self._expenses:
            self._expenses.add(expense)
            return True
        return False

    def add_loan(self, loan: Loan) -> bool:
        if loan not in self._loans:
            self._loans.add(loan)
            return True
        return False

    def add_tax_bracket(self, tax: TaxBracket):
        if tax not in self._tax_bracket:
            self._tax_bracket.add(tax)
            return True
        return False

    def rem_job(self, job: Job) -> bool:
        if job in self._jobs:
            self._jobs.remove(job)
            return True
        return False

