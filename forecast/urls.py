from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('emergency/', views.emg_contacts, name='emergency')
]