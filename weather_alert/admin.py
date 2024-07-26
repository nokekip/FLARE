from django.contrib import admin
from .models import WeatherAlert, WeatherAlertFile, AlertSubscription

# Register your models here.
admin.site.register(WeatherAlert)
admin.site.register(WeatherAlertFile)
admin.site.register(AlertSubscription)
