# Author: Hobs Towler
# Date: 12/1/2021
# Description:

import math
import tkinter
import tkinter as tk
from datetime import date
from tkinter import W, E, LEFT, RIGHT, N, S, X

from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from misc import ErrorBox, Style
from income import FinanceObj, colors, Window


class ExtraPayment:
    """Class representing an extra payment on a loan. Has a defined start, length, and amount."""
    def __init__(self, start_month, length, amount):
        """
        Initializes the extra payment with a start month, length, and amount.
        :param start_month: The month that extra payments start occurring.
        :param length: The number of months that extra payments will be made.
        :param amount: The amount of extra money paid in each installment.
        """
        self.start = start_month
        self.length = length
        self.end = start_month + length
        self.amount = amount


class ExtraPaymentWindow(Window):
    """
    Class representing a window interface for adding new and removing existing ExtraPayments from a Loan.
    """
    def __init__(self, root, parent, loan):
        super().__init__(root, parent, loan)
        self._parent = parent
        self._loan = loan

        self._start = tk.IntVar()
        self._duration = tk.IntVar()
        self._amount = tk.IntVar()

        self._window = tk.Toplevel(root)
        self._window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self._window.title("Add Extra Payments")
        self._window.grid_propagate(True)
        self._frame = tk.Frame(self._window)
        self._frame.grid(column=0, row=0)
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

    def delete_extra_payment(self, extra_payment):
        extra_payments_list = self._loan.get_extra_payments()
        if extra_payment in extra_payments_list:
            extra_payments_list.remove(extra_payment)
        self.populate()

    def populate(self):
        for c in self._frame.winfo_children():
            c.destroy()

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
        add_button = tk.Button(frame, text='Add', width=6)
        add_button.grid(column=6, row=3, sticky=W+E)
        add_button.bind("<Button-1>", lambda e: self.new_extra_payment())

        last = 6
        for i in range(len(extra_payments)):
            tk.Label(frame, text=extra_payments[i].start).grid(column=0, row=6+i, columnspan=2, sticky=W+E)
            tk.Label(frame, text=extra_payments[i].length).grid(column=2, row=6+i, columnspan=2, sticky=W+E)
            tk.Label(frame, text=extra_payments[i].amount).grid(column=4, row=6+i, columnspan=2, sticky=W+E)
            del_button = tk.Button(frame, text="Delete", width=6)
            del_button.bind("<Button-1>", lambda e, p=extra_payments[i]: self.delete_extra_payment(p))
            del_button.grid(column=6, row=6+i, columnspan=2, sticky=W+E)
            last += 1


class Loan(FinanceObj):
    def __init__(self, name: str, desc: str = ""):
        super(Loan, self).__init__(name, desc)
        self._type = "Loan"
        #self._monthly_payment = 1200
        self._extra_payments = []

        self._data.update({
            "total": 240000,
            "rate": 2.875,
            "term": 360,
            "down payment": 80000,
            "principal": 160000,
            "origination": date(2020, 1, 1),
            'first payment': date(2020, 2, 1),
            'monthly payment': 1200
        })
        self.calc_monthly()

    @staticmethod
    def __str__():
        return f'Loan'

    @classmethod
    def button_hover_message(cls):
        return f"Click to populate a list of {cls.__str__()} Loans."

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

    def calc_principal(self):
        total = self.data('total')
        down = self.data('down payment')
        principal = total - down
        self._data.update({'principal': principal})

    def calc_monthly(self) -> None:
        """
        Calculates the monthly payment.
        :return: Nothing.
        """
        self.calc_principal()
        principal = self._data.get("principal")
        m_rate = float(self._data.get("rate")) / 100 / 12
        compound = math.pow(1 + m_rate, self._data.get("term"))

        monthly = (principal * m_rate * compound) / (compound - 1)
        self._data.update({'monthly payment': monthly})
        return monthly

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
        monthly_payment = self.data('monthly payment')
        print('monthly payment:', monthly_payment)
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
                    print("last month:", i)
                    extra -= principal
                    principal = 0
                    last_month = i
                schedule.append([i, principal, interest, extra])
                total_interest += interest
                total += extra + interest + principal
            else:
                schedule.append([0, 0, 0])

        amortization.update({'total': round(total, 2)})
        amortization.update({'total interest': round(total_interest, 2)})
        amortization.update({'monthly payment': monthly_payment})
        amortization.update({'schedule': schedule})
        if last_month == 0:
            last_month = term
        amortization.update({'last month': last_month})

        return amortization

    def compare_schedules(self, display_graph=False) -> tuple:
        """
        Returns the amortization schedules of the loan with and without extra payments applied.
        :param display_graph: Optional. Displays a graph of the two schedules principal amounts over time.
        :return: Tuple of the schedules, Schedule with no extra payments and Schedule with extra payments.
        """
        no_extra = self.amortization_schedule()
        extra = self.amortization_schedule(True)
        m_saved =(no_extra.get('last month') - extra.get('last month')) % 12
        print(no_extra.get('last month'))
        print(extra.get('last month'))
        y_saved = int((no_extra.get('last month') - extra.get('last month')) / 12)
        diff_interest = (no_extra.get('total interest') - extra.get('total interest'))
        difference = {
            'months saved': m_saved,
            'years saved': y_saved,
            'interest saved': diff_interest
        }
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

    def get_editable(self, root, parent, name: str = None, desc: str = None) -> tuple:
        frame, index = super().get_editable(root, parent, name, desc)

        index = self.tk_line_break(frame, index)
        index = self.tk_editable_entry('origination', 'Loan Start (MM/DD/YYYY)', frame, parent, index)
        index = self.tk_editable_entry('term', 'Loan Term (Months)', frame, parent, index)
        index = self.tk_line_break(frame, index)
        index = self.tk_editable_entry('total', 'Total Amount', frame, parent, index)
        index = self.tk_editable_entry('down payment', 'Down Payment', frame, parent, index)
        index = self.tk_editable_entry('rate', 'Rate', frame, parent, index)
        index = self.tk_line_break(frame, index)

        return frame, index


class Mortgage(Loan):
    def __init__(self, name: str, desc: str = "") -> None:
        super(Mortgage, self).__init__(name, desc)
        self._type = "Mortgage"

        self._pmi_required = True
        self._property_tax_required = True
        self._data.update({
            'pmi': 100,
            'property tax': 1890,
            'hoa': 0,
            'mortgage company': "Friendly Neighborhood Credit Union",
            'insurance premium': 550,
            'insurance company': "State Farm",
            'total monthly': 0
        })
        self._assumptions.update({
            'pmi rate': 0.005,
            'property tax rate': 1
        })
        self.calc_total_monthly()

    @staticmethod
    def __str__():
        return f'Mortgage'

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
            principal = self.data('principal')
        percent_down = round(1-(principal / self.data('total')), 2)
        #print(percent_down)
        if percent_down < 0.2 and self._pmi_required:
            return round((principal * self.assume('pmi rate'))/12, 2)
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

    def calc_total_monthly(self) -> None:
        """
        Calculates the monthly payment.
        :return: Nothing.
        """
        monthly = super().calc_monthly()
        pmi = 0
        if self._pmi_required:
            pmi = self.PMI()

        monthly += (self.data('insurance premium') / 12) + (self.data('property tax') / 12) + pmi
        self._data.update({'total monthly': monthly})
        print("m:", monthly)
        return monthly

    def launch_extra_payment_editor(self, parent):
        root = parent.get_root()
        ExtraPaymentWindow(root, parent, self)

    def get_editable(self, root, parent) -> tuple:
        frame, index = super().get_editable(root, parent, "Street Address", "City, State ZIP")

        index = self.tk_line_break(frame, index)

        extra_payments = tk.Button(frame, text='Extra Payments')
        extra_payments.grid(column=1, row=index)
        extra_payments.bind("<Button-1>", lambda e, p=parent: self.launch_extra_payment_editor(p))
        index += 1

        return frame, index

    def get_detail(self, root, parent):
        self.calc_total_monthly()
        comparison = self.compare_schedules()
        differences = comparison.get('difference')
        months_saved = differences.get('months saved')
        years_saved = differences.get('years saved')
        interest_saved = differences.get('interest saved')

        frame, information = super().get_detail(root, parent)

        desc = tk.Label(information, text=self.data('mortgage company'))
        desc.grid(column=0, row=1, sticky=W)
        desc['bg'] = Style.color('bg_header')

        # BASE STATS WINDOW
        base_stats = tk.Frame(root, width=190, height=290)
        base_stats.grid(column=0, row=1, columnspan=2, sticky=N+S+W+E, padx=(0, 10), pady=(5,5))
        base_stats.pack_propagate(False)

        stat_desc = tk.Frame(base_stats)
        stat_desc.pack(side=LEFT)

        #tk.Label(stat_desc, text='Total:')
        #tk.Label(stat_desc, text='Down Payment:')
        tk.Label(stat_desc, text='Principal:')
        tk.Label(stat_desc, text='Loan Term:')
        tk.Label(stat_desc, text='Monthly Payment:')
        if self._property_tax_required:
            tk.Label(stat_desc, text='Property Tax:')
        tk.Label(stat_desc, text='Insurance:')
        if self._pmi_required:
            tk.Label(stat_desc, text='Monthly PMI:')
        tk.Label(stat_desc, text='Total Monthly:')
        tk.Label(stat_desc, text='Rate:')
        for c in stat_desc.winfo_children():
            c.configure(anchor=W)
            c.pack(fill=X)
            c['bg'] = 'orange'

        stats = tk.Frame(base_stats)
        stats.pack(side=RIGHT)

        #tk.Label(stats, text=f'${self.data("total"):,}')
        #tk.Label(stats, text=f'${self.data("down payment"):,}')
        tk.Label(stats, text=f'${self.data("principal"):,}')
        tk.Label(stats, text=str(self._data.get('term')) + " months")
        tk.Label(stats, text=f'${round(self.data("monthly payment"),2):,}')
        if self._property_tax_required:
            tk.Label(stats, text=f'${round(self.data("property tax")/12,2):,}')
        tk.Label(stats, text=f'${round(self.data("insurance premium")/12,2):,}')
        if self._pmi_required:
            tk.Label(stats, text=f'${round(self.data("pmi"),2):,}')
        tk.Label(stats, text=f'${round(self.data("total monthly"),2):,}')
        tk.Label(stats, text=str(self._data.get('rate')) + " %")
        for c in stats.winfo_children():
            c.configure(anchor=E)
            c.pack(fill=X)
            c['bg'] = 'green'

        # MAIN GRAPH
        graph = tk.Frame(root, width=500, height=300)
        graph.grid(column=2, row=1, columnspan=5, sticky=N+S+W+E)
        graph.pack_propagate(False)

        s1 = [sched[1] for sched in comparison.get('no extra').get('schedule')]
        s2 = [sched[1] for sched in comparison.get('extra').get('schedule')]
        schedules = [s1, s2]
        self.create_graph(graph, schedules, title="Loan Comparison")

        summary = tk.Frame(root, height=100, width=500)
        summary.grid(column=0, row=2, columnspan=5, sticky=W+E)
        summary.grid_propagate(False)
        summary['bg'] = 'red'
        savings_header = 'By making extra payments...'
        savings_string = f'You could pay off your mortgage {years_saved} year(s) and {months_saved} month(s) earlier.'
        interest_string = f'You could save ${interest_saved:,} in interest over the life of the loan.'
        tk.Label(summary, text='Summary', font=('bold', 14), anchor=W)
        tk.Label(summary, text=savings_header, anchor=W)
        tk.Label(summary, text=savings_string, anchor=W)
        tk.Label(summary, text=interest_string, anchor=W)
        row = 0
        for c in summary.winfo_children():
            c.grid(column=0, columnspan=5, row=row, sticky=W+E)
            c['bg'] = 'red'
            if row > 1:
                c.grid(padx=(10, 0))
            row += 1

        detail = tk.Frame(root, height=100, width=200)
        detail.grid(column=5, row=2, columnspan=2, sticky=W+E)
        detail.pack_propagate(False)
        detail['bg'] = 'blue'

        loan_detail = tk.Frame(root, width=300, height=350)
        loan_detail.grid(column=0, row=3, columnspan=3)
        tk.Label(loan_detail, text="Loan Detail without Extra Payments", font=('bold', 14)).pack(fill=X)

        extra_detail = tk.Frame(root, width=300, height=350)
        extra_detail.grid(column=4, row=3, columnspan=3)
        tk.Label(extra_detail, text="Loan Detail with Extra Payments", font=('bold', 14)).pack(fill=X)


    def create_graph(self, root, schedules, title=""):
        fig = pyplot.Figure(figsize=(5, 3), dpi=100)
        fig.suptitle(title, fontsize=14)
        p = fig.add_subplot(111)

        for schedule in schedules:
            p.plot(range(0, len(schedule)), schedule)

        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().pack()

    def get_list_button(self, root, parent):
        #super().get_list_button(root, parent)
        frame = tk.Frame(root, borderwidth=2, relief='groove', height=40)
        frame.pack(fill="x", ipady=2)
        frame.bind("<Button-1>", lambda e: self.left_click())
        # TODO Move to JSON for data load to allow changes to main attributes
        # if self._active:
        #    frame['bg'] = Style.color("b_sel")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        name = tk.Label(frame, text=self._data.get('name'), justify=LEFT, anchor="w", foreground=Style.color('fin_type'))
        name.grid(column=0, row=0, sticky=W)
        f_type = tk.Label(frame, text=self.type(), justify=RIGHT, anchor="e", foreground=Style.color("t_type"))
        f_type.grid(column=1, row=0, sticky=E)
        desc = tk.Label(frame, text=self._data.get('desc'), justify=LEFT, anchor="w")
        desc.grid(column=0, row=1, sticky=W, columnspan=2)
        amount_string = str(self._data.get('total')) + " | " + str(self._data.get('principal')) + " | "+ str(self._data.get('rate'))
        tk.Label(frame, text=amount_string).grid(column=0, row=2, sticky=W, columnspan=3)

        frame.bind("<Button-1>", lambda e, p=parent: self.left_click(p))
        frame.bind("<Button-3>", lambda e, p=parent: self.right_click(p))
        frame.bind("<Enter>", lambda e, p=parent: self.list_button_enter(p, e))
        frame.bind("<Leave>", lambda e, p=parent: self.list_button_leave(p, e))
        for c in frame.winfo_children():
            c.bind("<Button-1>", lambda e, p=parent: self.left_click(p))
            c.bind("<Button-3>", lambda e, p=parent: self.right_click(p))
            c.bind("<Enter>", lambda e, p=parent: self.list_button_enter(p, e))
            #c.bind("<Leave>", self.list_leave)
            if self._active:
                c['bg'] = Style.color("b_sel")


#TODO Implement
class VariableRateMortgage(Mortgage):
    def __init__(self, total=0, rate=1, length=60) -> None:
        super(Mortgage, self).__init__()


#TODO Implement
class Auto(Loan):
    def __init__(self, name: str, desc: str = ""):
        super().__init__(name, desc)

    @staticmethod
    def __str__():
        return f'Auto'


class Student(Loan):
    def __init__(self, name: str, desc: str = ""):
        super().__init__(name, desc)

    @staticmethod
    def __str__():
        return f'Student'


class Personal(Loan):
    def __init__(self, name: str, desc: str = ""):
        super().__init__(name, desc)

    @staticmethod
    def __str__():
        return f'Personal'


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
