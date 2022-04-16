# Author: Hobs Towler
# Date: 12/1/2021
# Description:
import locale
import math
import tkinter
import tkinter as tk
from datetime import date
from tkinter import W, E, LEFT, RIGHT, N, S, X, Y, BOTH, ttk, BOTTOM

from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from misc import ErrorBox, Style, ExtraPaymentWindow, ExtraPayment
from income import FinanceObj


class Loan(FinanceObj):
    def __init__(self, app, name: str, desc: str = ""):
        super().__init__(app, name, desc)
        self._type = "Loan"
        self._extra_payments = []

        self._data.update({
            "total": 240000,
            "down payment": 80000,
            "principal": 160000,
            "rate": 2.875,
            "term": 360,
            "down payment": 80000,
            "principal": 160000,
            "origination": date(2020, 1, 1),
            'first payment': date(2020, 2, 1),
            'monthly payment': 1200,
            'loan company': 'Neighborhood Loan Company'
        })
        self.calc_principal()
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

    def calc_principal(self) -> float:
        total = self.data('total')
        down = self.data('down payment')
        principal = total - down
        self._data.update({'principal': principal})
        return round(principal, 2)

    def calc_monthly(self) -> float:
        """
        Calculates the monthly payment.
        :return: Nothing.
        """
        self.calc_principal()
        principal = self._data.get("principal")
        m_rate = float(self._data.get("rate")) / 100 / 12
        compound = math.pow(1 + m_rate, self._data.get("term"))

        monthly = round((principal * m_rate * compound) / (compound - 1), 2)
        self._data.update({'monthly payment': monthly})
        return round(monthly, 2)

    def get_extra_payments(self) -> list:
        return self._extra_payments

    def launch_extra_payment_editor(self):
        root = self._app.get_root()
        ExtraPaymentWindow(root, self._app, self)

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
        term = int(self._data.get("term"))

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
                    #print("last month:", i)
                    extra -= principal
                    principal = 0
                    last_month = i
                schedule.append([i, principal, interest, extra])
                total_interest += interest
                total += extra + interest + principal
            else:
                schedule.append([0, 0, 0, 0])

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

    def get_editable(self, root, name: str = None, desc: str = None) -> tuple:
        monthly = self.calc_monthly()

        frame, index = super().get_editable(root, name, desc)
        index = self.tk_editable_entry('loan company', 'Loan Company', frame, index)

        index = self.tk_line_break(frame, index)
        index = self.tk_editable_entry('origination', 'Loan Start', frame, index)
        index = self.tk_editable_entry('term', 'Loan Term ', frame, index, 'Months')
        index = self.tk_line_break(frame, index)
        index = self.tk_editable_entry('total', 'Total Amount', frame, index)

        principal = self.calc_principal()
        index = self.tk_editable_entry('down payment', 'Down Payment', frame, index, f" =${principal:,}")

        index = self.tk_editable_entry('rate', 'Rate', frame, index)
        tk.Label(frame, text=f'= ${monthly:,}', anchor='e').grid(column=2, row=index, columnspan=1, sticky=W+E)
        index += 1
        index = self.tk_line_break(frame, index)

        extra_payments = tk.Button(frame, text='Extra Payments')
        extra_payments.grid(column=1, row=index, columnspan=2, sticky=W+E)
        extra_payments.bind("<Button-1>", lambda e: self.launch_extra_payment_editor())
        index += 1

        return frame, index


class Mortgage(Loan):
    def __init__(self, app, name: str, desc: str = "") -> None:
        super().__init__(app, name, desc)
        self._type = "Mortgage"

        self._assessment_override = False

        self._data.update({
            'pmi': 100,
            'pmi required': 1,
            'property tax': 1890,
            'hoa': 0,
            'mortgage company': "Friendly Neighborhood Credit Union",
            'insurance premium': 550,
            'insurance company': "State Farm",
            'total monthly': 0,
            'escrow': 0
        })
        self._assumptions.update({
            'assessed value': 200000,
            'property tax rate': 1,
            'pmi rate': 0.5
        })
        self.calc_total_monthly()
        self.calculate_assessed_value()

    @staticmethod
    def __str__():
        return f'Mortgage'

    def calculate_assessed_value(self) -> float:
        if self._assessment_override:
            return round(self.data('assessed value'), 2)
        else:
            self._data.update({'assessed value': self.data('total') * 0.95})
            return round(self.data('assessed value'), 2)

    #TO DO: may need to reconsider this calculation.
    def calc_PMI(self) -> float:
        """
        Returns the PMI amount if PMI is required and the remaining principal if greater than 80% of the total.
        :return: The PMI amount if required.
        """
        principal = self.data('principal')
        percent_down = round(1-(principal / self.data('total')), 2)

        if percent_down < 0.2 and self.data('pmi required') == 1:
            pmi_rate = self.assume('pmi rate') / 100
            pmi = round((principal * pmi_rate)/12, 2)
            self._data.update({'pmi': pmi})
            print(pmi)
            return pmi
        else:
            return 0

    def calc_escrow(self) -> float:
        pmi = 0
        if self.data('pmi required') == 1:
            pmi = self.calc_PMI()

        escrow = round(((self.data('insurance premium') + self.data('property tax')) / 12) + pmi, 2)
        self._data.update({'escrow': escrow})
        return escrow

    def calc_total_monthly(self) -> float:
        """
        Calculates the monthly payment.
        :return: Nothing.
        """
        print('monthly total?')
        monthly = self.calc_monthly()
        escrow = self.calc_escrow()
        print('escrow:', escrow)
        total = round(monthly + escrow, 2)
        self._data.update({'total monthly': total})
        return total

    def get_editable(self, root) -> tuple:
        frame, index = super().get_editable(root, "Street Address", "City, State ZIP")

        self._form_vars
        index += 1

        return frame, index

    def get_list_button(self, root):
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

        frame.bind("<Button-1>", lambda e: self.left_click())
        frame.bind("<Button-3>", lambda e: self.right_click())
        frame.bind("<Enter>", lambda e: self.list_button_enter(e))
        frame.bind("<Leave>", lambda e: self.list_button_leave(e))
        for c in frame.winfo_children():
            c.bind("<Button-1>", lambda e: self.left_click())
            c.bind("<Button-3>", lambda e: self.right_click())
            c.bind("<Enter>", lambda e: self.list_button_enter(e))
            #c.bind("<Leave>", self.list_leave)
            if self._active:
                c['bg'] = Style.color("b_sel")

    def get_detail(self, root):
        self.calc_total_monthly()
        comparison = self.compare_schedules()
        differences = comparison.get('difference')
        months_saved = differences.get('months saved')
        years_saved = differences.get('years saved')
        interest_saved = differences.get('interest saved')

        super().get_detail(root, desc=self.data('mortgage company'))

        # BASE STATS WINDOW
        stats = tk.Frame(root, height=290)
        stats.pack(fill=X, padx=10, pady=15)
        stats.pack_propagate(False)
        self.get_detail_stat(stats)

        # MAIN GRAPH
        graph = tk.Frame(stats)
        graph.pack(side=RIGHT)
        graph.pack_propagate(False)

        s1 = [schedule[1] for schedule in comparison.get('no extra').get('schedule')]
        s2 = [schedule[1] for schedule in comparison.get('extra').get('schedule')]
        schedules = [s1, s2]
        self.create_graph(graph, schedules, title="Loan Comparison")

        summary = tk.Frame(root, height=75)
        summary.pack(fill=X, padx=10)
        summary.grid_propagate(False)

        savings_string = f'You could pay off your mortgage {years_saved} year(s) and {months_saved} month(s) earlier.'
        interest_string = f'You could save ${interest_saved:,} in interest over the life of the loan.'

        savings_header = tk.Label(summary, text='By making extra payments...', font=('bold', 13), anchor=W)
        savings_header['fg'] = Style.color('detail subtitle')
        tk.Label(summary, text=savings_string, anchor=W)
        tk.Label(summary, text=interest_string, anchor=W)
        row = 0
        for c in summary.winfo_children():
            c.grid(column=0, columnspan=5, row=row, sticky=W+E)
            if row > 0:
                c.grid(padx=(10, 0))
            row += 1

        detail = tk.Frame(root)
        detail.pack(fill=BOTH, expand=True, padx=10, pady=15)
        detail.pack_propagate(False)

        #loan_detail = tk.Frame(detail, width=300)
        #loan_detail.pack(side=LEFT, expand=True, fill=Y, padx=15)
        #tk.Label(loan_detail, text="Loan Detail without Extra Payments", font=('bold', 12))\
        #    .grid(column=0, row=0, columnspan=2)

        #extra_detail = tk.Frame(detail, width=300)
        #extra_detail.pack(side=RIGHT, expand=True, fill=Y, padx=15)
        #tk.Label(extra_detail, text="Loan Detail with Extra Payments", font=('bold', 12))\
        #    .grid(column=0, row=0, columnspan=2)

        tree = ttk.Treeview(detail)
        tree.pack(side=BOTTOM, expand=True, fill=BOTH)
        tree['columns'] = ('normal', 'normal interest', 'accelerated', 'accelerated interest', 'extra payment')
        tree.column('normal', width=50)
        tree.heading('normal', text='Principal')
        tree.column('normal interest', width=50)
        tree.heading('normal interest', text='Interest')
        tree.column('accelerated', width=50)
        tree.heading('accelerated', text='Accelerated')
        tree.column('accelerated interest', width=50)
        tree.heading('accelerated interest', text='Interest')
        tree.column('extra payment', width=50)
        tree.heading('extra payment', text='Extra Payment')
        tree.insert('', 'end', 'schedule', text='test')

        s1 = comparison.get('no extra').get('schedule')
        s2 = comparison.get('extra').get('schedule')
        for i in range(len(s1)):
            tree.insert('', 'end', f'{i}', text=f'Month: {i}')
            tree.set(f'{i}', 'normal', f'{locale.currency(s1[i][1], grouping=True)}')
            tree.set(f'{i}', 'normal interest', f'{locale.currency(s1[i][2], grouping=True)}')
            if i < len(s2):
                #print(i)
                tree.set(f'{i}', 'accelerated', f'{locale.currency(s2[i][1], grouping=True)}')
                tree.set(f'{i}', 'accelerated interest', f'{locale.currency(s2[i][2], grouping=True)}')
                tree.set(f'{i}', 'extra payment', f'{locale.currency(s2[i][3], grouping=True)}')
            elif i == len(s2):
                tree.set(f'{i}', 'accelerated', f'$0.00')

    def get_detail_stat(self, root):
        stat_detail = tk.Frame(root, width=200)
        stat_detail.pack(side=LEFT, fill=Y, padx=(0, 10), pady=(15, 0))
        stat_detail.columnconfigure(0, weight=1)
        stat_detail.columnconfigure(1, weight=1)

        index = 0
        glance = tk.Label(stat_detail, text='At a Glance...', anchor='e', font=('bold', 12))
        glance.grid(column=0, row=index, sticky=W + E)
        glance['fg'] = Style.color('detail subtitle')
        index += 1

        tk.Label(stat_detail, text='Final Sale Price:', anchor='e').grid(column=0, row=index, sticky=W + E)
        tk.Label(stat_detail, text=f' ${self.data("total"):,}', anchor='e').grid(column=1, row=index, sticky=W + E)
        index += 1

        tk.Label(stat_detail, text='Down Payment:', anchor='e').grid(column=0, row=index, sticky=W + E)
        tk.Label(stat_detail, text=f' ${self.data("down payment"):,}', anchor='e').grid(column=1, row=index,
                                                                                        sticky=W + E)
        index += 1

        tk.Label(stat_detail, text='Principal:', anchor='e').grid(column=0, row=index, sticky=W + E)
        tk.Label(stat_detail, text=f' ${self.data("principal"):,}', anchor='e').grid(column=1, row=index, sticky=W + E)
        index += 1

        terms = f'{self.data("term")} months at {self.data("rate")}%'
        tk.Label(stat_detail, text=terms, anchor='e').grid(column=0, row=index, columnspan=2, sticky=W + E)
        index += 1
        index = self.tk_line(stat_detail, index, colspan=2, padding=(10, 0))
        tk.Label(stat_detail, text=f'= ${self.data("monthly payment"):,}', anchor='e') \
            .grid(column=1, row=index, columnspan=2, sticky=W + E)
        index += 1

        #   Escrow Display
        index = self.tk_line_break(stat_detail, index)

        if self.data('property tax') > 0:
            property_tax = round(self.data("property tax") / 12, 2)
            tk.Label(stat_detail, text='Property Tax:', anchor='e').grid(column=0, row=index, sticky=W + E)
            tk.Label(stat_detail, text=f' ${property_tax:,}', anchor='e').grid(column=1, row=index, sticky=W + E)
            index += 1

        percent_down = round(1 - (self.data('principal') / self.data('total')), 2)
        if self.data('pmi required') == 1 and percent_down < 0.2:
            tk.Label(stat_detail, text='PMI Payment:', anchor='e').grid(column=0, row=index, sticky=W + E)
            tk.Label(stat_detail, text=f' ${self.data("pmi"):,}', anchor='e').grid(column=1, row=index, sticky=W + E)
            index += 1

        insurance_premium = round(self.data("insurance premium") / 12, 2)
        tk.Label(stat_detail, text='Insurance Premium:', anchor='e').grid(column=0, row=index, sticky=W + E)
        tk.Label(stat_detail, text=f' ${insurance_premium:,}', anchor='e').grid(column=1, row=index, sticky=W + E)
        index += 1

        index = self.tk_line(stat_detail, index, colspan=2, padding=(10, 0))
        tk.Label(stat_detail, text=f'= ${self.data("escrow"):,}', anchor='e') \
            .grid(column=1, row=index, columnspan=2, sticky=W + E)
        index += 1

        index = self.tk_line_break(stat_detail, index)
        index = self.tk_line(stat_detail, index, colspan=2, padding=(10, 0))
        tk.Label(stat_detail, text=f'= ${self.data("total monthly"):,}', anchor='e') \
            .grid(column=1, row=index, columnspan=2, sticky=W + E)

    def create_graph(self, root, schedules, title=""):
        fig = pyplot.Figure(figsize=(5, 3), dpi=100)
        fig.suptitle(title, fontsize=14)
        p = fig.add_subplot(111)

        for schedule in schedules:
            p.plot(range(0, len(schedule)), schedule)

        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().grid(row=0, column=0)


#TODO Implement
class VariableRateMortgage(Mortgage):
    def __init__(self, total=0, rate=1, length=60) -> None:
        super(Mortgage, self).__init__()


#TODO Implement
class Auto(Loan):
    def __init__(self, app, name: str, desc: str = ""):
        super().__init__(app, name, desc)

    @staticmethod
    def __str__():
        return f'Auto'

    def get_editable(self, root, name: str = None, desc: str = None) -> tuple:
        super().get_editable(root, 'Model', 'Make')


class Student(Loan):
    def __init__(self, app, name: str, desc: str = ""):
        super().__init__(app, name, desc)

    @staticmethod
    def __str__():
        return f'Student'

    def get_editable(self, root, name: str = None, desc: str = None) -> tuple:
        super().get_editable(root, 'School', 'Degree')


class Personal(Loan):
    def __init__(self, app, name: str, desc: str = ""):
        super().__init__(app, name, desc)

    @staticmethod
    def __str__():
        return f'Personal'

    def get_editable(self, root, name: str = None, desc: str = None) -> tuple:
        super().get_editable(root, 'Item', 'Description')


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
