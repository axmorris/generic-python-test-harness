#!/usr/bin/python3

"""
Single self-contained "test" (excercises some unit)
A Test may contain a list of Test Cases or a list of one Test Case.
These Test Cases are used for variations on some test where parameters may be varied.
"""
import json
import sys
import syslog

from functools import reduce
from operator import and_
from collections import namedtuple

from test_case import TestCase
from result_writer import ResultWriter


TestResult = namedtuple('TestResult', ['description', 'success', 'duration'])


class Test:


    def __init__(self, test_description: str, result_writer: ResultWriter, setup: callable, teardown: callable, test_cases: list, multi_result_test: bool=False):
        self._test_description = test_description
        self._result_writer = result_writer
        self._setup = setup
        self._teardown = teardown
        self._test_cases = test_cases
        self._multi_result_test = multi_result_test
        self._results = []


    def __repr__(self):
        return 'Test: %r, Test Cases: %r' % (self._description, self._test_cases)


    def report(self) -> list:
        '''
        Print results of all test cases run.
        '''
        report = []
        for test in self._results:
            report.append('Test: {} | Duration: {}, Success: {}'.format(
                        test.description, test.duration, test.success))
        print(report)
        return report


    def __len__(self) -> int:
        '''
        returns the length of results if tests complete
            if multipart test
        otherwise, returns the number of test cases
        '''
        if self._multi_result_test and len(self._results):
            return len(self._results)
        return len(self._test_cases)


    def __getitem__(self, position) -> TestCase:
        return self._test_cases[position]


    def __call__(self) -> bool:
        if self._setup is not None:
            rc = 0
            rc = self._setup()
            if not rc:
                print("Setup failed for test: ({})".format(self._test_description))
        if self._multi_result_test:
            '''
            This assumes that there was only one thing that ran (one test script)
                but that it had several things to report on individually
            '''
            for test_case in self._test_cases:
                self._results.extend(test_case(multi_part_result=True))
        else:
            for test_case in self._test_cases:
                self._results.append(test_case()[0])
        self.write()
        if self._teardown is not None:
            rc = 0
            rc = self._teardown()
            if not rc:
                print("Teardown failed for test: ({})".format(self._test_description))
        return reduce(and_, [result.success for result in self._results])


    def write(self):
        '''
        Write all test results for this Test (all test cases) to File.
        '''
        for test in self._results:
            print(test)
            self._result_writer.add_test_entry(test.description, test.success, test.duration)

