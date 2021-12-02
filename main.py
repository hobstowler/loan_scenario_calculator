# Author: Hobs Towler
# Date: 12/1/2021
# Description:

from loans import *
from income import *

class Scenario:
    def __init__(self) -> None:
        self._jobs = set({})
        self._incomes = set({})
        self._expenses = set({})
        self._loans = set({})

    def add_job(self, job: Job):
        if not job in self._jobs:
            self._jobs.add(job)

    def rem_job(self, job: Job):
        if job in self._jobs:
            self._jobs.remove(job)

