from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Hash password only for new users
        is_new = not self.pk
        if is_new:
            self.password = make_password(self.password)
        
        # Save the user first
        super().save(*args, **kwargs)
 
    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authors')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    website = models.URLField(blank=True)
    social_links = models.JSONField(default=dict)  # JSONField
    follower_count = models.PositiveIntegerField(default=0)
    post_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.name
    
    class Meta:
        db_table = "authors"
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["-created_at"]
