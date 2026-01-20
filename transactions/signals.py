from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction
from django.db import models

@receiver ( post_save, sender=Transaction )
def update_card_balance_on_create(sender, instance, created, **kwargs) :
    if instance.card :
        card = instance.card

        income_sum = card.transactions.filter ( transaction_type='income' ).aggregate (
            models.Sum ( 'amount' )
        )['amount__sum'] or 0

        expense_sum = card.transactions.filter ( transaction_type='expense' ).aggregate (
            models.Sum ( 'amount' )
        )['amount__sum'] or 0

        card.balance = income_sum - expense_sum
        card.save ()


@receiver ( post_delete, sender=Transaction )
def update_card_balance_on_delete(sender, instance, **kwargs) :
    if instance.card :
        card = instance.card

        income_sum = card.transactions.filter ( transaction_type='income' ).aggregate (
            models.Sum ( 'amount' )
        )['amount__sum'] or 0

        expense_sum = card.transactions.filter ( transaction_type='expense' ).aggregate (
            models.Sum ( 'amount' )
        )['amount__sum'] or 0

        card.balance = income_sum - expense_sum
        card.save ()