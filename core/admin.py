from django.contrib import admin

from .models import Pin, Board,Look


class PinAdmin(admin.ModelAdmin):
    pass


admin.site.register(Pin, PinAdmin)
admin.site.register(Board)
admin.site.register(Look)
