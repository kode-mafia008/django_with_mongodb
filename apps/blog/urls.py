from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.blog_list, name='blog_list'),
    path('all_raw/', views.blog_list_raw, name='blog_list_raw'),
    path('all_orm/', views.blog_list_orm, name='blog_list_orm'),

    # select_related, prefetch_related
    path('all_select_related/', views.blog_list_select_related, name='blog_list_select_related'),
    path('all_prefetch_related/', views.blog_list_prefetch_related, name='blog_list_prefetch_related'),

    # Aggregation and Annotation
    path('aggregation/', views.blog_aggregation, name='blog_aggregation'),
    path('annotation/', views.blog_annotation, name='blog_annotation'),

]
