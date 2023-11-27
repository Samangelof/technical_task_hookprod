from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import generics
from django.db.models import Count
from django.contrib.auth.models import User

from .models import RouletteRound, SpinResult, Channel
from .serializers import UserSerializer


class CreateUserAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpinRoulette(APIView):
    permission_classes = [AllowAny]

    def check_required_fields(self, data):
        required_fields = ["room_id", "round_number", "user_id", "cell_number"]
        missing_fields = []
        for field in required_fields:
            if data.get(field) is None:
                missing_fields.append(field)
        return missing_fields

    def post(self, request):
        """ Вращение рулетки """
        room_id = request.data.get('room_id')
        round_number = request.data.get('round_number')
        user_id = request.data.get('user_id')
        cell_number = request.data.get('cell_number')

        try:
            channel = Channel.objects.get(id=room_id)
            roulette_round = channel.rounds.get(round_number=round_number)
        except (Channel.DoesNotExist, RouletteRound.DoesNotExist):
            return Response({"message": "Комната или раунд с указанными номерами не существует"}, status=status.HTTP_404_NOT_FOUND)

        missing_fields = self.check_required_fields(request.data)
        if missing_fields:
            return Response(
                {
                    "message": "Отсутствуют обязательные поля",
                    "missing_fields": missing_fields
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if SpinResult.objects.filter(round_number=roulette_round, cell_number=cell_number).exists():
            return Response({"message": f"Ячейка {cell_number} уже выпала в этом раунде"}, status=status.HTTP_400_BAD_REQUEST)

        spin_result = SpinResult(round_number=roulette_round, cell_number=cell_number, user_id=user_id)
        spin_result.save()

        spin_results_count = SpinResult.objects.filter(round_number=roulette_round, cell_number__lt=11).count()
        if spin_results_count == 10 and not roulette_round.jackpot:
            roulette_round.jackpot = True
            roulette_round.save()

            new_round_number = int(round_number) + 1
            new_roulette_round = RouletteRound(round_number=new_round_number, user_id=user_id)
            new_roulette_round.save()
            channel.rounds.add(new_roulette_round)
            return Response({"message": "*** хъ!!! Джекпот !!!хъ *** ", "jackpot": True}, status=status.HTTP_200_OK)
        return Response({"message": "Рулетка прокручена успешно"}, status=status.HTTP_200_OK)


class RouletteParticipants(APIView):
    def get(self, request):
        # Получение количества уникальных пользователей для каждого раунда
        rounds = RouletteRound.objects.annotate(
            user_count=Count('user', distinct=True)
        ).values('round_number', 'user_count')

        # Формирование списка словарей для JSON ответа
        data = [
            {
                'round_number': round_data['round_number'],
                'user_count': round_data['user_count']
            }
            for round_data in rounds
        ]

        return Response(data)


class ActiveUsers(APIView):
    def get(self, request):
        active_users = (
        User.objects.annotate(rounds_played=Count('spinresult__round_number', distinct=True))
            .filter(rounds_played__gt=0)
            .order_by('-rounds_played')
            .values('id', 'username', 'rounds_played', 'avg_spins_per_round')[:10],
        )
        
        data = list(active_users)

        return Response(data)