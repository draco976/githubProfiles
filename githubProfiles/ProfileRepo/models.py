from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from django.utils.timezone import datetime

REQUESTS_BASE_DIR = 'https://api.github.com/users/'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.IntegerField()
    last_update_time = models.DateTimeField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        response = requests.get(REQUESTS_BASE_DIR+instance.username)
        data = response.json()
        profile = Profile.objects.create(user=instance, followers=data['followers'], last_update_time=datetime.now())

        response = requests.get(REQUESTS_BASE_DIR+instance.username+'/repos')
        repos_data = response.json()
        for repo in repos_data:
            Repository.objects.create(profile=profile, name=repo["name"], num_stars=repo["stargazers_count"])
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Repository(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    num_stars = models.IntegerField()
