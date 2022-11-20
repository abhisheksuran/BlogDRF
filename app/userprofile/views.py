from rest_framework import generics, authentication, permissions, mixins
from .serializers import ProfileSerializer, GetFollowersForUserSerializer, FollowUserSerializer
from .permissions import ViewOwnDetails
from  core.models import UserProfile, Follower, User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (ViewOwnDetails, permissions.IsAuthenticated,)
    http_method_names = ['get', 'patch']


    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


# @api_view(['GET'])
# def ProfileView(request, *arg, **kwargs):

#     serializer = ProfileSerializer(data=request.data, context={'request': request})
#     if serializer.is_valid(raise_exception= True):
#         instance = UserProfile.objects.get(user=request.user)
#         data = serializer.data
#         return Response(data)


class UserFollow(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):

    """follow/unfollow a user with a POST request, get list of users followed by a user with GET request"""


    serializer_class = FollowUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        q = Follower.objects.filter(user=user)

        return q

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        follow_to = get_object_or_404(User, username=self.kwargs['username'])
        serializer.save()


class GetFollowers(generics.ListAPIView):

    """Get all followers of a user"""
    serializer_class = GetFollowersForUserSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        followers = Follower.objects.filter(following_to=user)
        return followers
