#!/usr/bin/python3

"""
Single self-contained "test" (exercises some unit)
A TestCase runs a specified test function and returns a TestResult tuple
    (most likely to a Test object)
The function called should return only the boolean result of the test.
"""

import sys
import syslog

from collections import namedtuple
from datetime import datetime

TestResult = namedtuple('TestResult', ['description', 'duration', 'success'])


class TestCase:


    def __init__(self, func: callable, test_description: str):
        self._func = func
        self._test_description = test_description
        self._start_time = 0
        self._end_time = 0
        self._success = False


    def __repr__(self):
        return 'Test: %r, Function: %r' % (self._test_description, self._func)


    def report(self, verbose: bool) -> str:
        '''
        Print stats of the test run.
        '''
        duration = self._end_time - self._start_time
        report = 'Test: %s | Duration: %r, Success: %r' % (self._test_description, duration, self._success)
        if verbose:
            print(report)
        return report


    def __call__(self, multi_part_result:bool=False) -> TestResult:
        syslog.syslog(syslog.LOG_INFO, ("Running test: ({})").format(self._test_description))
        self._start_time = datetime.now()
        '''
        multi_part_result assumes that the function (self._func) that got called
            is going to return a dict with descriptions and results
        This is for test scripts that test multiple things so that each test
            can be reported on individually even though it was run from the same test_driver call.
        '''
        if multi_part_result:
            success, results = self._func()
            self._end_time = datetime.now()
            self._success = success
            duration = self._end_time - self._start_time
            test_results = []
            for result in results:
                if result.duration != None:
                    test_results.append(TestResult(result.description, result.duration, result.success))
                else:
                    # use the duration for the overall test if none provided
                    test_results.append(TestResult(result.description, duration, result.success))
        else:
            self._success = bool(self._func())
            self._end_time = datetime.now()
            duration = self._end_time - self._start_time
            test_results = [TestResult(self._test_description, duration, self._success)]
        return test_results