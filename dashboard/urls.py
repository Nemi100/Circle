from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('<str:username>/', views.user_dashboard, name='user_dashboard'),
    path('add_profile/', views.add_profile, name='add_profile'),
    path('edit_profile/<str:username>/', views.edit_profile, name='edit_profile'),
    path('delete_profile/<str:username>/', views.delete_profile, name='delete_profile'),
    path('view_profile/<str:username>/', views.view_profile, name='view_profile'),  
    path('post-job/', views.post_job, name='post_job'),

]
