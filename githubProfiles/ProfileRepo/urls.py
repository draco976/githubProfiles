from django.urls import path

from . import views

urlpatterns = [
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/update/<int:user_id>/', views.update, name='update'),
    path('profile/explore/', views.explore, name='explore')
]