from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('leave-review/<str:freelancer_username>/', views.leave_review, name='leave_review'),
    path('profile/', views.profile_view, name='profile'),  
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('manage-employers/', views.manage_employers, name='manage_employers'),  # Example URL for manage_employers
    path('client-profile/', views.client_profile_view, name='client_profile_view'),  # URL for client profile view
    path('client-edit-profile/', views.client_edit_profile, name='client_edit_profile'),  # URL for client edit profile
]
