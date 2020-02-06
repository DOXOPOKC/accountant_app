from django import template
from django.template.defaultfilters import stringfilter
from .num2t4ru import decimal2text
import pymorphy2
import decimal


register = template.Library()


@register.filter(name='literal')
@stringfilter
def literal(value):
    return decimal2text(decimal.Decimal(value),
                        int_units=((u'рубль', u'рубля', u'рублей'), 'm'),
                        exp_units=((u'копейка', u'копейки', u'копеек'), 'f'))


@register.filter(name='percentage')
def percentage(value, arg: int = 1):
    if arg:
        return f'{(value/arg)*100}%'
    else:
        return f'{value}%'


@register.filter(name='gent_case')
def gent_case(value: str):
    return gent_case_filter(value)


def gent_case_filter(value: str):
    morph = pymorphy2.MorphAnalyzer()
    normalizer_val = value.strip()
    word_list = normalizer_val.split(' ')
    res = list()
    for word in word_list:
        parsed_phrase = morph.parse(word)[0]
        gent_form = parsed_phrase.inflect({'gent'})[0]
        res.append(gent_form)
    return str(' '.join(res)).title()


def pretty_date_filter(date_value):
    months = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
              'августа', 'сентября', 'октября', 'ноября', 'декабря')
    return f'"{date_value.day}" {months[date_value.month-1]} {date_value.year}'
