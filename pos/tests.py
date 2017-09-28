from django.test import TestCase

from pos.models import A
from pos.functions import Position


class CategoryTestCase(TestCase):
    fixtures = [
        'a.json',
    ]

    def test_pos_function_simple_search(self):
        """
        Simple test with usually used data
        """
        search = 'port'
        qs = A.objects.filter(
            title__icontains=search
        ).annotate(
            pos=Position('title', search)
        ).order_by('pos').values_list('title', flat=True)
        qs_list = list(qs)
        valid_list = ['Port 2', 'port 1', 'Bport', 'A port', 'Endport']
        self.assertListEqual(qs_list, valid_list)

    def test_pos_function_before_crash_search(self):
        """
        Search in the same lines as in crashed test, but simple search string
        """
        search = "from myapp_suburb;"
        qs = A.objects.filter(
            title__icontains=search
        ).annotate(
            pos=Position('title', search)
        ).order_by('pos').values_list('title', flat=True)

        qs_list = list(qs)
        valid_list = [
            "') in '') from myapp_suburb; b45646",
            "') in '') from myapp_suburb;",
            "gfg ') in '') from myapp_suburb; b45646 por t",
            "dev456 ') in '') from myapp_suburb; _subURb ert"]
        self.assertListEqual(qs_list, valid_list)

    def test_pos_function_crash_search(self):
        """
        Crashed test.
        """
        search = "') in '') from myapp_suburb;"
        qs = A.objects.filter(
            title__icontains=search
        ).annotate(
            pos=Position('title', search)
        ).order_by('pos').values_list('title', flat=True)

        qs_list = list(qs)
        valid_list = [
            "') in '') from myapp_suburb; b45646",
            "') in '') from myapp_suburb;",
            "gfg ') in '') from myapp_suburb; b45646 por t",
            "dev456 ') in '') from myapp_suburb; _subURb ert"]
        self.assertListEqual(qs_list, valid_list)
