# Django Testing Guide - Interview Question Q14

## Q14: How do you write effective Django tests?

This guide demonstrates comprehensive Django testing strategies with practical examples from this project.

---

## Table of Contents

1. [Testing Fundamentals](#testing-fundamentals)
2. [Types of Tests](#types-of-tests)
3. [Test Setup](#test-setup)
4. [Running Tests](#running-tests)
5. [Best Practices](#best-practices)
6. [Common Patterns](#common-patterns)
7. [Pytest vs Django TestCase](#pytest-vs-django-testcase)

---

## Testing Fundamentals

### Why Test?

- **Catch bugs early**: Find issues before production
- **Refactor confidently**: Change code without fear
- **Documentation**: Tests show how code should work
- **Regression prevention**: Ensure old bugs don't return

### Django Test Framework

Django provides:
- **TestCase**: Full-featured test class with database transactions
- **TransactionTestCase**: For testing transaction-specific behavior
- **SimpleTestCase**: Lightweight, no database access
- **LiveServerTestCase**: For integration testing with Selenium

---

## Types of Tests

### 1. Model Tests

Test model creation, methods, and relationships:

```python
from django.test import TestCase
from apps.blog.models import Post
from apps.users.models import User, Author

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass'
        )
        self.author = Author.objects.create(user=self.user)
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.author
        )
    
    def test_post_creation(self):
        """Test post is created correctly"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.author)
        self.assertIsNotNone(self.post.created_at)
    
    def test_post_str_method(self):
        """Test __str__ returns title"""
        self.assertEqual(str(self.post), 'Test Post')
```

### 2. API Tests

Test REST API endpoints:

```python
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class PostAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test data
        self.user = User.objects.create(
            name='API User',
            email='api@example.com',
            password='testpass'
        )
        self.author = Author.objects.create(user=self.user)
    
    def test_get_post_list(self):
        """Test retrieving post list"""
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
```

### 3. Integration Tests

Test complete workflows:

```python
class BlogIntegrationTest(TestCase):
    def test_complete_workflow(self):
        """Test: create user -> create post -> add comment"""
        # 1. Create user
        user = User.objects.create(...)
        author = Author.objects.create(user=user)
        
        # 2. Create post
        post = Post.objects.create(title='Test', author=author)
        
        # 3. Add comment
        comment = Comment.objects.create(
            post=post,
            author=author,
            content='Great post!'
        )
        
        # Verify workflow
        self.assertEqual(post.comments.count(), 1)
```

### 4. View Tests

Test Django views:

```python
from django.test import Client

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')
```

---

## Test Setup

### setUp() Method

Runs before **each** test method:

```python
class MyTest(TestCase):
    def setUp(self):
        """Runs before each test_* method"""
        self.user = User.objects.create(...)
        self.client = APIClient()
    
    def test_something(self):
        # self.user is available here
        pass
```

### setUpTestData() Method

Runs **once** for the entire test class (faster for read-only data):

```python
class MyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Runs once for all tests in class"""
        cls.user = User.objects.create(...)
    
    def test_something(self):
        # self.user is available (but don't modify it!)
        pass
```

---

## Running Tests

### Django Test Commands

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test apps.blog

# Run specific test class
python manage.py test apps.blog.tests.PostModelTest

# Run specific test method
python manage.py test apps.blog.tests.PostModelTest.test_post_creation

# Run with verbosity
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb

# Run tests in parallel
python manage.py test --parallel
```

### Pytest Commands

```bash
# Install pytest-django first
pip install pytest pytest-django

# Run all tests
pytest

# Run specific file
pytest apps/blog/tests.py

# Run with verbose output
pytest -v

# Run specific test
pytest apps/blog/tests.py::PostModelTest::test_post_creation

# Run with coverage
pytest --cov=apps --cov-report=html

# Run with print statements
pytest -s
```

---

## Best Practices

### 1. Test One Thing Per Test

❌ **Bad:**
```python
def test_everything(self):
    post = Post.objects.create(...)
    self.assertEqual(post.title, 'Test')
    comment = Comment.objects.create(...)
    self.assertEqual(comment.post, post)
    self.assertTrue(post.published)
```

✅ **Good:**
```python
def test_post_creation(self):
    post = Post.objects.create(...)
    self.assertEqual(post.title, 'Test')

def test_comment_creation(self):
    comment = Comment.objects.create(...)
    self.assertEqual(comment.post, self.post)

def test_post_is_published(self):
    self.assertTrue(self.post.published)
```

### 2. Use Descriptive Names

```python
# Good test names
def test_user_cannot_delete_other_users_posts(self)
def test_password_is_hashed_on_save(self)
def test_post_with_no_tags_returns_empty_list(self)
```

### 3. Test Edge Cases

```python
def test_empty_title(self):
    """Test post with empty title raises validation error"""
    with self.assertRaises(ValidationError):
        Post.objects.create(title='', content='Test')

def test_very_long_title(self):
    """Test post with title exceeding max_length"""
    long_title = 'x' * 201  # max_length is 200
    with self.assertRaises(ValidationError):
        Post.objects.create(title=long_title, content='Test')
```

### 4. Use Assertions Effectively

```python
# Common assertions
self.assertEqual(a, b)
self.assertNotEqual(a, b)
self.assertTrue(x)
self.assertFalse(x)
self.assertIsNone(x)
self.assertIsNotNone(x)
self.assertIn(item, list)
self.assertNotIn(item, list)
self.assertRaises(Exception)
self.assertGreater(a, b)
self.assertLess(a, b)
```

### 5. Test Relationships

```python
def test_post_author_relationship(self):
    """Test ForeignKey relationship"""
    self.assertEqual(self.post.author, self.author)
    self.assertIn(self.post, self.author.posts.all())

def test_post_tags_many_to_many(self):
    """Test ManyToMany relationship"""
    tag = Tag.objects.create(name='Django')
    self.post.tags.add(tag)
    self.assertEqual(self.post.tags.count(), 1)
    self.assertIn(tag, self.post.tags.all())
```

### 6. Test Custom Methods

```python
class PostStatisticsTest(TestCase):
    def test_increment_view_count(self):
        """Test custom increment method"""
        initial = self.stats.view_count
        self.stats.update_view_count()
        self.assertEqual(self.stats.view_count, initial + 1)
```

### 7. Test Query Performance

```python
def test_select_related_optimization(self):
    """Test that select_related reduces queries"""
    from django.test.utils import override_settings
    from django.db import connection
    
    # Enable query logging
    with self.assertNumQueries(1):
        posts = Post.objects.select_related('author__user').all()
        list(posts)  # Force evaluation
```

### 8. Mock External Dependencies

```python
from unittest.mock import patch, Mock

class ExternalAPITest(TestCase):
    @patch('requests.get')
    def test_api_call(self, mock_get):
        """Test external API call with mock"""
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'ok'}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Call function that uses requests.get
        result = fetch_data_from_api()
        self.assertEqual(result['status'], 'ok')
```

---

## Common Patterns

### Testing Unique Constraints

```python
def test_unique_email_constraint(self):
    """Test email uniqueness"""
    User.objects.create(email='test@example.com', ...)
    
    from django.db import IntegrityError
    with self.assertRaises(IntegrityError):
        User.objects.create(email='test@example.com', ...)
```

### Testing Cascade Delete

```python
def test_cascade_delete(self):
    """Test CASCADE on_delete behavior"""
    user_id = self.user.id
    post_id = self.post.id
    
    self.user.delete()
    
    # Post should be deleted too
    self.assertFalse(Post.objects.filter(id=post_id).exists())
```

### Testing Signals

```python
from django.test import override_settings

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_signal_creates_notification(self):
    """Test signal creates notification on comment"""
    comment = Comment.objects.create(...)
    
    # Check notification was created by signal
    notification = Notification.objects.filter(
        content_object_id=comment.post.id
    )
    self.assertTrue(notification.exists())
```

### Testing Authentication

```python
class AuthenticatedAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(...)
        self.client.force_authenticate(user=self.user)
    
    def test_authenticated_request(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 200)
```

---

## Pytest vs Django TestCase

### Pytest with Fixtures

**Advantages:**
- Reusable fixtures
- Cleaner syntax
- Better parametrization
- Rich plugin ecosystem

**Example:**

```python
# conftest.py
import pytest

@pytest.fixture
def user(db):
    return User.objects.create(
        name='Test User',
        email='test@example.com'
    )

@pytest.fixture
def author(user):
    return Author.objects.create(user=user)

# test_models.py
import pytest

@pytest.mark.django_db
def test_post_creation(author):
    post = Post.objects.create(
        title='Test',
        author=author
    )
    assert post.title == 'Test'
    assert post.author == author

@pytest.mark.django_db
class TestPost:
    def test_create(self, author):
        post = Post.objects.create(title='Test', author=author)
        assert post.id is not None
```

### Django TestCase

**Advantages:**
- Built into Django
- Transactional test cases
- setUp/tearDown hooks
- Familiar Django patterns

**Example:**

```python
class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(...)
        self.author = Author.objects.create(user=self.user)
    
    def test_post_creation(self):
        post = Post.objects.create(
            title='Test',
            author=self.author
        )
        self.assertEqual(post.title, 'Test')
```

---

## Test Coverage

### Install Coverage

```bash
pip install coverage
```

### Run Tests with Coverage

```bash
# Run tests with coverage
coverage run --source='.' manage.py test

# Generate report
coverage report

# Generate HTML report
coverage html

# Open HTML report
open htmlcov/index.html
```

### Coverage Configuration (.coveragerc)

```ini
[run]
source = .
omit =
    */migrations/*
    */tests/*
    */venv/*
    manage.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test
    
    - name: Run coverage
      run: |
        coverage run manage.py test
        coverage report
```

---

## Summary: Key Takeaways

1. ✅ **Test models**: Creation, relationships, custom methods
2. ✅ **Test APIs**: Endpoints, status codes, response data
3. ✅ **Use setUp()**: Initialize test data efficiently
4. ✅ **Test one thing**: Each test should have single purpose
5. ✅ **Descriptive names**: `test_what_is_being_tested`
6. ✅ **Test edge cases**: Empty values, boundaries, errors
7. ✅ **Mock external**: Don't call real APIs in tests
8. ✅ **Check coverage**: Aim for 80%+ coverage
9. ✅ **Run regularly**: Include in CI/CD pipeline
10. ✅ **Keep fast**: Tests should run quickly

---

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-django](https://pytest-django.readthedocs.io/)

---

## Files in This Project

- `apps/blog/tests.py` - Comprehensive blog app tests
- `apps/blog/conftest.py` - Pytest fixtures for blog app
- `apps/users/tests.py` - User and author model tests
- `TESTING_GUIDE.md` - This guide

**Run the tests:**
```bash
# Django way
python manage.py test apps.blog
python manage.py test apps.users

# Pytest way
pytest apps/blog/tests.py -v
pytest apps/users/tests.py -v
```
