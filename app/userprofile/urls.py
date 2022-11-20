from django.urls import path
from .views import ProfileView, UserFollow, GetFollowers

urlpatterns = [
    path('details/', ProfileView.as_view(), name='user-details'),
    path('<str:username>/follow/', UserFollow.as_view(), name='follow-user'),
    path('<str:username>/followers/', GetFollowers.as_view(), name='user-followers')
]