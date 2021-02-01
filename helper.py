import config
import dbhelper as db
from decimal import Decimal


def connect_to_db():
    status, msg = db.init()

    if not status:
        print(msg)

    status = True

    return status, msg


def process_input(raw_input):
    status = False
    payload = ''

    try:
        user_input = raw_input.strip().split()
    except Exception as error:
        msg = config.err_msg_cmd_invalid_cmd_with_err.format(str(error))
    else:
        status, msg, command = get_command(user_input)

        if not status:
            return False, msg, payload

        if command == config.login:
            status, msg, argument1 = get_login_name(user_input)

            if not status:
                return status, msg, argument1
            else:
                status = True
                payload = {config.cmd_key: command, config.arg1_key: argument1}
        elif command == config.topup:
            status, msg, argument1 = get_top_up_amount(user_input)

            if not status:
                return status, msg, argument1
            else:
                status = True
                payload = {config.cmd_key: command, config.arg1_key: argument1}
        elif command == config.pay:
            status, msg, argument1, argument2 = get_pay_name_amount(user_input)

            if not status:
                return status, msg, payload
            else:
                status = True
                payload = {config.cmd_key: command, config.arg1_key: argument1, config.arg2_key: argument2}
        else:
            status = False
            msg = config.err_msg_cmd_invalid_cmd

    return status, msg, payload


def get_argument_at_position(user_input, index):
    status = False
    msg = ''
    arg = ''

    try:
        arg = user_input[index]
    except IndexError:
        msg = config.err_msg_cmd_invalid_or_missing_arg
    else:
        status = True

    return status, msg, arg


def get_command(user_input):
    status = False
    msg = ''
    payload = ''

    try:
        payload = user_input[0]
    except IndexError:
        msg = config.err_msg_cmd_invalid_cmd
    else:
        status = True

    return status, msg, payload


def get_login_name(data):
    status = True
    msg = ''
    payload = ''
    raw_data = data[1:]

    for raw_arg in raw_data:
        if raw_arg.isalpha():
            payload += raw_arg + (' ' if len(raw_data) > 1 else '')
        else:
            msg = config.err_msg_login_contains_non_alpha
            return False, msg, payload

    if len(raw_data) > 1:
        payload = payload[:-1]

    return status, msg, payload


def get_top_up_amount(data):
    if len(data) > 2:
        msg = config.err_msg_general_too_many_argument
        return False, msg, data

    status, msg, argument = get_argument_at_position(data, 1)

    if not status:
        return False, msg, argument
    else:
        status, msg, argument = validate_amount(argument)

    return status, msg, argument


def get_pay_name_amount(data):
    argument1 = ''
    argument2 = 0
    raw_data = data[1:]

    status, msg, payload = get_argument_at_position(data, 1)

    if not status:
        return False, msg, argument1, argument2
    elif not payload.isalpha():
        msg = config.err_msg_login_contains_non_alpha
        return False, msg, argument1, argument2

    name_argument = []
    amount_argument = []

    for idx, val in enumerate(raw_data):
        if not val.isalpha():
            name_argument = raw_data[:idx]
            amount_argument = raw_data[idx:]

    if not len(amount_argument):
        msg = config.err_msg_pay_no_amount_arg
        return False, msg, argument1, argument2

    if not len(name_argument):
        msg = config.err_msg_pay_no_name_arg
        return False, msg, argument1, argument2

    if len(amount_argument) > 1:
        msg = config.err_msg_general_too_many_argument
        return False, msg, argument1, argument2

    status, msg, payload = validate_amount(amount_argument[0])

    if not status:
        return status, msg, argument1, argument2
    else:
        argument2 = payload

        for raw_argument in name_argument:
            argument1 += raw_argument + (' ' if len(name_argument) > 1 else '')

    if len(name_argument) > 1:
        argument1 = argument1[:-1]

    return status, msg, argument1, argument2


def get_client_info(name):
    status, msg, payload = db.check_existing_client(name)

    if not status:
        return False, msg, payload

    existing_client = payload

    if not existing_client:
        status, msg = db.insert_client(name)

    if not status:
        return False, msg, payload

    status, msg, payload = db.get_balance(name)

    if not status:
        return False, msg, payload

    bal = payload

    status, msg, payload = db.get_credit_debt(name)

    if not status:
        return False, msg, payload

    credit_debt = payload

    status = True
    payload = {config.bal_key: bal, config.credit_debt_key: credit_debt}
    config.client = name

    return status, msg, payload


def top_up():
    status, msg = db.top_up(config.client, config.client_pending_bal)

    if not status:
        return False, msg, ''

    status, msg, payload = db.get_balance(config.client)

    if not status:
        return False, msg, payload

    status = True
    payload = {config.bal_key: payload}

    return status, msg, payload


def pay(name, amount):
    status, msg, client_bal = db.get_balance(config.client)

    if not status:
        return False, msg, ''

    status, msg, credit_debt = db.get_credit_debt_between_two(config.client, name)

    if not status:
        return False, msg, ''

    if credit_debt:
        status, msg, payload = process_pay_credit_debt(client_bal, credit_debt, amount)
    elif client_bal == 0:
        status, msg = db.insert_debt(name, config.client, amount)

        if not status:
            return False, msg, ''

        status, msg, credit_debt = db.get_credit_debt(config.client)

        if not status:
            return False, msg, ''

        payload = {config.bal_key: 0, config.credit_debt_key: credit_debt}
    else:
        status, msg = db.update_pay_balance(config.client, name, amount)

        if not status:
            return False, msg, ''
        else:
            status, msg, bal = db.get_balance(config.client)

            if not status:
                return False, msg, ''
            else:
                payload = {config.bal_key: bal}

    return status, msg, payload


def repay_debt_with_top_up(debt):
    msg = ''

    for data in debt:
        creditor = data['creditor']
        amount = data['amount']

        if config.client_pending_bal <= amount:
            remainder = amount - config.client_pending_bal
            is_clear = remainder == 0
            status, msg = db.update_credit_debt(creditor, config.client, remainder, is_clear)
            config.client_pending_bal = 0

            if not status:
                return False, msg, ''

            return db.get_credit_debt(config.client)
        else:
            status, msg = db.delete_debt(creditor, config.client)

            if not status:
                return status, msg, ''

            config.client_pending_bal -= amount

    return True, msg, ''


def process_pay_credit_debt(client_bal, credit_debt, amount):
    creditor = credit_debt[config.creditor_key]
    debtor = credit_debt[config.debtor_key]
    debt_amount = credit_debt[config.amount_key]

    new_bal = 0 if client_bal - amount < 0 else client_bal - amount

    is_client_debtor = config.client == debtor

    updated_bal = debt_amount + amount if is_client_debtor else debt_amount - amount

    is_clear = debt_amount - amount == 0
    is_debtor_now_creditor = updated_bal < 0

    if is_debtor_now_creditor:
        status, msg, target_bal = db.get_balance(creditor)

        if not status:
            return False, msg, ''
        else:
            status, msg = db.restructure_debt(debtor, creditor, updated_bal * -1)

            if not status:
                return False, msg, ''
    else:
        status, msg = db.update_credit_debt(creditor, debtor, updated_bal, is_clear)

        if not status:
            return False, msg, ''

    status, msg = db.update_balance(config.client, new_bal)

    if not status:
        return False, msg, ''

    status, msg, bal = db.get_balance(config.client)

    if not status:
        return False, msg, ''

    status, msg, credit_debt = db.get_credit_debt(config.client)

    if not status:
        return False, msg, ''

    payload = {config.bal_key: bal, config.credit_debt_key: credit_debt}

    return status, msg, payload


def validate_amount(raw):
    status = False
    msg = ''
    amount = 0

    try:
        amount = float(raw)
    except ValueError:
        msg = config.err_msg_top_up_non_digit_amount
    else:
        status = True

    if not status:
        return False, msg, amount

    amount = Decimal(amount * 100)
    only_two_decimal = amount % 1 == 0

    if not only_two_decimal:
        status = False
        msg = config.err_msg_top_up_more_than_two_decimal
    else:
        status = True

    return status, msg, amount


def check_has_login():
    return config.client is not None


def format_amount(amount):
    return '0' if amount <= 0 else str(amount / 100).rstrip('0').rstrip('.')
