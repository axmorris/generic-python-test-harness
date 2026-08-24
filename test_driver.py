#!/usr/bin/python3

"""
Extend this class as a general purpose test driver.
A test driver keeps a list of all tests.
"""

import sys
import re
from abc import ABC
from datetime import datetime
from functools import reduce
from operator import and_

from result_writer import ResultWriter
from test import Test


class TestDriver(ABC):


    def __init__(self, report_file: str, tests_type: str):
        self._report_file = report_file
        self._tests_type = tests_type
        self._test_status = True
        self._result_writer = ResultWriter(report_file, log_to_syslog=True)
        self._tests = []


    def run(self) -> bool:
        self._start_time = datetime.now()
        results = [test() for test in self._tests]
        self._end_time = datetime.now()
        self._test_status = reduce(and_, [result for result in results])
        self._num_tests = sum(len(tests) for tests in self._tests)
        self._tests.clear()
        return self._test_status


    def __len__(self) -> int:
        return sum(len(test) for test in self._tests)


    def __getitem__(self, position) -> Test:
        return self._tests[position]


    def add_test(self, test_description: str, setup: callable, 
                 teardown: callable, test_cases: list, multi_result_test: bool=False) -> None:
        self._tests.append(
                               Test(
                                    test_description, 
                                    self._result_writer,
                                    setup,
                                    teardown, 
                                    test_cases, 
                                    multi_result_test)
                          )
        return None
