import datetime

from django.test import SimpleTestCase
from django.utils.timezone import localtime, now

from App.templatetags.customtags import days_since, is_today


class CustomTagsTests(SimpleTestCase):
    def test_is_today(self):
        today = localtime(now()).date()

        self.assertTrue(is_today(today))
        self.assertFalse(is_today(today - datetime.timedelta(days=1)))

    def test_days_since(self):
        today = localtime(now()).date()

        self.assertEqual(days_since(today), "Today")
        self.assertEqual(days_since(today - datetime.timedelta(days=1)), "Yesterday")
        self.assertEqual(days_since(today + datetime.timedelta(days=1)), "Tomorrow")
        self.assertEqual(days_since(today - datetime.timedelta(days=4)), "4 days")
        self.assertEqual(days_since(today - datetime.timedelta(days=7)), "last week")
        self.assertEqual(days_since(today - datetime.timedelta(days=40)), "last month")
        self.assertEqual(days_since(today - datetime.timedelta(days=400)), "last year")
