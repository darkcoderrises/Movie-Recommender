from .models import UserProfile,TheaterOwner
from django import forms

class UserProfileCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ["age", "gender", "phone", "genre_pref", "username", "password", "first_name", "last_name"]  


class TheaterOwnerCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = TheaterOwner
        fields = ["age", "gender", "phone", "username", "password", "first_name", "last_name"]  

