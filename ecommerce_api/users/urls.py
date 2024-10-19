from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, user_dashboard, RegisterViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    
]
