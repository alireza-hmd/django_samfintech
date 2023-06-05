from django.urls import path
from . import views


urlpatterns = [
    path('VerifyUser/', views.VerifyUser.as_view(), name='verify_user'),
    path('BuyStock/', views.StockView.as_view(), name='buy_stock'),
]