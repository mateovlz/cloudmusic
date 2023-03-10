from django.urls import path
from cloudmusic import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('song/list/<str:public>', views.SongList.as_view(), name='song-list'),
    path('song/<int:pk>', views.SongDetail.as_view(), name='song-pk'),
    path('song', views.SongDetail.as_view(), name='song'),
    path('signUp', views.UserSignUp.as_view(), name='signUp'),
    path('login', views.UserLogin.as_view(), name="login"),
]

urlpatterns = format_suffix_patterns(urlpatterns)