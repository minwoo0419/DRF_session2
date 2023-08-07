from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    like_cnt = serializers.IntegerField(read_only=True)
    dislike_cnt = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_field = [
            "id",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    def get_post(self, instance):
        return instance.post.title

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_field = [
            "id",
            "created_at",
            "updated_at",
            "post",
        ]


class PostListSerializer(serializers.ModelSerializer):
    comment_cnt = serializers.IntegerField(read_only=True)
    like_cnt = serializers.IntegerField(read_only=True)
    dislike_cnt = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "writer",
            "created_at",
            "updated_at",
            "comment_cnt",
            "like_cnt",
            "dislike_cnt",
        ]
        read_only_field = [
            "id",
            "created_at",
            "updated_at",
        ]
