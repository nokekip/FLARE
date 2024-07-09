from django.urls import path
from .views import community_home, forum, create_forum


urlpatterns = [
    path('', community_home, name='community-home'),
    path('forum/<str:forum_id>/', forum, name='forum'),
    path('create-forum/', create_forum, name='create-forum')
]