from django.urls import path
from rest_framework.authtoken import views as auth_views
from .views import RegisterView, LoginView, BuyStockView, SellStockView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('buy/', BuyStockView.as_view(), name='buy_stock'),
    path('sell/', SellStockView.as_view(), name='sell_stock'),
]
