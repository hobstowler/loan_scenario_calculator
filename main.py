# Author: Hobs Towler
# Date: 12/1/2021
# Description:

class Scenario:
    def __init__(self) -> None:
        self._jobs = set({})
        self._incomes = set({})
        self._expenses = set({})
        self._loans = set({})