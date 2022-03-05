# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import math
from datetime import date
from income import FinanceObj
from matplotlib import pyplot
import tkinter as tk
import tkinter.ttk as ttk


class ExtraPayment:
    def __init__(self, start_month, length, amount):
        self.start = start_month
        self.end = start_month + length
        self.amount = amount


class Loan(FinanceObj):
    def __init__(self, name: str, desc: str = ""):
        super(Loan, self).__init__(name, desc)
        self._type = "Loan"
        self._monthly_payment = 0
        self._extra_payments = []

        self._data.update({"total": 0})
        self._data.update({"rate": 0})
        self._data.update({"term": 0})
        self._data.update({"down payment": 0})
        self._data.update({"principal": 0})

        self._data.update({"origination": date(2020, 1, 1)})
        self._data.update({'first payment': date(2020, 2, 1)})

    def set_origination(self, new_year, new_month, new_day=1) -> None:
        """
        Sets a new loan origination date. Also updates the first payment to the first day of the next month.
        :param new_year: The new year of the origination date.
        :param new_month: The new month of the origination date.
        :param new_day: The new day of the origination date.
        :return: Nothing.
        """
        origination = self._data.get("origination")
        first_payment = self._data.get("first payment")

        origination.replace(year=new_year, month=new_month, day=new_day)
        if new_month == 12:
            new_month = 1
            new_year += 1
        first_payment.replace(year=new_year, month=new_month, day=1)

    def get_first_payment_date(self) -> date:
        """
        Returns the first payment date of the loan.
        :return: The date object with the date of first payment.
        """
        return self._data.get("first payment")

    def set_total(self, new_total, down_payment=None) -> None:
        """
        Sets the total value of the item for which the loan was taken out. If a down payment is specified, calculates
        the principal amount for the loan.
        :param down_payment: Optional. The down payment for the loan.
        :param new_total: The new total value.
        :return: Nothing.
        """
        self._data.update({"total": new_total})
        if down_payment is not None:
            self._data.update({"principal": new_total - down_payment})

    def get_total(self) -> float:
        """
        Returns the total amount without down payment.
        @return: The total amount for the loan.
        """
        return self._data.get("total")

    def get_principal(self) -> float:
        """
        Returns the principal amount of the loan
        :return:
        """
        return self._data.get("principal")

    def set_rate(self, new_rate):
        """
        Sets the rate for the loan.
        :param new_rate: The new rate
        :return: Nothing.
        """
        self._data.update({"rate": new_rate})

    def get_rate(self):
        """
        Returns the rate for the loan.
        @return: The rate.
        """
        return self._data.get("rate")

    def set_term(self, new_length):
        """
        Sets the length of the loan in months.
        :param new_length: New length in months
        :return: Nothing
        """
        self._data.update({"term": new_length})

    def get_term(self):
        """
        Returns the length of the loan in months.
        @return: The length in months
        """
        return self._data.get("term")

    def calc_m_interest(self, amount) -> float:
        """
        Calculates the monthly interest for a given amount and month.
        To be called when calculating amortization schedule.
        :param amount: The principal remaining at the start of the period.
        :param month: The month for which interest is to be calculated.
        :return: The amount of interest accrued that month
        """
        m_rate = float(self._data.get("rate")) / 100 / 12 # TODO make this work by month
        return round(amount * m_rate, 2)

    def calc_monthly(self):
        principal = self._data.get("principal")
        m_rate = float(self._data.get("rate")) / 100 / 12
        compound = math.pow(1 + m_rate, self._data.get("term"))

        numer = principal * m_rate * compound
        denom = compound - 1

        self._monthly_payment = numer / denom

    def get_monthly(self):
        return round(self._monthly_payment, 2)

    def add_extra_payment(self, new_ex_payment: ExtraPayment):
        if new_ex_payment not in self._extra_payments:
            self._extra_payments.append(new_ex_payment)

    # TO DO: factor in a prorated amount and use the start of the loan
    def amortization_schedule(self, extra_payments=False) -> list:
        """
        Calculates the amortization schedule with extra payments for the loan and returns the schedule as a list.
        @param extra_payments: The amount of extra payment per month
        @return: The amortization schedule.
        """
        principal = self._data.get("principal")
        monthly_payment = self._monthly_payment
        term = self._data.get("term")

        origination = self._data.get("origination")
        first_payment = self._data.get("first payment")

        schedule = []
        schedule.append(principal)
        print(schedule[0])
        for i in range(1, term + 1):
            interest = self.calc_m_interest(principal)
            principal = principal + interest - monthly_payment
            if extra_payments:
                print("so extra")
                for e in self._extra_payments:
                    print(e.start)
                    if e.start <= i < e.end:
                        principal -= e.amount
            if principal < 0:
                principal = 0
            schedule.append(principal)
            print(schedule[i])

        #pyplot.bar(range(0, term + 1), schedule, color='r')
        #pyplot.bar(range(0, term + 1), test, bottom=schedule, color='b')
        #pyplot.xlabel("months")
        #pyplot.ylabel("principal")
        #pyplot.legend(loc='upper left')
        #pyplot.show()

        return schedule

    def compare_schedules(self, display_graph=False) -> tuple:
        schedule_no_extra = self.amortization_schedule()
        schedule_extra = self.amortization_schedule(True)

        if display_graph:
            term = self._data.get("term")
            pyplot.plot(range(term+1), schedule_no_extra, color='r', label="no extra payment")
            pyplot.plot(range(term+1), schedule_extra, color='b', label="with extra payments")
            pyplot.xlabel("months")
            pyplot.ylabel("principal")
            pyplot.show()

        return schedule_no_extra, schedule_extra

    def get_form(self, root):
        form = tk.Frame(root)
        form.grid(column=0, row=0)



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
        Returns the PMI amount if PMI is required and the remaining principal if greater than 80% of the total.
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


def loan_to_mortgage(self, loan: Loan) -> Mortgage:
    new_mortgage = Mortgage(self.name(), self.desc())
    new_mortgage.set_data(self._data)
    return new_mortgage


def to_auto(self, loan: Loan) -> Auto:
    new_auto = Auto(self.name(), self.desc())
    new_auto.set_data(self._data)
    return new_auto


def main():
    loan = Loan("test", "test desc")
    loan.set_total(400000, 160000)
    loan.set_term(360)
    loan.set_rate(2.875)
    print(loan.calc_monthly())
    print(loan.calc_m_interest(240000))
    loan.add_extra_payment(ExtraPayment(5, 24, 1000))
    loan.add_extra_payment(ExtraPayment(60, 24, 1000))
    loan.compare_schedules(True)

if __name__ == "__main__":
    main()
