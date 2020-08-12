from django.contrib import admin
from django.contrib.auth.models import Group

from core import models


class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        'ip',
        'date',
        'http_method',
        'request_uri',
        'status_code',
        'response_size',
    )
    search_fields = ('date', 'ip', 'response_size')


admin.site.site_header = "Log Analyzer"
admin.site.register(models.LogEntry, LogEntryAdmin)
