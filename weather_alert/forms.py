from django import forms
from .models import AlertSubscription, WeatherAlert, WeatherAlertFile


class AlertSubscriptionForm(forms.ModelForm):
    class Meta:
        model = AlertSubscription
        fields = ['regions']