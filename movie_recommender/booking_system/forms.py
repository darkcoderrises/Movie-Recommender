from .models import UserProfile
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_id = 'id-auth'
        self.helper.form_method = 'post'
        self.helper.form_action = 'signup'
        self.helper.add_input(Submit('submit', 'Submit'))


class UpdateProfile(forms.ModelForm): 
    pass

class UserProfileCreationForm(forms.ModelForm):
    pass

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )



