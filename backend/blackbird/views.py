from blackbird.models import Formula
from bluebird.models import NormativeCategory

from datetime import date
import calendar


def calculate(*args, **kwargs):
    since_date = kwargs.get('since_date', None)  # Дата с начала расчета
    up_to_date = kwargs.get('up_to_date', None)  # Дата конца расчета
    stat_value = kwargs.get('stat_value', None)  # Значение показателя (м2, кол. чел. и т.д.)
    norm_value = kwargs.get('norm_value', None)  # Ключ на норматив

    # Что делать с активными днями и днями невывоза?

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
        print(curr_date)
        norm = get_normative(curr_date, norm_value)  # Норматив

        formula_obj_r = get_formula_object(curr_date)  # Объект формулы грубый подсчет
        formula_rough = formula_obj_r.get_formula()  # Формула (в виде строки)

        formula_obj_p = get_formula_object(curr_date, rough=False) # Объект формулы точный расчет
        formula_precise = formula_obj_p.get_formula()  # Формулы точного рассчета в вике строки

        m_day_count = calendar.monthrange(curr_date.year, curr_date.month)[1]  # Количество дней в месяце
        a_day_count = m_day_count - start_day  # Количество активных дней
        V_as_rough = eval(eval(formula_rough))  # Грубый объем расситаный по формуле
        V_as_precise = eval(eval(formula_precise))  # точный объем рассчитаный по формуле

        summ_precise = V_as_precise * formula_obj_p.get_tariff()  # Точная сумма по объему
        tax_price_precise = summ_precise * formula_obj_p.get_tax()  # Точный НДС по объему
        summ_tax_precise = summ_precise + tax_price_precise  # Точная сумма с НДС

        summ_rough = V_as_rough * formula_obj_r.get_tariff()  # Грубая сумма по объему
        tax_price_rough = summ_rough * formula_obj_r.get_tax()  # Грубый НДС по объему
        summ_tax_rough = summ_rough + tax_price_rough  # Грубая сумма с НДС

        tariff_tax = formula_obj_p.get_tariff() * (1 + formula_obj_p.get_tax())  # Тариф с НДС

        result.append(
            {
                'curr_date': curr_date,
                'V_as_rough': format(V_as_rough, '.5f'),
                'summ_rough': format(summ_rough, '.2f'),
                'tax_price_rough': format(tax_price_rough, '.2f'),
                'summ_tax_rough': format(summ_tax_rough, '.2f'),
                'tax': formula_obj_p.get_tax(),
                'tariff': formula_obj_p.get_tariff(),
                'tariff_tax': format(tariff_tax, '.2f'),
                'V_as_precise': format(V_as_precise, '.5f'),
                'summ_precise': format(summ_precise, '.2f'),
                'tax_price_precise': format(tax_price_precise, '.2f'),
                'summ_tax_precise': format(summ_tax_precise, '.2f')
            })
        start_day = 0
    return result


def get_formula_object(curr_date, rough=True):
    formulas = Formula.objects.filter(is_rough=rough)
    for f in formulas:
        if f.since_date <= curr_date <= f.up_to_date:
            return f


def get_normative(curr_date, norm_value):
    norm = NormativeCategory.objects.get(pk=norm_value)
    norm_vals = norm.normative.all()
    for n in norm_vals:
        if n.since_date <= curr_date <= n.up_to_date:
            return n.value


def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12*start_year + start_month - 1
    ym_end = 12*end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m + 1


if __name__ == '__main__':
    p = calculate(since_date=date.fromisoformat('2019-01-05'),
                  up_to_date=date.fromisoformat('2020-01-10'),
                  stat_value=75,
                  norm_value=2)
    print(p)
