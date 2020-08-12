from django.test import TestCase
from core.models import LogEntry
from django.core.management import call_command
from unittest import mock

LOG_FILE = b"""
91.233.165.63 - - [13/Dec/2015:20:58:27 +0100] "POST /administrator/index.php HTTP/1.1" 200 4494 "http://almhuette-raith.at/administrator/" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
109.61.180.115 - - [13/Dec/2015:20:58:30 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
109.61.180.115 - - [13/Dec/2015:20:58:30 +0100] "POST /administrator/index.php HTTP/1.1" 200 4494 "http://almhuette-raith.at/administrator/" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
95.47.158.158 - - [13/Dec/2015:20:59:25 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
"""


class TestDownloadLog(TestCase):
    @mock.patch('core.management.commands.download_log.requests.get')
    def test_download(self, get_mock):
        get_mock.return_value = mock.Mock(
            iter_lines=mock.Mock(return_value=LOG_FILE.split(b"\n")), status_code=200)

        call_command('download_log',
                     "http://www.almhuette-raith.at/apache-log/access.log")
        log_entry = LogEntry.objects.filter(ip='109.61.180.115').first()
        self.assertTrue(get_mock.called)
        self.assertEqual(LogEntry.objects.count(), 4)
        self.assertEqual(log_entry.date.day, 13)
        self.assertEqual(log_entry.date.month, 12)
        self.assertEqual(log_entry.date.hour, 19)
