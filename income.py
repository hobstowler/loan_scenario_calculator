# Author: Hobs Towler
# Date: 12/1/2021
# Description:


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
        self._name = name
        self._desc = desc
        self._type = "FibObj"
        self._data = {}

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
        return self._name

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
        return self._desc

    def get_data(self) -> dict:
        return self._data

    def type(self) -> str:
        return self._type


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
        self._type = "Expense"
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


class Job(FinanceObj):
    def __init__(self, name, desc="") -> None:
        super(Job, self).__init__(name, desc)
        self._type = "Job"
        self._title = "Blank"
        self._company = "Some Company"
        self._income = 0
        #self._pre_tax = Expenses()
        #self._post_tax = Expenses()
        self._401k_rate = 0
        self._roth_rate = 0

    def get_income(self):
        return self._income

    def get_pretax(self):
        return self._pre_tax

    def get_posttax(self):
        return self._post_tax

    def set_company(self, new_company):
        if new_company.isalnum():
            self._company = new_company
    
    def company(self):
        return self._company

    def set_title(self, new_title):
        if new_title.isalnum():
            self._title = new_title

    def set_401k(self, rate):
        self._401k_rate = rate

    def set_roth(self, rate):
        self._roth_rate = rate


class TaxBracket(FinanceObj):
    """
    Represents a tax bracket for income. Includes methods for getting the taxed amount and effective tax rate.
    """
    def __init__(self, name: str, desc: str="") -> None:
        super(TaxBracket, self).__init__(name, desc)
        self._type = "Tax Bracket"
        self._brackets = []
        self._label = ""
        self._type = type
        self._state = ""
        self._status = ""

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

    def change_type(self, new_type):
        """
        Changes the tax type if it is one of the valid types: Federal, State, or Local.
        :param new_type: The new tax type.
        :return: Nothing.
        """
        if new_type.isalpha() and new_type.upper() in self._valid_types:
            self._type = new_type.capitalize()

    def tax_type(self):
        """
        Returns the tax type: Federal, State, or Local.
        :return: The tax type
        """
        return self._type

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

    def add_range(self, upper_range, rate):
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
        if not isinstance(upper_range,(int,float)) or not isinstance(rate, (int,float)):
            return
        index = self._get_range(upper_range)
        if index == None:
            self._brackets.append([upper_range, rate/100])
            self._brackets.sort()
        else:
            self._brackets[index] = [upper_range, rate/100]

    def rem_range(self, upper_range):
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

    def calculate(self, income):
        """
        Calculates the total taxed amount and the effective tax rate for a given income.
        :param income: The yearly income to be taxed
        :return: A list of the taxed amount and the effective rate.
        """
        if len(self._brackets) == 0:
            return None

        taxed_amount = 0
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


#TODO add support for assets like 401k, IRA, houses, bank accounts
class Assets(FinanceObj):
    def __init__(self):
        pass


expense = Expenses("testExpense")
expense.add("car", 1500)
expense.add("food", 150)
expense.add("fOod", 250.111)
expense.add("something", "thing")
#print(expense.total())
expense.reset()
#print(expense.total())

bracket = TaxBracket("test bracket")
bracket.add_range(50000,6)
bracket.add_range(20000,5)
bracket.add_range(1000,4)
bracket.add_range(1000,4.2)
bracket.add_range(20000,5.1)
bracket.add_range(None,12)
#print(bracket._brackets)
#print(bracket.calculate(10000))
#print(bracket.calculate(15678))
#print(bracket._get_range(2000))
#print("name",bracket.name())
bracket.set_desc("a tax bracket for testing")
#print("desc",bracket.desc())
bracket.set_desc(55)
#print("desc",bracket.desc())