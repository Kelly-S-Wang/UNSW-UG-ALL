from backend import *
import os, shutil
from email_runner import send_email
from secrets import token_urlsafe

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, MetaData, Float, and_, or_
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

import datetime

# setup db
engine = create_engine("sqlite:///budget.db?check_same_thread=False")
metadata = MetaData()

Session = sessionmaker(bind=engine)
session = Session()


'''
given a list of objects, return a list of that object
used to prevent seeing object return in bash
'''
def loop_append(results):
    to_return = []
    for result in results:
        to_return.append(result)
    return to_return


# get all data given a table name and column
def get_all_given(table, column):
    query_text = "SELECT {} FROM {}".format(column, table)
    results = session.execute(query_text)
    return loop_append(results)


# get specific data given a table name, column, parameter and key
# use * to get all data
# separate column with , if you are taking multiple columns
def get_where(table, column, parameter):
    query_text = "SELECT {} FROM {} WHERE {}".format(column, table, parameter)
    results = session.execute(query_text)
    return loop_append(results)


# get data in ascending / descending order ASC|DESC
def get_ordered_where(table, column, parameter1, parameter2, order):
    query_text = "SELECT {} FROM {} WHERE {} ORDER BY {} {}".format(column, table, parameter1, parameter2, order)
    results = session.execute(query_text)
    return loop_append(results)


# get data in ascending / descending order ASC|DESC
def get_ordered(table, column, parameter, order):
    query_text = "SELECT {} FROM {} ORDER BY {} {}".format(column, table, parameter, order)
    results = session.execute(query_text)
    return loop_append(results)


# find object(s) with filter(s) (SQL) but return the object itself with the class
def object_query(obj_type, filter, num="one"):
    res = session.query(obj_type).filter(filter)
    if num == "one":
        return res.first()
    else:
        return res.all()


# find a list of objects using the filter(s) and return it in sorted order
def object_query_sorted(obj_type, filter, sort_type):
    res = session.query(obj_type).filter(filter).order_by(sort_type)
    return res.all()


# used as last option where you need to execute SQL queries directly
def execute_sql_query(query):
    results = session.execute(query)
    return loop_append(results)


# register a new user to the confirmation table and set as not registered in profile table
def register_new_user(username, name, gender, dob, email, password):
    token = token_urlsafe()
    add_new_profile(username, name, gender, dob, email, password, False)
    profile = object_query(Profile, Profile.username == username)
    profile_id = profile.id
    add_new_confirmation(token, profile_id)

    recepient = email
    subject = "Please confirm your registration"
    text_body = """\
    <html>
        <head></head>
        <body>
            <p>Hi {}!<br>
                We are glad to have you around. Just one more step and you will be registered, please click the link the link below<br>
                <a href="http://hdnmages.pythonanywhere.com/confirm={}">Click here</a><br><br>
                If the link above doesn't work, copy this to your web browser
                http://hdnmages.pythonanywhere.com/confirm={}
            </p>
        <body>
    <html>
    """.format(name, token, token)

    send_email(recepient, subject, text_body)


# add a new user profile
def add_new_profile(username, name, gender, dob, email, password, confirmed):
    new_profile = Profile(username, name, gender, dob, email, password, confirmed)
    session.add(new_profile)
    session.commit()
    os.mkdir(os.getcwd() + "/static/users/" + username)
    shutil.copy(os.getcwd() + "/static/profile.jpg", os.getcwd() + "/static/users/" + username)

# add a new confirmation
def add_new_confirmation(token, profile_id):
    new_confirmation = Confirmation(token, profile_id)
    session.add(new_confirmation)
    session.commit()


# add new transaction to database
def add_new_transaction(profile_id, date_time, amount, comment, inc_exp, type):
    new_transaction = Transaction(profile_id, date_time, amount, comment, inc_exp, type)
    session.add(new_transaction)
    session.commit()

# edit existing transaction from database
def edit_existing_transaction(profile_id, transaction_id, date_time, amount, comment, inc_exp, category):

    # get object
    curr_transaction = object_query(Transaction, Transaction.id == transaction_id)

    # sanity check
    if curr_transaction.profile_id == profile_id:
        # make changes
        curr_transaction.set_amount(amount)
        curr_transaction.set_date_time(date_time)
        curr_transaction.set_comment(comment)
        curr_transaction.set_type(category)
        #curr_transaction.set_inc_exp(inc_exp)

        # commit to db
        session.commit()
    else:
        print("error, profile_id does not match")


# edit existing recurring transaction from database
def edit_existing_recurring_transaction(profile_id, recurring_id, start_date_time, end_date_time, recurrence_value, recurrence_type, amount,
                                        comment, inc_exp, type):
    
    # get object
    curr_recurring_transaction = object_query(Recurring_transaction, Recurring_transaction.id == recurring_id)

    # sanity check
    if curr_recurring_transaction.profile_id == profile_id:
        # make changes
        curr_recurring_transaction.set_start_date_time(start_date_time)
        curr_recurring_transaction.set_end_date_time(end_date_time)
        curr_recurring_transaction.set_recurrence_value(recurrence_value)
        curr_recurring_transaction.set_recurrence_type(recurrence_type)
        curr_recurring_transaction.set_amount(amount)
        curr_recurring_transaction.set_comment(comment)
        #curr_recurring_transaction.set_inc_exp(inc_exp)
        curr_recurring_transaction.set_type(type)

        # commit to db
        session.commit()
    else:
        print("error, profile_id does not match")


# delete an existing recurring transaction
def delete_existing_recurring_transaction(recurring_id, profile_id):

    # get object
    recurring_transaction = session.query(Recurring_transaction).filter(Recurring_transaction.id==recurring_id).first()

    # sanity check
    if recurring_transaction.profile_id == profile_id:

        # delete relevant object
        session.delete(recurring_transaction)
        session.commit()
    else:
        print("error, profile_id does not match")


# delete an existing message
def delete_existing_message(message_id, profile_id):

    # get object
    message = session.query(Message).filter(Message.id==message_id).first()

    # sanity check
    if message.profile_id == profile_id:

        # delete relevant object
        session.delete(message)
        session.commit()
    else:
        print("error, profile_id does not match")

# Delete a transaction
def remove_transaction(t_id, p_id):
    
    transaction = session.query(Transaction).filter(Transaction.id == t_id).first()
    #a = transaction.amount
    if transaction.profile_id == p_id:
        session.delete(transaction)
        session.commit()
        
# add new recurring transaction to database
def add_new_recurring_transaction(profile_id, start_date_time, end_date_time, recurrence_value, recurrence_type, amount,
                                  comment, inc_exp, type):
    new_recurring_transaction = Recurring_transaction(profile_id, start_date_time, end_date_time, recurrence_value,
                                                      recurrence_type, amount, comment, inc_exp, type)
    session.add(new_recurring_transaction)
    session.commit()

    return new_recurring_transaction.id


# add new limit to database
def add_new_limit(type, profile, amount, datetime):
    new_limit = Limit(type, profile, amount, datetime)
    session.add(new_limit)
    session.commit()


# add new message to database
def add_new_message(profile_id, recurring_transaction_id, date_time):
    new_message = Message(profile_id, recurring_transaction_id, date_time)
    session.add(new_message)
    session.commit()


# get transaction for a profile
def get_transaction(profile_id, order_inc=False):
    if order_inc:
        query = """SELECT t.id, t.date_time, t.amount, t.comment, t.inc_exp, t.type
		FROM transactions t 
		JOIN profiles p ON p.id = t.profile_id WHERE p.id = {}
		ORDER BY t.inc_exp""".format(profile_id)
    else:
        query = """SELECT t.id, t.date_time, t.amount, t.comment, t.inc_exp, t.type
		FROM transactions t 
		JOIN profiles p ON p.id = t.profile_id WHERE p.id = {}""".format(profile_id)
    results = session.execute(query)
    keys = results.keys()
    values = loop_append(results)
    to_return = []
    for value in values:
        to_return.append(dict(zip(keys, value)))
    return to_return


# returns a tuple containing 2 lists. One income one expense
def get_split_transaction(profile_id):
    query = """SELECT t.id, t.date_time, t.amount, t.comment, t.inc_exp, t.type
	FROM transactions t 
	JOIN profiles p ON p.id = t.profile_id WHERE p.id = {} AND t.inc_exp = 'I'""".format(profile_id)
    results = session.execute(query)
    keys = results.keys()
    values = loop_append(results)
    income = []
    for value in values:
        income.append(dict(zip(keys, value)))

    query1 = """SELECT t.id, t.date_time, t.amount, t.comment, t.inc_exp, t.type
	FROM transactions t 
	JOIN profiles p ON p.id = t.profile_id WHERE p.id = {} AND t.inc_exp = 'E'""".format(profile_id)
    results1 = session.execute(query1)
    keys1 = results.keys()
    values1 = loop_append(results1)
    expense = []
    for value1 in values1:
        expense.append(dict(zip(keys1, value1)))
    return (income, expense)


# get recurring transaction for a profile
def get_recurring_transactions(profile_id):
    query = """SELECT t.id, t.start_date_time, t.end_date_time, t.recurrence_value, t.recurrence_type, t.amount, t.comment, t.inc_exp, t.type
	FROM recurring_transactions t 
	JOIN profiles p ON p.id = t.profile_id WHERE p.id = {}""".format(profile_id)
    results = session.execute(query)
    keys = results.keys()
    values = loop_append(results)
    to_return = []
    for value in values:
        to_return.append(dict(zip(keys, value)))
    return to_return


# group transactions
# must only be used after get_transaction, or fed something of similar format
def group_transactions(transaction_dict_list):
    dictionary = {}
    for elem in transaction_dict_list:
        if elem["type"] not in dictionary:
            dictionary[elem["type"]] = []
        key = elem["type"]
        elem.pop("type", None)
        dictionary[key].append(elem)
    return dictionary


# a function that acts as a macro to get a grouped transaction based on profile_id
def get_grouped_transactions(profile_id):
    return group_transactions(get_transaction(profile_id))


# a function that acts as a macro to get a grouped recurring transaction based on profile_id
def get_grouped_recurring_transactions(profile_id):
    return group_transactions(get_recurring_transactions(profile_id))

# a function to remove a specific limit from a profile given the transaction type which limit is to be removed
def remove_limit(profile_id, type):
    limit = session.query(Limit).filter(Limit.profile_id==profile_id, Limit.type==type).first()
    try:
        session.delete(limit)
        session.commit()
    except Exception as e:
        print(e)

# delete all relevant entries from entire database given a profile_id
def delete_profile_and_details(profile_id):
    transactions = session.query(Transaction).filter(Transaction.profile_id==profile_id).all()
    messages = session.query(Message).filter(Message.profile_id==profile_id).all()
    recurring_transactions = session.query(Recurring_transaction).filter(Recurring_transaction.profile_id==profile_id).all()
    limits = session.query(Limit).filter(Limit.profile_id==profile_id).all()
    confirmations = session.query(Confirmation).filter(Confirmation.profile_id==profile_id).all()
    profiles = session.query(Profile).filter(Profile.id==profile_id).all()

    object_list = []
    object_list.append(transactions)
    object_list.append(messages)
    object_list.append(recurring_transactions)
    object_list.append(limits)
    object_list.append(confirmations)
    object_list.append(profiles)

    for obj in object_list:
        for item in obj:
            try:
                session.delete(item)
            except Exception as e:
                print(e)

    session.commit()


# find all total spendings that are over limi
# used for demonstration purpose only
# BUGGED: new field added to limits, need to readjust
def find_spendings_over_limit():
    to_return = []
    count_query = "SELECT COUNT(id) FROM profiles"
    result = execute_sql_query(count_query)
    profile_count = result[0][0]
    for i in range(1, profile_count + 1):
        query = "SELECT t.type, SUM(t.amount) FROM transactions t JOIN profiles p ON t.profile_id = p.id JOIN limits l ON p.id = l.profile_id WHERE p.id = {} GROUP BY t.type".format(
            i)
        type_amount = execute_sql_query(query)
        print("for user {}".format(str(i)))
        type_amount_dict = dict(type_amount)
        queryii = "SELECT type, amount FROM limits WHERE profile_id = {}".format(i)
        limit_amount = execute_sql_query(queryii)
        limit_amount_dict = dict(limit_amount)
        keys = limit_amount_dict.keys()
        for key in keys:
            spending = type_amount_dict.get(key)
            if spending is not None:
                limit = limit_amount_dict.get(key)
                if spending > limit:
                    tup = (i, spending, limit, key)
                    to_return.append(tup)
    return to_return


# given a profile_id, try to find if there is any recurring transaction that falls today
# meant to be run through the server every midnight of a new day
# returns a list of id of recurring transactions
def check_recurrence(profile_id):
    # get today's date
    today = datetime.datetime.today()

    # get the rules for a user's recurring transactions
    rule_list = object_query(Recurring_transaction, Recurring_transaction.profile_id == profile_id, "all")

    # placeholder list to be returned
    to_return = []

    # loop through all the rules in rule_list
    for rule in rule_list:
        # check if today is within the repeat period
        if today >= rule.start_date_time and today <= rule.end_date_time:
            # if today is, check the recurrence type
            if rule.recurrence_type == 'day':
                to_return.append(rule.id)

            # if the recurrence type is month
            elif rule.recurrence_type == 'week':
                if today.weekday() == rule.start_date_time.weekday():
                    to_return.append(rule.id)

            # if the recurrence type is year
            elif rule.recurrence_type == 'month':
                if today.day == rule.start_date_time.day:
                    to_return.append(rule.id)

    # return a list of the recurring transaction id that fall today
    return to_return
