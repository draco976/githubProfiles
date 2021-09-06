from githubProfiles.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect,render
import requests

REQUESTS_BASE_DIR = 'https://api.github.com/users/'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
        else:
            return redirect('/accounts/login')
    else :
        form = RegistrationForm() 
        args = {'form':form}

        return render(request,'reg_form.html',args)


def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/profile/' + str(user.id))
    else:
        return redirect('/accounts/login')
