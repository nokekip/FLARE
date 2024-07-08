from django.urls import path
from .views import community_home


urlpatterns = [
    path('', community_home, name='community-home'),
]