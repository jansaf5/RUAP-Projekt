# urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('real-estate', views.real_estate_input, name='real_estate'),
    path('profile', views.profile, name='profile'),
]
