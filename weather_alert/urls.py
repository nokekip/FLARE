from django.urls import path
from .views import add_alert


urlpatterns = [
    path('', add_alert, name='weather-alert')
]