import logging
import time
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponse
from django.http import Http404

logger = logging.getLogger(__name__)


class NitAppMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        response = self.get_response(request)
        return response

    def process_view(self,request,view_func,view_args,view_kwargs):
        """Called just before Django calls the view"""
        return None
    
    def process_exception(self,request,exception):
        """Called if an exception is raised on view"""
        return None
    
    def process_template_response(self,request,response):
        """
        Called just after the view has finished 
        Called for responses with render() method
        """
        return response



class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        start_time = time.time()
        
        request_data = {
            'method': request.method,
            'path': request.path,
            'user': getattr(request.user, 'username', 'anonymous'),
            'ip': self.get_client_ip(request),
        }
        
        logger.info(f"Request: {request_data}")
        print(f"Request: {request_data}")
        
        response = self.get_response(request)
        
        # Log response details
        duration = time.time() - start_time
        logger.info(
            f"Response: {request.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.2f}s"
        )
        
        return response
    
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 100  # requests
        self.time_window = 3600  # seconds (1 hour)

    def __call__(self, request):
        if self.is_rate_limited(request):
            return HttpResponse(
                'Rate limit exceeded. Try again later.',
                status=429
            )
        
        response = self.get_response(request)
        return response

    def is_rate_limited(self, request):
        ip = self.get_client_ip(request)
        cache_key = f'rate_limit:{ip}'
        
        request_count = cache.get(cache_key, 0)
        
        if request_count >= self.rate_limit:
            return True
        
        cache.set(cache_key, request_count + 1, self.time_window)
        return False

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


# 3. Tenant Isolation Middleware (Multi-tenancy)

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract tenant from subdomain or header
        tenant = self.get_tenant(request)
        
        if not tenant:
            raise Http404("Tenant not found")
        
        # Store tenant in thread-local storage
        request.tenant = tenant
        
        # Set database schema or filter here...
        
        response = self.get_response(request)
        return response

    def get_tenant(self, request):
        # Extract from subdomain: tenant1.example.com
        host = request.get_host().split(':')[0]
        subdomain = host.split('.')[0]
        
        # Or from custom header
        tenant_id = request.META.get('HTTP_X_TENANT_ID')
        
        return tenant_id, subdomain


# 4. API Authentication Middleware
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = self.get_token_from_header(request)
        
        # if token:
        #     try:
        #         payload = jwt.decode(
        #             token,
        #             settings.SECRET_KEY,
        #             algorithms=['HS256']
        #         )
        #         # user = User.objects.get(id=payload['user_id'])
        #         # request.user = user
        #     except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        #         request.user = AnonymousUser()
        # else:
        #     request.user = AnonymousUser()
        
        response = self.get_response(request)
        return response

    @staticmethod
    def get_token_from_header(request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]
        return None

from math import ceil

class RequestTimingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        response['X-Request-Duration'] = round(duration,2)
        logger.info(f"Request: {request.path} took {duration:.2f}s")
        return response

    

        