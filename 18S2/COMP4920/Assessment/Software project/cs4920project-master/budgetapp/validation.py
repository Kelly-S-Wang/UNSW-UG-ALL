"""This is for generating a pseudom random number to confirm emails after registering for
account authentication

register -> secrets.py -> url -> email -> confirmation
"""

import string
from secrets import token_urlsafe
from django.core.mail import send_mail


# take in the email from the user
# provide a link for user to press on
# record into the table
"""def validate(email): 
	activation_link = 'http://127.0.0.1:8000/confirm' + token_urlsafe(16)
	send_mail('Confirmation for APP NAME',
	 'Please press this "' + activation_link + '" to activate your account',
	 'testing495810@gmail.com',
	 ['puapao123@gmail.com'], 
	 fail_silently=False) """

def send_email(request):
    msg = EmailMessage('Request Callback',
                       'Here is the message.', to=['puapao123@gmail.com'])
    msg.send()
    return HttpResponseRedirect('/')
