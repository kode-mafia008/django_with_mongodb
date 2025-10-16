# Interview Answer: Q14 - How do you write effective Django tests?

## Quick Answer (2-3 minutes)

**"I write effective Django tests using Django's TestCase and REST framework's APITestCase. I follow these key practices:"**

---

## 1. Model Tests ✅

```python
from django.test import TestCase
from apps.blog.models import Post
from apps.users.models import User, Author

class PostModelTest(TestCase):
    def setUp(self):
        # Create test data - runs before each test
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(user=self.user)
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.author
        )
    
    def test_post_creation(self):
        """Test basic model creation"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.author)
        self.assertIsNotNone(self.post.created_at)
    
    def test_post_relationships(self):
        """Test model relationships"""
        tags = Tag.objects.create(name='Django', slug='django')
        self.post.tags.add(tags)
        self.assertEqual(self.post.tags.count(), 1)
    
    def test_custom_methods(self):
        """Test custom model methods"""
        stats = PostStatistics.objects.create(post=self.post)
        stats.update_view_count()
        self.assertEqual(stats.view_count, 1)
```

---

## 2. API Tests ✅

```python
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class PostAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='API User',
            email='api@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(user=self.user)
        
        # Authenticate if needed
        # self.client.force_authenticate(user=self.user)
    
    def test_get_post_list(self):
        """Test API endpoint returns correct data"""
        Post.objects.create(
            title='API Post',
            content='Content',
            author=self.author
        )
        
        response = self.client.get('/blog/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
    
    def test_post_serialization(self):
        """Test response includes correct fields"""
        response = self.client.get('/blog/')
        data = response.json()
        
        if len(data) > 0:
            post = data[0]
            self.assertIn('author_name', post)
            self.assertIn('author_email', post)
```

---

## 3. Pytest with Fixtures ✅

```python
# conftest.py
import pytest
from apps.users.models import User, Author
from apps.blog.models import Post

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

# test_models_pytest.py
import pytest

@pytest.mark.django_db
def test_post_list(api_client, test_post):
    """Test using pytest fixtures"""
    response = api_client.get('/blog/')
    assert response.status_code == 200
    assert len(response.json()) >= 1

@pytest.mark.django_db
def test_post_creation(test_author):
    post = Post.objects.create(
        title='New Post',
        content='Content',
        author=test_author
    )
    assert post.title == 'New Post'
    assert post.author == test_author

@pytest.mark.django_db
class TestPostAPI:
    def test_get_posts(self, api_client, test_post):
        response = api_client.get('/blog/')
        assert response.status_code == 200
```

---

## 4. Key Best Practices 🎯

### ✅ Test Structure
```python
class MyTest(TestCase):
    def setUp(self):
        """Initialize test data"""
        pass
    
    def test_specific_behavior(self):
        """Test one thing"""
        pass
```

### ✅ Common Assertions
```python
# Equality
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# Boolean
self.assertTrue(condition)
self.assertFalse(condition)

# Null checks
self.assertIsNone(value)
self.assertIsNotNone(value)

# Collections
self.assertIn(item, collection)
self.assertNotIn(item, collection)

# Exceptions
with self.assertRaises(ValidationError):
    Model.objects.create(invalid_data)

# Comparison
self.assertGreater(a, b)
self.assertLess(a, b)
```

### ✅ Test Edge Cases
```python
def test_unique_constraint(self):
    """Test duplicate email raises error"""
    User.objects.create(email='test@example.com', ...)
    
    from django.db import IntegrityError
    with self.assertRaises(IntegrityError):
        User.objects.create(email='test@example.com', ...)

def test_cascade_delete(self):
    """Test CASCADE behavior"""
    self.user.delete()
    self.assertFalse(Author.objects.filter(user=self.user).exists())
```

### ✅ Test Performance
```python
def test_select_related_optimization(self):
    """Test query optimization"""
    posts = Post.objects.select_related('author__user').all()
    
    # This should not trigger additional queries
    for post in posts:
        author_name = post.author.user.name  # No extra query
```

---

## 5. Running Tests 🚀

```bash
# Django TestCase
python manage.py test                              # All tests
python manage.py test apps.blog                    # Specific app
python manage.py test apps.blog.tests.PostModelTest  # Specific class
python manage.py test --keepdb                     # Keep test DB
python manage.py test --parallel                   # Parallel execution

# Pytest
pytest                                   # All tests
pytest apps/blog/tests.py               # Specific file
pytest -v                               # Verbose
pytest -k "test_post"                   # Match pattern
pytest --cov=apps --cov-report=html     # With coverage

# Coverage
coverage run manage.py test
coverage report
coverage html
```

---

## 6. Interview Talking Points 💡

**When answering, mention:**

1. **Test Types:**
   - Model tests (business logic, relationships)
   - API tests (endpoints, status codes, responses)
   - Integration tests (complete workflows)

2. **Test Organization:**
   - `setUp()` for test data initialization
   - One test per behavior
   - Descriptive test names: `test_what_is_being_tested`

3. **Best Practices:**
   - Test edge cases and error conditions
   - Test relationships (ForeignKey, ManyToMany)
   - Test custom model methods
   - Mock external dependencies
   - Use fixtures for reusable test data

4. **Tools:**
   - Django TestCase for database tests
   - APITestCase for REST API tests
   - pytest for fixture-based tests
   - coverage.py for code coverage

5. **CI/CD:**
   - Run tests automatically in CI pipeline
   - Maintain 80%+ code coverage
   - Keep tests fast (parallel execution)

---

## 7. Example Project Structure 📁

```
project/
├── apps/
│   ├── blog/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── tests.py          # Django TestCase
│   │   └── conftest.py        # Pytest fixtures
│   └── users/
│       ├── models.py
│       └── tests.py
├── manage.py
├── pytest.ini                 # Pytest config
└── .coveragerc               # Coverage config
```

---

## 8. Quick Reference Card 📋

| Aspect | Approach |
|--------|----------|
| **Test Framework** | Django TestCase, APITestCase, pytest |
| **Setup Data** | `setUp()` method or pytest fixtures |
| **Test Database** | Automatic creation/destruction |
| **Assertions** | `assertEqual`, `assertTrue`, `assertIn`, etc. |
| **API Testing** | APIClient with force_authenticate |
| **Mocking** | `unittest.mock` or `pytest-mock` |
| **Coverage** | coverage.py with 80%+ target |
| **CI/CD** | GitHub Actions, GitLab CI |

---

## Summary Statement for Interview

**"In my Django project, I implement comprehensive testing using Django's TestCase for model tests and APITestCase for REST API endpoints. I follow TDD principles, writing tests for models, relationships, custom methods, and API endpoints. I use setUp() for test data initialization, write descriptive test names, and test edge cases including constraints and cascade deletes. I also use pytest with fixtures for more complex scenarios and maintain high code coverage using coverage.py. All tests are integrated into our CI/CD pipeline to ensure code quality."**

---

## Files to Review Before Interview

1. ✅ `apps/blog/tests.py` - 500+ lines of comprehensive examples
2. ✅ `apps/users/tests.py` - User/Author model tests
3. ✅ `apps/blog/conftest.py` - Pytest fixtures
4. ✅ `TESTING_GUIDE.md` - Detailed guide

**Practice running:**
```bash
python manage.py test apps.blog -v
python manage.py test apps.users -v
```
