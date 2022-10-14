from user.views import UserCreation, UserManage, GetAuthToken
from django.urls import path

urlpatterns = [
    path('register/', UserCreation.as_view(), name='user-register'),
    path('user-edit/', UserManage.as_view(), name='user-edit'),
    path('token/', GetAuthToken.as_view(), name='get-token'),
    ]
