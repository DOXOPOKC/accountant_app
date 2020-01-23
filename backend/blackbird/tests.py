from django.test import TestCase
from .views import calculate, round_hafz
from datetime import date

from bluebird.models import NormativeCategory, Normative
from .models import Formula


class ViewTest(TestCase):

    def test_calculate(self):
        """ Тестируем считающую функцию """

        # Фикстуры для временной тестовой базы
        Formula.objects.create(since_date=date.fromisoformat('2018-09-01'),
                               up_to_date=date.fromisoformat('2020-02-29'),
                               tax_rate=0.2,
                               tariff=415.37,
                               is_rough=True,
                               equasion="""f'{stat_value} * {norm}'""")
        eq = """f'({norm}/{m_day_count}) * {stat_value} * {a_day_count}'"""
        Formula.objects.create(since_date=date.fromisoformat('2018-09-01'),
                               up_to_date=date.fromisoformat('2020-02-29'),
                               tax_rate=0.2,
                               tariff=415.37,
                               is_rough=False,
                               equasion=eq)

        norm = Normative.objects.create(
            since_date=date.fromisoformat('2018-09-01'),
            up_to_date=date.fromisoformat('2020-02-29'),
            value=0.0266
        )
        norm_cat = NormativeCategory.objects.create(name='аптека')
        norm_cat.normative.set([norm.pk, ])
        # Конец фикстур

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
        self.assertEqual(test_res, res)

    def test_round_function(self):
        """ Тест функции округления. """
        test_1 = round_hafz(12.345, 2)
        test_2 = round_hafz(-12.345, 2)
        test_3 = round_hafz(0.000886666666667, 7)
        self.assertEqual(test_1, 12.35)
        self.assertEqual(test_2, -12.35)
        self.assertEqual(test_3, 0.0008867)
