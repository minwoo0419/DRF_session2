from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    like_cnt = serializers.SerializerMethodField()
    def get_like_cnt(self, instance):
        return instance.like.count()
    class Meta:
        model = Post
        fields = '__all__'
        read_only_field = ['id', 'created_at', 'updated_at','like_cnt']

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    def get_post(self, instance):
        return instance.post.title
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_field = ['id', 'created_at', 'updated_at', 'post']

class PostListSerializer(serializers.ModelSerializer):
    comment_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    def get_comment_cnt(self, instance):
        return instance.comments.count()
    def get_like_cnt(self, instance):
        return instance.like_cnt
    class Meta:
        model = Post
        fields = ['id', 'title', 'writer', 'created_at', 'updated_at', 'comment_cnt', 'like_cnt']
        read_only_field = ['id', 'created_at', 'updated_at', 'comment_cnt','like_cnt']