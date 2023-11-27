from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max
from .models import RouletteRound, Channel

@receiver(post_save, sender=User)
def create_initial_roulette_round(sender, instance, created, **kwargs):
    if created:
        print(f"User {instance.username} is created!")  # Проверяем, вызывается ли этот вывод
        channel, _ = Channel.objects.get_or_create(user=instance)
        if channel:
            max_round_number = channel.rounds.aggregate(max_round_number=Max('round_number'))['max_round_number']
            new_round_number = max_round_number + 1 if max_round_number is not None else 1
            roulette_round = RouletteRound.objects.create(round_number=new_round_number, user=instance)
            channel.rounds.add(roulette_round)
