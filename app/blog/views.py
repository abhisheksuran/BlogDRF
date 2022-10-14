from rest_framework import viewsets, mixins, generics, status, response
from blog import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from core.models import Blog, UserComment, Tag
from blog.permissions import EditOwnPost, EditOwnComment, EditOwnReply, UpdateOwnTag
from blog.custom_mixins import RUDMixi
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes
from django.contrib.contenttypes.models import ContentType


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'search',
                OpenApiTypes.STR,
                description='Search for post titles.'
                )
            ]
        )
    )
class BlogView(viewsets.ModelViewSet):
    """Blog View"""
    serializer_class = serializers.BlogDetailedSerializer
    queryset = Blog.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (EditOwnPost, IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = self.queryset.all()
        search = str(self.request.query_params.get('search', ''))
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_serializer_class(self):

        if self.action == 'list':
            return serializers.BlogSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Sets the user profile to logged in user"""
        serializer.save(author=self.request.user)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned', 
                OpenApiTypes.INT, 
                enum=[0,1], 
                description='Search Tags that are assigned or not.'
                )
            ]
        )
    )
class TagView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """View for our post Tags"""
    serializer_class = serializers.TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [UpdateOwnTag, IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete']

    def get_queryset(self):
        assigned = bool(int(self.request.query_params.get('assigned', 0)))
        queryset = Tag.objects.all()
        if assigned:
            queryset = queryset.filter(blog__isnull=False)
        if not assigned:
            queryset = queryset.filter(blog__isnull=True)

        return queryset.filter(user=self.request.user).order_by('caption').distinct()
    


class CommentPerPostListView(generics.ListAPIView):
    """View for creating and retriving comments"""
    serializer_class = serializers.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        blog_type = ContentType.objects.get_for_model(Blog)
       # blog = Blog.objects.get(slug=self.kwargs['slug'])
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
        query_set = UserComment.objects.filter(content_type=blog_type, object_id=blog.id)

        return query_set


class ListCreateUserCommentView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    """List Comments created by a user on a post  or create new one."""
    serializer_class = serializers.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        blog_type = ContentType.objects.get_for_model(Blog)
       # blog = Blog.objects.get(slug=self.kwargs['slug'])
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
       # comments = UserComment.objects.filter(user=self.request.user, content_type=blog_type, object_id=blog.id)
        comments = UserComment.objects.filter(user=self.request.user, content_type=blog_type, object_id=blog.id)
        return comments

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args,**kwargs)

    def perform_create(self, serializer):
        try:
            post = Blog.objects.get(slug=self.kwargs['slug'])
            serializer.save(user=self.request.user, content_object=post)
        except Blog.DoesNotExist:
            pass


class EditUserCommentView(RUDMixi, generics.GenericAPIView):
    """view for individual comment"""
    serializer_class = serializers.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (EditOwnComment, IsAuthenticated,)

    def get_object(self):
        # try:
        #     comments = UserComment.objects.get(id=self.kwargs['pk'] ,post__slug=self.kwargs['slug'])
        # except UserComment.DoesNotExist:
        #     return None
        blog_type = ContentType.objects.get_for_model(Blog)
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
        return get_object_or_404(UserComment, id=self.kwargs['pk'] , content_type=blog_type, object_id=blog.id)


class ListCreateReplyView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    """Create or list Replies for a Comment"""
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print(kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        comment_type = ContentType.objects.get_for_model(UserComment)
        comment = get_object_or_404(UserComment, id=self.kwargs['comment_id'])
        return UserComment.objects.filter(content_type=comment_type, object_id=self.kwargs['comment_id'])

    def perform_create(self, serializer):
        try:
            comment = UserComment.objects.get(id=self.kwargs['comment_id'])
            serializer.save(user=self.request.user, content_object=comment)
        except UserComment.DoesNotExist:
            pass



class EditReplyView(RUDMixi, generics.GenericAPIView):
    """Edit repy or delete reply"""
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [EditOwnReply, IsAuthenticated]

    def get_object(self):
        # try:
        #     return UserReply.objects.get(id=self.kwargs['pk'], comment__id=self.kwargs['comment_id'])
        # except UserReply.DoesNotExist:
        #     return None
        #comment_type = ContentType.objects.get_for_model(UserComment)
        #comment = get_object_or_404(UserComment, id=self.kwargs['comment_id'])
        return get_object_or_404(UserComment, id=self.kwargs['pk'])
