from django.urls import path
from .views import add_alert, manage_subscription, weather_alerts


urlpatterns = [
    path('', weather_alerts, name='weather-alert'),
    path('add-alert/', add_alert, name='add-alert'),
    path('manage-subscription/', manage_subscription, name='manage-subscription'),
]