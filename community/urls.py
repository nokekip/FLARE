from django.urls import path
from .views import community_home, forum, create_forum, upload_media


urlpatterns = [
    path('', community_home, name='community-home'),
    path('forum/<str:forum_id>/', forum, name='forum'),
    path('create-forum/', create_forum, name='create-forum'),
    path('upload_media/', upload_media, name='upload-media')
]