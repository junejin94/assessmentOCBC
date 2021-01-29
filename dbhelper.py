import config
from sqlite3 import connect, Error, Row


def init():
    status, msg = connect_db()

    if not status:
        return status, msg

    status, msg = check_db()

    if not status:
        return status, msg

    return True, msg


def connect_db():
    msg = ''
    status = False

    try:
        config.conn = connect(config.db_path)
        config.conn.row_factory = Row
    except Error as db_error:
        msg = config.err_msg_db_conn_fail.format(db_error)
    else:
        config.curs = config.conn.cursor() if config.conn else None
        status = config.curs

    return status, msg


def check_db():
    msg = ''
    status = False

    if config.curs is None:
        msg = config.err_msg_db_conn_fail
    else:
        try:
            config.curs.execute('SELECT name FROM sqlite_master WHERE type = \'table\' AND name = \'user\'')
        except Error as db_error:
            msg = config.err_msg_db_verify_fail.format(db_error)
        finally:
            status = True if config.curs.fetchall() else create_table()

    return status, msg


def create_table():
    status = False

    try:
        config.curs.execute('CREATE TABLE IF NOT EXISTS user (name text NOT NULL PRIMARY KEY, '
                            'balance INTEGER NOT NULL)')
        config.curs.execute('CREATE TABLE IF NOT EXISTS debt (creditor text NOT NULL, '
                            'debtor INTEGER NOT NULL, amount INTEGER NOT NULL)')
        config.conn.commit()
    except Error as db_error:
        msg = config.err_msg_db_create_table_fail.format(db_error)
    else:
        status, msg = verify_table()

    return status, msg


def verify_table():
    msg = ''
    status = False

    try:
        config.curs.execute('SELECT name FROM sqlite_master WHERE type = \'table\' AND name = \'user\'')
    except Error as db_error:
        msg = config.err_msg_db_verify_fail.format(db_error)
    else:
        status = config.curs.fetchall()

    return status, msg


def check_existing_client(name):
    msg = ''
    status = False
    payload = ''

    try:
        config.curs.execute('SELECT COUNT(*) FROM user WHERE name = ? LIMIT 1', (name,))
    except Error as db_error:
        msg = config.err_msg_db_bal_fail.format(db_error)
    else:
        data = config.curs.fetchone()

        if data:
            try:
                payload = data['COUNT(*)']
            except IndexError:
                msg = config.err_msg_db_verify_client_fail.format(IndexError)
            else:
                status = True

    return status, msg, payload


def get_balance(name):
    msg = ''
    status = False
    payload = ''

    try:
        config.curs.execute('SELECT balance FROM user WHERE name = ? LIMIT 1', (name,))
    except Error as db_error:
        msg = config.err_msg_db_bal_fail.format(db_error)
    else:
        data = config.curs.fetchone()

        if data:
            try:
                payload = data['balance']
            except IndexError:
                msg = config.err_msg_db_verify_client_fail.format(IndexError)
            else:
                status = True
        else:
            msg = config.err_msg_db_verify_client_fail.format(config.err_msg_db_empty_data)

    return status, msg, payload


def get_credit_debt(name):
    status = False
    msg = ''
    payload = []

    try:
        config.curs.execute('SELECT creditor, debtor, amount FROM debt WHERE debtor = ? OR creditor = ?', (name, name))
    except Error as db_error:
        msg = config.err_msg_db_bal_fail.format(db_error)
    else:
        data = config.curs.fetchall()

        if data is not None:
            status = True
            payload = data
        else:
            msg = config.err_msg_db_verify_client_fail.format(config.err_msg_db_empty_data)

    return status, msg, payload


def get_credit_debt_between_two(name1, name2):
    status = False
    msg = ''
    payload = []

    try:
        config.curs.execute('SELECT creditor, debtor, amount FROM debt WHERE (debtor = ? AND creditor = ?)'
                            ' OR (creditor = ? AND debtor = ?)', (name1, name2, name1, name2))
    except Error as db_error:
        msg = config.err_msg_db_bal_fail.format(db_error)
    else:
        status = True
        payload = config.curs.fetchone()

    return status, msg, payload


def get_debt(name):
    status = False
    msg = ''
    payload = []

    try:
        config.curs.execute('SELECT creditor, amount FROM debt WHERE debtor = ?', (name,))
    except Error as db_error:
        msg = config.err_msg_db_bal_fail.format(db_error)
    else:
        data = config.curs.fetchall()

        if data is not None:
            status = True
            payload = data
        else:
            msg = config.err_msg_db_verify_client_fail.format(config.err_msg_db_empty_data)

    return status, msg, payload


def top_up(name, amount):
    status = False
    msg = ''

    try:
        config.curs.execute('UPDATE user SET balance = balance + ? WHERE name = ?', (int(amount), name))
        config.conn.commit()
    except Error as db_error:
        msg = config.err_msg_db_top_up_failed.format(db_error)
    else:
        status = True

    return status, msg


def update_credit_debt(creditor, debtor, amount, is_clear):
    status = False
    msg = ''

    try:
        if is_clear:
            config.curs.execute('DELETE FROM debt WHERE creditor = ? AND debtor = ?', (creditor, debtor))
        else:
            config.curs.execute('UPDATE debt SET amount = ? WHERE creditor = ? AND debtor = ?', (int(amount), creditor,
                                                                                                 debtor))

        config.conn.commit()
    except Error as db_error:
        msg = config.err_msg_db_update_credit_debt_fail.format(db_error)
    else:
        status = True

    return status, msg


def update_balance(name, amount):
    status = False
    msg = ''

    try:
        config.curs.execute('UPDATE user SET balance = ? WHERE name = ?', (int(amount), name))
        config.conn.commit()
    except Error as db_error:
        msg = config.err_msg_db_update_balance_fail.format(db_error)
    else:
        status = True

    return status, msg


def update_pay_balance(name1, name2, amount):
    status = False
    msg = ''

    try:
        config.curs.execute('UPDATE user SET balance = balance - ? WHERE name = ?;', (int(amount), name1))
        config.curs.execute('UPDATE user SET balance = balance + ? WHERE name = ?', (int(amount), name2))
        config.conn.commit()
    except Error as db_error:
        msg = config.err_msg_db_update_balance_fail.format(db_error)
    else:
        status = True

    return status, msg


def insert_client(name):
    msg = ''
    status = False

    try:
        config.curs.execute('INSERT INTO user (\'name\', \'balance\') VALUES (?,0)', (name,))
        config.conn.commit()
    except Error as db_error:
        msg = config.err_msg_db_insert_client_fail.format(db_error)
    else:
        status = True

    return status, msg


def insert_debt(creditor, debtor, amount):
    msg = ''
    status = False

    try:
        config.curs.execute('INSERT INTO debt (creditor, debtor, amount) VALUES (?, ?, ?)', (creditor, debtor,
                                                                                             int(amount)))
        config.curs.execute('UPDATE user SET balance = 0 WHERE name = ?', (debtor,))
        config.conn.commit()
    except Error as db_error:
        msg = config.err_msg_db_insert_client_fail.format(db_error)
    else:
        status = True

    return status, msg


def delete_debt(creditor, debtor):
    msg = ''
    status = False

    try:
        config.curs.execute('DELETE FROM debt WHERE creditor = ? AND debtor = ?', (creditor, debtor))
        config.conn.commit()
    except Error as db_error:
        msg = config.err_msg_db_insert_client_fail.format(db_error)
    else:
        status = True

    return status, msg


def restructure_debt(creditor, debtor, amount):
    msg = ''
    status = False

    try:
        config.curs.execute('DELETE FROM debt WHERE creditor = ? AND debtor = ?', (debtor, creditor))
        config.curs.execute('INSERT INTO debt (creditor, debtor, amount) VALUES (?, ?, ?)', (creditor, debtor,
                                                                                             int(amount)))
        config.curs.execute('UPDATE user SET balance = 0 WHERE name = ?', (creditor,))
        config.conn.commit()
    except Error as db_error:
        msg = config.err_msg_pay_restructure_debt.format(db_error)
    else:
        status = True

    return status, msg
