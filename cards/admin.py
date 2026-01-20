from django.contrib import admin
from .models import Card


@admin.register ( Card )
class CardAdmin ( admin.ModelAdmin ) :
    list_display = ['name', 'user', 'card_type', 'currency', 'balance', 'is_active', 'created_at']
    list_filter = ['card_type', 'currency', 'is_active', 'created_at']
    search_fields = ['name', 'user__username', 'card_number', 'bank_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields' : ('user', 'name', 'card_type', 'currency', 'is_active')
        }),
        ('Moliyaviy ma\'lumotlar', {
            'fields' : ('balance', 'credit_limit')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields' : ('card_number', 'bank_name', 'color', 'description')
        }),
        ('Vaqt', {
            'fields' : ('created_at', 'updated_at')
        }),
    )