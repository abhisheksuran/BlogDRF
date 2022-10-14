from rest_framework import serializers
from core.models import UserProfile, Blog, Tag, User
from user.serializers import UserSerializer
from blog.serializers import TagSerializer, BlogSerializer



class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField(read_only=True)
    posts = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'profile_pic', 'about', 'gender', 'posts', 'tags']

    def get_posts(self, obj):
        """Get all user posts"""
        posts = Blog.objects.filter(author=self.context["request"].user)
    
        #posts = posts.values('user__blog__title')
        if not posts:
            return None
        else:
            data = []
            for d in posts.filter():
                data.append(BlogSerializer(d, context=self.context).data['url'])
            return data
            return BlogSerializer(posts.filter(), context=self.context).data
        #return BlogSerializer(obj.user.blog_set.all(), context=self.context, many=True).data
        

    def get_tags(self, obj):
        """Get all user tags"""

        tags = Tag.objects.filter(user=self.context["request"].user)
        if not tags:
            return None
        else:
            data = []
            for d in tags.filter():
                data.append(TagSerializer(d).data['caption'])
            return data
            #return TagSerializer(tags.get()).data
        
    def get_user(self, obj):
        # This is where the problem is !!!!
        user = User.objects.get(id=self.context["request"].user.id)
        if not user:
            return None
        else:
            return UserSerializer(user).data
        
