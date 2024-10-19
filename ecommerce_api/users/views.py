from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shop.models import Order, Wishlist, Cart, CartItem

# Create your views here.
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

@api_view(['GET'])
def user_dashboard(request):
    user = request.user
    recent_orders = Order.objects.filter(user=user)[:5]
    wishlist_items = Wishlist.objects.filter(user=user)
    user_info = CustomUserSerializer(user).data
    cart = Cart.objects.filter(user=user).first()
    cart_items = CartSerializer(cart).data if cart else None
    data = {
        'user_info': user_info,
        'recent_orders': recent_orders,
        'wishlist_items': wishlist_items,
        'cart_items': cart_items
    }
    return Response(data)

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
