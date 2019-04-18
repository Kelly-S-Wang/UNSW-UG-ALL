from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Validators used to check if fields are valid
default_char = RegexValidator(r'^[A-Za-z0-9]+$', "No special characters. a-z, A-Z, 0-9 only.")
password_test = RegexValidator(r'[a-zA-Z0-9]*[0-9]+[a-zA-Z0-9]*', "Password needs at least 1 number")
# To improve, as a string '39/19/2999' is technically considered valid
dob_valid = RegexValidator(r'^[0-3]{1}[0-9]{1}\/[0-1]{1}[0-9]{1}\/[1-2]{1}[0-9]{3}$', "Date must be valid")
# Ensures only an integer is inputed
money_valid = RegexValidator(r'^[0-9]+\.?[0-9]+$', "Must be a number with maximum 1 decimal point if needed")
# Checks time is valid
time_valid =  RegexValidator(r'^[0-2]{1}[0-9]{1}\:[0-6]{1}[0-9]{1}$', 'Time must be in format HH:MM')

# Create new form which contains fields needed
class RegisterForm(forms.Form):
	username = forms.CharField(label='username', max_length=20, validators=[default_char], required = True)
	email = forms.EmailField(label='email', required = True)
	password = forms.CharField(label='password', required = True, min_length = 7, validators = [default_char, password_test])
	confirm_password = forms.CharField(label='c_password', required = True, min_length = 7, validators = [default_char, password_test])

	# Superclass which adds in checking functionality for passwords
	def clean(self):

		# Get data from forms, specifically passwords
		cleaned_data = super(RegisterForm, self).clean()
		orig_pass = cleaned_data.get("password")
		conf_pass = cleaned_data.get("confirm_password")
		if orig_pass != conf_pass:
			print("NO MATCH")
			raise forms.ValidationError("Passwords do not match.")

		return self.cleaned_data

# Changeform which does all the error checking
class ChangeForm(forms.Form):
	email = forms.EmailField(label='email', required = True)
	password = forms.CharField(label='password', required = True, min_length = 7, validators = [default_char, password_test])
	confirm_password = forms.CharField(label='c_password', required = True, min_length = 7, validators = [default_char, password_test])
	#dob = forms.CharField(label='dob', required = True, validators = [dob_valid])
	# Superclass which adds in checking functionality for passwords
	def clean(self):

		# Get data from forms, specifically passwords
		cleaned_data = super(ChangeForm, self).clean()
		orig_pass = cleaned_data.get("password")
		conf_pass = cleaned_data.get("confirm_password")
		if orig_pass != conf_pass:
			print("NO MATCH")
			raise forms.ValidationError("Passwords do not match.")

		return self.cleaned_data

# Form which contains fields for a valid transaction
class TransactionForm(forms.Form):
	money = forms.CharField(label='money', validators=[money_valid], required = True)
	date = forms.CharField(label='date', required = True, validators = [dob_valid])
	time = forms.CharField(label='time', required = True, validators = [time_valid])

	