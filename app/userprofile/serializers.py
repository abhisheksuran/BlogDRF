from rest_framework import serializers
from core.models import UserProfile, Follower, User
#from  core.models import Blog, Tag, User
# from user.serializers import UserSerializer
# from blog.serializers import TagSerializer, BlogSerializer



# class ProfileSerializer(serializers.ModelSerializer):

#     user = serializers.SerializerMethodField(read_only=True)
#     posts = serializers.SerializerMethodField(read_only=True)
#     tags = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = UserProfile
#         fields = ['user', 'profile_pic', 'about', 'gender', 'posts', 'tags']

#     def get_posts(self, obj):
#         """Get all user posts"""
    
#         return BlogSerializer(obj.user.blog_set.all(), context=self.context, many=True).data
        

#     def get_tags(self, obj):
#         """Get all user tags"""

#         return TagSerializer(obj.user.tag_set.all(), many=True).data
        
#     def get_user(self, obj):
#         # This is where the problem is !!!!
#         user = User.objects.get(id=self.context["request"].user.id)
#         if not user:
#             return None
#         else:
#             return UserSerializer(user).data
        

class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user.email', read_only=True)
    posts = serializers.ListField(source='get_user_blogs', read_only=True)
    tags = serializers.ListField(source='get_user_tags', read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'profile_pic', 'about', 'gender', 'posts', 'tags']


class FollowUserSerializer(serializers.ModelSerializer):
    """Serializer to follow a user"""
    
    following_to = serializers.CharField(read_only=True)
    class Meta:
        model = Follower
        fields = ['following_to', 'created_on']

    def create(self, validated_data):
        auth_user = self.context.get('request').user
        username = self.context.get('view').kwargs.get('username')
        username = User.objects.get(username=username)
        try:
            follow = Follower.objects.get(user=auth_user, following_to=username)
            if follow:
               follow = Follower.objects.get(user=auth_user, following_to=username.id).delete()
        except Follower.DoesNotExist:
            follow = Follower.objects.create(user=auth_user, following_to=username)

        return follow


class GetFollowersForUserSerializer(serializers.ModelSerializer):
    """Serializer for getting followers for a user"""
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Follower
        fields = ['user', 'created_on']
