from os import getcwd, sep


# Client Information
client = None
client_pending_bal = 0

# Database
conn = None
curs = None

# Commands
pay = 'pay'
login = 'login'
topup = 'topup'

# Path
db_path = getcwd() + sep + 'local.db'

# Message
msg_owe_money_msg = 'Owing {} {} {}.\n'
msg_welcome_msg = 'Hello, {}!\nYour balance is {}.'
msg_top_up_debt_paid_msg = 'Debt has been paid with top-up.\n'
msg_pay_successful_msg = 'Pay successful.\nYour balance is {}.'
msg_already_login_msg = 'You\'re already login to that account'
msg_top_up_sucessful_msg = 'Top-up successful.\nYour balance is {}'
msg_outstanding_debt_msg = 'You must repay all your outstanding debt, and any remainder will be added to balance.\n'

# Error Message
# - General
err_msg_general_too_many_argument = 'You have key in too many arguments.'
err_msg_general_has_not_login = 'You must login prior to using this command.'

# - Command
err_msg_cmd_invalid_cmd = 'Invalid command'
err_msg_cmd_invalid_cmd_with_err = 'Invalid command:\n{}'
err_msg_cmd_invalid_or_missing_arg = 'Invalid or missing argument'

# - Database
err_msg_db_empty_data = 'Empty data was returned'
err_msg_db_top_up_failed = 'Failed to top-up:\n{}'
err_msg_db_bal_fail = 'Failed to retrieve balance:\n{}'
err_msg_db_create_table_fail = 'Failed to create tables:\n{}'
err_msg_db_insert_client_fail = 'Failed to insert client:\n{}'
err_msg_db_update_balance_fail = 'Failed to update balance:\n{}'
err_msg_db_verify_fail = 'Failed to verify content of database:\n{}'
err_msg_db_verify_client_fail = 'Failed to retrieve client\'s data:\n{}'
err_msg_db_conn_fail = 'Failed to establish connection to database:\n{})'
err_msg_db_update_credit_debt_fail = 'Failed to update credit/debt information:\n{}'

# - Login
err_msg_login_no_arg = 'Please key in your name.'
err_msg_login_contains_non_alpha = 'Name must only contain alphabets.'
err_msg_credit_debt_extract_fail = 'Failed to extract credit, and debt information.'

# - Top-up
err_msg_top_up_amount_no_arg = 'Please key in top-up amount.'
err_msg_top_up_non_digit_amount = 'Please key in only numeric only.'
err_msg_top_up_extract_fail = 'Failed to extract top-up information.'
err_msg_top_up_amount_invalid_arg = 'Please key in valid top-up amount.'
err_msg_top_up_get_debt_fail = 'Failed to extract client\'s debt data:\n{}'
err_msg_top_up_more_than_two_decimal = 'Please key in amount up to 2 decimal place only.'

# - Pay

err_msg_pay_cannot_pay_to_self = 'Unable to pay to oneself.'
err_msg_pay_no_amount_arg = 'Please key in the amount you wish to pay'
err_msg_pay_restructure_debt = 'Failed to update debt information:\n{}'
err_msg_pay_target_not_exist = 'The person whom you wish to pay to doesn\'t exist'
err_msg_pay_no_name_arg = 'Please key in the name of the person whom you wish to pay'

# Dictionary Key
cmd_key = 'cmd'
bal_key = 'bal'
name_key = 'name'
arg1_key = 'arg1'
arg2_key = 'arg2'
debtor_key = 'debtor'
amount_key = 'amount'
creditor_key = 'creditor'
credit_debt_key = 'credit_debt'
