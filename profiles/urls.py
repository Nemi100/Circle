from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('leave-review/<str:freelancer_username>/', views.leave_review, name='leave_review'),
    path('profile/', views.profile_view, name='profile'),  
]
