from .models import Post
from rest_framework import serializers

# Option 1: Nested Serializer (Structured approach)
class AuthorUserSerializer(serializers.Serializer):
    """Serializer for user details within author"""
    id = serializers.IntegerField(source='user.id', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

class PostSerializer(serializers.ModelSerializer):
    # Option 1: Nested author with user data
    author_details = AuthorUserSerializer(source='author', read_only=True)
    
    # Option 2: Flattened fields using source (simpler, no nesting in response)
    author_name = serializers.CharField(source='author.user.name', read_only=True)
    author_email = serializers.CharField(source='author.user.email', read_only=True)
    
    # Option 3: Custom method field (most flexible)
    author_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 
            'title', 
            'created_at',
            # Choose which approach to include:
            'author_details',      # Nested structure
            'author_name',         # Flattened individual fields
            'author_email',        # Flattened individual fields
            'author_info',         # Custom method
        ]
    
    def get_author_info(self, obj):
        """Custom method to return author data in any format you want"""
        return {
            'id': obj.author.user.id,
            'name': obj.author.user.name,
            'email': obj.author.user.email,
            'follower_count': obj.author.follower_count,
        }
        
class PostRawSerializer(serializers.Serializer):
    """Serializer for raw SQL query results"""
    # Base Serializer requires explicit field declarations (no Meta class)
    id = serializers.IntegerField()
    title = serializers.CharField()
    version_title = serializers.CharField(allow_null=True)  # From pv.title
    email = serializers.EmailField()
    name = serializers.CharField()
    website = serializers.URLField(allow_blank=True)
    social_links = serializers.JSONField()

class PostORMSerializer(serializers.Serializer):
    """Serializer for Django ORM query results with flattened author data"""
    # Base Serializer requires explicit field declarations (NO Meta class)
    id = serializers.IntegerField()
    title = serializers.CharField()
    version_title = serializers.CharField(allow_null=True)  # From pv.title
    email = serializers.EmailField(source='author.user.email')
    name = serializers.CharField(source='author.user.name')
    website = serializers.URLField(source='author.website', allow_blank=True)
    social_links = serializers.JSONField(source='author.social_links')
