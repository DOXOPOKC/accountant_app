from blackbird.models import Formula
from bluebird.models import NormativeCategory

from datetime import date
import calendar
import math


def calculate(*args, **kwargs):
    """
    Функция принимает на вход словарь с параметрами
        since_date: Дата с начала расчета
        up_to_date: Дата конца расчета
        stat_value: Значение показателя (м2, кол. чел. и т.д.)
        norm_value: Ключ на норматив

    Если параметров нет (или переданы не все) вызывает AttributeError().

    Функция итерирует по датам, берет формулу расчета в виде строки на конец
    месяца, вычисляет некоторые необходимые в расчетах значения и возвращает
    массив словарей.
    -------------------------------------------------------------------------
    Формулы:
        formula_obj_r: Объект формулы грубого подсчета
        formula_rough: Формула грубого подсчета(в виде строки)
        formula_obj_p: Объект формулы точного подсчета
        formula_precise: Формула точного подсчета(в виде строки)
    -------------------------------------------------------------------------
    Значения которые могут быть использованы в формулах:
        norm: Норматив на текущую дату
        m_day_count: Количество дней в месяце
        a_day_count: Количество активных дней
    -------------------------------------------------------------------------
    Вычисляемые значения:
        V_as_rough: Грубый объем расситаный по формуле
        V_as_precise: Точный объем рассчитаный по формуле
        summ_precise: Точная сумма по объему
        tax_price_precise: Точный НДС по объему
        summ_tax_precise: Точная сумма с НДС
        summ_rough: Грубая сумма по объему
        tax_price_rough: Грубый НДС по объему
        summ_tax_rough: Грубая сумма с НДС
        tariff_tax: Тариф с НДС
    -------------------------------------------------------------------------
    Словарь результата:
        curr_date: Текущая дата
        V_as_rough: Грубый объем расситаный по формуле
        summ_rough: Грубая сумма по объему
        tax_price_rough: Грубый НДС по объему
        summ_tax_rough: Грубая сумма с НДС
        tax: НДС на текущую дату
        tariff: Тариф на текущую дату
        tariff_tax: Тариф с НДС
        V_as_precise: Точный объем рассчитаный по формуле
        summ_precise: Точная сумма по объему
        tax_price_precise: Точный НДС по объему
        summ_tax_precise: Точная сумма с НДС
    """
    since_date = kwargs.get('since_date', None)
    up_to_date = kwargs.get('up_to_date', None)
    stat_value = kwargs.get('stat_value', None)
    norm_value = kwargs.get('norm_value', None)

    # Что делать с активными днями и днями невывоза?
    # Что еще добавить сюда?
    # Переработать механизм вычисления по формуле?

    if not (stat_value and norm_value and since_date and up_to_date):
        raise AttributeError()

    result = []
    print(since_date, up_to_date, stat_value, norm_value)
    start_day = since_date.day

    for dt in month_year_iter(since_date.month, since_date.year,
                              up_to_date.month, up_to_date.year,):
        curr_date = date(day=calendar.monthrange(dt[0], dt[1])[1],
                         month=dt[1],
                         year=dt[0])
        # print(curr_date)
        norm = get_normative(curr_date, norm_value)

        formula_obj_r = get_formula_object(curr_date)
        formula_rough = formula_obj_r.get_formula()

        formula_obj_p = get_formula_object(curr_date, rough=False)
        formula_precise = formula_obj_p.get_formula()

        m_day_count = calendar.monthrange(curr_date.year, curr_date.month)[1]
        a_day_count = m_day_count - start_day
        print(norm, a_day_count)

        # print(eval(formula_rough))
        # print(eval(formula_precise))

        V_as_rough = round_hafz(eval(eval(formula_rough)), 5)
        V_as_precise = round_hafz(eval(eval(formula_precise)), 5)

        summ_precise = round_hafz(V_as_precise * formula_obj_p.get_tariff(), 2)
        tax_price_precise = round_hafz(summ_precise * formula_obj_p.get_tax(),
                                       2)
        summ_tax_precise = round_hafz(summ_precise + tax_price_precise, 2)

        summ_rough = round_hafz(V_as_rough * formula_obj_r.get_tariff(), 2)
        tax_price_rough = round_hafz(summ_rough * formula_obj_r.get_tax(), 2)
        summ_tax_rough = round_hafz(summ_rough + tax_price_rough, 2)

        print(summ_precise)

        tariff_tax = formula_obj_p.get_tariff() * (1 + formula_obj_p.get_tax())

        result.append(
            {
                'curr_date': curr_date,
                'V_as_rough': str(V_as_rough),
                'summ_rough': str(summ_rough),
                'tax_price_rough': str(tax_price_rough),
                'summ_tax_rough': str(summ_tax_rough),
                'tax': formula_obj_p.get_tax(),
                'tariff': formula_obj_p.get_tariff(),
                'tariff_tax': str(round_hafz(tariff_tax, 2)),
                'V_as_precise': str(V_as_precise),
                'summ_precise': str(summ_precise),
                'tax_price_precise': str(tax_price_precise),
                'summ_tax_precise': str(summ_tax_precise)
            })
        start_day = 0
    return result


def get_formula_object(curr_date, rough=True):
    """ Функция возвращает объект формулы на переданную дату. Параметр `rough`
    отвечает за то, будет формула грубого подсчета или нет.
    """
    formulas = Formula.objects.filter(is_rough=rough)
    for f in formulas:
        # print(f.since_date, '|', f.up_to_date, '| is', curr_date)
        if f.since_date <= curr_date <= f.up_to_date:
            return f


def get_normative(curr_date, norm_value):
    """ Функция возвращает значение норматива на переданную дату.
    Параметр `pk` первичный ключ норматива.
    """
    norm = NormativeCategory.objects.get(pk=norm_value)
    norm_vals = norm.normative.all()
    for n in norm_vals:
        if n.since_date <= curr_date <= n.up_to_date:
            return n.value


def month_year_iter(start_month, start_year, end_month, end_year):
    """ Функция возвращает итератор дат.
    Принимает на вход 4 параметра:
        start_month - начальный месяц
        start_year - начальный год
        end_month - конечный месяц
        end_year - конечный год
     """
    ym_start = 12*start_year + start_month - 1
    ym_end = 12*end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m + 1


def round_hafz(n, decimals=0):
    """ Функция правильного округления. 12.345 => 12.35 -12.567 => -12.57 """
    multiplier = 10 ** decimals
    temp_calc = math.floor(abs(n)*multiplier + 0.5) / multiplier
    return math.copysign(temp_calc, n)


if __name__ == '__main__':
    p = calculate(since_date=date.fromisoformat('2019-01-05'),
                  up_to_date=date.fromisoformat('2020-01-10'),
                  stat_value=75,
                  norm_value=2)
    print(p)
