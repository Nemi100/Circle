from django.urls import path
from . import views
from jobs.models import Job

app_name = 'profiles'

urlpatterns = [
    # Onboarding and User Dashboard
    path('onboarding/', views.onboarding, name='onboarding'),
    path('freelancer/dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('freelancer/<str:username>/', views.view_freelancer_profile, name='view_freelancer_profile'),
    path('freelancer/public-profile/<str:username>/', views.freelancer_public_profile, name='freelancer_public_profile'),
    

    # Client Views
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client/update-profile/', views.update_client_dashboard, name='update_client_dashboard'),
    path('update/', views.update_client_profile, name='update_client_profile'),  
    path('client/manage-jobs/', views.client_job_management, name='client_job_management'),

    

    # Profile Management
    path('delete-account/', views.delete_account, name='delete_account'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('create-client-profile/', views.create_client_profile, name='create_client_profile'),  # Client profile


    # Subscription 
    path('subscription/', views.manage_subscription, name='manage_subscription'),
    
    # Support and Search
    path('search-freelancers/', views.search_freelancers, name='search_freelancers'),
    path('contact-support/', views.contact_support, name='contact_support'),

    #admin
    path('admin/user-management/', views.admin_user_management, name='admin_user_management'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  
    path('admin/user-management/', views.admin_user_management, name='admin_user_management'),
    path('admin/user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/user/create/', views.create_admin, name='create_admin'),  
    path('admin/report/', views.admin_report, name='admin_report'),
    path('admin/growth-report/', views.user_growth_report, name='user_growth_report'),  
]
