# Author: Hobs Towler
# Date: 12/1/2021
# Description:

class Loan:
    def __init__(self, label, total=10000, rate=1, length=60):
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

        self._hoa = 0

        self._insurance = 75
        self._insurance_co = "None"

        self._m_payment = self.mortgage_monthly()
        self._t_payment = self.mortgage_total()

    def mortgage_monthly(self):
        """
        Calculates the monthly mortgage payment based on rate and length of the loan. This is the amount without taxes,
        insurance, PMI, or HOA
        :return: The monthly payment.
        """
        monthly_rate = self._rate/12
        numerator = self._principal * (monthly_rate * ((1 + monthly_rate) ** self._length))
        denominator = ((1 + monthly_rate) ** self._length) - 1
        return round(numerator/denominator,2)

    def mortgage_total(self):
        """
        Sums the total of the mortgage, monthly property tax, PMI, insurance, and HOA.
        :return: The monthly total.
        """
        #print((self._property_tax / 12))
        #print(self.PMI())
        #print(self._insurance)
        return round(self.mortgage_monthly() + (self._property_tax / 12) + self.PMI() + self._insurance + self._hoa, 2)

    #TO DO: may need to reconsider this calculation.
    def PMI(self, principal=None):
        """
        Returns the PMI amount if PMI is required and the remaining principal is greater than 80% of the total.
        :return: The PMI amount if required.
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
        """
        Sets the PMI rate. PMI is a yearly percentage of your total loan amount at origination. Typically between 0.5%
        and 2% depending on various factors like credit score.
        :param new_pmi_rate: The new PMI rate.
        :return: Nothing.
        """
        self._PMI_rate = new_pmi_rate

    def no_PMI(self):
        """
        Indicates that PMI is not required for this mortgage.
        :return: Nothing.
        """
        self._pmi_required = False

    def req_PMI(self):
        """
        Indicates that PMI is required for this mortgage.
        :return: Nothing.
        """
        self._pmi_required = True

    def is_PMI_required(self):
        """
        Checks to see if PMI is required.
        :return: True if PMI is required.
        """
        return self._pmi_required

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