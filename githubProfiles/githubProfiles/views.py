from githubProfiles.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect,render
import requests

REQUESTS_BASE_DIR = 'https://api.github.com/users/'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
    else :
        form = RegistrationForm() 
        args = {'form':form}
    return render(request,'reg_form.html',args)


def home(request):
    user = request.user
    if user.is_authenticated:
        response = requests.get(REQUESTS_BASE_DIR+user.username)
        data = response.json()
        response = requests.get(REQUESTS_BASE_DIR+user.username+'/repos')
        repos_data = response.json()
        return render(request, 'home.html', {
            'followers': data['followers'],
            'name': data['name'],
            'login': data['login'],
            'repos_data': repos_data
        })
    else:
        return render(request, 'home.html', {
            'type': '',
            'name': ''
        })
