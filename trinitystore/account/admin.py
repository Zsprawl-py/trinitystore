from django.contrib import admin

from .models import Profile, Subscribe


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'vip']
    raw_id_fields = ['user']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'acceptance', 'expiration', 'vip_type']