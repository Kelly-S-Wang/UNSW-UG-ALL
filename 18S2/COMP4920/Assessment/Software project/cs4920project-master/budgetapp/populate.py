import random
import string
import time
import datetime
import argparse
import os
import shutil
from query_calls import loop_append, add_new_profile, add_new_transaction, get_all_given, add_new_recurring_transaction, add_new_limit, add_new_message, check_recurrence, remove_limit


'''
--- random date generator ---
generates a random date
takes two parameters, floor and ceiling, which are the lowest and highest year that will be generated respectively
returns a string of format "YYYY MM DD"
'''
def random_date(floor, ceiling):
    year = random.choice(range(floor, ceiling))
    month = random.choice(range(1, 12))
    date = random.choice(range(1, 28))

    if len(str(month)) == 1:
        month = '0' + str(month)

    if len(str(date)) == 1:
        date = '0' + str(date)

    to_return = str(year) + " " + str(month) + " " + str(date)
    return to_return


'''
--- random time generator ---
generates a random time
doesn't take any parameters
returns a string of format "HH:MM", 24 hour format
'''
def random_time():
    hour = random.choice(range(0, 23))
    minute = random.choice(range(0, 59))

    if len(str(hour)) == 1:
        hour = '0' + str(hour)

    if len(str(minute)) == 1:
        minute = '0' + str(minute)

    to_return = str(hour) + ":" + str(minute)
    return to_return


'''
--- date time to epoch converter ---
converts a date time string to epoch time
takes two parameters, date string and time string (defaults to 00:00)
returns a floating point numbber of epoch time
'''
def date_time_to_epoch(date, random_time='00:00'):
    date_time = date + " " + random_time
    time_tuple = time.strptime(date_time, '%Y %m %d %H:%M')
    time_epoch = time.mktime(time_tuple)
    return time_epoch


'''
--- string to datetime converter ---
converts a string to datetime object
takes two parameters, date and random time (defaults to 00:00)
returns a datetime object
'''
def string_to_datetime(date, random_time="00:00"):
    date_time = date + " " + random_time
    time_obj = datetime.datetime.strptime(date_time, '%Y %m %d %H:%M')
    return time_obj


'''
--- epoch to date time converter ---
converts an epoch time to date time object
takes one parameter, epoch_time which is the floating point number to convert
returns a datetime object
'''
def convert_epoch_date_time(epoch_time):
    return (time.strftime('%Y %m %d %H:%M', time.localtime(epoch_time)))


'''
--- random money generator ---
generates a random amount of money to fill up the database
doesn't take any parameter
returns a string of format "(dollar).(cents)"
'''
def random_money():
    dollar = random.choice(range(0, 999))
    cents = random.choice(range(0, 99))
    to_return = str(dollar) + '.' + str(cents)
    return to_return


'''
--- random password generator ---
generates a random and sound password
takes two parameters, size (defaults to 10) and chars (defaults to ascii letters and digits)
size determines how long the generated password is
chars acts a pool of characters to choose from for the random generator, should be sound as is
returns a string of length size
'''
def password_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


'''
--- simple password generator ---
!!! use strictly for demo purposes !!!
takes a parameter, i which is the number to append to the end of the password
returns a string of "password{}.format(i)"
'''
def simple_password_generator(i):
    return "password" + str(i)


'''
--- fill profiles ---
creates n_user random profiles
takes a parameter, n_user which is the number of users to generate
doesn't return anything, calls a query to add the profile to the database
'''
def fill_profiles(n_user):
    for i in range(n_user):
        first_name = random.choice(names)
        last_name = random.choice(names)
        name = first_name + " " + last_name

        username = first_name.lower() + last_name.lower() + str(i)

        gender = random.choice(genders)

        dob = random_date(1940, 2000)
        dob = string_to_datetime(dob, "00:00")
        
        email = first_name.lower() + last_name.lower() + random.choice(domains)

        # password = password_generator()
        password = simple_password_generator(i)

        confirmed = True

        add_new_profile(username, name, gender, dob, email, password, confirmed)


'''
--- fill transactions ---
creates n_transaction random transactions
takes two parameters, n_user which is the number of users to choose from, n_transaction which is the numbers of transactions to create
doesn't return anything, calls a query to add the transactions to the database
'''
def fill_transactions(n_user, n_transaction):
    for i in range(n_transaction):
        profile_id = random.choice(range(1, n_user+1))
        date = random_date(2018, 2019)
        time = random_time()
        date_time = string_to_datetime(date, time)
        amount = random_money()
        comment = random.choice(comments)
        type_id = random.choice(range(0, len(transaction_types)))
        type = transaction_types[type_id][0]
        inc_exp = transaction_types[type_id][1]
        add_new_transaction(profile_id, date_time, amount, comment, inc_exp, type)


'''
--- fill recurring transactions ---
creates n_recurring_transaction random recurring transactions
takes two parameters, n_user which is the number of users to choose from, n_recurring_transaction which is the numbers of recurring transactions to create
doesn't return anything, calls a query to add the recurring transactions to the database
'''
def fill_recurring_transactions(n_user, n_recurring_transaction):
    for i in range(n_recurring_transaction):
        profile_id = random.choice(range(n_user))
        start_date = random_date(2014, 2015)
        end_date = random_date(2019, 2020)
        start_time = "00:00"
        end_time = "23:59"
        start_date_time = string_to_datetime(start_date, start_time)
        end_date_time = string_to_datetime(end_date, end_time)
        recurrence_type = random.choice(['day', 'week', 'month'])
        recurrence_value = 1
        # if recurrence_type == 'day':
        #     recurrence_value = random.choice(range(1, 30))
        # elif recurrence_type == 'month':
        #     recurrence_value = random.choice(range(1, 12))
        # else:
        #     recurrence_value = random.choice(range(1, 10))
        amount = random_money()
        comment = random.choice(comments)

        type_id = random.choice(range(0, len(transaction_types)))
        type = transaction_types[type_id][0]
        inc_exp = transaction_types[type_id][1]

        add_new_recurring_transaction(profile_id, start_date_time, end_date_time, recurrence_value, recurrence_type,
                                      amount, comment, inc_exp, type)


'''
--- initialise limits ---
initialises the limits for a given profile_id, set where the amount is 0 and the date set as None
Used to, as the name suggests, initialise the tables so the front end can display it
'''
def initialise_limits(profile_id, transaction_types):
    expenses = [item[0] for item in transaction_types if 'E' in item]
    for category in expenses:
        add_new_limit(category, profile_id, 0, None)


'''
--- fill limits ---
fills n_limit for expenses for first n_user
takes two parameters, n_user which is the number of users to choose from, n_limit which is the number of limit for expenses to generate
doesn't return anything, calls a query to add the limits to the database
'''
def fill_limits(n_user, n_limit):
    for i in range(1, n_user+1):
        profile_id = i
        generated = []
        for j in range(n_limit):
            type_id = random.choice(range(3, len(transaction_types))) # hardcoded to only fill the expenses
            if type_id in generated:
                type_id = random.choice(range(3, len(transaction_types)))
                while type_id in generated:
                    type_id = random.choice(range(3, len(transaction_types)))

            type = transaction_types[type_id][0]
            amount = random_money()
            start_date = random_date(2016, 2018)
            start_time = "00:00"
            start_date_time = string_to_datetime(start_date, start_time)
            generated.append(type_id)

            remove_limit(profile_id, type)
            add_new_limit(type, profile_id, amount, start_date_time)

'''
---  fill messages --- 
fill the messages for each user if there's a recurring transaction that falls today
takes no parameters, doesn't return anything, calls a query to add the messages to the database
'''
def fill_messages():
    today = datetime.datetime.today()
    for i in range(1, n_user+1):
        profile_id = i
        rec = check_recurrence(profile_id)
        if rec:
            for recurring_id in rec:
                add_new_message(profile_id, recurring_id, today)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--feedback", required=False,
                    default=False,
                    help="prints input populating the database if true")
    args = ap.parse_args()
    if os.path.exists(os.getcwd() + "/static/users/"):
        shutil.rmtree(os.getcwd() + "/static/users/")

    os.mkdir(os.getcwd() + "/static/users/")
    # read common names file
    with open('names.txt') as f:
        names = f.read().splitlines()

    # used to assign gender
    genders = ['M', 'F', 'O']

    # list of common email providers
    domains = ['@hotmail.com', '@gmail.com', '@yahoo.com', '@outlook.com']

    # transaction types for database populating
    transaction_types = [('Salary', 'I'), ('Investments', 'I'), ('Other/Income', 'I'), ('Food/Drinks', 'E'), ('Bills', 'E'),
                         ('Electronics', 'E'), ('Entertainment', 'E'),
                         ('Travel', 'E'), ('Debt', 'E'), ('Clothing', 'E'), ('Automobile', 'E'), ('Pets', 'E'),
                         ('Other/Expenses', 'E')]

    # list of test comments
    comments = ['BLAH BLAH', 'hur dur', 'HELLO WORLD', 'loss', 'what', 'am', 'i', 'even', 'doing', 'with', 'my', 'life',
                'compsci ftw', 'this project rocks', 'jk',
                'The quick brown fox jumps over the lazy dog and this is really just a long comment for testing purposes to see how it handles long comments yep exactly that is \
                 why this is so bloody long is so I can see how frontend handles this comment oh my god it keeps on going the end full stop']

    # number of users to generate
    n_user = 30

    # number of transactions to generate
    n_transaction = 2000

    # number of recurring transactions to generate
    n_recurring_transaction = 150

    # number of limit for transactions to generate
    n_limit = 3

    # run to populate database
    fill_profiles(n_user)
    if args.feedback:
        print("--PROFILES--")
        print(get_all_given("profiles", "*"))
        print("")
        print("")

    for i in range(1, n_user+1):
        initialise_limits(i, transaction_types)
    if args.feedback:
        print("--INITIALISED LIMITS--")
        print(get_all_given("limits", "*"))
        print("")
        print("")

    fill_transactions(n_user, n_transaction)
    if args.feedback:
        print("--TRANSACTIONS--")
        print(get_all_given("transactions", "*"))
        print("")
        print("")

    fill_recurring_transactions(n_user, n_recurring_transaction)
    if args.feedback:
        print("--RECURRING TRANSACTIONS--")
        print(get_all_given("recurring_transactions", "*"))
        print("")
        print("")

    fill_limits(n_user, n_limit)
    if args.feedback:
        print("--LIMITS--")
        print(get_all_given("limits", "*"))
        print("")
        print("")

    fill_messages()
    if args.feedback:
        print("--MESSAGES--")
        print(get_all_given("messages", "*"))
        print("")
        print("")

    print("DATABASE SUCCESSFULLY POPULATED")
