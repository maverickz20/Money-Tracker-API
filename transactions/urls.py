from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    TransactionListCreateView,
    TransactionDetailView,
    TransactionStatsView,
    CategoryStatsView
)

urlpatterns = [
    path ( 'categories/', CategoryListCreateView.as_view (), name='category-list-create' ),
    path ( 'categories/<int:pk>/', CategoryDetailView.as_view (), name='category-detail' ),
    path ( 'categories/stats/', CategoryStatsView.as_view (), name='category-stats' ),

    path ( '', TransactionListCreateView.as_view (), name='transaction-list-create' ),
    path ( '<int:pk>/', TransactionDetailView.as_view (), name='transaction-detail' ),
    path ( 'stats/', TransactionStatsView.as_view (), name='transaction-stats' ),
]