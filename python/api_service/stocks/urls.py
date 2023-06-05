from django.urls import path
from . import views


urlpatterns = [
    path('BuyStock/', views.StockView.as_view(), name='buy_stock'),
]