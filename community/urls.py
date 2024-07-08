from django.urls import path
from .views import community_home, forum


urlpatterns = [
    path('', community_home, name='community-home'),
    path('forum/', forum, name='forum'),
]