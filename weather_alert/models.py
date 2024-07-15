import uuid
from django.db import models
from community.models import Region
from django.contrib.auth import get_user_model

User = get_user_model()

# Alerts Media
class WeatherAlertFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='weather_alerts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str___(self):
        return f'File for alert: {self.alert.title}'

# Weather alert model.
class WeatherAlert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    media = models.ForeignKey(WeatherAlertFile, on_delete=models.SET_NULL, blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# ALert subscription
class AlertSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    regions = models.ManyToManyField(Region)

    def __str__(self):
        return f'{self.user.username} subscriptions'
