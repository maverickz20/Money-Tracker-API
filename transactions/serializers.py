from rest_framework import serializers
from .models import Category, Transaction
from cards.serializers import CardListSerializer


class CategorySerializer ( serializers.ModelSerializer ) :
    transaction_count = serializers.IntegerField ( read_only=True )
    total_amount = serializers.DecimalField ( max_digits=15, decimal_places=2, read_only=True )

    class Meta :
        model = Category
        fields = [
            'id', 'name', 'transaction_type', 'icon', 'color',
            'transaction_count', 'total_amount', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data) :
        validated_data['user'] = self.context['request'].user
        return super ().create ( validated_data )


class CategoryListSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Category
        fields = ['id', 'name', 'transaction_type', 'icon', 'color']


class TransactionSerializer ( serializers.ModelSerializer ) :
    category_detail = CategoryListSerializer ( source='category', read_only=True )
    card_detail = CardListSerializer ( source='card', read_only=True )

    class Meta :
        model = Transaction
        fields = [
            'id', 'transaction_type', 'amount', 'currency', 'category',
            'category_detail', 'card', 'card_detail', 'description',
            'date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs) :
        user = self.context['request'].user
        category = attrs.get ( 'category' )
        card = attrs.get ( 'card' )
        transaction_type = attrs.get ( 'transaction_type' )

        if category and category.user != user :
            raise serializers.ValidationError ( {
                'category' : 'This category does not belong to you.'
            } )

        if card and card.user != user :
            raise serializers.ValidationError ( {
                'card' : 'This card does not belong to you.'
            } )

        if category and category.transaction_type != transaction_type :
            raise serializers.ValidationError ( {
                'category' : f'Category type must be {transaction_type}'
            } )

        return attrs

    def create(self, validated_data) :
        validated_data['user'] = self.context['request'].user
        return super ().create ( validated_data )


class TransactionCreateSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Transaction
        fields = [
            'transaction_type', 'amount', 'currency', 'category',
            'card', 'description', 'date'
        ]

    def validate(self, attrs) :
        user = self.context['request'].user
        category = attrs.get ( 'category' )
        card = attrs.get ( 'card' )
        transaction_type = attrs.get ( 'transaction_type' )

        if category and category.user != user :
            raise serializers.ValidationError ( {
                'category' : 'This category does not belong to you.'
            } )

        if card and card.user != user :
            raise serializers.ValidationError ( {
                'card' : 'This card does not belong to you.'
            } )

        if category and category.transaction_type != transaction_type :
            raise serializers.ValidationError ( {
                'category' : f'Category type must be {transaction_type}'
            } )

        return attrs

    def create(self, validated_data) :
        validated_data['user'] = self.context['request'].user
        return super ().create ( validated_data )


class TransactionUpdateSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Transaction
        fields = [
            'transaction_type', 'amount', 'currency', 'category',
            'card', 'description', 'date'
        ]


class TransactionStatsSerializer ( serializers.Serializer ) :
    total_income = serializers.DecimalField ( max_digits=15, decimal_places=2 )
    total_expense = serializers.DecimalField ( max_digits=15, decimal_places=2 )
    balance = serializers.DecimalField ( max_digits=15, decimal_places=2 )
    income_count = serializers.IntegerField ()
    expense_count = serializers.IntegerField ()
    currency = serializers.CharField ()