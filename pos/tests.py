from django.test import TestCase
from django.db.models import Func, F, Value


from pos.models import A
from pos.functions import Position, Instr


class CategoryTestCase(TestCase):
    fixtures = [
        'a.json',
    ]

    def get_ann_cond(self, search):
        """ Modify it for change annotate condition."""
        # return Func(F('title'), Value(search), function='INSTR')
        return Instr('title', search, insensitive=True)

    def test_pos_function_simple_search(self):
        """
        Simple test with usually used data
        """
        search = 'PORt'
        qs = A.objects.filter(
            title__icontains=search
        ).annotate(
            pos=self.get_ann_cond(search)
        ).order_by('pos').values_list('title', flat=True)
        qs_list = list(qs)
        valid_list = ['Port 2', 'port 1', 'Bport', 'A port', 'Endport']
        self.assertListEqual(qs_list, valid_list)

    def test_pos_function_before_crash_search(self):
        """
        Search in the same lines as in crashed test, but simple search string
        """
        search = "from myApp_suburb;"
        qs = A.objects.filter(
            title__icontains=search
        ).annotate(
            pos=self.get_ann_cond(search)
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
        search = "') in '') from myApp_suburb;"
        qs = A.objects.filter(
            title__icontains=search
        ).annotate(
            pos=self.get_ann_cond(search)
        ).order_by('pos').values_list('title', flat=True)
        qs_list = list(qs)
        valid_list = [
            "') in '') from myapp_suburb; b45646",
            "') in '') from myapp_suburb;",
            "gfg ') in '') from myapp_suburb; b45646 por t",
            "dev456 ') in '') from myapp_suburb; _subURb ert"]
        self.assertListEqual(qs_list, valid_list)
