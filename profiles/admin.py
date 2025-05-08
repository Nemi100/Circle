from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FreelancerProfile, ClientProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'has_active_subscription', 'current_subscription_type')
    list_filter = ('role', 'is_staff', 'is_active', 'has_active_subscription', 'current_subscription_type')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}), 
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_picture', 'phone_number')}), 
        ('Subscription Info', {'fields': ('has_active_subscription', 'current_subscription_type')}), 
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'has_active_subscription', 'current_subscription_type')} 
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)



@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    model = ClientProfile
    list_display = ('get_username', 'get_first_name', 'get_last_name', 'company_name', 'get_email', 'location', 'get_subscription_status')
    list_filter = ('location',)
    search_fields = ('user__username', 'company_name', 'user__email', 'location')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = "First Name"

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = "Last Name"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

    def get_subscription_status(self, obj):
        return "Active" if obj.user.has_active_subscription else "Inactive"
    get_subscription_status.short_description = "Subscription Status"


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    model = FreelancerProfile
    list_display = ('get_username', 'get_first_name', 'get_last_name', 'get_email', 'location', 'get_skills', 'get_subscription_status')
    list_filter = ('location',)
    search_fields = ('user__username', 'user__email', 'location', 'skills__name')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = "First Name"

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = "Last Name"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = "Skills"

    def get_subscription_status(self, obj):
        return "Active" if obj.user.has_active_subscription else "Inactive"
    get_subscription_status.short_description = "Subscription Status"