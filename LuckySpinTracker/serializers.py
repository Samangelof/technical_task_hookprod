from rest_framework import serializers
from .models import RouletteRound, SpinResult
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Обязательные поля
        fields = ('id', 'username', 'email', 'password')  

        extra_kwargs = {
            # Пароль доступен только для записи
            'password': {'write_only': True}, 
            # Обязательное поле при создании пользователя
            'email': {'required': True},  
        }

    def create(self, validated_data):
        # Создать нового пользователя с хэшированным паролем
        user = User.objects.create_user(**validated_data)
        return user


class RouletteRoundSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    total_spins = serializers.SerializerMethodField()

    class Meta:
        model = RouletteRound
        fields = ('id', 'round_number', 'jackpot_activated', 'user_id', 'username', 'total_spins')

    def get_total_spins(self, obj):
        return SpinResult.objects.filter(round_number=obj).count()
    

class SpinResultSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    round_number = RouletteRoundSerializer()  
    cell_number = serializers.IntegerField()  

    class Meta:
        model = SpinResult
        fields = ('id', 'round_number', 'user', 'username', 'cell_number')

