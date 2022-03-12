# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import math
import tkinter
from datetime import date
from tkinter import W, E

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from income import FinanceObj
from matplotlib import pyplot
import tkinter as tk
import tkinter.ttk as ttk
from errors import ErrorBox


class ExtraPayment:
    def __init__(self, start_month, length, amount):
        self.start = start_month
        self.length = length
        self.end = start_month + length
        self.amount = amount


class ExtraPaymentWindow:
    def __init__(self, root, loan):
        self._loan = loan

        self._start = tk.IntVar()
        self._duration = tk.IntVar()
        self._amount = tk.IntVar()

        window = tk.Toplevel(root)
        window.title("Add Extra Payments")
        #window.geometry("200x200")
        window.grid_propagate(True)
        self._frame = tk.Frame(window)
        self._frame.grid(column=0, row=0)
        #self._frame.pack_propagate(True)
        self.populate()
        self._root = root

    def new_extra_payment(self):
        try:
            if self._start.get() == 0 or self._duration.get() == 0 or self._amount.get() == 0:
                ErrorBox(self._root, "invalid inputs")
            else:
                new_extra_payment = ExtraPayment(self._start.get(), self._duration.get(), self._amount.get())
                self._loan.add_extra_payment(new_extra_payment)
            self.populate()
        except tkinter.TclError:
            ErrorBox(self._root, "invalid inputs")
        self._start.set(0)
        self._duration.set(0)
        self._amount.set(0)

    def populate(self):
        for c in self._frame.winfo_children():
            c.destroy()
        print('populating')
        frame = self._frame
        extra_payments = self._loan.get_extra_payments()
        tk.Label(frame, text=self._loan.name().title()).grid(column=0, row=0, columnspan=6)
        tk.Label(frame, text="").grid(column=0, row=1)

        tk.Label(frame, text="Start Month").grid(column=0, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._start).grid(column=0, row=3, columnspan=2)
        tk.Label(frame, text="Duration").grid(column=2, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._duration).grid(column=2, row=3, columnspan=2)
        tk.Label(frame, text="Amount").grid(column=4, row=2, columnspan=2)
        tk.Entry(frame, textvariable=self._amount).grid(column=4, row=3, columnspan=2)
        add_button = tk.Button(frame, text='Add')
        add_button.grid(column=5, row=5, sticky=W+E)
        add_button.bind("<Button-1>", lambda e: self.new_extra_payment())

        last = 6
        for i in range(len(extra_payments)):
            tk.Label(frame, text=extra_payments[i].start).grid(column=0, row=6+i, columnspan=2, sticky=W+E)
            tk.Label(frame, text=extra_payments[i].length).grid(column=2, row=6+i, columnspan=2, sticky=W+E)
            tk.Label(frame, text=extra_payments[i].amount).grid(column=4, row=6+i, columnspan=2, sticky=W+E)
            last += 1

        tk.Label(frame, text="").grid(column=0, row=last)

        quit_button = tk.Button(frame, text='Close')
        quit_button.grid(column=2, row=last+1, columnspan=2, sticky=W+E)
        quit_button.bind("<Button-1>", lambda e: self.exit())

    def exit(self):
        self._frame.winfo_toplevel().destroy()




class Loan(FinanceObj):
    def __init__(self, name: str, desc: str = ""):
        super(Loan, self).__init__(name, desc)
        self._type = "Loan"
        self._monthly_payment = 1200
        self._extra_payments = []

        self._data.update({"total": 240000})
        self._data.update({"rate": 2.875})
        self._data.update({"term": 360})
        self._data.update({"down payment": 80000})
        self._data.update({"principal": 160000})

        self._data.update({"origination": date(2020, 1, 1)})
        self._data.update({'first payment': date(2020, 2, 1)})
        self.calc_monthly()

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

    def calc_monthly(self) -> None:
        """
        Calculates the monthly payment.
        :return: Nothing.
        """
        principal = self._data.get("principal")
        m_rate = float(self._data.get("rate")) / 100 / 12
        compound = math.pow(1 + m_rate, self._data.get("term"))

        numer = principal * m_rate * compound
        denom = compound - 1

        self._monthly_payment = numer / denom

    def get_monthly(self):
        """
        Returns the monthly payment amount for this loan.
        :return: The monthly amount in dollars.
        """
        return round(self._monthly_payment, 2)

    def add_extra_payment(self, new_ex_payment: ExtraPayment) -> None:
        """
        Adds an ExtraPayment object to the loan. Extra payments have a defined amount, duration, and start month.
        :param new_ex_payment: The ExtraPayment object to be added.
        :return: Nothing.
        """
        if new_ex_payment not in self._extra_payments:
            self._extra_payments.append(new_ex_payment)

    def remove_extra_payment(self, extra_payment: ExtraPayment) -> bool:
        """
        Removes an ExtraPayment from the list if it is present.
        :param extra_payment: The ExtraPayment to be removed.
        :return: True if successfully removed.
        """
        if extra_payment in self._extra_payments:
            self._extra_payments.remove(extra_payment)
            return True
        return False

    def get_extra_payments(self) -> list:
        return self._extra_payments

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

        #TODO support for real dates
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

        return schedule

    def compare_schedules(self, display_graph=False) -> tuple:
        """
        Returns the amortization schedules of the loan with and without extra payments applied.
        :param display_graph: Optional. Displays a graph of the two schedules principal amounts over time.
        :return: Tuple of the schedules, Schedule with no extra payments and Schedule with extra payments.
        """
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
        super(Mortgage, self).__init__(name, desc)
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

    def launch_extra_payments(self, parent):
        root = parent.get_root()
        ExtraPaymentWindow(root, self)

    def get_editable(self, root, parent):
        frame = tk.Frame(root)
        frame.pack(fill='both')
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)
        frame.columnconfigure(2, weight=4)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)

        cancel = tk.Button(frame, text='X', anchor='e')
        cancel.grid(column=4, row=0)
        cancel.bind('<Button-1>', lambda e, w=parent: self.cancel(w))

        name_string = tk.StringVar()
        name_string.set(self._name)
        tk.Label(frame, text="Name", anchor='e').grid(column=1, row=1)
        tk.Entry(frame, name='name', textvariable=name_string).grid(column=2, row=1, columnspan=2, sticky=W + E)

        desc_string = tk.StringVar()
        desc_string.set(self._desc)
        tk.Label(frame, text="Description", anchor='e').grid(column=1, row=2)
        tk.Entry(frame, name='desc', textvariable=desc_string).grid(column=2, row=2, columnspan=2, sticky=W + E)

        extra_payments =tk.Button(frame, text='Extra Payments')
        extra_payments.grid(column=1, row=3)
        extra_payments.bind("<Button-1>", lambda e, p=parent: self.launch_extra_payments(p))

    def get_detail(self, root, parent):
        frame = tk.Frame(root)
        frame.pack(fill='both')
        frame.pack_propagate(True)
        sched1, sched2 = self.compare_schedules()
        #print(schedule)
        fig = pyplot.Figure(figsize=(5, 3), dpi=100)
        p = fig.add_subplot(111)
        p.plot(range(0, len(sched1)), sched1)
        p.plot(range(0, len(sched2)), sched2)
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.get_tk_widget().pack()
        #canvas.show()


#TODO Implement
class VariableRateMortgage(Mortgage):
    def __init__(self, total=0, rate=1, length=60) -> None:
        super(Mortgage, self).__init__()


#TODO Implement
class Auto(Loan):
    def __init__(self, name: str, desc: str = ""):
        super().__init__(name, desc)


class Student(Loan):
    def __init__(self, name: str, desc: str = ""):
        super().__init__(name, desc)


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
