from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_users_list, name='api_users_list'),
    path('<int:user_id>/', views.api_user_detail, name='api_user_detail'),
]
