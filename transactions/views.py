from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Transaction
from .serializers import (
    CategorySerializer,
    CategoryListSerializer,
    TransactionSerializer,
    TransactionCreateSerializer,
    TransactionUpdateSerializer,
    TransactionStatsSerializer
)


class CategoryListCreateView ( generics.ListCreateAPIView ) :
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['transaction_type']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['transaction_type', 'name']

    def get_queryset(self) :
        return Category.objects.filter ( user=self.request.user )

    def get_serializer_class(self) :
        if self.request.method == 'POST' :
            return CategorySerializer
        return CategoryListSerializer

    @swagger_auto_schema (
        operation_description="Barcha kategoriyalarni olish",
        responses={200 : CategoryListSerializer ( many=True )}
    )
    def get(self, request, *args, **kwargs) :
        return super ().get ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Yangi kategoriya yaratish",
        request_body=CategorySerializer,
        responses={201 : CategorySerializer ()}
    )
    def post(self, request, *args, **kwargs) :
        return super ().post ( request, *args, **kwargs )


class CategoryDetailView ( generics.RetrieveUpdateDestroyAPIView ) :
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self) :
        return Category.objects.filter ( user=self.request.user )

    @swagger_auto_schema (
        operation_description="Bitta kategoriya ma'lumotlarini olish",
        responses={200 : CategorySerializer ()}
    )
    def get(self, request, *args, **kwargs) :
        return super ().get ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Kategoriyani to'liq yangilash",
        request_body=CategorySerializer,
        responses={200 : CategorySerializer ()}
    )
    def put(self, request, *args, **kwargs) :
        return super ().put ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Kategoriyani qisman yangilash",
        request_body=CategorySerializer,
        responses={200 : CategorySerializer ()}
    )
    def patch(self, request, *args, **kwargs) :
        return super ().patch ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Kategoriyani o'chirish",
        responses={204 : 'Category deleted successfully'}
    )
    def delete(self, request, *args, **kwargs) :
        return super ().delete ( request, *args, **kwargs )


class TransactionListCreateView ( generics.ListCreateAPIView ) :
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['transaction_type', 'currency', 'category', 'card']
    search_fields = ['description']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']

    def get_queryset(self) :
        queryset = Transaction.objects.filter ( user=self.request.user )

        date_from = self.request.query_params.get ( 'date_from' )
        date_to = self.request.query_params.get ( 'date_to' )

        if date_from :
            queryset = queryset.filter ( date__gte=date_from )
        if date_to :
            queryset = queryset.filter ( date__lte=date_to )

        return queryset

    def get_serializer_class(self) :
        if self.request.method == 'POST' :
            return TransactionCreateSerializer
        return TransactionSerializer

    @swagger_auto_schema (
        operation_description="Barcha tranzaksiyalarni olish (filter, search, ordering bilan)",
        manual_parameters=[
            openapi.Parameter ( 'date_from', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)",
                                type=openapi.TYPE_STRING ),
            openapi.Parameter ( 'date_to', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)",
                                type=openapi.TYPE_STRING ),
        ],
        responses={200 : TransactionSerializer ( many=True )}
    )
    def get(self, request, *args, **kwargs) :
        return super ().get ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Yangi tranzaksiya yaratish",
        request_body=TransactionCreateSerializer,
        responses={201 : TransactionSerializer ()}
    )
    def post(self, request, *args, **kwargs) :
        serializer = TransactionCreateSerializer ( data=request.data, context={'request' : request} )
        serializer.is_valid ( raise_exception=True )
        transaction = serializer.save ()
        return Response (
            TransactionSerializer ( transaction ).data,
            status=status.HTTP_201_CREATED
        )


class TransactionDetailView ( generics.RetrieveUpdateDestroyAPIView ) :
    permission_classes = [IsAuthenticated]

    def get_queryset(self) :
        return Transaction.objects.filter ( user=self.request.user )

    def get_serializer_class(self) :
        if self.request.method in ['PUT', 'PATCH'] :
            return TransactionUpdateSerializer
        return TransactionSerializer

    @swagger_auto_schema (
        operation_description="Bitta tranzaksiya ma'lumotlarini olish",
        responses={200 : TransactionSerializer ()}
    )
    def get(self, request, *args, **kwargs) :
        return super ().get ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Tranzaksiyani to'liq yangilash",
        request_body=TransactionUpdateSerializer,
        responses={200 : TransactionSerializer ()}
    )
    def put(self, request, *args, **kwargs) :
        return super ().put ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Tranzaksiyani qisman yangilash",
        request_body=TransactionUpdateSerializer,
        responses={200 : TransactionSerializer ()}
    )
    def patch(self, request, *args, **kwargs) :
        return super ().patch ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Tranzaksiyani o'chirish",
        responses={204 : 'Transaction deleted successfully'}
    )
    def delete(self, request, *args, **kwargs) :
        return super ().delete ( request, *args, **kwargs )


class TransactionStatsView ( APIView ) :
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema (
        operation_description="Umumiy statistika - valyuta bo'yicha kirim, chiqim va balans",
        manual_parameters=[
            openapi.Parameter ( 'currency', openapi.IN_QUERY, description="Valyuta (UZS, USD, EUR, RUB)",
                                type=openapi.TYPE_STRING ),
            openapi.Parameter ( 'date_from', openapi.IN_QUERY, description="Boshlanish sanasi",
                                type=openapi.TYPE_STRING ),
            openapi.Parameter ( 'date_to', openapi.IN_QUERY, description="Tugash sanasi", type=openapi.TYPE_STRING ),
        ],
        responses={200 : TransactionStatsSerializer ()}
    )
    def get(self, request) :
        currency = request.query_params.get ( 'currency', 'UZS' )
        date_from = request.query_params.get ( 'date_from' )
        date_to = request.query_params.get ( 'date_to' )

        queryset = Transaction.objects.filter ( user=request.user, currency=currency )

        if date_from :
            queryset = queryset.filter ( date__gte=date_from )
        if date_to :
            queryset = queryset.filter ( date__lte=date_to )

        income_data = queryset.filter ( transaction_type='income' ).aggregate (
            total=Sum ( 'amount' ),
            count=Count ( 'id' )
        )

        expense_data = queryset.filter ( transaction_type='expense' ).aggregate (
            total=Sum ( 'amount' ),
            count=Count ( 'id' )
        )

        total_income = income_data['total'] or 0
        total_expense = expense_data['total'] or 0

        stats = {
            'total_income' : total_income,
            'total_expense' : total_expense,
            'balance' : total_income - total_expense,
            'income_count' : income_data['count'],
            'expense_count' : expense_data['count'],
            'currency' : currency
        }

        serializer = TransactionStatsSerializer ( stats )
        return Response ( serializer.data )


class CategoryStatsView ( APIView ) :
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema (
        operation_description="Kategoriyalar bo'yicha statistika",
        manual_parameters=[
            openapi.Parameter ( 'transaction_type', openapi.IN_QUERY, description="Tranzaksiya turi (income/expense)",
                                type=openapi.TYPE_STRING ),
            openapi.Parameter ( 'currency', openapi.IN_QUERY, description="Valyuta", type=openapi.TYPE_STRING ),
        ],
        responses={200 : openapi.Response ( 'Category statistics' )}
    )
    def get(self, request) :
        transaction_type = request.query_params.get ( 'transaction_type' )
        currency = request.query_params.get ( 'currency' )

        queryset = Transaction.objects.filter ( user=request.user )

        if transaction_type :
            queryset = queryset.filter ( transaction_type=transaction_type )
        if currency :
            queryset = queryset.filter ( currency=currency )

        category_stats = queryset.values ( 'category__name', 'category__icon' ).annotate (
            total=Sum ( 'amount' ),
            count=Count ( 'id' )
        ).order_by ( '-total' )

        return Response ( category_stats )