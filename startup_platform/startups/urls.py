from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('public/', views.PublicStartupListView.as_view(), name='public-startup-list'),
    
    # User endpoints
    path('', views.UserStartupListCreateView.as_view(), name='user-startup-list-create'),
    path('<int:pk>/', views.UserStartupDetailView.as_view(), name='user-startup-detail'),
    
    # Admin endpoints
    path('admin/all/', views.AdminStartupListView.as_view(), name='admin-startup-list'),
    path('admin/pending/', views.AdminPendingStartupListView.as_view(), name='admin-pending-startups'),
    path('admin/<int:pk>/approve/', views.approve_startup, name='approve-startup'),
    path('admin/<int:pk>/reject/', views.reject_startup, name='reject-startup'),
    path('admin/stats/', views.admin_stats, name='admin-stats'),
]
