from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, OrderViewSet, PromotionViewSet
from .views import ProductImageViewSet
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'promotions', PromotionViewSet)
router.register(r'product_images', ProductImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
