from datetime import datetime
import re

from django.core.management import BaseCommand
from django.core.validators import URLValidator, ValidationError

import requests
from core.models import LogEntry


class FileNotFound(Exception):
    pass


def parse_log_file(resp: requests.Response) -> int:
    """
    Parse downloaded log file from requests' response, return inserted objects count.
    Raises exception if response's status code is not 200 or similar.
    """
    if not (200 <= resp.status_code < 300):
        raise FileNotFound("Can't download file")

    regex = '([(\d\.)]+) - - \[(.*?)\] \"(.*?)\" (\d+) (\d+) \"(.*?)\" \"(.*?)\"'
    log_file_iterator = resp.iter_lines()
    log_entries = []

    for line in log_file_iterator:
        line = line.decode()
        match = re.match(regex, line)
        if not match or not line:
            # Skip empty lines, or lines without necessary info.
            continue

        ip_address, date, req, status, size, url, agent = re.match(
            regex, line).groups()
        date = datetime.strptime(date, "%d/%b/%Y:%H:%M:%S %z")
        log_entries.append(
            LogEntry(ip=ip_address,
                     date=date,
                     http_method=req.split(' ')[0],
                     status_code=int(status),
                     response_size=int(size),
                     request_uri=url))

    LogEntry.objects.bulk_create(log_entries, ignore_conflicts=True)
    return LogEntry.objects.count()


class Command(BaseCommand):
    help = 'Download log file from provided link'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        url = options['url']
        validator = URLValidator()

        try:
            validator(url)
        except ValidationError:
            raise

        # Download first ~200mb bytes of log.
        resp = requests.get(url, headers={"Range": "bytes=0-200000000"})
        print(parse_log_file(resp))
