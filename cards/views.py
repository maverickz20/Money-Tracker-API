from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Card
from .serializers import (
    CardSerializer,
    CardCreateSerializer,
    CardUpdateSerializer,
    CardListSerializer
)


class CardListCreateView ( generics.ListCreateAPIView ) :
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['card_type', 'currency', 'is_active']
    search_fields = ['name', 'bank_name', 'card_number']
    ordering_fields = ['balance', 'created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self) :
        return Card.objects.filter ( user=self.request.user )

    def get_serializer_class(self) :
        if self.request.method == 'POST' :
            return CardCreateSerializer
        return CardListSerializer

    @swagger_auto_schema (
        operation_description="Barcha kartalarni olish (filter, search, ordering bilan)",
        responses={200 : CardListSerializer ( many=True )}
    )
    def get(self, request, *args, **kwargs) :
        return super ().get ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Yangi karta yaratish",
        request_body=CardCreateSerializer,
        responses={201 : CardSerializer ()}
    )
    def post(self, request, *args, **kwargs) :
        serializer = CardCreateSerializer ( data=request.data, context={'request' : request} )
        serializer.is_valid ( raise_exception=True )
        card = serializer.save ()
        return Response (
            CardSerializer ( card ).data,
            status=status.HTTP_201_CREATED
        )


class CardDetailView ( generics.RetrieveUpdateDestroyAPIView ) :
    permission_classes = [IsAuthenticated]

    def get_queryset(self) :
        return Card.objects.filter ( user=self.request.user )

    def get_serializer_class(self) :
        if self.request.method in ['PUT', 'PATCH'] :
            return CardUpdateSerializer
        return CardSerializer

    @swagger_auto_schema (
        operation_description="Bitta karta ma'lumotlarini olish",
        responses={200 : CardSerializer ()}
    )
    def get(self, request, *args, **kwargs) :
        return super ().get ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Kartani to'liq yangilash",
        request_body=CardUpdateSerializer,
        responses={200 : CardSerializer ()}
    )
    def put(self, request, *args, **kwargs) :
        return super ().put ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Kartani qisman yangilash",
        request_body=CardUpdateSerializer,
        responses={200 : CardSerializer ()}
    )
    def patch(self, request, *args, **kwargs) :
        return super ().patch ( request, *args, **kwargs )

    @swagger_auto_schema (
        operation_description="Kartani o'chirish",
        responses={204 : 'Card deleted successfully'}
    )
    def delete(self, request, *args, **kwargs) :
        return super ().delete ( request, *args, **kwargs )


class CardStatsView ( generics.RetrieveAPIView ) :
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self) :
        return Card.objects.filter ( user=self.request.user )

    @swagger_auto_schema (
        operation_description="Karta bo'yicha batafsil statistika",
        responses={200 : CardSerializer ()}
    )
    def get(self, request, *args, **kwargs) :
        return super ().get ( request, *args, **kwargs )