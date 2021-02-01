import config
import unittest
import test_input
from helper import init_test_db


if __name__ == '__main__':
    suiteList = []

    if config.test_input:
        suiteList.append(unittest.TestLoader().loadTestsFromTestCase(test_input.TestInput))

    status = False

    # Initialize Test DB
    if config.test_login or config.test_topup or config.test_pay:
        status, msg = init_test_db()

    if not status:
        print('Error: {}'.format(msg))

    comboSuite = unittest.TestSuite(suiteList)
    unittest.TextTestRunner(verbosity=2).run(comboSuite)
