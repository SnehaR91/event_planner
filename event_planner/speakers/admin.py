from django.contrib import admin
from .models import Guest, Speaker

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'organization', 'event')
    search_fields = ('name', 'email', 'organization')

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'topic', 'event')
    search_fields = ('name', 'email', 'topic')

