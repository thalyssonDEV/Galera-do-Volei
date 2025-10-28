from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JogadorViewSet, PartidaViewSet
from .auth_views import LoginView

router = DefaultRouter()
router.register(r'jogadores', JogadorViewSet, basename='jogador')
router.register(r'partidas', PartidaViewSet, basename='partida')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]