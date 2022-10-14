from rest_framework import serializers
from core.models import Blog, Tag, UserComment
from user.serializers import UserSerializer


# class CommentRelatedField(serializers.RelatedField):
#     """Custom field for GenericForeignKey"""
#     def to_representation(self, value):
#         """Serialize comment object"""
#         print(value)
#         if isinstance(value, UserComment):
#             serializer = CommentSerializer(value)
#         elif isinstance(value, Blog):
#             serializer = BlogSerializer(value)
#         else:
#             raise Exception('Unexpected type of commented_on object')
#         return serializer.data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['pk', 'caption']
      

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    updated = serializers.BooleanField(read_only=True)
    

    class Meta:
        model = Blog
        fields = ['url', 'image',  'title', 'author', 'tags', 'created_on', 'updated']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def _get_or_create_tags(self, tags, instance):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            instance.tags.add(tag_obj)

    def create(self, validate_data):
        tags = validate_data.pop('tags', [])
        blog = Blog.objects.create(**validate_data)
        self._get_or_create_tags(tags, blog)

        return blog

    def update(self, instance, validated_data):
        setattr(instance, 'updated', True)
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class BlogDetailedSerializer(BlogSerializer):

    class Meta(BlogSerializer.Meta):
        fields = BlogSerializer.Meta.fields + ['sub_title', 'content']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for user comments"""
    user = serializers.CharField(read_only=True)
    updated = serializers.BooleanField(read_only=True)
    commented_on = serializers.CharField(source='content_object.id', read_only=True)
    # root_comment = CommentRelatedField(many=True, queryset=UserComment.objects.all())


    class Meta:
        model = UserComment
        fields = ['pk', 'user', 'content', 'updated' , 'created_on', 'commented_on']

    def update(self, instance, validated_data):
            setattr(instance, 'updated', True)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            return instance

