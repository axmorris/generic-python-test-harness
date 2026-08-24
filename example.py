#!/usr/bin/python3

from test_case import TestCase
from test_driver import TestDriver


class ExampleDriver(TestDriver):
    pass


def setup():
    return True


def teardown():
    return True


def test_one():
    return True


def test_two():
    return 2 + 2 == 4


if __name__ == "__main__":
    driver = ExampleDriver("results.jsonl", "example")
    driver.add_test(
        "basic example",
        setup,
        teardown,
        [
            TestCase(test_one, "test_one"),
            TestCase(test_two, "test_two"),
        ],
    )

    ok = driver.run()
    print("PASS" if ok else "FAIL")
