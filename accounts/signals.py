from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver ( post_save, sender=User )
def create_user_profile(sender, instance, created, **kwargs) :
    if created :
        Profile.objects.create ( user=instance )

        from transactions.models import Category

        income_categories = [
            {'name' : 'Salary', 'icon' : '💰'},
            {'name' : 'Freelance', 'icon' : '💻'},
            {'name' : 'Investment', 'icon' : '📈'},
            {'name' : 'Bonus', 'icon' : '🎁'},
            {'name' : 'Other Income', 'icon' : '➕'},
        ]

        expense_categories = [
            {'name' : 'Food', 'icon' : '🍔'},
            {'name' : 'Transport', 'icon' : '🚗'},
            {'name' : 'Utilities', 'icon' : '💡'},
            {'name' : 'Entertainment', 'icon' : '🎬'},
            {'name' : 'Shopping', 'icon' : '🛍️'},
            {'name' : 'Health', 'icon' : '❤️'},
            {'name' : 'Education', 'icon' : '📚'},
            {'name' : 'Other Expense', 'icon' : '➖'},
        ]

        for cat_data in income_categories :
            Category.objects.create (
                user=instance,
                transaction_type='income',
                name=cat_data['name'],
                icon=cat_data['icon']
            )

        for cat_data in expense_categories :
            Category.objects.create (
                user=instance,
                transaction_type='expense',
                name=cat_data['name'],
                icon=cat_data['icon']
            )


@receiver ( post_save, sender=User )
def save_user_profile(sender, instance, **kwargs) :
    if hasattr ( instance, 'profile' ) :
        instance.profile.save ()