from rest_framework import serializers
from .models import Author, Post

class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    author = AuthorSerializer()

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author = Author.objects.create(**author_data)
        post = Post.objects.create(author=author, **validated_data)
        return post

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        if author_data:
            instance.author.name = author_data.get('name', instance.author.name)
            instance.author.save()
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)
        
        # Replace the 'author' object with just the author's name
        representation['author'] = instance.author.name
        created_at_human_readable = instance.created_at.strftime("%B %d, %Y")
        representation['created_at'] = created_at_human_readable

        return representation
