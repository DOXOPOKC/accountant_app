from django.test import TestCase
from bluebird.utils import generate_act
from bluebird.models import Contragent
from datetime import date


class test_creation_doc(TestCase):
    generate_act(
        {
            'curr_date': date.fromisoformat('2020-01-14'),
            'V_as_precise': '3.00000',
            'tariff_tax': '498.44',
            'summ_tax_precise': '1495.44',
            'tax_price_precise': '249.22'
        },
        Contragent.objects.get(pk=1))
    assert True
