from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import User
from .serializers import UserSerializer

@require_http_methods(["GET"])
def api_users_list(request):
    """
    API endpoint to list all users
    GET /api/users/
    """
    users = User.objects.all()
    
    return JsonResponse({
        'users': UserSerializer(users, many=True).data,
        'count': users.count()
    })

@require_http_methods(["GET"])
def api_user_detail(request, user_id):
    """
    API endpoint to get a single user
    GET /api/users/<id>/
    """
    try:
        user = User.objects.get(id=user_id)
        user_data = UserSerializer(user).data
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
