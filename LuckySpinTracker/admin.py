from django.contrib import admin
from .models import RouletteRound, SpinResult, Channel


class RouletteRoundAdmin(admin.ModelAdmin):
    list_display = ('get_user_username', 'round_number', 'jackpot_display')

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'Пользователь'

    def jackpot_display(self, obj):
        if obj.jackpot:
            return True
        else:
            return False
    jackpot_display.short_description = 'Джекпот'
    jackpot_display.boolean = True 


class SpinResultAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'user', 'cell_number')
    list_filter = ('round_number',)
    search_fields = ('round_number__round_number', 'user__username', 'cell_number')
    ordering = ('round_number',)

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('id', 'user__username')


admin.site.register(Channel, ChannelAdmin)
admin.site.register(RouletteRound, RouletteRoundAdmin)
admin.site.register(SpinResult)