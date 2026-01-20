from django.contrib import admin
from .models import Category, Transaction


@admin.register ( Category )
class CategoryAdmin ( admin.ModelAdmin ) :
    list_display = ['name', 'user', 'transaction_type', 'icon', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at']


@admin.register ( Transaction )
class TransactionAdmin ( admin.ModelAdmin ) :
    list_display = ['user', 'transaction_type', 'amount', 'currency', 'category', 'card', 'date']
    list_filter = ['transaction_type', 'currency', 'date', 'created_at']
    search_fields = ['description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields' : ('user', 'transaction_type', 'amount', 'currency')
        }),
        ('Bog\'lanishlar', {
            'fields' : ('category', 'card')
        }),
        ('Qo\'shimcha', {
            'fields' : ('description', 'date')
        }),
        ('Vaqt', {
            'fields' : ('created_at', 'updated_at')
        }),
    )