# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import datetime
from income import FinanceObj


class Loan(FinanceObj):
    def __init__(self, name: str, desc: str = ""):
        super(Loan, self).__init__(name, desc)
        self._type = "Loan"

        self._data.update({"total": 0})
        self._data.update({"rate": 0})
        self._data.update({"length": 0})
        self._data.update({"down payment": 0})
        self._data.update({"principal": 0})

        #self._loan_start = datetime.datetime(2021)

    def set_total(self, new_total):
        """
        Sets the total value of the item for which the loan was taken out.
        :param new_total: The new total value.
        :return: Nothing.
        """
        self._data.update({"total": new_total})

    def set_rate(self, new_rate):
        """
        Sets the rate for the loan.
        :param new_rate: The new rate
        :return: Nothing.
        """
        self._data.update({"rate": new_rate})

    def set_length(self, new_length):
        """
        Sets the length of the loan in months.
        :param new_length: New length in months
        :return: Nothing
        """
        self._data.update({"length": new_length})

    def get_amount(self):
        """
        Returns the total amount without down payment.
        @return: The total amount for the loan.
        """
        return self._data.get("total")

    def get_rate(self):
        """
        Returns the rate for the loan.
        @return: The rate.
        """
        return self._data.get("rate")

    def get_length(self):
        """
        Returns the length of the loan in months.
        @return: The length in months
        """
        return self._data.get("length")

    # TO DO: factor in a prorated amount and use the start of the loan
    def amortization_schedule(self, extra_amount=0) -> dict:
        """
        Calculates the amortization schedule with extra payments for the loan and returns the schedule as a dictionary.
        @param extra_amount: The amount of extra payment per month
        @return: The amortization schedule.
        """
        principal = self._data.get("principal")
        schedule = {0: principal}
        for i in range(1, self._data.get("length") + 1):
            interest = self._m_interest(principal)
            principal = round(principal + interest - self._m_payment - extra_amount, 2)
            schedule.update({i: [principal, interest, extra_amount]})
        return schedule


class Mortgage(Loan):
    def __init__(self, name: str, desc: str = "") -> None:
        super(Loan, self).__init__(name, desc)
        self._type = "Mortgage"

        self._pmi_required = True
        self._PMI_rate = .005

        self._property_tax = 1890
        self._property_tax_rate = 1
        self._property_tax_override = False

        self._hoa = 0

        self._insurance = 75
        self._insurance_co = "None"

        self._m_payment = ""
        self._t_payment = ""

    def mortgage_monthly(self) -> float:
        """
        Calculates the monthly mortgage payment based on rate and length of the loan. This is the amount without taxes,
        insurance, PMI, or HOA
        :return: The monthly payment.
        """
        monthly_rate = self._rate/12
        numerator = self._principal * (monthly_rate * ((1 + monthly_rate) ** self._length))
        denominator = ((1 + monthly_rate) ** self._length) - 1
        return round(numerator/denominator,2)

    def mortgage_total(self) -> float:
        """
        Sums the total of the mortgage, monthly property tax, PMI, insurance, and HOA.
        :return: The monthly total.
        """
        #print((self._property_tax / 12))
        #print(self.PMI())
        #print(self._insurance)
        return round(self.mortgage_monthly() + (self._property_tax / 12) + self.PMI() + self._insurance + self._hoa, 2)

    #TO DO: may need to reconsider this calculation.
    def PMI(self, principal=None) -> float:
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

    def set_PMI_rate(self, new_pmi_rate) -> None:
        """
        Sets the PMI rate. PMI is a yearly percentage of your total loan amount at origination. Typically between 0.5%
        and 2% depending on various factors like credit score.
        :param new_pmi_rate: The new PMI rate.
        :return: Nothing.
        """
        self._PMI_rate = new_pmi_rate

    def no_PMI(self) -> None:
        """
        Indicates that PMI is not required for this mortgage.
        :return: Nothing.
        """
        self._pmi_required = False

    def req_PMI(self) -> None:
        """
        Indicates that PMI is required for this mortgage.
        :return: Nothing.
        """
        self._pmi_required = True

    def is_PMI_required(self) -> bool:
        """
        Checks to see if PMI is required.
        :return: True if PMI is required.
        """
        return self._pmi_required

    def _m_interest(self, amount) -> float:
        """
        Calculates the monthly interest for a given amount and month.
        To be called when calculating amortization schedule.
        :param amount: The principal remaining at the start of the period.
        :param month: The month for which interest is to be calculated.
        :return: The amount of interest accrued that month
        """
        return round(amount * (self._rate / 12), 2)

    def set_property_tax(self, tax_amount) -> float:
        """
        Sets a user-defined property tax and sets the override flag.
        :param tax_amount: The yearly amount of property tax.
        :return: The property tax.
        """
        self._property_tax_override = True
        self._property_tax = tax_amount
        return self.calculate_property_tax()


    def set_property_tax_rate(self, new_rate) -> float:
        """
        Changes the tax rate and recalculates the property tax.
        :param new_rate: The new tax rate.
        :return: The calculated tax.
        """
        self._property_tax_rate = new_rate
        return self.calculate_property_tax()

    def clear_property_tax(self) -> None:
        """
        clears a user-defined property tax and sets the override flag back.
        :return: The calculated tax.
        """
        self._property_tax_override = False
        return self.calculate_property_tax()

    def calculate_property_tax(self) -> float:
        """
        Calculates the yearly property tax for a defined tax rate.
        :return: The calculated tax.
        """
        if not self._property_tax_override:
            self._property_tax = self._total * (self._property_tax_rate / 100)
        return self._property_tax


#TODO Implement
class VariableRateMortgage(Mortgage):
    def __init__(self, total=0, rate=1, length=60) -> None:
        super(Mortgage, self).__init__(total=total, rate=rate, length=length)
        self._type = "ARM"


#TODO Implement
class Auto(Loan):
    def __init__(self, name:str, desc: str = ""):
        super().__init__(name,desc)
        self._type = "Auto Loan"

