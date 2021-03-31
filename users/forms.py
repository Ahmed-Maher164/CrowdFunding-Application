from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Users
from django.contrib.auth import authenticate

class RegistraionForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = Users
        fields = ('email','first_name','last_name','phone','photo','password1','password2')

#================================================================================================
class LoginForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ('email','password')

#=================================================================================================
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError('invalid login data...')

#===================================================================================================
