from django.http import JsonResponse
from django.db.models import Prefetch
from .models import (
    Post,
    PostVersion
)
from .serializers import (
    PostSerializer,
    PostRawSerializer,
    PostORMSerializer,
    )


def blog_list(request):
    # Need to select_related all the way to 'user' and include FK fields
    posts = Post.objects.select_related('author__user').only(
        'id', 'title', 'created_at', 'author_id',  # Post fields + author FK
        'author__id', 'author__user_id',            # Author fields + user FK
        'author__user__id', 'author__user__name'    # User fields
    )
    
    # Method 1: Print the actual SQL query being executed
    print("SQL Query:")
    print(posts.query)
    print("\n" + "="*50 + "\n")
    
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data,safe=False)


def blog_list_raw(request):
    ''' Raw Query '''
    # Need to select_related all the way to 'user' and include FK fields
    posts = Post.objects.raw(
        '''
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
        WHERE u.email= %s
        ORDER BY p.created_at DESC;
        '''
        ,('john.doe@gmail.com',)
        )

    serializer = PostRawSerializer(posts, many=True)
    return JsonResponse(serializer.data,safe=False)


def blog_list_orm(request):
    ''' ORM Query '''
    posts = Post.objects.select_related(
        'author__user'
    ).prefetch_related(
        Prefetch('versions', queryset=PostVersion.objects.all())
    ).filter(
        author__user__email='john.doe@gmail.com'
    ).order_by('-created_at')

    # Use PostPostORMSerializerSerializer for ORM queries (PostRawSerializer is only for raw SQL)
    serializer = PostORMSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)

