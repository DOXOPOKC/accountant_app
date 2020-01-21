from django.test import TestCase
from .views import calculate
from datetime import date

from bluebird.models import NormativeCategory


class test_calculate(TestCase):
    """ Тестируем считающую функцию """
    date_from = date.fromisoformat('2019-05-05')
    date_to = date.fromisoformat('2019-07-02')
    norm = NormativeCategory.objects.filter(name='аптека').first().pk
    val = 200
    data_dict = {
        'since_date': date_from,
        'up_to_date': date_to,
        'stat_value': val,
        'norm_value': norm
        }
    res = calculate(**data_dict)
    test_res = [
            {
                'curr_date': date.fromisoformat('2019-05-31'),
                'V_as_rough': '5.32',
                'summ_rough': '2209.77',
                'tax_price_rough': '441.95',
                'summ_tax_rough': '2651.72',
                'tax': 0.2,
                'tariff': 415.37,
                'tariff_tax': '498.44',
                'V_as_precise': '4.46194',
                'summ_precise': '1853.36',
                'tax_price_precise': '370.67',
                'summ_tax_precise': '2224.03'
            },
            {
                'curr_date': date.fromisoformat('2019-06-30'),
                'V_as_rough': '5.32',
                'summ_rough': '2209.77',
                'tax_price_rough': '441.95',
                'summ_tax_rough': '2651.72',
                'tax': 0.2,
                'tariff': 415.37,
                'tariff_tax': '498.44',
                'V_as_precise': '5.32',
                'summ_precise': '2209.77',
                'tax_price_precise': '441.95',
                'summ_tax_precise': '2651.72'
            }
        ]
    print(res)
    assert res == test_res
