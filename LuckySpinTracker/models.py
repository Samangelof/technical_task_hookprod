from django.contrib.auth.models import User
from django.db import models


class RouletteRound(models.Model):
    round_number = models.IntegerField(verbose_name='Номер раунда')
    jackpot = models.BooleanField(default=False, verbose_name='Джекпот')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roulette_rounds', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Раунд рулетки'
        verbose_name_plural = 'Раунды рулетки'

    def __str__(self):
        return f"Пользователь: {self.user.username} | Раунд {self.round_number}: Джекпот - {self.jackpot}"



class SpinResult(models.Model):
    round_number = models.ForeignKey(RouletteRound, on_delete=models.CASCADE, verbose_name='Номер раунда')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    cell_number = models.IntegerField(verbose_name='Выпавшая ячейка')

    # Подразумевает под собой, что в рулетке могут участвовать несколько ((( игроков )))
    # users = models.ManyToManyField(User, verbose_name='Пользователи')
    
    class Meta:
        verbose_name = 'Информация о выпадениях'
        verbose_name_plural = 'Информация о выпадениях' 

    def __str__(self):
        return f"{self.round_number} | Выпавшая ячейка {self.cell_number}"
    

class Channel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='channel')
    rounds = models.ManyToManyField(RouletteRound, verbose_name='Раунды', related_name='channels')

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f"Комната пользователя {self.user.username}"
