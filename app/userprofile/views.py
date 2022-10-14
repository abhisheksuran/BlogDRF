from rest_framework import generics, authentication, permissions
from .serializers import ProfileSerializer
from .permissions import ViewOwnDetails
from  core.models import UserProfile


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


