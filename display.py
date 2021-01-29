import config
import helper


def login_info(data):
    bal = data[config.bal_key]
    credit_debt = data[config.credit_debt_key]

    status = False
    msg = ''
    string = config.msg_welcome_msg.format(config.client, helper.format_amount(bal))

    if credit_debt:
        string += '\n'

        for data in credit_debt:
            creditor = data[config.creditor_key]
            debtor = data[config.debtor_key]
            amount = data[config.amount_key]

            if not creditor and not debtor and not amount:
                msg = config.err_msg_credit_debt_extract_fail
            else:
                status = True
                formatted_amount = helper.format_amount(amount)

                if config.client == debtor:
                    string += config.msg_owe_money_msg.format(formatted_amount, 'to', creditor)
                elif config.client == creditor:
                    string += config.msg_owe_money_msg.format(formatted_amount, 'from', debtor)

        string = string[:-3]
    else:
        status = True

    return status, msg, string


def top_up_info(data):
    status = False
    msg = ''
    payload = ''

    bal = data[config.bal_key]

    if not bal:
        msg = config.err_msg_top_up_extract_fail
    else:
        status = True
        payload = config.msg_top_up_sucessful_msg.format(helper.format_amount(bal))

    return status, msg, payload


def post_top_up_with_debt_left_info(credit_debt):
    status = False
    msg = ''
    string = config.msg_top_up_debt_paid_msg

    for data in credit_debt:
        creditor = data[config.creditor_key]
        debtor = data[config.debtor_key]
        amount = data[config.amount_key]

        if not creditor and not debtor and not amount:
            msg = config.err_msg_credit_debt_extract_fail
        else:
            status = True
            formatted_amount = helper.format_amount(amount)

            if config.client == debtor:
                string += config.msg_owe_money_msg.format(formatted_amount, 'to', creditor)
            elif config.client == creditor:
                string += config.msg_owe_money_msg.format(formatted_amount, 'from', debtor)

    return status, msg, string[:-3]


def post_pay_info(data):
    bal = data[config.bal_key]
    credit_debt = data[config.credit_debt_key]

    status = False
    msg = ''
    string = config.msg_pay_successful_msg.format(helper.format_amount(bal))

    if credit_debt:
        string += '\n'

        for data in credit_debt:
            creditor = data[config.creditor_key]
            debtor = data[config.debtor_key]
            amount = data[config.amount_key]

            if not creditor and not debtor and not amount:
                msg = config.err_msg_credit_debt_extract_fail
            else:
                status = True
                formatted_amount = helper.format_amount(amount)

                if config.client == debtor:
                    string += config.msg_owe_money_msg.format(formatted_amount, 'to', creditor)
                elif config.client == creditor:
                    string += config.msg_owe_money_msg.format(formatted_amount, 'from', debtor)
    else:
        status = True

    return status, msg, string[:-3]
