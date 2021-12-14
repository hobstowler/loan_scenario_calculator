# Author: Hobs Towler
# Date: 12/5/2021
# Description:

import pickle

data_file_path = "\data"

def load_scenarios() -> list:
    """
    Imports scenarios from the Scenarios folder.
    :return:
    """
    pass


def load_expenses() -> list:
    pass


def load_jobs() -> list:
    pass


def load_incomes() -> list:
    pass


def load_loans() -> list:
    pass


def save_scenarios():
    pass


def save_expenses():
    pass


def save_jobs():
    pass


def save_incomes():
    pass


def save_loans():
    pass

def save_all(data: dict):
    for k in data:
        if k == "loans":
            save_loans()
        if k == "incomes":
            save_incomes()