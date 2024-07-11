import uuid
from django.db import models
from community.models import Region
from django.contrib.auth import get_user_model

User = get_user_model

# Weather alert model.
class WeatherAlert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# Alerts Media
class WeatherAlertFile(models.Model):
    alert = models.ForeignKey(WeatherAlert, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='weather_alerts/')

    def __str___(self):
        return f'File for alert: {self.alert.title}'
    
# ALert subscription
class AlertSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    regions = models.ManyToManyField(Region)

    def __str__(self):
        return f'{self.user.username} subscriptions'
