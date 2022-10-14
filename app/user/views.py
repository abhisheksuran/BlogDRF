from rest_framework import generics, authentication, permissions, status
from user.serializers import UserSerializer, TokenAuthSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
#from user import serializers
from core.models import User, Blog, UserProfile
#from rest_framework.decorators import api_view


class UserCreation(generics.CreateAPIView):

    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request=request, username=email, password=password)
        tkn = Token.objects.create(user=user)
        return Response({'STATUS': 'User created Successfully!', 'DATA': res.data, 'Auth_Token': str(tkn)}, status=status.HTTP_201_CREATED)


class UserManage(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    #http_method_names = ['get', 'patch']

    def get_object(self):

        return self.request.user


class GetAuthToken(ObtainAuthToken):

    serializer_class = TokenAuthSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
