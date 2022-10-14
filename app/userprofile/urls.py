from django.urls import path
from .views import ProfileView

urlpatterns = [
    path('details/', ProfileView.as_view(), name='user-details'),
]