from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import Post, Comment, Reaction
from .serializers import PostSerializer, CommentSerializer, PostListSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwerOrReadOnly
from rest_framework.decorators import action
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.


class PostViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Post.objects.annotate(
        like_cnt=Count(
            "reactions", filter=Q(reactions__reaction="like"), distinct=True
        ),
        dislike_cnt=Count(
            "reactions", filter=Q(reactions__reaction="dislike"), distinct=True
        ),
        comments_cnt=Count("comments"),
    )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "title"]
    search_fields = ["title", "=title"]
    ordering_fields = ["title", "created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsOwerOrReadOnly()]
        elif self.action in ["likes"]:
            return [IsAuthenticated()]
        return []

    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def likes(self, request, pk=None):
        post = self.get_object()
        reaction = post.reactions.filter(user=request.user, reaction="dislike")
        if reaction.exists():
            reaction.delete()
            Reaction.objects.create(post=post, user=request.user, reaction="like")
        else:
            reaction = post.reactions.filter(user=request.user, reaction="like")
            if reaction.exists():
                reaction.delete()
            else:
                Reaction.objects.create(post=post, user=request.user, reaction="like")
        return Response()

    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def dislikes(self, request, pk=None):
        post = self.get_object()
        reaction = post.reactions.filter(user=request.user, reaction="like")
        if reaction.exists():
            reaction.delete()
            Reaction.objects.create(post=post, user=request.user, reaction="dislike")
        else:
            reaction = post.reactions.filter(user=request.user, reaction="dislike")
            if reaction.exists():
                reaction.delete()
            else:
                Reaction.objects.create(
                    post=post, user=request.user, reaction="dislike"
                )
        return Response()

    @action(methods=["GET"], detail=False)
    def top5(self, request):
        queryset = self.get_queryset().order_by("-like_cnt")[:5]
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsOwerOrReadOnly()]
        return []


class PostCommentViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post_id=post)
        return queryset

    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)
