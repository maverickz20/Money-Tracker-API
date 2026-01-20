from django.db import models
from django.contrib.auth.models import User


class Category ( models.Model ) :
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey ( User, on_delete=models.CASCADE, related_name='categories' )
    name = models.CharField ( max_length=100, help_text='Kategoriya nomi' )
    transaction_type = models.CharField ( max_length=10, choices=TRANSACTION_TYPES )
    icon = models.CharField ( max_length=50, default='📌', help_text='Emoji yoki icon' )
    color = models.CharField ( max_length=7, default='#3498db', help_text='Rang kodi (hex)' )
    created_at = models.DateTimeField ( auto_now_add=True )

    def __str__(self) :
        return f"{self.name} ({self.get_transaction_type_display ()})"

    @property
    def transaction_count(self) :
        return self.transactions.count ()

    @property
    def total_amount(self) :
        from django.db.models import Sum
        result = self.transactions.aggregate ( Sum ( 'amount' ) )
        return result['amount__sum'] or 0

    class Meta :
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['transaction_type', 'name']
        unique_together = ['user', 'name', 'transaction_type']


class Transaction ( models.Model ) :
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    CURRENCIES = (
        ('UZS', 'UZS - O\'zbek so\'mi'),
        ('USD', 'USD - US Dollar'),
        ('EUR', 'EUR - Euro'),
        ('RUB', 'RUB - Russian Ruble'),
    )

    user = models.ForeignKey ( User, on_delete=models.CASCADE, related_name='transactions' )
    transaction_type = models.CharField ( max_length=10, choices=TRANSACTION_TYPES )
    amount = models.DecimalField ( max_digits=15, decimal_places=2, help_text='Tranzaksiya summasi' )
    currency = models.CharField ( max_length=3, choices=CURRENCIES, default='UZS' )
    category = models.ForeignKey (
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions',
        help_text='Tranzaksiya kategoriyasi'
    )
    card = models.ForeignKey (
        'cards.Card',
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions',
        help_text='Qaysi karta/hisobdan'
    )
    description = models.TextField ( blank=True, null=True, help_text='Izoh' )
    date = models.DateTimeField ( help_text='Tranzaksiya sanasi' )
    created_at = models.DateTimeField ( auto_now_add=True )
    updated_at = models.DateTimeField ( auto_now=True )

    def __str__(self) :
        return f"{self.get_transaction_type_display ()} - {self.amount} {self.currency}"

    class Meta :
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date']