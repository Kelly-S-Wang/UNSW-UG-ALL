import re, random, math, secrets, os, datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

from .myforms import RegisterForm, TransactionForm, ChangeForm
from .jsfunctions import *
from query_calls import *
from validation import *
from populate import initialise_limits
from ocr import ocr_execute


# Landing page of the website
def index(request):
    return render(request, "index.html")

# Register page
def register(request):
    # Only go here if it is a POST instead of a GET
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(request.POST.get('gender'))
        # Check for validity of form data
        if form.is_valid():
            user_error = ""
            email_error = ""
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            if (username,) in get_all_given("profiles", "username"):
                return render(request, "register.html", {'user_error': "Username already exists"})
            elif (email,) in get_all_given("profiles", "email"):
                return render(request, "register.html", {'email_error': "email already exists"})
            else:
                username = form.cleaned_data["username"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                name = username
                gender = "FM"
                dob = datetime.datetime.now()
                register_new_user(username, name, gender, dob, email, password)
                return render(request, "confirmregister.html", {'email' : email})
        else:

            # Sort error data to display
            user_error = ""
            email_error = ""
            password_error = ""
            dob_error = ""
            # Check if errors appear in the form
            if "username" in form.errors:
                user_error = form.errors["username"]
            if "email" in form.errors:
                email_error = form.errors["email"]
            if "password" in form.errors:
                password_error = form.errors["password"]
                if form.non_field_errors():
                    password_error.append(form.non_field_errors())
            if not password_error:
                if form.non_field_errors():
                    password_error = form.non_field_errors()
            if "dob" in form.errors:
                dob_error = form.errors["dob"]
            return render(request, "register.html", {'user_error': user_error,
                                                     'email_error': email_error, 'password_error': password_error,
                                                     'dob_error': dob_error})
    else:
        return render(request, "register.html")

#confirm profile creation
def confirm(request, token):
    has_token = object_query(Confirmation, Confirmation.token == token)
    if has_token:
        profile = object_query(Profile, Profile.id == has_token.profile_id)
        profile.set_confirmed(True)
        print("CONFIRMING")
        user = User.objects.create_user(profile.username, profile.email, profile.password)
        user.save()
        profile.set_password("We don't store plaintext passwords bruh")
        transaction_types = [('Salary', 'I'), ('Investments', 'I'), ('Other/Income', 'I'), ('Food/Drinks', 'E'), ('Bills', 'E'),
                             ('Electronics', 'E'), ('Entertainment', 'E'),
                             ('Travel', 'E'), ('Debt', 'E'), ('Clothing', 'E'), ('Automobile', 'E'), ('Pets', 'E'),
                             ('Other/Expenses', 'E')]
        initialise_limits(profile.id, transaction_types)
        session.commit()

    return render(request, "confirmed.html")

#gather data for statistic visualisation on overview page
def overview_graph(request):
    username = request.user.username
    # Get user information
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]

    transactions = object_query_sorted(Transaction, Transaction.profile_id == pid, Transaction.date_time)
    transactions.reverse()

    past_months = get_prev_months()
    tmp = {}
    for i in past_months:
        tmp[i] = 0

    for transaction in transactions:
        d = transaction.date_time.day
        m = transaction.date_time.month
        y = transaction.date_time.year

        if (m, y) in tmp and transaction.inc_exp == 'E':
            tmp[(m, y)] += transaction.amount
    return tmp

# Get previous 6 months
def get_prev_months():
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    curr_year = datetime.datetime.now().year

    # If month > 6, then we can safetly assume there is no year rollback
    if month >= 6:
        return reversed([(month, curr_year), (month - 1, curr_year), (month - 2, curr_year), (month - 3, curr_year),
                (month - 4, curr_year), (month - 5, curr_year)])
    else:
        # Else there will be a year rollback
        to_return = []
        curr_month = month
        for i in range(0, 6):
            to_return.append((curr_month, curr_year))
            # Roll back a year
            if curr_month == 1:
                curr_year -= 1
                curr_month = 12
            else:
                curr_month -= 1
        return reversed(to_return)

# Features Page
def features(request):
    return render(request, "features.html")


# Test pages to test out new functions and such
def test(request):
    tmp = get_all_given("profiles", "username")
    if ("latishahiedi86",) in tmp:
        print("I'M IN HERE")
    print(secrets.token_urlsafe(10))
    if (request.GET.get('del')):
        for users in User.objects.all():
            if (users.username != "admin"):
                users.delete()
    if (request.GET.get('repop')):
        for profile in get_all_given("profiles", "*"):
            _, usr, _, _, _, eml, pss, _ = profile
            user = User.objects.create_user(usr, eml, pss)
            user.save()
    names = []
    for users in User.objects.all():
        names.append(users.username)

    return render(request, "test.html", {'a': 4, 'b': 20, 'c': 0, 'd': 11,
                                         'label1': "PASSED", 'label2': "NICE", 'names': names})


# Basic overview page for dashboard
@login_required
def overview(request):

    curr_day = datetime.datetime.now().day
    curr_month = datetime.datetime.now().month
    curr_year = datetime.datetime.now().year
    username = request.user.username
    print(username)

    # Get user information
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]
    # Check messages
    messages = object_query(Message, Message.profile_id == pid, "all")
    # Get transactions
    limits = object_query_sorted(Limit, Limit.profile_id == pid, Limit.amount)
    limits_d = {}
    for i in limits:
        if i.type == "Food/Drinks":
            limits_d["Food"] = i.amount
        elif i.type == "Other/Expenses":
            limits_d["Other"] = i.amount
        else:
            limits_d[i.type] = i.amount

    # Get the sum of all expenses for the month
    _, sum_expense = get_category_sum(pid, True)
    print(sum_expense)

    # Get the percentage value
    percentage = {}
    for key, val in limits_d.items():
        if limits_d[key] == 0:
            percentage[key] = 0
        elif key in sum_expense:
            percentage[key] = round((sum_expense[key] / limits_d[key])*100)

    transactions = object_query_sorted(Transaction, Transaction.profile_id == pid, Transaction.date_time)
    transactions.reverse()

    odometer_daily = 0
    odometer_expense_monthly = 0
    odometer_income_monthly = 0

    # Sum up daily/monthly spending/earning
    for transaction in transactions:
        d = transaction.date_time.day
        m = transaction.date_time.month
        y = transaction.date_time.year
        if (m == curr_month) and (y == curr_year):
            if transaction.inc_exp == 'E':
                odometer_expense_monthly += transaction.amount
                if d == curr_day:
                    odometer_daily += transaction.amount
            else:
                odometer_income_monthly += transaction.amount
    tmp = overview_graph(request)
    print(tmp)
    response = render(request, "overview.html", {'overview': test_overview_graph(tmp), 'full_name': username,
                                             'odometer': overview_odometer(round(odometer_daily, 1), round(odometer_expense_monthly, 1), round(odometer_income_monthly, 1)),
                                             'transaction_list': transactions[:5], 'page_name' : 'Overview', 'messages' : len(messages), "sum_expense" : sum_expense, "limits" : limits_d,
                                              'percentage' : percentage})

    if request.COOKIES.get("helper"):
        response.set_cookie("helper", "b")
    else:
        response.set_cookie('helper', "a")
    return response

#receives POST to create transactions
@login_required
def transactions(request):
    username = request.user.username
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]
    print(request.path)
    messages = object_query(Message, Message.profile_id == pid, "all")
    if request.method == 'POST':
        # If there's money, add
        if request.POST.get('money_expense'):
            got_date = request.POST.get('date_expense')
            date_time = datetime.datetime.today()
            if got_date:
                date_time = datetime.datetime.strptime(got_date, "%b %d, %Y")
            amount = request.POST.get('money_expense')

            # Not valid money, redirect
            if not is_valid_cash(amount):
                redirect(request.POST.get('curr_path').lower())
            comment = request.POST.get("comment_exp")
            inc_exp = "E"

            trans_type_num = request.POST.get('expense_type')

            trans_types = ['0', 'Food/Drinks', 'Bills', 'Electronics', 'Entertainment', 'Travel', 'Debt', 'Clothing',
                       'Health', 'Automobile', 'Pets', 'Other/Expenses']
            transaction_type = trans_types[int(trans_type_num)]

            #check for recurring transaction input
            if request.POST.get('freq_exp') and request.POST.get('from_exp') and request.POST.get('to_exp'):
                freq_options = ['', '', 'day', 'week', 'month']
                freq = freq_options[int(request.POST.get('freq_exp'))]
                from_date = datetime.datetime.strptime(request.POST.get('from_exp'), "%b %d, %Y")
                to_date = datetime.datetime.strptime(request.POST.get('to_exp'), "%b %d, %Y")
                r_id = add_new_recurring_transaction(pid, from_date, to_date, 1, freq, amount, comment, inc_exp, transaction_type)

                #check if need to add message
                today = datetime.datetime.today()
                if from_date.day == today.day and from_date.month == today.month and from_date.year == today.year:
                    add_new_message(pid, r_id, today)

                return redirect('recurring')
            else:
                add_new_transaction(pid, date_time, amount, comment, inc_exp, transaction_type)

        else:
            # Else process income instead of expense
            got_date = request.POST.get('date_income')
            date_time = datetime.datetime.today()
            if got_date:
                date_time = datetime.datetime.strptime(got_date, "%b %d, %Y")
            amount = request.POST.get('money_income')
            # Not valid money, redirect
            if not is_valid_cash(amount):
                redirect(request.POST.get('curr_path').lower())
            comment = request.POST.get("comment_inc")
            inc_exp = "I"

            trans_type_num = request.POST.get('income_type')

            trans_types = ['0', 'Salary', 'Investments', 'Other/Income']
            transaction_type = trans_types[int(trans_type_num)]

            #check for recurring transaction input
            if request.POST.get('freq_inc') and request.POST.get('from_inc') and request.POST.get('to_inc'):
                freq_options = ['', '', 'day', 'week', 'month']
                freq = freq_options[int(request.POST.get('freq_inc'))]
                from_date = datetime.datetime.strptime(request.POST.get('from_inc'), "%b %d, %Y")
                to_date = datetime.datetime.strptime(request.POST.get('to_inc'), "%b %d, %Y")
                r_id = add_new_recurring_transaction(pid, from_date, to_date, 1, freq, amount, comment, inc_exp, transaction_type)

                #check if need to add message
                today = datetime.datetime.today()
                if from_date.day == today.day and from_date.month == today.month and from_date.year == today.year:
                    add_new_message(pid, r_id, today)

                return redirect('recurring')
            else:
                add_new_transaction(pid, date_time, amount, comment, inc_exp, transaction_type)

        # return redirect(request.path)
        return redirect(request.POST.get('curr_path').lower())

    else:
        return redirect('history') #transactions page is deprecated - redirect to history

#manage recurring transactions
@login_required
def recurring(request):
    username = request.user.username
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]

    if request.method == "POST": #received edit

        r_id = request.POST.get("r_id")
        print("recurring ID = " + str(r_id))

        new_amount = request.POST.get("money")
        # Not valid money, redirect
        if not is_valid_cash(new_amount):
            redirect('recurring')

        ie = request.POST.get("transaction_inc_exp")

        category_num = int(request.POST.get("transaction_type"))
        trans_types = ['0', 'Food/Drinks', 'Bills', 'Electronics', 'Entertainment', 'Travel', 'Debt', 'Clothing',
                       'Health', 'Automobile', 'Pets', 'Other/Expenses']
        if ie == "I":
            trans_types = ['0', 'Salary', 'Investments', 'Other/Income']
        category = trans_types[category_num]

        from_date = datetime.datetime.strptime(request.POST.get("from"), "%b %d, %Y")
        to_date = datetime.datetime.strptime(request.POST.get("to"), "%b %d, %Y")

        r_freq = request.POST.get("freq")

        new_comment = request.POST.get("comment")


        edit_existing_recurring_transaction(pid, r_id, from_date, to_date,
                                                0, r_freq, new_amount,
                                                new_comment, ie, category)
        return redirect('recurring') #refresh this page with updated transaction

    else:
        transactions = object_query(Recurring_transaction, Recurring_transaction.profile_id == pid, "all")
        messages = object_query(Message, Message.profile_id == pid, "all")
        current_t = []
        for m in messages:
            r_id = m.recurring_transaction_id
            current_t.append([m, object_query(Recurring_transaction, Recurring_transaction.id == r_id)])
        print(current_t)
        return render(request, "recurring.html", {'full_name': username, 'page_name' : 'Recurring', 'transaction_list' : transactions, 'messages': messages, 'current_t': current_t })


#confirm message (an instance of recurring transaction)
@login_required
def confirm_message(request):
    username = request.user.username
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]
    if request.method == "POST":
        m_id = request.POST.get('message_id')

        #get relevant message and recurring transaction objects
        msg = object_query(Message, Message.id == m_id)
        recurring_t = object_query(Recurring_transaction, Recurring_transaction.id == msg.recurring_transaction_id)

        #insert new transaction
        add_new_transaction(pid, msg.date_time, recurring_t.amount, recurring_t.comment, recurring_t.inc_exp, recurring_t.type)
        #delete message
        delete_existing_message(m_id, pid)

        return redirect('history')
    else:
        return redirect('overview')

#page for managing spending limits
@login_required
def budget(request):
    username = request.user.username
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]
    limits = object_query_sorted(Limit, Limit.profile_id == pid, Limit.type)
    trans_types = ['Food/Drinks', 'Bills', 'Electronics', 'Entertainment', 'Travel', 'Debt', 'Clothing',
               'Health', 'Automobile', 'Pets', 'Other/Expenses']
    messages = object_query(Message, Message.profile_id == pid, "all")
    _, sum_expense = get_category_sum(pid, True)
    # Set each limit to whatever is in POST
    if request.method == "POST":
        for i in request.POST:
            for j in limits:
                if j.type == i and is_valid_cash(request.POST.get(i)):
                    j.amount = request.POST.get(i)
                    session.commit()
    for i in limits:
        if i.type in trans_types:
            trans_types.remove(i.type)
    no_limit = []
    for i in trans_types:
        tmp = {}
        tmp[i] = 0
        no_limit.append(tmp)
    print(sum_expense)
    return render(request, "budget.html", {'full_name': username, 'page_name' : 'Budget', 'limits' : limits, 'no_limit' : no_limit, 'messages' : len(messages), 'sum_expense' : sum_expense})

#delete user account
@login_required
def delete(request):
    username = request.user.username
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]
    user = User.objects.get(username = username)
    user.delete()
    delete_profile_and_details(pid)
    logout(request)
    return render(request, "index.html")

#change profile attributes
@login_required
def settings(request):
    username = request.user.username
    pid, _, name, _, _, email, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]
    messages = object_query(Message, Message.profile_id == pid, "all")

    # Only go here if it is a POST instead of a GET
    if request.method == 'POST':
        if "profile_img" in request.FILES:
            with open(os.getcwd() + static("users\\" + username + "\\profile.jpg"), 'wb+') as f:
                    for chunk in request.FILES["profile_img"].chunks():
                        f.write(chunk)
        form = ChangeForm(request.POST)
        # Check for validity of form data
        if form.is_valid():
            print("Ayo gg")
            user_error = ""
            email_error = ""
            n_email = form.cleaned_data["email"]
            if n_email != email and (n_email,) in get_all_given("profiles", "email"):
                return render(request, "settings.html", {'email_error': "Email already exists.", 'full_name': username, 
                                                         'email': email, 'page_name' : 'Settings', 'messages' : len(messages)})
            else:
                n_email = form.cleaned_data["email"]
                n_password = form.cleaned_data["password"]
                n_name = username
                profile = object_query(Profile, Profile.id == pid)
                profile.set_email(n_email)
                user = User.objects.get(username=username)
                user.set_password(n_password)
                user.save()
                logout(request)
                return render(request, "index.html")
        else:
            #print(request.FILES["profile_img"])
            print(print(static("images")))
            print("Form not valid?")
            print(form.errors)
            # Sort error data to display
            email_error = ""
            password_error = ""
            # Check if errors appear in the form
            if "email" in form.errors:
                email_error = form.errors["email"]
            if "password" in form.errors:
                password_error = form.errors["password"]
                if form.non_field_errors():
                    password_error.append(form.non_field_errors())
            if not password_error:
                if form.non_field_errors():
                    password_error = form.non_field_errors()

            return render(request, "settings.html", {'email_error': email_error, 'password_error': password_error, 'full_name': username, 
                                                     'email': email, 'page_name' : 'Settings', 'messages' : len(messages)})
    else:
        return render(request, "settings.html", {'full_name': username, 'email': email, 'page_name' : 'Settings', 'messages' : len(messages)})


#view transaction history
@login_required
def history(request):
    username = request.user.username
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]
    transactions = object_query_sorted(Transaction, Transaction.profile_id == pid, Transaction.date_time)
    transactions.reverse()
    messages = object_query(Message, Message.profile_id == pid, "all")
    print(messages)
    # Show categorized transactions instead
    if (request.GET.get('category')):
        t_income = {}
        t_expense = {}
        for transaction in transactions:
            if transaction.inc_exp == "E":
                if transaction.type not in t_expense:
                    t_expense[transaction.type] = []
                    t_expense[transaction.type].append(transaction)
                else:
                    t_expense[transaction.type].append(transaction)
            else:
                if transaction.type not in t_income:
                    t_income[transaction.type] = []
                    t_income[transaction.type].append(transaction)
                else:
                    t_income[transaction.type].append(transaction)

        sum_income, sum_expense = get_category_sum(pid)

        return render(request, "categorized.html",
                      {'full_name': username, 'catincome': t_income, 'catexpense': t_expense, 'sum_income': sum_income,
                       'sum_expense': sum_expense, 'page_name' : 'History', 'messages' : len(messages)})

    else: #paginated history display
        paginator = Paginator(transactions, 10)
        page = request.GET.get('page')
        this_page_transactions = paginator.get_page(page)
        return render(request, "history.html",
                      {'full_name': username, 'transaction_list': this_page_transactions, 'page_name' : "History", 'messages' : len(messages)})

#edit a transaction
@login_required
def edit_transaction(request):
    username = request.user.username
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]

    if request.method == "POST":
        print("Received from form...")
        t_id = request.POST.get("transaction_id")
        ie = request.POST.get("money_type") #income/expense type
        new_money = request.POST.get("money"
                                     "")
        new_time = "00:00"
        new_date = request.POST.get("date")
        page = request.POST.get("page")
        date_time = datetime.datetime.strptime(new_date + " " + new_time, "%b %d, %Y %H:%M")
        if not is_valid_cash(new_money):
            return redirect(page.lower())
        category_num = int(request.POST.get("transaction_type"))
        trans_types = ['0', 'Food/Drinks', 'Bills', 'Electronics', 'Entertainment', 'Travel', 'Debt', 'Clothing',
                       'Health', 'Automobile', 'Pets', 'Other/Expenses']
        if ie == "I":
            trans_types = ['0', 'Salary', 'Investments', 'Other/Income']
        new_category = trans_types[category_num]

        new_comment = request.POST.get("comment")
        #edit transaction
        edit_existing_transaction(pid, t_id, date_time, new_money, new_comment, ie, new_category)  # don't specify category, I/E for now

        return redirect(page.lower())
    else:
        return redirect('index')


#delete a specific transaction
@login_required
def delete_transaction(request):
    username = request.user.username
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]

    if request.method == "POST":
        t_id = request.POST.get("transaction_id")
        page = request.POST.get("page")
        remove_transaction(t_id, pid)
        return redirect(page.lower())
    else:
        return redirect('index')

#delete a specific recurring transaction
@login_required
def delete_recurring(request):
    username = request.user.username
    pid, _, name, _, _, _, _, _ = get_where("profiles", "*", "username='" + username + "'")[0]

    if request.method == "POST":
        r_id = request.POST.get("r_id")
        delete_existing_recurring_transaction(r_id, pid)
        print("deleting transaction with id = " + str(r_id))
        return redirect('recurring')
    else:
        return redirect('index')

# WIP function for receiving recipt images and passing through OCR
@login_required
def receipt_upload(request):
    if request.method == "POST":
        f = request.FILES['profile_img']
        # SANITISE

        print(f)
        with open('sample_receipts/new_img.jpg', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        result = ocr_execute("sample_receipts/new_img.jpg")
        print(result)

        return redirect('overview')

    else:
        return redirect('index')

# Get the sum of each category
def get_category_sum(pid, month = False):
    transactions = object_query_sorted(Transaction, Transaction.profile_id == pid, Transaction.date_time)
    transactions.reverse()

    t_income = {}
    t_expense = {}
    for transaction in transactions:

        if transaction.inc_exp == "E":
            if transaction.type not in t_expense:
                t_expense[transaction.type] = []
                t_expense[transaction.type].append(transaction)
            else:
                t_expense[transaction.type].append(transaction)
        else:
            if transaction.type not in t_income:
                t_income[transaction.type] = []
                t_income[transaction.type].append(transaction)
            else:
                t_income[transaction.type].append(transaction)

    sum_income = {}
    sum_expense = {}
    # Initialise the dicts
    for key, value in t_income.items():
        if key == "Other/Income":
            sum_income["Other"] = 0
        sum_income[key] = 0

    for key, value in t_expense.items():
        if key == "Other/Expenses":
            sum_expense["Other"] = 0
        if key == "Food/Drinks":
            sum_expense["Food"] = 0
        sum_expense[key] = 0

    # If month, only process sum from the month
    if month:
        for key, value in t_income.items():
            for value1 in value:
                if value1.date_time.month == datetime.datetime.now().month:
                    if key == "Other/Income":
                        sum_income["Other"] += int(value1.amount)
                    else:
                        sum_income[key] += int(value1.amount)

        for key, value in t_expense.items():
            for value1 in value:
                if value1.date_time.month == datetime.datetime.now().month:
                    if key == "Other/Expenses":
                        sum_expense["Other"] += int(value1.amount)
                    if key == "Food/Drinks":
                        sum_expense["Food"] += int(value1.amount)
                    else:
                        sum_expense[key] += int(value1.amount)
    # Else process all
    else:
        for key, value in t_income.items():
            for value1 in value:
                if key == "Other/Income":
                    sum_income["Other"] += int(value1.amount)
                else:
                    sum_income[key] += int(value1.amount)

        for key, value in t_expense.items():
            for value1 in value:
                if key == "Other/Expenses":
                    sum_expense["Other"] += int(value1.amount)
                if key == "Food/Drinks":
                    sum_expense["Food"] += int(value1.amount)
                else:
                    sum_expense[key] += int(value1.amount)

    return (sum_income, sum_expense)

# Download page
def download(request):
    return render(request, "download.html")

# Credits page
def credits(request):
    return render(request, "credits.html")

# TESTING ONLY
# Display spending of past 6 months.
def test_overview_graph(past):
    name = "overview6"
    title = "'Monthly spending past 6 months'"
    labels = []
    data = []
    for key, val in past.items():
        m, y = key
        labels.append(int_to_month(m))
        data.append(str(val))
        print(val)
    return bar_graph_monthly(name, title, labels, data)

# Checks if number is a valid input
def is_valid_cash(amount):
    if re.match(r'^[0-9]+\.?[0-9]+$', amount):
        return True
    return False

# Janky, but returns int to string of month
def int_to_month(num):
    if num == 1:
        return "Jan"
    elif num == 2:
        return "Feb"
    elif num == 3:
        return "Mar"
    elif num == 4:
        return "Apr"
    elif num == 5:
        return "May"
    elif num == 6:
        return "Jun"
    elif num == 7:
        return "Jul"
    elif num == 8:
        return "Aug"
    elif num == 9:
        return "Sep"
    elif num == 10:
        return "Oct"
    elif num == 11:
        return "Nov"
    else:
        return "Dec"