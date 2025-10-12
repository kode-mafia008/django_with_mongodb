from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random
from .models import (
    Post, 
    PostStatistics,
    PostVersion,
    Comment,
    Bookmark,
    Notification,
    PostSchedule,
)


# Random post titles for testing/demo purposes
POST_TITLES = (
    "Getting Started with Django ORM: A Comprehensive Guide",
    "10 Best Practices for Writing Clean Python Code",
    "Understanding Database Optimization in Modern Web Apps",
    "The Ultimate Guide to RESTful API Design",
    "Building Scalable Applications with Microservices",
    "Docker and Kubernetes: A Beginner's Journey",
    "Machine Learning 101: From Theory to Practice",
    "React vs Vue vs Angular: Which Framework to Choose in 2025?",
    "Mastering Git: Advanced Workflows for Teams",
    "GraphQL vs REST: Making the Right Choice for Your API",
    "Cybersecurity Essentials Every Developer Should Know",
    "The Rise of AI-Powered Development Tools",
    "Building Real-Time Applications with WebSockets",
    "Cloud Computing: AWS, Azure, or Google Cloud?",
    "Test-Driven Development: A Practical Introduction",
    "Optimizing Frontend Performance: Tips and Tricks",
    "Understanding Blockchain Technology Beyond Cryptocurrency",
    "The Future of Web Development: Trends to Watch",
    "Debugging Like a Pro: Tools and Techniques",
    "Creating Accessible Web Applications for Everyone",
    "From Monolith to Microservices: A Migration Story",
    "Data Science for Beginners: Where to Start",
    "Building Mobile Apps with React Native",
    "The Art of Code Review: Best Practices",
    "Understanding Authentication and Authorization",
    "Serverless Architecture: Pros and Cons",
    "Writing Technical Documentation That Developers Love",
    "The Psychology of User Experience Design",
    "Continuous Integration and Deployment Made Simple",
    "Exploring the JAMstack: Modern Web Architecture",
)

# Random post content for testing/demo purposes
POST_CONTENT = (
    """Django's ORM (Object-Relational Mapping) is one of the most powerful features of the framework. It provides a high-level, Pythonic way to interact with databases without writing raw SQL queries. In this comprehensive guide, we'll explore the core concepts of Django ORM, from basic queries to advanced techniques like select_related and prefetch_related for optimizing database performance. Whether you're a beginner or an experienced developer, mastering the ORM will significantly improve your productivity and application performance.""",
    
    """Writing clean, maintainable Python code is essential for building scalable applications. In this article, we'll explore 10 best practices that every Python developer should follow. From proper naming conventions and documentation to leveraging type hints and understanding Python's PEP 8 style guide, these practices will help you write code that's not only functional but also easy to read and maintain. We'll also cover common pitfalls to avoid and tools that can help enforce these standards in your development workflow.""",
    
    """Database optimization is crucial for building high-performance web applications. Slow queries can significantly impact user experience and server costs. This article dives deep into database optimization techniques, including indexing strategies, query optimization, connection pooling, and caching mechanisms. We'll explore both SQL and NoSQL optimization approaches, and discuss how to use profiling tools to identify and resolve performance bottlenecks in your application.""",
    
    """RESTful API design is both an art and a science. A well-designed API is intuitive, consistent, and scalable. In this ultimate guide, we'll cover the fundamental principles of REST architecture, including resource naming, HTTP methods, status codes, and versioning strategies. We'll also discuss authentication, rate limiting, pagination, and error handling. By following these best practices, you'll create APIs that developers love to use and that stand the test of time.""",
    
    """Microservices architecture has revolutionized how we build and deploy applications. Unlike monolithic applications, microservices break down complex systems into smaller, independent services that can be developed, deployed, and scaled independently. This article explores the benefits and challenges of microservices, design patterns, inter-service communication, and deployment strategies. We'll also discuss when microservices make sense and when a monolithic approach might be more appropriate for your project.""",
    
    """Docker and Kubernetes have become essential tools in modern software development. Docker simplifies application packaging and deployment through containerization, while Kubernetes orchestrates these containers at scale. This beginner-friendly guide will walk you through the basics of both technologies, from creating your first Docker container to deploying a multi-container application on Kubernetes. We'll cover key concepts, practical examples, and common use cases to get you started on your containerization journey.""",
    
    """Machine Learning is transforming industries and creating new possibilities every day. This introductory guide takes you from theory to practice, covering fundamental concepts like supervised and unsupervised learning, neural networks, and model evaluation. We'll work through practical examples using popular Python libraries like scikit-learn and TensorFlow, and discuss real-world applications. Whether you're looking to add ML skills to your toolkit or start a career in data science, this guide provides a solid foundation.""",
    
    """Choosing the right JavaScript framework can significantly impact your project's success. React, Vue, and Angular are the three most popular options, each with its own strengths and use cases. In this comprehensive comparison, we'll analyze performance, learning curve, ecosystem, community support, and enterprise readiness. We'll help you understand which framework aligns best with your project requirements, team expertise, and long-term goals for 2025 and beyond.""",
    
    """Git is more than just version control—it's a powerful collaboration tool that, when used correctly, can dramatically improve team productivity. This article goes beyond basic commits and branches to explore advanced workflows like Git Flow, trunk-based development, and rebasing strategies. We'll cover conflict resolution, cherry-picking, bisecting for bug hunting, and creating effective commit messages. These techniques will help your team collaborate more effectively and maintain a clean project history.""",
    
    """The debate between GraphQL and REST continues in the API development world. Both have their place, but understanding their strengths and weaknesses is crucial for making the right choice. This article provides an in-depth comparison, examining performance, flexibility, caching, tooling, and learning curve. We'll explore real-world scenarios where each approach excels and provide guidance on choosing the right solution for your specific use case.""",
)


@receiver(post_save, sender=Post)
def create_post_related_objects(sender, instance, created, **kwargs):
    """
    Automatically create all related objects when a Post is created:
    - PostStatistics: Track views, likes, shares
    - PostVersion: Create initial version (v1)
    - PostSchedule: Schedule for immediate publish or future date
    """
    if created:
        Post.objects.filter(id=instance.id).update(
            title=random.choice(POST_TITLES), 
            content=random.choice(POST_CONTENT)
        )

        # Create PostStatistics
        PostStatistics.objects.get_or_create(
            post=instance,
            defaults={
                'view_count': 0,
                'like_count': 0,
                'share_count': 0,
                'last_viewed_at': timezone.now()
            }
        )
        
        # Create initial PostVersion (version 1)
        PostVersion.objects.create(
            post=instance,
            title=instance.title,
            content=instance.content,
            version_number=1,
            created_by=instance.author
        )
        
        # Create default PostSchedule (scheduled for immediate publish)
        PostSchedule.objects.create(
            post=instance,
            scheduled_for=timezone.now(),
            is_published=False,
            retry_count=0
        )

        random_comments = (
            "Great article! This really helped me understand the topic better.",
            "Thanks for sharing this valuable insight. Looking forward to more content like this.",
            "Interesting perspective, though I'd love to see more examples.",
            "This is exactly what I was looking for. Bookmarking for future reference!",
            "Well written and informative. Keep up the excellent work!",
            "I disagree with some points, but appreciate the different viewpoint.",
            "Could you elaborate more on this topic? Would love to learn more.",
            "Brilliant explanation! Shared this with my team.",
            "Not sure I completely agree, but definitely thought-provoking.",
            "This answered so many questions I had. Thank you!",
            "Absolutely amazing content. One of the best posts I've read recently.",
            "Good points overall, though a bit more depth would be helpful.",
            "Love the practical examples you've included here.",
            "This is very insightful. Can't wait to apply this knowledge.",
            "Thanks for breaking this down so clearly. Very helpful!",
            "Interesting read, but I think there's another side to this.",
            "Exactly what I needed today. Perfect timing!",
            "Well researched and presented. Impressive work!",
            "I learned something new today. Thank you for this post.",
            "Could use some improvement, but overall a solid effort.",
        )
        # Create default Comment (scheduled for immediate publish)
        Comment.objects.create(
            post=instance,
            content=random.choice(random_comments),
            author=instance.author,
            is_approved=True,
        )
        
        random_notes = (
            "Save this for later reference - great resource!",
            "Must read again when working on my next project.",
            "Bookmarking to share with my team tomorrow.",
            "Important concepts here, need to review in detail.",
            "Excellent tutorial, saving for future implementation.",
            "This will be useful for the upcoming sprint.",
            "Need to revisit this when I have more time.",
            "Perfect timing! Exactly what I needed for my current task.",
            "Adding to my learning resources collection.",
            "Great insights, will come back to this.",
            "Saving for quick reference during development.",
            "This answers many questions I had - bookmarked!",
            "Useful tips that I'll definitely apply soon.",
            "Comprehensive guide, worth revisiting multiple times.",
            "Marking for the code review discussion next week.",
        )
        # Create default Bookmark
        Bookmark.objects.create(
        user=instance.author,
        post=instance,
        notes=random.choice(random_notes)  # ✅ Use random_notes, not random_comments
        )

        notification_messages = (
            "New Comment",
            "New Like",
            "New Follow",
            "New Bookmark",
            "New Share",
        )
        # Create default Notification (scheduled for immediate publish)
        Notification.objects.create(
            recipient=instance.author,
            content_object_id=instance.id,
            notification_type=random.choice(notification_messages),
            message=random.choice(notification_messages),
            is_read=False,
        )