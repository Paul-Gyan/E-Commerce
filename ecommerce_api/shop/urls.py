from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, OrderViewSet, PromotionViewSet
from .views import ProductImageViewSet, WishlistViewSet, ReviewViewSet, PaymentViewSet
from .views import CartViewSet, CartItemViewSet
from .models import Cart, CartItem


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'promotions', PromotionViewSet)
router.register(r'product_images', ProductImageViewSet)
router.register(r'wishlists', WishlistViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
