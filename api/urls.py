from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, BuyStockView, SellStockView, PortfolioView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('buy/', BuyStockView.as_view(), name='buy_stock'),
    path('sell/', SellStockView.as_view(), name='sell_stock'),
    path('portfolio/<int:user_id>/', PortfolioView.as_view(), name='user-portfolio'),
]
