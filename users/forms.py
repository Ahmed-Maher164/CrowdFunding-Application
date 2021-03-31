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

    def clean(self,*args,**kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email,password=password)
            if not user:
                raise forms.ValidationError("The user not exist")
            if not user.check_password(password):
                raise forms.ValidationError("the password not correct")


#===================================================================================================

