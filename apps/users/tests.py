"""
Additional Django Test Examples for Users App
Demonstrates testing user models, authentication, and relationships
"""

from django.test import TestCase
from django.contrib.auth.hashers import check_password
from rest_framework.test import APITestCase, APIClient
from .models import User, Author


class UserModelTest(TestCase):
    """Test User model functionality"""
    
    def setUp(self):
        """Create test user"""
        self.user = User.objects.create(
            name='John Doe',
            email='john@example.com',
            password='securepass123'
        )
    
    def test_user_creation(self):
        """Test that user is created with correct attributes"""
        self.assertEqual(self.user.name, 'John Doe')
        self.assertEqual(self.user.email, 'john@example.com')
        self.assertIsNotNone(self.user.created_at)
    
    def test_user_str_method(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'John Doe')
    
    def test_user_email_unique(self):
        """Test that email must be unique"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create(
                name='Another User',
                email='john@example.com',  # Duplicate email
                password='password'
            )
    
    def test_password_hashing(self):
        """Test that password is automatically hashed on save"""
        # Password should be hashed, not plain text
        self.assertNotEqual(self.user.password, 'securepass123')
        # Verify password was hashed correctly
        self.assertTrue(check_password('securepass123', self.user.password))
    
    def test_updated_at_changes_on_save(self):
        """Test that updated_at timestamp changes on save"""
        original_updated_at = self.user.updated_at
        
        # Update user
        self.user.name = 'Jane Doe'
        self.user.save()
        
        # updated_at should change
        self.assertNotEqual(self.user.updated_at, original_updated_at)


class AuthorModelTest(TestCase):
    """Test Author model and relationships"""
    
    def setUp(self):
        """Create test user and author"""
        self.user = User.objects.create(
            name='Author User',
            email='author@example.com',
            password='authorpass'
        )
        self.author = Author.objects.create(
            user=self.user,
            website='https://authorblog.com',
            social_links={'twitter': '@author', 'github': 'authordev'}
        )
    
    def test_author_creation(self):
        """Test author is created correctly"""
        self.assertEqual(self.author.user, self.user)
        self.assertEqual(self.author.website, 'https://authorblog.com')
        self.assertEqual(self.author.follower_count, 0)  # Default value
    
    def test_author_str_method(self):
        """Test author string representation uses user name"""
        self.assertEqual(str(self.author), 'Author User')
    
    def test_one_to_one_relationship(self):
        """Test one-to-one relationship between User and Author"""
        # Access author from user
        self.assertEqual(self.user.authors, self.author)
        
        # Cannot create another author with same user
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Author.objects.create(user=self.user)
    
    def test_author_json_field(self):
        """Test JSONField for social links"""
        self.assertIsInstance(self.author.social_links, dict)
        self.assertEqual(self.author.social_links['twitter'], '@author')
        self.assertEqual(self.author.social_links['github'], 'authordev')
    
    def test_author_cascade_delete(self):
        """Test that deleting user also deletes author (CASCADE)"""
        user_id = self.user.id
        author_id = self.author.id
        
        # Delete user
        self.user.delete()
        
        # Author should also be deleted
        self.assertFalse(Author.objects.filter(id=author_id).exists())
    
    def test_update_follower_count(self):
        """Test updating follower count"""
        self.author.follower_count = 150
        self.author.save()
        
        # Refresh from database
        self.author.refresh_from_db()
        self.assertEqual(self.author.follower_count, 150)
    
    def test_update_post_count(self):
        """Test updating post count"""
        self.author.post_count = 25
        self.author.save()
        
        self.author.refresh_from_db()
        self.assertEqual(self.author.post_count, 25)


class UserAPITest(APITestCase):
    """Test User-related API endpoints (if they exist)"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = APIClient()
        self.user = User.objects.create(
            name='API Test User',
            email='apiuser@example.com',
            password='apipass123'
        )
        self.author = Author.objects.create(user=self.user)
    
    def test_user_data_structure(self):
        """Test user data has expected structure"""
        self.assertTrue(hasattr(self.user, 'name'))
        self.assertTrue(hasattr(self.user, 'email'))
        self.assertTrue(hasattr(self.user, 'created_at'))
        self.assertTrue(hasattr(self.user, 'updated_at'))
    
    def test_author_has_user_relationship(self):
        """Test that author correctly links to user"""
        self.assertEqual(self.author.user.email, 'apiuser@example.com')
        self.assertEqual(self.author.user.name, 'API Test User')


class UserQueryTest(TestCase):
    """Test database queries for User model"""
    
    def setUp(self):
        """Create multiple users"""
        self.users = []
        for i in range(5):
            user = User.objects.create(
                name=f'User {i}',
                email=f'user{i}@example.com',
                password='pass123'
            )
            self.users.append(user)
            # Create author for each user
            Author.objects.create(user=user)
    
    def test_get_all_users(self):
        """Test querying all users"""
        users = User.objects.all()
        self.assertEqual(users.count(), 5)
    
    def test_filter_by_email(self):
        """Test filtering users by email"""
        user = User.objects.get(email='user2@example.com')
        self.assertEqual(user.name, 'User 2')
    
    def test_users_ordered_by_created_at(self):
        """Test that users are ordered by created_at DESC"""
        users = User.objects.all()
        # Should be in reverse chronological order
        for i in range(len(users) - 1):
            self.assertGreaterEqual(
                users[i].created_at, 
                users[i + 1].created_at
            )
    
    def test_select_related_author(self):
        """Test using select_related to optimize queries"""
        # This should fetch users with their authors in single query
        users_with_authors = User.objects.select_related('authors').all()
        
        # Access author without additional query
        for user in users_with_authors:
            # This should not trigger additional database queries
            author = user.authors
            self.assertIsNotNone(author)

