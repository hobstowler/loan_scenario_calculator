# Author: Hobs Towler
# Date: 12/5/2021
# Description:

import pickle

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


def load_scenarios() -> dict:
    """
    Loads scenarios from saved data. Can be called independently.
    :return: Saved scenarios.
    """
    pickle.load(open(data_file_path + scenarios_file_name, "rb"))


def load_expenses() -> dict:
    """
    Loads expenses from saved data. Can be called independently.
    :return: Saved expenses
    """
    pickle.load(open(data_file_path + expenses_file_name, "rb"))


def load_jobs() -> dict:
    """
    Loads jobs from saved data. Can be called independently.
    :return: Saved jobs.
    """
    pickle.load(open(data_file_path + jobs_file_name, "rb"))


def load_incomes() -> dict:
    """
    Loads incomes from saved data. Can be called independently.
    :return: Saved incomes.
    """
    pickle.load(open(data_file_path + incomes_file_name, "rb"))


def load_loans() -> dict:
    """
    Loads loans from saved data. Can be called independently.
    :return: Saved loans.
    """
    pickle.load(open(data_file_path + loan_file_name, "rb"))


def save_scenarios(data: dict):
    """
    Saves scenarios to scenarios.p file in data folder.
    :param data: The scenarios to be saved.
    :return: None.
    """
    pickle.dump(data, open(data_file_path + scenarios_file_name, 'wb'))


def save_expenses(data: dict):
    """
    Saves expenses to the expenses.p file in data folder.
    :param data: The expenses to be saved.
    :return: None.
    """
    pickle.dump(data, open(data_file_path + expenses_file_name, 'wb'))


def save_jobs(data: dict):
    """
    Saves jobs to the jobs.p file in data folder.
    :param data: The jobs to be saved.
    :return: None.
    """
    pickle.dump(data, open(data_file_path + jobs_file_name, 'wb'))


def save_incomes(data: dict):
    """
    Saves incomes to the incomes.p file in data folder.
    :param data: The incomes to be saved.
    :return: None.
    """
    pickle.dump(data, open(data_file_path + incomes_file_name, 'wb'))


def save_loans(data: dict):
    """
    Saves loans to the loans.p file in data folder.
    :param data: The loans to be saved.
    :return: None
    """
    pickle.dump(data, open(data_file_path + loan_file_name, 'wb'))


#TODO improve by just getting each key?
def save_all(data: dict):
    """
    Saves all data by calling sub methods based on key.
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