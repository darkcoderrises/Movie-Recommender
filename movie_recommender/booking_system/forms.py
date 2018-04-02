from .models import UserProfile,TheaterOwner
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
#from dobwidget import DateOfBirthWidget
#from django.forms.widgets import DateInput
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper


#class LoginForm(forms.ModelForm):
#    username = forms.CharField()
#    password = forms.CharField(widget=forms.PasswordInput())
#
#    def __init__(self, *args, **kwargs):
#        super(LoginForm, self).__init__(*args, **kwargs)
#        self.helper.form_id='id-loginForm'
#		self.helper.form_method='post'
#		self.helper.form_action='login'
#        self.helper.add_input(Login('login', 'Login'))

class UserProfileCreationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = UserProfile
		fields = ["gender", "phone","genre_pref", "username", "password", "first_name", "last_name"] 


	def __init__(self, *args, **kwargs):
		super(UserProfileCreationForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-UserProfileCreationForm'
		self.helper.form_class = 'blueForms'
		self.helper.form_method = 'post'
		self.helper.form_action = 'submit_profile'

		self.helper.add_input(Submit('submit', 'Submit'))

    #class Meta:
    #    model = UserProfile
    #    fields = ["dob","gender", "phone", "genre_pref", "username", "password", "first_name", "last_name"]  
    #    labels = {
    #    'dob': ('D.O.B'),
    #}
    #widgets = {
    #    'dob': DateInput(attrs={'type': 'date'})
    #}

    #class Meta:
    #    model = UserProfile
    #    fields = ["date_of_birth","gender", "phone", "genre_pref", "username", "password", "first_name", "last_name"]  
    #widgets = {
    #    'date_of_birth': DateOfBirthWidget(order='DMY'),
    #}


class UpdateProfile(forms.ModelForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	
    #username = forms.CharField(required=True)
	

	class Meta:
		model = UserProfile
		fields = ('email', 'first_name', 'last_name')

	def clean_email(self):
	    username = self.cleaned_data.get('username')
	    email = self.cleaned_data.get('email')

	    if email and UserProfile.objects.filter(email=email).exclude(username=username).count():
	        raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
	    return email

	def save(self, commit=True):
	    user = super(UpdateProfile, self).save(commit=False)
	    user.email = self.cleaned_data['email']

	    if commit:
	        user.save()

	    return user

	def __init__(self, *args, **kwargs):
		super(UpdateProfile, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
    

class TheaterOwnerCreationForm(forms.ModelForm):
	
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = TheaterOwner
        fields = ["gender", "phone", "username", "password", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(TheaterOwnerCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  

