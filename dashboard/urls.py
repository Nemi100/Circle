from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('view-profile/<str:username>/', views.view_profile, name='view_profile'),
    path('add-profile/', views.add_profile, name='add_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('post-job/', views.post_job, name='post_job'),
    path('review-list/', views.review_list, name='review_list'),
    path('review-create/', views.review_create, name='review_create'),
    path('review-update/<int:pk>/', views.review_update, name='review_update'),
    path('review-delete/<int:pk>/', views.review_delete, name='review_delete'),
    path('update-user-type/', views.update_user_type, name='update_user_type'),
    path('inbox/', views.inbox, name='inbox'),
    path('message-detail/<int:message_id>/', views.message_detail, name='message_detail'),
    path('job-listings/', views.job_listings, name='job_listings'),
    path('job-detail/<int:job_id>/', views.job_detail, name='job_detail'),  
]
