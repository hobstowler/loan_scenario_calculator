class Scenario:
    def __init__(self) -> None:
        pass


class Income:
    def __init__(self) -> None:
        self._amount = 50000
        self._pay_periods = 26


class Expenses:
    def __init__(self):
        self._expenses = {}

    def add(self, name, amount):
        if not name.isalpha() or not isinstance(amount, (int, float)):
            #print("bad input")
            return
        amount = round(amount, 2)
        name = name.upper()
        self._expenses.update({name: amount})

    def rem(self, name):
        if self._expenses.get(name):
            del self._expenses[name]

    def reset(self):
        self._expenses.clear()

    def total(self):
        total = 0
        for e in self._expenses:
            total += self._expenses.get(e)
        return round(total, 2)

    def change(self, old_name, new_name):
        self.add(new_name, self._expenses.get(old_name))
        self.rem(old_name)


class Job:
    def __init__(self):
        self._title = "Blank"
        self._company = "Some Company"
        self._income = Income()
        self._pre_tax = Expenses()
        self._post_tax = Expenses()

class TaxBracket:
    def __init__(self) -> None:
        pass

class Loan:
    def __init__(self, total=0, rate=1, length=60):
        self._total = total
        self._rate = float(rate/100)
        self._length = length
        self._principal = total * .8

        self._loan_start = "01/01/1999"

        self._months = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

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
    def __init__(self, total=100000, rate=1, length=60) -> None:
        super().__init__(total=total, rate=rate, length=length)

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


mort = Mortgage(280000, 3.25, 360)
print(mort.PMI())
print(mort.mortgage_monthly())
print(mort.mortgage_total())
print(mort.amortization_schedule())

expense = Expenses()
expense.add("car", 1500)
expense.add("food", 150)
expense.add("fOod", 250.111)
expense.add("something", "thing")
print(expense.total())
expense.reset()
print(expense.total())