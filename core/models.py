from django.db import models



class LogEntry(models.Model):
    """
    Model for log entry.
    """
    HTTP_METHODS = models.TextChoices('HttpMethod', 'GET POST DELETE PUT PATCH OPTIONS')

    ip = models.GenericIPAddressField()
    date = models.DateTimeField()
    http_method = models.CharField(blank=True, choices=HTTP_METHODS.choices, max_length=8)
    request_uri = models.URLField()
    status_code = models.IntegerField()
    response_size = models.IntegerField()

    def __str__(self):
        return f"Log Entry for {self.ip}"

    class Meta:
        verbose_name_plural = 'Entries'
        # Add unique constraint to prevent duplicate records.
        constraints = [
            models.UniqueConstraint(fields=['ip', 'date', 'request_uri'], name='unique_records'),
        ]
