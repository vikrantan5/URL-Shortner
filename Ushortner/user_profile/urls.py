from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.profile_dashboard, name='profile_dashboard'),
    path('create/', views.create_profile, name='create_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('preview/', views.preview_profile, name='preview_profile'),
    
    # Link management
    path('links/add/', views.add_link, name='add_link'),
    path('links/<int:link_id>/edit/', views.edit_link, name='edit_link'),
    path('links/<int:link_id>/delete/', views.delete_link, name='delete_link'),
    path('links/<int:link_id>/toggle/', views.toggle_link_status, name='toggle_link_status'),
    path('links/<int:link_id>/click/', views.track_link_click, name='track_link_click'),
]
