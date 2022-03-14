# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import math
import tkinter
from datetime import date
from tkinter import W, E, LEFT, RIGHT, N, S, BOTH, X

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from income import FinanceObj, colors
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

    # TODO support for insurance and property tax escrow
    def amortization_schedule(self, extra_payments=False) -> dict:
        """
        Calculates the amortization schedule with extra payments for the loan and returns the schedule as a list.
        @param extra_payments: The amount of extra payment per month
        @return: The amortization schedule.
        """
        amortization ={}
        principal = self._data.get("principal")
        monthly_payment = self._monthly_payment
        term = self._data.get("term")

        #TODO support for real dates
        origination = self._data.get("origination")
        first_payment = self._data.get("first payment")

        schedule = [[0, principal, 0, 0]]
        total_interest = 0
        total = 0
        last_month = 0
        for i in range(1, term + 1):
            if principal != 0:
                extra = 0
                interest = self.calc_m_interest(principal)
                principal = principal + interest - monthly_payment
                if extra_payments:
                    for e in self._extra_payments:
                        if e.start <= i < e.end:
                            extra += e.amount
                    principal -= extra
                if principal < 0:
                    extra -= principal
                    principal = 0
                    amortization.update({'last_month': i})
                schedule.append([i, principal, interest, extra])
            else:
                schedule.append([0, 0, 0])

        amortization.update({'total': total})
        amortization.update({'total interest': total_interest})
        amortization.update({'monthly payment': monthly_payment})
        amortization.update({'schedule': schedule})
        if last_month == 0:
            amortization.update({'last_month': term})

        return amortization

    def compare_schedules(self, display_graph=False) -> tuple:
        """
        Returns the amortization schedules of the loan with and without extra payments applied.
        :param display_graph: Optional. Displays a graph of the two schedules principal amounts over time.
        :return: Tuple of the schedules, Schedule with no extra payments and Schedule with extra payments.
        """
        no_extra = self.amortization_schedule()
        extra = self.amortization_schedule(True)
        difference = {}
        comparison = {
            'no extra': no_extra,
            'extra': extra,
            'difference': difference
        }

        if display_graph:
            schedule_no_extra = [item[1] for item in no_extra.get('schedule')]
            schedule_extra = [item[1] for item in extra.get('schedule')]
            term = self._data.get("term")
            pyplot.plot(range(term+1), schedule_no_extra, color='r', label="no extra payment")
            pyplot.plot(range(term+1), schedule_extra, color='b', label="with extra payments")
            pyplot.xlabel("months")
            pyplot.ylabel("principal")
            pyplot.show()

        return comparison

    def get_editable(self, root, parent) -> tuple:
        frame, index = super().get_editable(root, parent)

        index = self.tk_line_break(frame, index)

        start_string = tk.StringVar()
        start_string.set(self._data.get('origination'))
        tk.Label(frame, text="Loan Start (MM/DD/YYYY)", anchor='e').grid(column=1, row=index)
        tk.Entry(frame, name='origination', textvariable=start_string).grid(column=2, row=index, columnspan=2, sticky=W+E)
        index += 1

        term = tk.StringVar()
        term.set(self._data.get('term'))
        tk.Label(frame, text="Loan Term (Months)", anchor='e').grid(column=1, row=index)
        tk.Entry(frame, name='term', textvariable=term).grid(column=2, row=index, columnspan=2, sticky=W+E)
        index += 1

        index = self.tk_line_break(frame, index)

        total = tk.StringVar()
        total.set(self._data.get('total'))
        tk.Label(frame, text="Total Amount", anchor='e').grid(column=1, row=index)
        tk.Entry(frame, name='total', textvariable=total).grid(column=2, row=index, columnspan=2, sticky=W+E)
        index += 1

        down_payment = tk.StringVar()
        down_payment.set(self._data.get('down payment'))
        tk.Label(frame, text="Down Payment", anchor='e').grid(column=1, row=index)
        tk.Entry(frame, name='down payment', textvariable=down_payment).grid(column=2, row=index, columnspan=2, sticky=W+E)
        index += 1

        rate = tk.StringVar()
        rate.set(self._data.get('rate'))
        tk.Label(frame, text="Rate", anchor='e').grid(column=1, row=index)
        tk.Entry(frame, name='rate', textvariable=rate).grid(column=2, row=index, columnspan=2, sticky=W+E)
        index += 1

        index = self.tk_line_break(frame, index)

        return frame, index


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
        frame, index = super().get_editable(root, parent,)

        index = self.tk_line_break(frame, index)

        extra_payments = tk.Button(frame, text='Extra Payments')
        extra_payments.grid(column=1, row=index)
        extra_payments.bind("<Button-1>", lambda e, p=parent: self.launch_extra_payments(p))

    def get_detail(self, root, parent):
        comparison = self.compare_schedules()

        frame = tk.Frame(root)
        frame.pack(fill='both')
        frame.pack_propagate(True)

        base_stats = tk.Frame(root, width=200, height=300)
        base_stats.grid(column=0, row=1, columnspan=2, sticky=N+S+W+E)
        base_stats.pack_propagate(False)

        tk.Label(base_stats, text='Total:').pack()
        tk.Label(base_stats, text=self._data.get('total')).pack()
        tk.Label(base_stats, text='Down Payment:').pack()
        tk.Label(base_stats, text=self._data.get('down payment')).pack()
        tk.Label(base_stats, text='Principal:').pack()
        tk.Label(base_stats, text=self._data.get('principal')).pack()
        tk.Label(base_stats, text='Loan Term:').pack()
        term_string = str(self._data.get('term')) + " months"
        tk.Label(base_stats, text=term_string).pack()
        tk.Label(base_stats, text='Rate:').pack()
        tk.Label(base_stats, text=self._data.get('rate')).pack()

        graph = tk.Frame(root, width=500, height=300)
        graph.grid(column=2, row=1, columnspan=5, sticky=N+S+W+E)
        graph.pack_propagate(False)

        self.create_graph(graph, title="Loan Comparison")

        tk.Frame(root, height=10).grid(column=0, row=2)

        loan_detail = tk.Frame(root, width=300, height=350)
        loan_detail.grid(column=0, row=3, columnspan=3)
        tk.Label(loan_detail, text="Loan Detail without Extra Payments", font=('bold', 14)).pack(fill=X)

        extra_detail = tk.Frame(root, width=300, height=350)
        extra_detail.grid(column=4, row=3, columnspan=3)
        tk.Label(extra_detail, text="Loan Detail with Extra Payments", font=('bold', 14)).pack(fill=X)


    def create_graph(self, root, title=""):
        sched1, sched2 = self.compare_schedules()
        fig = pyplot.Figure(figsize=(5, 3), dpi=100)
        fig.suptitle(title, fontsize=14)
        p = fig.add_subplot(111)
        p.plot(range(0, len(sched1)), sched1)
        p.plot(range(0, len(sched2)), sched2)
        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().pack()

    def get_list_button(self, root, parent):
        #super().get_list_button(root, parent)
        frame = tk.Frame(root, borderwidth=2, relief='groove', height=40)
        frame.pack(fill="x", ipady=2)
        frame.bind("<Button-1>", lambda e: self.left_click())
        # TODO Move to JSON for data load to allow changes to main attributes
        # if self._active:
        #    frame['bg'] = colors.get("b_sel")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        name = tk.Label(frame, text=self._data.get('name'), justify=LEFT, anchor="w", foreground=colors.get('fin_type'))
        name.grid(column=0, row=0, sticky=W)
        f_type = tk.Label(frame, text=self.type(), justify=RIGHT, anchor="e", foreground=colors.get("t_type"))
        f_type.grid(column=1, row=0, sticky=E)
        desc = tk.Label(frame, text=self._data.get('desc'), justify=LEFT, anchor="w")
        desc.grid(column=0, row=1, sticky=W, columnspan=2)
        amount_string = str(self._data.get('total')) + " | " + str(self._data.get('principal')) + " | "+ str(self._data.get('rate'))
        tk.Label(frame, text=amount_string).grid(column=0, row=2, sticky=W, columnspan=3)

        frame.bind("<Button-1>", lambda e, p=parent: self.left_click(p))
        frame.bind("<Button-3>", lambda e, p=parent: self.right_click(p))
        frame.bind("<Enter>", self.list_enter)
        frame.bind("<Leave>", self.list_leave)
        for c in frame.winfo_children():
            c.bind("<Button-1>", lambda e, p=parent: self.left_click(p))
            c.bind("<Button-3>", lambda e, p=parent: self.right_click(p))
            c.bind("<Enter>", self.list_enter)
            c.bind("<Leave>", self.list_leave)
            if self._active:
                c['bg'] = colors.get("b_sel")


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
