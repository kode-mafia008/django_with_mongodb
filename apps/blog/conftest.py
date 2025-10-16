"""
Pytest fixtures for blog app tests

Fixtures provide reusable test data and setup.
They help keep tests DRY (Don't Repeat Yourself)
"""

import pytest
from apps.users.models import User, Author
from apps.blog.models import Post, Tag, Category, Comment


@pytest.fixture
def api_client():
    """Returns an API client for testing endpoints"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def test_user(db):
    """Create a test user"""
    return User.objects.create(
        name='Test User',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def test_author(test_user):
    """Create a test author linked to test_user"""
    return Author.objects.create(
        user=test_user,
        website='https://example.com',
        follower_count=50
    )


@pytest.fixture
def test_post(test_author):
    """Create a test post"""
    return Post.objects.create(
        title='Test Post',
        content='Test content for pytest',
        author=test_author
    )


@pytest.fixture
def test_tag(db):
    """Create a test tag"""
    return Tag.objects.create(
        name='Django',
        slug='django',
        color='#092E20'
    )


@pytest.fixture
def test_category(db):
    """Create a test category"""
    return Category.objects.create(
        name='Technology',
        slug='technology',
        description='Tech-related posts'
    )


@pytest.fixture
def multiple_posts(test_author):
    """Create multiple posts for testing lists"""
    posts = []
    for i in range(5):
        post = Post.objects.create(
            title=f'Post {i}',
            content=f'Content {i}',
            author=test_author
        )
        posts.append(post)
    return posts


@pytest.fixture
def authenticated_client(api_client, test_user):
    """Returns an authenticated API client"""
    api_client.force_authenticate(user=test_user)
    return api_client
