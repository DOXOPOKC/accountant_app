from django.test import TestCase
from bluebird.utils import generate_act, generate_document
from bluebird.models import (Contragent, ContractNumberClass,
                             ActUNGen)
from datetime import date


class GenerationDocsTest(TestCase):
    """ Тесты генерации документов """

    ACT = """
        # TODO create a example HTML document
    """

    def test_creation_act(self):
        """ Тест генерации акта. """
        # Добавляем фикстуры
        contragent = Contragent.objects.create(
            klass=1,
            excell_name='ИП Лупа и Пупа',
            inn=422553212,
            kpp=422880055,
            rs='880005553575',
            ks='3010181020000000077799563254',
            bank='ФИЛИАЛ БАНКА ПРИЕМА ВКЛАДОВ "РОГА И КОПЫТА" В Г. МОСКВЕ',
            bik=8008135,
            is_func=True,
            physical_address='КЕМЕРОСКАЯ ОБЛАСТЬ, г. НОВОКУЗНЕЦК, ул. Пушкина \
                д. Колотушкина',
            legal_address='КЕМЕРОСКАЯ ОБЛАСТЬ, г. КЕМЕРОВО, ул. Ленина д. 15',
            number_contract=ContractNumberClass.create(new=True),
            current_date=date.fromisoformat('2019-05-21')
        )
        calc_result = {
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
        }
        unique_number = ActUNGen.create(calc_result['curr_date'], contragent)
        calc_result['uniq_num_id'] = unique_number
        # Конец фикстур

        res = generate_act(calc_result, contragent)
        generate_document(res, 'test_act.pdf')
        self.assertTrue(res)
        # self.assertEqual(res, self.ACT)

    def test_generate_pay_count(self):
        """ Тест генерации счета на оплату. """
        pass

    def test_generate_count_list(self):
        """ Тест генерации счета фактуры. """
        pass
