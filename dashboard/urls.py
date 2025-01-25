from django.urls import path
from .views import user_dashboard, view_profile, add_profile, edit_profile, delete_profile, post_job, review_list, review_create, review_update, review_delete

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('add_profile/', add_profile, name='add_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('view_profile/<str:username>/', view_profile, name='view_profile'),
    path('post-job/', post_job, name='post_job'),
    path('reviews/', review_list, name='review_list'),
    path('reviews/create/', review_create, name='review_create'),
    path('reviews/<int:pk>/update/', review_update, name='review_update'),
    path('reviews/<int:pk>/delete/', review_delete, name='review_delete'),
]
