from django.urls import path
from .views import add_alert, manage_subscription


urlpatterns = [
    path('', add_alert, name='weather-alert'),
    path('manage-subscription/', manage_subscription, name='manage-subscription'),
]