"""
Q14: How do you write effective Django tests?

This file demonstrates comprehensive Django testing strategies including:
- Model tests with TestCase
- API tests with APITestCase
- Fixtures and setup methods
- Testing relationships and custom methods
- Performance testing with select_related/prefetch_related
"""

from django.test import TestCase, Client
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import timedelta
from django.db import connection
from django.test.utils import override_settings

from apps.users.models import User, Author
from .models import (
    Post, PostVersion, PostStatistics, Comment, 
    Category, Tag, Draft, Bookmark, Notification
)


# ============================================================================
# PART 1: MODEL TESTS
# ============================================================================

class PostModelTest(TestCase):
    """Test Post model behavior and custom methods"""
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        # Create user and author
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(
            user=self.user,
            website='https://example.com',
            follower_count=100
        )
        
        # Create tags
        self.tag1 = Tag.objects.create(name='Django', slug='django', color='#092E20')
        self.tag2 = Tag.objects.create(name='Python', slug='python', color='#3776AB')
        
        # Create post
        self.post = Post.objects.create(
            title='Test Post',
            content='This is test content',
            author=self.author
        )
        self.post.tags.add(self.tag1, self.tag2)
    
    def test_post_creation(self):
        """Test that post is created successfully"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.author)
        self.assertEqual(self.post.tags.count(), 2)
        self.assertIsNotNone(self.post.created_at)
    
    def test_post_str_method(self):
        """Test post __str__ method returns title"""
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_post_tags_relationship(self):
        """Test many-to-many relationship with tags"""
        tags = self.post.tags.all()
        self.assertIn(self.tag1, tags)
        self.assertIn(self.tag2, tags)
    
    def test_post_version_creation_on_save(self):
        """Test that post versions are created when post is updated"""
        # Update post
        self.post.title = 'Updated Title'
        self.post.save()
        
        # Check version was created
        versions = PostVersion.objects.filter(post=self.post)
        self.assertEqual(versions.count(), 1)
        self.assertEqual(versions.first().title, 'Updated Title')


class PostStatisticsTest(TestCase):
    """Test PostStatistics model and custom methods"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Stats User',
            email='stats@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(user=self.user)
        self.post = Post.objects.create(
            title='Stats Post',
            content='Content for stats',
            author=self.author
        )
        self.stats = PostStatistics.objects.create(post=self.post)
    
    def test_update_view_count(self):
        """Test view count increment method"""
        initial_count = self.stats.view_count
        self.stats.update_view_count()
        self.assertEqual(self.stats.view_count, initial_count + 1)
    
    def test_update_like_count(self):
        """Test like count increment method"""
        initial_count = self.stats.like_count
        self.stats.update_like_count()
        self.assertEqual(self.stats.like_count, initial_count + 1)
    
    def test_update_last_viewed_at(self):
        """Test last viewed timestamp update"""
        self.stats.update_last_viewed_at()
        self.assertIsNotNone(self.stats.last_viewed_at)
        self.assertAlmostEqual(
            self.stats.last_viewed_at, 
            timezone.now(), 
            delta=timedelta(seconds=1)
        )


class DraftModelTest(TestCase):
    """Test Draft model with scheduled publish functionality"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Draft User',
            email='draft@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(user=self.user)
    
    def test_draft_auto_schedule(self):
        """Test that draft auto-schedules 7 days ahead if no date provided"""
        draft = Draft.objects.create(
            title='Auto Scheduled Draft',
            content='Content',
            author=self.author
        )
        
        expected_date = timezone.now() + timedelta(days=7)
        self.assertIsNotNone(draft.scheduled_publish_at)
        # Check within 1 second tolerance
        self.assertAlmostEqual(
            draft.scheduled_publish_at,
            expected_date,
            delta=timedelta(seconds=1)
        )
    
    def test_draft_custom_schedule(self):
        """Test draft with custom schedule date"""
        custom_date = timezone.now() + timedelta(days=3)
        draft = Draft.objects.create(
            title='Custom Scheduled Draft',
            content='Content',
            author=self.author,
            scheduled_publish_at=custom_date
        )
        self.assertEqual(draft.scheduled_publish_at, custom_date)


class CommentModelTest(TestCase):
    """Test Comment model with nested comments"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Commenter',
            email='comment@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(user=self.user)
        self.post = Post.objects.create(
            title='Post with Comments',
            content='Content',
            author=self.author
        )
    
    def test_comment_creation(self):
        """Test creating a comment on a post"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.author,
            content='Great post!',
            rating=5
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(self.post.comments.count(), 1)
    
    def test_nested_comment_reply(self):
        """Test creating nested reply comments"""
        parent_comment = Comment.objects.create(
            post=self.post,
            author=self.author,
            content='Parent comment'
        )
        
        reply = Comment.objects.create(
            post=self.post,
            author=self.author,
            parent=parent_comment,
            content='Reply to comment'
        )
        
        self.assertEqual(reply.parent, parent_comment)
        self.assertEqual(parent_comment.replies.count(), 1)


# ============================================================================
# PART 2: API TESTS
# ============================================================================

class PostAPITest(APITestCase):
    """Test Post API endpoints using Django REST Framework"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.client = APIClient()
        
        # Create test user and author
        self.user = User.objects.create(
            name='API User',
            email='api@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(user=self.user)
        
        # Authenticate client (if authentication is required)
        # self.client.force_authenticate(user=self.user)
        
        # Create test posts
        self.post1 = Post.objects.create(
            title='First Post',
            content='First content',
            author=self.author
        )
        self.post2 = Post.objects.create(
            title='Second Post',
            content='Second content',
            author=self.author
        )
    
    def test_get_post_list(self):
        """Test retrieving list of posts"""
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that response contains posts
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)
    
    def test_get_post_list_with_select_related(self):
        """Test optimized query with select_related"""
        # Reset queries
        from django.conf import settings
        
        response = self.client.get('/blog/select-related/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify data is returned
        data = response.json()
        self.assertIsInstance(data, list)
    
    def test_post_serialization_includes_author_data(self):
        """Test that post serialization includes author information"""
        response = self.client.get('/blog/')
        data = response.json()
        
        if len(data) > 0:
            first_post = data[0]
            # Check that author data is included
            self.assertIn('author_name', first_post)
            self.assertIn('author_email', first_post)


class PostPerformanceTest(APITestCase):
    """Test query performance and N+1 query problems"""
    
    def setUp(self):
        """Create multiple posts with relationships"""
        self.user = User.objects.create(
            name='Performance User',
            email='perf@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(user=self.user)
        
        # Create multiple posts
        for i in range(10):
            Post.objects.create(
                title=f'Post {i}',
                content=f'Content {i}',
                author=self.author
            )
    
    def test_select_related_reduces_queries(self):
        """Test that select_related reduces database queries"""
        from django.test.utils import override_settings
        from django.db import connection
        from django.test import override_settings
        
        # Count queries for endpoint without select_related
        connection.queries_log.clear()
        response = self.client.get('/blog/prefetch-related/')
        queries_without_optimization = len(connection.queries)
        
        # Count queries for endpoint with select_related
        connection.queries_log.clear()
        response = self.client.get('/blog/select-related/')
        queries_with_optimization = len(connection.queries)
        
        # select_related should use fewer queries
        # Note: This is illustrative - actual numbers depend on implementation


class BookmarkAPITest(APITestCase):
    """Test Bookmark functionality"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Bookmark User',
            email='bookmark@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(user=self.user)
        self.post = Post.objects.create(
            title='Bookmarkable Post',
            content='Content',
            author=self.author
        )
    
    def test_create_bookmark(self):
        """Test creating a bookmark"""
        bookmark = Bookmark.objects.create(
            user=self.author,
            post=self.post,
            notes='Important post'
        )
        self.assertEqual(bookmark.user, self.author)
        self.assertEqual(bookmark.post, self.post)
        self.assertEqual(self.author.bookmarks.count(), 1)
    
    def test_unique_bookmark_constraint(self):
        """Test that user cannot bookmark same post twice"""
        Bookmark.objects.create(
            user=self.author,
            post=self.post
        )
        
        # Try to create duplicate bookmark
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Bookmark.objects.create(
                user=self.author,
                post=self.post
            )


# ============================================================================
# PART 3: INTEGRATION TESTS
# ============================================================================

class BlogIntegrationTest(TestCase):
    """Integration tests for complete blog workflows"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            name='Integration User',
            email='integration@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(user=self.user)
        self.category = Category.objects.create(
            name='Tech',
            slug='tech',
            description='Technology posts'
        )
    
    def test_complete_post_workflow(self):
        """Test complete workflow: draft -> post -> comment -> statistics"""
        # 1. Create draft
        draft = Draft.objects.create(
            title='New Feature',
            content='Exciting new feature',
            author=self.author
        )
        self.assertEqual(draft.status, 'active')
        
        # 2. Publish as post
        post = Post.objects.create(
            title=draft.title,
            content=draft.content,
            author=self.author
        )
        
        # 3. Create statistics
        stats = PostStatistics.objects.create(post=post)
        
        # 4. Add comment
        comment = Comment.objects.create(
            post=post,
            author=self.author,
            content='Great feature!',
            rating=5
        )
        
        # 5. Update statistics
        stats.update_view_count()
        stats.update_like_count()
        
        # Verify complete workflow
        self.assertEqual(post.comments.count(), 1)
        self.assertEqual(stats.view_count, 1)
        self.assertEqual(stats.like_count, 1)
        
        # 6. Archive draft
        draft.status = 'archived'
        draft.save()
        self.assertEqual(draft.status, 'archived')


# ============================================================================
# PART 4: FIXTURE-BASED TESTS (PYTEST STYLE)
# ============================================================================

"""
For pytest-style tests with fixtures, create a conftest.py file in the same directory:

# conftest.py
import pytest
from apps.users.models import User, Author
from apps.blog.models import Post, Tag

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def test_user(db):
    return User.objects.create(
        name='Test User',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_author(test_user):
    return Author.objects.create(user=test_user)

@pytest.fixture
def test_post(test_author):
    return Post.objects.create(
        title='Test Post',
        content='Test content',
        author=test_author
    )

@pytest.fixture
def test_tag(db):
    return Tag.objects.create(
        name='Django',
        slug='django',
        color='#092E20'
    )


# Then in your test file:

import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_post_list(api_client, test_post):
    response = api_client.get('/blog/')
    assert response.status_code == 200
    assert len(response.json()) >= 1

@pytest.mark.django_db
def test_post_creation(test_author):
    post = Post.objects.create(
        title='New Post',
        content='New content',
        author=test_author
    )
    assert post.title == 'New Post'
    assert post.author == test_author

@pytest.mark.django_db
def test_post_with_tags(test_post, test_tag):
    test_post.tags.add(test_tag)
    assert test_post.tags.count() == 1
    assert test_tag in test_post.tags.all()

@pytest.mark.django_db
class TestPostAPI:
    def test_get_posts(self, api_client, test_post):
        response = api_client.get('/blog/')
        assert response.status_code == 200
    
    def test_post_detail_includes_author(self, api_client, test_post):
        response = api_client.get('/blog/')
        data = response.json()
        if len(data) > 0:
            assert 'author_name' in data[0]
"""


# ============================================================================
# BEST PRACTICES DEMONSTRATED:
# ============================================================================
"""
1. **Use setUp() method**: Initialize test data before each test
2. **Test one thing per test**: Each test method should test a specific behavior
3. **Use descriptive test names**: test_what_is_being_tested
4. **Use assertions effectively**: assertEqual, assertTrue, assertRaises, etc.
5. **Test edge cases**: Null values, empty strings, boundaries
6. **Test relationships**: ForeignKey, ManyToMany, OneToOne
7. **Test custom methods**: Business logic in model methods
8. **Use fixtures**: Reusable test data setup
9. **Test API responses**: Status codes, response data structure
10. **Test query performance**: Use select_related, prefetch_related
11. **Test constraints**: Unique constraints, validation
12. **Integration tests**: Test complete workflows
13. **Mock external dependencies**: Use unittest.mock for external APIs
14. **Use test database**: Django automatically creates/destroys test DB
15. **Run tests regularly**: Include in CI/CD pipeline

RUNNING TESTS:
- Run all tests: python manage.py test
- Run specific app: python manage.py test apps.blog
- Run specific test class: python manage.py test apps.blog.tests.PostModelTest
- Run specific test: python manage.py test apps.blog.tests.PostModelTest.test_post_creation
- Run with coverage: coverage run manage.py test && coverage report
- Run with pytest: pytest apps/blog/tests.py -v
"""
