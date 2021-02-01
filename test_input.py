import config
import helper
import unittest
import unittest.mock as mock
from decimal import Decimal


class TestInput(unittest.TestCase):
    # Input Test Case
    def test_input(self):
        # Command : Login
        # - Able to get COMMAND and 1 ARGUMENT correctly
        expected_result = (True, mock.ANY, {config.cmd_key: 'login', config.arg1_key: 'Alice'})
        self.assertEqual(helper.process_input('login Alice'), expected_result)

        # - Able to get COMMAND and 1 ARGUMENT correctly for name with space in between them
        expected_result = (True, mock.ANY, {config.cmd_key: 'login', config.arg1_key: 'Muhammad Bin Ali'})
        self.assertEqual(helper.process_input('login Muhammad Bin Ali'), expected_result)

        # - Able to get COMMAND and 1 ARGUMENT correctly with excess white space in between it
        expected_result = (True, mock.ANY, {config.cmd_key: 'login', config.arg1_key: 'Muhammad Bin Ali'})
        self.assertEqual(helper.process_input('   login   Muhammad   Bin   Ali   '), expected_result)

        # - Return error messsage if there's numeric in name
        expected_result = (False, config.err_msg_login_contains_non_alpha, mock.ANY)
        self.assertEqual(helper.process_input('login Alice1'), expected_result)

        # - Return error messsage if there's special character in name
        expected_result = (False, config.err_msg_login_contains_non_alpha, mock.ANY)
        self.assertEqual(helper.process_input('login Alice!'), expected_result)

        # Command: Topup
        # - Able to get COMMAND and 1 ARGUMENT correctly
        expected_result = (True, mock.ANY, {config.cmd_key: 'topup', config.arg1_key: Decimal(100 * 100)})
        self.assertEqual(helper.process_input('topup 100'), expected_result)

        # - Able to get COMMAND and 1 ARGUMENT correctly when there's decimal involve (up to 2 decimal place)
        expected_result = (True, mock.ANY, {config.cmd_key: 'topup', config.arg1_key: Decimal(0.99 * 100)})
        self.assertEqual(helper.process_input('topup 0.99'), expected_result)

        # - Able to get COMMAND and 1 ARGUMENT correctly with excess white space in between it
        expected_result = (True, mock.ANY, {config.cmd_key: 'topup', config.arg1_key: Decimal(100 * 100)})
        self.assertEqual(helper.process_input('   topup    100   '), expected_result)

        # - Return error message when input 3-decimal or above
        expected_result = (False, config.err_msg_top_up_more_than_two_decimal, mock.ANY)
        self.assertEqual(validate_amount('topup 0.999'), expected_result)

        # - Return error message when input non-numeric
        expected_result = (False, config.err_msg_top_up_non_digit_amount, mock.ANY)
        self.assertEqual(helper.process_input('topup A'), expected_result)

        # - Return error message when input special character
        expected_result = (False, config.err_msg_top_up_non_digit_amount, mock.ANY)
        self.assertEqual(helper.process_input('topup !'), expected_result)

        # - Return error message when input too many argument (it could be valid or invalid argument)
        expected_result = (False, config.err_msg_general_too_many_argument, mock.ANY)
        self.assertEqual(helper.process_input('topup 1 !'), expected_result)

        # Command : Pay
        # - Able to get COMMAND and 2 ARGUMENT correctly
        expected_result = (True, mock.ANY, {config.cmd_key: 'pay', config.arg1_key: 'Alice',
                                            config.arg2_key: Decimal(100 * 100)})
        self.assertEqual(helper.process_input('pay Alice 100'), expected_result)

        # - Able to get COMMAND and 2 ARGUMENT correctly for name with space in between them
        expected_result = (True, mock.ANY, {config.cmd_key: 'pay', config.arg1_key: 'Muhammad Bin Ali',
                                            config.arg2_key: Decimal(100 * 100)})
        self.assertEqual(helper.process_input('pay Muhammad Bin Ali 100'), expected_result)

        # - Able to get COMMAND and 2 ARGUMENT correctly with excess white space in between it
        expected_result = (True, mock.ANY, {config.cmd_key: 'pay', config.arg1_key: 'Muhammad Bin Ali',
                                            config.arg2_key: Decimal(100 * 100)})
        self.assertEqual(helper.process_input('  pay   Muhammad   Bin   Ali   100   '), expected_result)

        # - Return error messsage if there's numeric in name
        expected_result = (False, config.err_msg_login_contains_non_alpha, mock.ANY)
        self.assertEqual(helper.process_input('pay Alice1 100'), expected_result)

        # - Return error messsage if there's special character in name
        expected_result = (False, config.err_msg_login_contains_non_alpha, mock.ANY)
        self.assertEqual(helper.process_input('login Alice! 100'), expected_result)

        # - Return error message when input 3-decimal or above
        expected_result = (False, config.err_msg_top_up_more_than_two_decimal, mock.ANY)
        self.assertEqual(validate_amount('pay Alice 0.999'), expected_result)

        # - Return error message when input alphabet for amount
        expected_result = (False, config.err_msg_pay_no_amount_arg, mock.ANY)
        self.assertEqual(validate_amount('pay Alice A'), expected_result)

        # - Return error message when input special character value for amount
        expected_result = (False, config.err_msg_top_up_non_digit_amount, mock.ANY)
        self.assertEqual(validate_amount('pay Alice !'), expected_result)


def validate_amount(command):
    status, msg, payload = helper.process_input(command)

    if not status:
        return status, msg, payload

    return helper.validate_amount(payload[config.arg1_key])
