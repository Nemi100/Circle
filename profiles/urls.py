from django.urls import path
from .views import select_user_type, view_profile, edit_freelancer_profile, edit_client_profile, leave_review, manage_employers, client_profile_view, update_user_type
from . import views

app_name = 'profiles'

urlpatterns = [
    path('leave-review/<str:freelancer_username>/', leave_review, name='leave_review'),
    path('profile/<str:username>/', view_profile, name='view_profile'), 
    path('profile/edit/freelancer/', edit_freelancer_profile, name='edit_freelancer_profile'),
    path('profile/edit/client/', edit_client_profile, name='edit_client_profile'),
    path('manage-employers/', manage_employers, name='manage_employers'),
    path('select-user-type/', select_user_type, name='select_user_type'),
    path('client-profile/', client_profile_view, name='client_profile_view'),
    path('update-user-type/', update_user_type, name='update_user_type'),
]


