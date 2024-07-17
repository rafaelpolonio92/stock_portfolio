from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import User, Portfolio
from .serializers import UserSerializer, PortfolioSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_id": user.id
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuyStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        ticker = request.data.get('ticker')
        purchase_price = request.data.get('purchasePrice')
        portfolio, created = Portfolio.objects.get_or_create(user=user)
        portfolio_data = portfolio.portfolio
        portfolio_data.append({"ticker": ticker, "purchasePrice": purchase_price})
        portfolio.portfolio = portfolio_data
        portfolio.save()
        return Response(PortfolioSerializer(portfolio).data)

class SellStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        ticker = request.data.get('ticker')
        portfolio = Portfolio.objects.get(user=user)
        portfolio_data = [stock for stock in portfolio.portfolio if stock['ticker'] != ticker]
        portfolio.portfolio = portfolio_data
        portfolio.save()
        return Response(PortfolioSerializer(portfolio).data)

class PortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        if user_id is None:
            user_id = request.user.id
        try:
            portfolio = Portfolio.objects.get(user_id=user_id)
            serializer = PortfolioSerializer(portfolio)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Portfolio.DoesNotExist:
            return Response({"error": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND)