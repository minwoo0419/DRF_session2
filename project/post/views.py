from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostListSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwerOrReadOnly
from rest_framework.decorators import action
from django.db.models import Count
# Create your views here.

class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Post.objects.annotate(like_cnt=Count('like'))
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsOwerOrReadOnly()]
        return []
    @action(['GET'], detail=False)
    def manylike(self, request):
        top_post = self.get_queryset().order_by("-like_cnt")[:3]
        top_post_serializer = PostListSerializer(top_post, many=True)
        return Response(top_post_serializer.data)
    @action(['GET'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.like.all():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
        post.save()
        return Response()

class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsOwerOrReadOnly()]
        return []

class PostCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        movie = self.kwargs.get("movie_id")
        queryset = Comment.objects.filter(movie_id=movie)
        return queryset
    
    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)