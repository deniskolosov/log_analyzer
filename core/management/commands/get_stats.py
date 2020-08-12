from typing import Dict

from django.core.management import BaseCommand
from django.db.models import Count, Sum, QuerySet
from django.db.models.functions import Upper

from core.models import LogEntry


def get_unique_ips_count() -> int:
    """
    Returns number of unique ip addresses.
    """
    return LogEntry.objects.values('ip').distinct().count()


def get_most_common_ips() -> Dict[str, int]:
    """
    Returns dict with 10 most common ip addresses.
    """
    return {
        obj["ip"]: obj["ip_count"]
        for obj in LogEntry.objects.values('ip').annotate(
            ip_count=Count('ip')).order_by('-ip_count')[:10]
    }


def get_method_counts() -> Dict[str, int]:
    """
    Returns dict mapping methods to number of their occurencies.
    """
    qs = LogEntry.objects.annotate(method_upper=Upper('http_method')).values(
        'method_upper').distinct().annotate(count=Count('method_upper'))
    return {obj["method_upper"]: obj["count"] for obj in qs}


def get_total_transferred_bytes() -> QuerySet:
    """
    Get total number of transferred bytes by summing all response bytes count.
    """
    return LogEntry.objects.aggregate(
        total_size=Sum('response_size'))['total_size']


class Command(BaseCommand):
    help = 'Get stats from db.'

    def handle(self, *args, **options):
        self.stdout.write(f"Number of unique ips: {get_unique_ips_count()}")
        self.stdout.write("--")
        self.stdout.write("Top 10 ip addresses:")
        for k, v in get_most_common_ips().items():
            print(f'{k:20} {v:6}')
        self.stdout.write("--")
        self.stdout.write("Method counts:")
        for k, v in get_method_counts().items():

            if k not in ["GET", "POST", "HEAD", "OPTIONS", "PUT", "PATCH"]:
                continue  # Remove gibberish.
            print(f'{k:6} {v:4}')
        self.stdout.write("--")
        self.stdout.write(
            f"Total transferred bytes: {get_total_transferred_bytes()}"
        )
