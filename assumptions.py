class Scenario:
    def __init__(self) -> None:
        self._jobs = set({})
        self._incomes = set({})
        self._expenses = set({})
        self._loans = set({})


class Income:
    def __init__(self) -> None:
        self._amount = 50000
        self._pay_periods = 26


class Expenses:
    """
    An object that can keep track of monthly expenses and provide a total amount.
    """
    def __init__(self):
        """
        Initializes the Expenses object with a dictionary of expenses.
        """
        self._expenses = {}

    def add(self, label, amount):
        """
        Adds an expense with a label and monthly amount.
        :param label: The label for the expense.
        :param amount: The monthly amount
        :return: Nothing.
        """
        if not label.isalpha() or not isinstance(amount, (int, float)):
            #print("bad input")
            return
        self._expenses.update({label.capitalize(): round(amount, 2)})

    def rem(self, label):
        """
        Removes an expense.
        :param label: The label of the expense to be removed
        :return: True if removal was successful.
        """
        if self._expenses.get(label):
            del self._expenses[label]
            return True
        return False

    def reset(self):
        """
        Clears all of the expenses.
        :return: Nothing.
        """
        self._expenses.clear()

    def get(self):
        """
        Returns the dictionary of expenses.
        :return: The expenses.
        """
        return self._expenses

    def total(self):
        """
        Returns the total of all expenses.
        :return: the total monthly expenditure
        """
        total = 0
        for e in self._expenses:
            total += self._expenses.get(e)
        return round(total, 2)

    def change_label(self, old_label, new_label):
        """
        Changes the label for an expense.
        :param old_label: the old label.
        :param new_label: the new label.
        :return: True if succesful
        """
        if old_label in self._expenses:
            self.add(new_label, self._expenses.get(old_label))
            self.rem(old_label)
            return True
        return False


class Job:
    def __init__(self):
        self._title = "Blank"
        self._company = "Some Company"
        self._income = Income()
        self._pre_tax = Expenses()
        self._post_tax = Expenses()

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


class TaxBracket:
    """
    Represents a tax bracket for income. Includes methods for getting the taxed amount and effective tax rate.
    """
    def __init__(self, label, type="Federal", state="N/A", status="Single") -> None:
        self._brackets = []
        self._label = label
        self._type = type
        self._state = state
        self._status = status

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
        index = self._get_range(upper_range)
        if index != None:
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


class Loan:
    def __init__(self, label, total=0, rate=1, length=60):
        self._total = total
        self.label = label
        self._rate = float(rate/100)
        self._length = length
        self._principal = total * .8

        self._loan_start = "01/01/1999"

    def set_amount(self, new_amount):
        self._total = new_amount

    def set_rate(self, new_rate):
        self._rate = new_rate

    def set_length(self, new_length):
        self._length = new_length

    def get_amount(self):
        return self._total

    def get_rate(self):
        return self._rate

    def get_length(self):
        return self._length

    def calculate_schedule(self, amount, rate, length):
        pass

    def amortization_schedule(self):
        pass


class Mortgage(Loan):
    def __init__(self, label, total=100000, rate=1, length=60) -> None:
        super().__init__(label=label, total=total, rate=rate, length=length)

        self._pmi_required = True
        self._PMI_rate = .005

        self._property_tax = 1890
        self._property_tax_rate = 1
        self._property_tax_override = False

        self._insurance = 75
        self._insurance_co = "None"

        self._m_payment = self.mortgage_monthly()
        self._t_payment = self.mortgage_total()

    def mortgage_monthly(self):
        monthly_rate = self._rate/12
        numerator = self._principal * (monthly_rate * ((1 + monthly_rate) ** self._length))
        denominator = ((1 + monthly_rate) ** self._length) - 1
        return round(numerator/denominator,2)

    def mortgage_total(self):
        #print((self._property_tax / 12))
        #print(self.PMI())
        #print(self._insurance)
        return round(self.mortgage_monthly() + (self._property_tax / 12) + self.PMI() + self._insurance, 2)

    def PMI(self, principal=None):
        """
        Returns the PMI amount if PMI is required and the remaining principal is greater than 80% of the total.
        :return: The PMI amount
        """
        if principal == None:
            principal = self._principal
        percent_down = round(1-(principal / self._total),2)
        #print(percent_down)
        if percent_down < 0.2 and self._pmi_required:
            return round((principal * self._PMI_rate)/12, 2)
        else:
            return 0

    def set_PMI_rate(self, new_pmi_rate):
        self._PMI_rate = new_pmi_rate

    def no_PMI(self):
        self._pmi_required = False

    def req_PMI(self):
        self._pmi_required = True

    #TO DO: factor in a prorated amount and use the start of the loan
    def amortization_schedule(self):
        principal = self._principal
        schedule = {0: principal}
        for i in range(1, self._length+1):
            interest = self._m_interest(principal)
            principal = round(principal + interest - self._m_payment, 2)
            schedule.update({i: principal})
        return schedule


    def _m_interest(self, amount):
        """
        Calculates the monthly interest for a given amount and month.
        To be called when calculating amortization schedule.
        :param amount: The principal remaining at the start of the period.
        :param month: The month for which interest is to be calculated.
        :return: The amount of interest accrued that month
        """
        return round(amount * (self._rate / 12) , 2)

    def set_property_tax(self, tax_amount):
        """
        Sets a user-defined property tax and sets the override flag.
        :param tax_amount: The yearly amount of property tax.
        :return: The property tax.
        """
        self._property_tax_override = True
        self._property_tax = tax_amount
        return self.calculate_property_tax()


    def set_property_tax_rate(self, new_rate):
        """
        Changes the tax rate and recalculates the property tax.
        :param new_rate: The new tax rate.
        :return: The calculated tax.
        """
        self._property_tax_rate = new_rate
        return self.calculate_property_tax()

    def clear_property_tax(self):
        """
        clears a user-defined property tax and sets the override flag back.
        :return: The calculated tax.
        """
        self._property_tax_override = False
        return self.calculate_property_tax()

    def calculate_property_tax(self):
        """
        Calculates the yearly property tax for a defined tax rate.
        :return: The calculated tax.
        """
        if not self._property_tax_override:
            self._property_tax = self._total * (self._property_tax_rate / 100)
        return self._property_tax


class VariableRateMortgage(Mortgage):
    def __init__(self, total=0, rate=1, length=60) -> None:
        super().__init__(total=total, rate=rate, length=length)


class Auto(Loan):
    def __init__(self, total=0, rate=1, length=60):
        super().__init__(total=total, rate=rate, length=length)


mort = Mortgage("test mortgage", 280000, 3.25, 360)
#print(mort.PMI())
#print(mort.mortgage_monthly())
#print(mort.mortgage_total())
#print(mort.amortization_schedule())

expense = Expenses()
expense.add("car", 1500)
expense.add("food", 150)
expense.add("fOod", 250.111)
expense.add("something", "thing")
print(expense.total())
expense.reset()
print(expense.total())

bracket = TaxBracket("test bracket")
bracket.add_range(50000,6)
bracket.add_range(20000,5)
bracket.add_range(1000,4)
bracket.add_range(1000,4.2)
bracket.add_range(20000,5.1)
bracket.add_range(None,12)
print(bracket._brackets)
print(bracket.calculate(10000))
print(bracket.calculate(15678))
print(bracket._get_range(2000))