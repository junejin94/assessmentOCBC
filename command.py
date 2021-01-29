import config
import display
import helper
import dbhelper as db


def process_command(raw_input):
    text = ''
    status, msg, user_input = helper.process_input(raw_input)

    if status:
        command = user_input.get(config.cmd_key)
        arg1 = user_input.get(config.arg1_key)
        arg2 = user_input.get(config.arg2_key)

        if command == config.login:
            status, msg, payload = process_login(arg1)

            if status:
                config.client_pending_bal = 0
                status, msg, text = display.login_info(payload)
        elif command == config.topup:
            status = helper.check_has_login()

            if not status:
                msg = config.err_msg_general_has_not_login
            else:
                status, msg, payload, has_debt = process_topup(arg1)

                if status:
                    if has_debt:
                        status, msg, text = display.post_top_up_with_debt_left_info(payload)
                    else:
                        status, msg, text = display.top_up_info(payload)
        elif command == config.pay:
            status = helper.check_has_login()

            if not status:
                msg = config.err_msg_general_has_not_login
            else:
                status, msg, payload = process_pay(arg1, arg2)

                if status:
                    status, msg, text = display.post_pay_info(payload)
        else:
            status = False
            msg = config.err_msg_cmd_invalid_cmd

    print(msg if not status else text)

    get_input()


def process_login(name):
    if config.client == name:
        msg = config.msg_already_login_msg
        return False, msg, ''

    status, msg, payload = helper.get_client_info(name)

    if not status:
        return False, msg, payload

    bal = payload[config.bal_key]
    credit_debt = payload[config.credit_debt_key]
    payload = {config.bal_key: bal, config.credit_debt_key: credit_debt}

    return True, msg, payload


def process_topup(amount):
    has_debt = False
    config.client_pending_bal = amount
    status, msg, payload = db.get_debt(config.client)

    if not status:
        return False, msg, payload

    debt = payload

    if debt:
        status, msg, payload = helper.repay_debt_with_top_up(debt)

        if not status:
            return status, msg, payload

        has_debt = config.client_pending_bal == 0

        if not has_debt:
            status, msg, payload = helper.top_up()

            if status:
                config.client_pending_bal = 0
    else:
        status, msg, payload = helper.top_up()

        if status:
            config.client_pending_bal = 0

    return status, msg, payload, has_debt


def process_pay(name, amount):
    target_is_self = config.client == name

    if target_is_self:
        msg = config.err_msg_pay_cannot_pay_to_self
        return False, msg, ''

    status, msg, exist = db.check_existing_client(name)

    if not status or not exist:
        msg = config.err_msg_pay_target_not_exist
        return False, msg, ''

    status, msg, payload = helper.pay(name, amount)

    return status, msg, payload


def get_input():
    raw_input = input("Command : ")
    process_command(raw_input)
