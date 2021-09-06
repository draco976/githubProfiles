from django.shortcuts import get_object_or_404, render
from .models import Profile, Repository
from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'profile.html', {'user':user})


