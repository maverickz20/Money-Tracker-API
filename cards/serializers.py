from rest_framework import serializers
from .models import Card


class CardSerializer ( serializers.ModelSerializer ) :
    income_count = serializers.IntegerField ( read_only=True )
    expense_count = serializers.IntegerField ( read_only=True )
    total_income = serializers.DecimalField ( max_digits=15, decimal_places=2, read_only=True )
    total_expense = serializers.DecimalField ( max_digits=15, decimal_places=2, read_only=True )
    used_percentage = serializers.FloatField ( read_only=True )

    class Meta :
        model = Card
        fields = [
            'id', 'name', 'card_type', 'currency', 'card_number',
            'balance', 'credit_limit', 'bank_name', 'color', 'description',
            'is_active', 'income_count', 'expense_count', 'total_income',
            'total_expense', 'used_percentage', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_card_number(self, value) :
        if value and len ( value.replace ( ' ', '' ) ) > 19 :
            raise serializers.ValidationError ( "Card number cannot be longer than 19 digits." )
        return value

    def validate(self, attrs) :
        card_type = attrs.get ( 'card_type' )
        credit_limit = attrs.get ( 'credit_limit' )

        if card_type != 'credit' and credit_limit :
            raise serializers.ValidationError ( {
                'credit_limit' : 'Credit limit is only applicable for credit cards.'
            } )

        return attrs


class CardCreateSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Card
        fields = [
            'name', 'card_type', 'currency', 'card_number',
            'balance', 'credit_limit', 'bank_name', 'color', 'description'
        ]

    def create(self, validated_data) :
        validated_data['user'] = self.context['request'].user
        return super ().create ( validated_data )


class CardUpdateSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Card
        fields = [
            'name', 'card_type', 'currency', 'card_number',
            'credit_limit', 'bank_name', 'color', 'description', 'is_active'
        ]


class CardListSerializer ( serializers.ModelSerializer ) :
    class Meta :
        model = Card
        fields = [
            'id', 'name', 'card_type', 'currency', 'balance',
            'color', 'is_active', 'created_at'
        ]