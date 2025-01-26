from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from profiles.views import CustomSignupView, select_user_type
from profiles.views import CustomConfirmEmailView  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/confirm-email/<str:key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('select-user-type/', select_user_type, name='select_user_type'),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('subscription/', include('subscription.urls', namespace='subscription')),
    path('profiles/', include('profiles.urls', namespace='profiles')), 
    path('dashboard/', include('dashboard.urls', namespace='dashboard')), 
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
