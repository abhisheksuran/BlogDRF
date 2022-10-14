from rest_framework import serializers
from core.models import UserProfile
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
