from django.db import models
from apps.users.models import Author
from django.utils import timezone
from datetime import timedelta 

 
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-created_at"]

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, default='#000000')  # Hex color
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tags"
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["-name"]



class Draft(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    scheduled_publish_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "drafts"
        verbose_name = "Draft"
        verbose_name_plural = "Drafts"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.scheduled_publish_at:
            self.scheduled_publish_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.versions.update_or_create(version_number=self.versions.count() + 1, defaults={'title': self.title, 'content': self.content, 'created_by': self.author})
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = "posts"
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]

class PostVersion(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='versions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    version_number = models.PositiveIntegerField()
    created_by = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.post.title} - Version {self.version_number}"
    
    class Meta:
        db_table = "post_versions"
        verbose_name = "Post Version"
        verbose_name_plural = "Post Versions"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.version_number:
            self.version_number = self.post.versions.count() + 1
        super().save(*args, **kwargs) 
    
    def delete(self, *args, **kwargs):
        self.post.versions.remove(self)
        super().delete(*args, **kwargs)


class PostStatistics(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='statistics')
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    avg_read_time = models.DurationField(null=True)
    last_viewed_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"{self.post.title} - Statistics"
    
    class Meta:
        db_table = "post_statistics"
        verbose_name = "Post Statistics"
        verbose_name_plural = "Post Statistics"
        ordering = ["-view_count"]
    
    def update_view_count(self):
        self.view_count += 1
        self.save()
    
    def update_like_count(self):
        self.like_count += 1
        self.save()
    
    def update_share_count(self):
        self.share_count += 1
        self.save()
    
    def update_avg_read_time(self):
        self.avg_read_time = self.post.statistics.avg_read_time
        self.save()
    
    def update_last_viewed_at(self):
        self.last_viewed_at = timezone.now()
        self.save()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
    class Meta:
        db_table = "comments"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]


class Bookmark(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = "bookmarks"
        unique_together = [['user', 'post']]
        indexes = [models.Index(fields=['user', 'created_at'])]


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('comment', 'New Comment'),
        ('like', 'Post Liked'),
        ('follow', 'New Follower'),
        ('bookmark', 'New Bookmark'),
        ('share', 'Post Shared'),
    ]
    recipient = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20,default='like', choices=NOTIFICATION_TYPES)
    content_object_id = models.PositiveIntegerField()  # Generic FK pattern
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]

class PostSchedule(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='schedules')
    scheduled_for = models.DateTimeField(db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    retry_count = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        db_table = "post_schedules"
        verbose_name = "Post Schedule"
        verbose_name_plural = "Post Schedules"
        ordering = ["-scheduled_for"]



# SQL Queries
'''

SELECT 
p.title,
pv.title 
FROM posts AS p
LEFT JOIN  post_versions AS pv
ON p.id=pv.id;

SELECT 
p.title,
pv.title 
FROM posts AS p
RIGHT JOIN  post_versions AS pv
ON p.id=pv.id;

SELECT 
p.title,
pv.title 
FROM posts AS p
FULL OUTER JOIN post_versions AS pv
ON p.id=pv.id;

SELECT 
p.title,
pv.title 
FROM posts AS p
CROSS JOIN  post_versions AS pv;

SELECT 
p.title,
pv.title 
FROM posts AS p
LEFT JOIN  post_versions AS pv ON p.id=pv.id
LEFT JOIN notifications AS n ON p.id=n.content_object_id;

SELECT 
p.id,
p.title,
pv.title AS version_title,
u.email,u.name,
a.website,
a.social_links 
FROM posts AS p
LEFT JOIN  post_versions AS pv ON p.id = pv.id
INNER JOIN authors AS a ON p.author_id=a.id
INNER JOIN users AS u ON a.user_id=u.id
WHERE u.email= 'john.doe@gmail.com'
DISTINCT ON (u.email)
ORDER BY p.created_at DESC;
'''