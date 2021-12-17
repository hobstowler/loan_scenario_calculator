# Author: Hobs Towler
# Date: 12/5/2021
# Description:

import pickle
from os.path import exists

# Constants
data_file_path = "data/"
scenarios_file_name = "scenarios.p"
expenses_file_name = "expenses.p"
jobs_file_name = "jobs.p"
incomes_file_name = "incomes.p"
loan_file_name = "loans.p"


def load_all() -> dict:
    """
    Returns all the saved data as a dictionary. Calls into each separate load method.
    :return: Saved data.
    """
    data = {}
    data.update({"scenarios": load_scenarios()})
    data.update({"expenses": load_expenses()})
    data.update({"jobs": load_jobs()})
    data.update({"incomes": load_incomes()})
    data.update({"loans": load_loans()})
    return data


def load_scenarios() -> list:
    """
    Loads scenarios from saved data. Can be called independently.
    :return: List of saved scenarios.
    """
    file = data_file_path + scenarios_file_name
    if exists(file):
        return pickle.load(open(file, "rb"))
    return []


def load_expenses() -> list:
    """
    Loads expenses from saved data. Can be called independently.
    :return: List of saved expenses
    """
    file = data_file_path + expenses_file_name
    if exists(file):
        pickle.load(open(file, "rb"))
    return []


def load_jobs() -> list:
    """
    Loads jobs from saved data. Can be called independently.
    :return: List of saved jobs.
    """
    file = data_file_path + jobs_file_name
    if exists(file):
        pickle.load(open(file, "rb"))
    return []


def load_incomes() -> list:
    """
    Loads incomes from saved data. Can be called independently.
    :return: List of saved incomes.
    """
    file = data_file_path + incomes_file_name
    if exists(file):
        pickle.load(open(file, "rb"))
    return []


def load_loans() -> list:
    """
    Loads loans from saved data. Can be called independently.
    :return: List of saved loans.
    """
    file = data_file_path + loan_file_name
    if exists(file):
        pickle.load(open(file, "rb"))
    return []


def save_scenarios(data: list):
    """
    Saves scenarios to scenarios.p file in data folder.
    :param data: List of scenarios to be saved.
    :return: None.
    """
    pickle.dump(data, open(data_file_path + scenarios_file_name, 'wb'))


def save_expenses(data: list):
    """
    Saves expenses to the expenses.p file in data folder.
    :param data: List of expenses to be saved.
    :return: None.
    """
    pickle.dump(data, open(data_file_path + expenses_file_name, 'wb'))


def save_jobs(data: list):
    """
    Saves jobs to the jobs.p file in data folder.
    :param data: List of jobs to be saved.
    :return: None.
    """
    pickle.dump(data, open(data_file_path + jobs_file_name, 'wb'))


def save_incomes(data: list):
    """
    Saves incomes to the incomes.p file in data folder.
    :param data: List of incomes to be saved.
    :return: None.
    """
    pickle.dump(data, open(data_file_path + incomes_file_name, 'wb'))


def save_loans(data: list):
    """
    Saves loans to the loans.p file in data folder.
    :param data: List of loans to be saved.
    :return: None
    """
    pickle.dump(data, open(data_file_path + loan_file_name, 'wb'))


def save_all(data: dict):
    """
    Saves all data by calling sub methods based on key. Data is expected to be a dictionary containing lists of each
    type. For example:
    {"loans": [], "incomes": [], "jobs": [], "expenses": [], "scenarios": []}
    :param data: The data to be saved.
    :return: None.
    """
    if "loans" in data:
        save_loans(data.get("loans"))
    if "incomes" in data:
        save_incomes(data.get("incomes"))
    if "jobs" in data:
        save_jobs(data.get("jobs"))
    if "expenses" in data:
        save_expenses(data.get("expenses"))
    if "scenarios" in data:
        save_scenarios(data.get("scenarios"))