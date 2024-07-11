from django import forms
from .models import AlertSubscription, WeatherAlert, WeatherAlertFile


class AlertSubscriptionForm(forms.ModelForm):
    class Meta:
        model = AlertSubscription
        fields = ['regions']

class WeatherAlertForm(forms.ModelForm):
    class Meta:
        model = WeatherAlert
        fields = ['region', 'title', 'description']

class WeatherAlertFileForm(forms.ModelForm):
    class Meta:
        model = WeatherAlertFile
        fields = ['file']