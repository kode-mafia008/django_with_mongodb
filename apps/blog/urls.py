from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.blog_list, name='blog_list'),
    path('all_raw/', views.blog_list_raw, name='blog_list_raw'),
    path('all_orm/', views.blog_list_orm, name='blog_list_orm'),
]
