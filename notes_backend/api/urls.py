from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    NoteViewSet,
)

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('health/', health, name='Health'),
    path('auth/register/', UserRegisterView.as_view(), name="register"),
    path('auth/login/', UserLoginView.as_view(), name="login"),
    path('auth/logout/', UserLogoutView.as_view(), name="logout"),
    path('', include(router.urls)),
]
