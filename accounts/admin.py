from django.contrib import admin
from .models import Profile


@admin.register ( Profile )
class ProfileAdmin ( admin.ModelAdmin ) :
    list_display = ['user', 'phone', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']