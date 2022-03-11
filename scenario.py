# Author: Hobs Towler
# Date: 12/1/2021
# Description:

from loans import *
from income import *
from matplotlib import pyplot


class AlreadyExists(Exception):
    pass


class Scenario(FinanceObj):
    def __init__(self, name, desc="") -> None:
        super(Scenario, self).__init__(name, desc)
        self._jobs = []
        self._incomes = []
        self._expenses = []
        self._loans = []

        self._monthly_income = 0
        self._monthly_expense = 0

    @staticmethod
    def __str__():
        return f"Scenario"

    def add_job(self, job: Job) -> bool:
        """
        Adds a job to the list of jobs in the scenario. Raises exception if job is already in the list.
        Recalculates the scenario if method is successful.
        :param job: The job to be added
        :return: True if successfully added to list.
        """
        if job in self._jobs:
            raise AlreadyExists("There is already a job with that name in the list.")
        else:
            self._jobs.append(job)
            self._calculate()
            return True
        return False

    def get_jobs(self) -> dict:
        """
        Returns the list of jobs that have been added to the scenario.
        :return: The list of jobs.
        """
        return self._jobs

    def rem_job(self, job: Job) -> bool:
        """
        Removes a job from the list of jobs. Returns False if job is not in the list.
        Recalculates the scenario if method is successful.
        :param job: The job to be removed
        :return: True if successfully removed.
        """
        if job in self._jobs:
            self._jobs.remove(job)
            self._calculate()
            return True
        return False

    def add_income(self, income: Income) -> bool:
        """
        Adds income to the list of incomes in the scenario. Raises exception if income is already in the list.
        Recalculates the scenario if method is successful.
        :param income: The income to be added.
        :return: True if successfully added to list.
        """
        if income in self._incomes:
            raise AlreadyExists("There is already a job with that name in the list.")
        else:
            self._incomes.append(income)
            self._calculate()
            return True
        return False

    def get_incomes(self) -> list:
        """
        Returns the list of incomes in the scenario.
        :return: The list of incomes.
        """
        return self._incomes

    def rem_income(self, income: Income) -> bool:
        """
        Removes an income from the list of incomes. Returns False if job is not in the list.
        Recalculates the scenario if method is successful.
        :param income: The income to be removed.
        :return: True if successfully removed.
        """
        if income in self._incomes:
            self._incomes.remove(income)
            self._calculate()
            return True
        return False

    def add_expense(self, expense: Expenses) -> bool:
        """
        Adds an expense to the list of expenses in the scenario. Raises exception if income is already in the list.
        Recalculates the scenario if method is successful.
        :param expense: The expense to be added to the scenario.
        :return: True if successfully added.
        """
        if expense in self._expenses:
            raise AlreadyExists("There is already a job with that name in the list.")
        else:
            self._expenses.append(expense)
            self._calculate()
            return True
        return False

    def get_expenses(self) -> list:
        """
        Returns the list of expenses in the scenario.
        :return: The list of expenses.
        """
        return self._expenses

    def rem_expense(self, expense: Expenses) -> bool:
        """
        Remove an expense from the list of expenses. Returns False if expense is not in the list.
        Recalculates the scenario if method is successful.
        :param expense: The expense to be removed.
        :return: True if successfully removed.
        """
        if expense in self._expenses:
            self._expenses.remove(expense)
            self._calculate()
            return True
        return False

    def add_loan(self, loan: Loan) -> bool:
        """
        Adds a loan to the list of loans in the scenario. Raises an exception if the loan is already in the list.
        Recalculates the scenario if method is successful.
        :param loan: The loan to be added to the scenario.
        :return: True if successfully added.
        """
        if loan in self._loans:
            raise AlreadyExists("There is already a job with that name in the list.")
        else:
            self._loans.add(loan)
            self._calculate()
            return True
        return False

    def get_loans(self) -> list:
        """
        Returns the list of loans in the scenario.
        :return: The list of loans.
        """
        return self._loans

    def rem_loan(self):
        """
        Removes a loan from the scenario. Returns False if the loan is not in the list.
        Recalculates the scenario if method is successful.
        :return: True if successfully removed.
        """
        for loan in self._loans:
            self._loans.remove(loan)
            self._calculate()
            return True
        return False

    def _calculate(self):
        """
        Calculates weekly, monthly, and annual amounts and schedules.
        :return: Nothing
        """
        self._calculate_weekly()
        self._calculate_monthly()
        self._calculate_annual()

    def _calculate_monthly(self):
        """
        Calculates the monthly amounts and schedules.
        :return: Nothing.
        """
        for income in self._incomes:
            self._monthly_income += income.get_monthly()
        for job in self._jobs:
            self._monthly_income += job.get_monthly()

        for expense in self._expenses:
            self._monthly_expense += expense.get_monthly()
        for loan in self._loans:
            self._monthly_expense += loan.get_monthly()

    def get_monthly_cash_flow(self) -> float:
        return self._monthly_income - self._monthly_expense

    def _calculate_weekly(self):
        pass

    def get_weekly_cash_flow(self):
        pass

    def calculate_annual(self):
        pass

    def get_annual_cash_flow(self):
        pass

