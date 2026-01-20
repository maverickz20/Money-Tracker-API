from django.db import models
from django.contrib.auth.models import User


class Card ( models.Model ) :
    CARD_TYPES = (
        ('cash', 'Cash'),
        ('debit', 'Debit Card'),
        ('credit', 'Credit Card'),
        ('bank_account', 'Bank Account'),
    )

    CURRENCIES = (
        ('UZS', 'UZS - O\'zbek so\'mi'),
        ('USD', 'USD - US Dollar'),
        ('EUR', 'EUR - Euro'),
        ('RUB', 'RUB - Russian Ruble'),
    )

    user = models.ForeignKey ( User, on_delete=models.CASCADE, related_name='cards' )
    name = models.CharField ( max_length=100, help_text='Karta nomi' )
    card_type = models.CharField ( max_length=20, choices=CARD_TYPES )
    currency = models.CharField ( max_length=3, choices=CURRENCIES, default='UZS' )
    card_number = models.CharField ( max_length=19, blank=True, null=True, help_text='Karta raqami (ixtiyoriy)' )
    balance = models.DecimalField ( max_digits=15, decimal_places=2, default=0, help_text='Joriy balans' )
    credit_limit = models.DecimalField (
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Kredit limit (faqat credit card uchun)'
    )
    bank_name = models.CharField ( max_length=100, blank=True, null=True, help_text='Bank nomi' )
    color = models.CharField ( max_length=7, default='#3498db', help_text='Rang kodi (hex)' )
    description = models.TextField ( blank=True, null=True, help_text='Qo\'shimcha ma\'lumot' )
    is_active = models.BooleanField ( default=True, help_text='Faol holat' )
    created_at = models.DateTimeField ( auto_now_add=True )
    updated_at = models.DateTimeField ( auto_now=True )

    def __str__(self) :
        return f"{self.name} - {self.balance} {self.currency}"

    @property
    def income_count(self) :
        return self.transactions.filter ( transaction_type='income' ).count ()

    @property
    def expense_count(self) :
        return self.transactions.filter ( transaction_type='expense' ).count ()

    @property
    def total_income(self) :
        from django.db.models import Sum
        result = self.transactions.filter ( transaction_type='income' ).aggregate ( Sum ( 'amount' ) )
        return result['amount__sum'] or 0

    @property
    def total_expense(self) :
        from django.db.models import Sum
        result = self.transactions.filter ( transaction_type='expense' ).aggregate ( Sum ( 'amount' ) )
        return result['amount__sum'] or 0

    @property
    def used_percentage(self) :
        if self.credit_limit and self.credit_limit > 0 :
            return round ( (abs ( self.balance ) / self.credit_limit) * 100, 1 )
        return 0

    class Meta :
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        ordering = ['-created_at']