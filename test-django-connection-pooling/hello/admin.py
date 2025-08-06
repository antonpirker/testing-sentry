from django.contrib import admin
from .models import Greeting


@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ('message', 'count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('message',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
