from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

# Register your models here.
admin.site.register(LogEntry)
admin.site.register(ContentType)