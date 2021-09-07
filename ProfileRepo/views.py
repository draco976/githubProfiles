from django.shortcuts import redirect,render
from .models import Profile, Repository
from django.http import HttpResponse
from django.contrib.auth.models import User
import requests
from django.utils import timezone

REQUESTS_BASE_DIR = 'https://api.github.com/users/'

def profile(request, user_id):
    user = request.user
    if user.is_authenticated:
        user1 = User.objects.get(id=user_id)
        return render(request, 'profile.html', {'user':user1, 'current_user_id':user.id,})
    else:
        return redirect('/accounts/login')
    

def explore(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'explore.html', {
            'user_list':User.objects.all(), 
            'current_user_id':user.id,
        })
    else:
        return redirect('/accounts/login')

def update(request, user_id):
    user = request.user
    if user.is_authenticated:
        user = User.objects.get(id=user_id)
        response = requests.get(REQUESTS_BASE_DIR+user.username)
        data = response.json()
        user.profile.last_update_time = timezone.localtime() 
        user.profile.followers = data['followers']
        user.profile.save()

        user.profile.repository_set.all().delete()
        response = requests.get(REQUESTS_BASE_DIR+user.username+'/repos')
        repos_data = response.json()
        for repo in repos_data:
            Repository.objects.create(profile=user.profile, name=repo["name"], num_stars=repo["stargazers_count"])
        return redirect('/profile/'+str(user.id))
    else:
        return redirect('/accounts/login')



