from django.shortcuts import render, redirect
from users.forms import RegistraionForm, LoginForm
from users.models import Users

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistraionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
    else:
        form = RegistraionForm()
    return render(request, 'users/register.html', {'form': form})

def login(request):
    form = LoginForm()
    return render(request, 'users/login.html', {'form' : form})


