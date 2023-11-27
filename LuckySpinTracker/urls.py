from django.urls import path, include
from .views import (
    SpinRoulette,
    RouletteParticipants,
    ActiveUsers,
    CreateUserAPIView)


urlpatterns = [
    # Прокрутки рулетки
    path('spin/', SpinRoulette.as_view(), name='spin_roulette'),

    # Количества участников рулетки
    path('members/', RouletteParticipants.as_view(), name='roulette_participants'),
     
    # Список самых активных пользователей
    path('active_users/', ActiveUsers.as_view(), name='active_users'),

    # Создать пользователя (игрока)
    path('create_user/', CreateUserAPIView.as_view(), name='create_user'),
]