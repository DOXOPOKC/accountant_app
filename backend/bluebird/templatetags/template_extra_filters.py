from django import template
from django.template.defaultfilters import stringfilter
from .num2t4ru import decimal2text
import pymorphy2
import decimal


register = template.Library()


@register.filter(name='literal')
@stringfilter
def literal(value):
    if bool(value) or value is not None:
        return decimal2text(decimal.Decimal(value),
                            int_units=((u'рубль', u'рубля', u'рублей'), 'm'),
                            exp_units=((u'копейка', u'копейки', u'копеек'),
                                       'f'))
    return ''


@register.filter(name='percentage')
def percentage(value, arg: int = 1):
    if arg:
        return f'{(value/arg)*100}%'
    else:
        return f'{value}%'


@register.filter(name='gent_case')
def gent_case(value: str):
    if bool(value) or value is not None:
        return gent_case_filter(value)
    return ''


def gent_case_filter(value: str):
    if bool(value) or value is not None:
        morph = pymorphy2.MorphAnalyzer()
        normalizer_val = value.strip()
        word_list = normalizer_val.split(' ')
        res = list()
        for word in word_list:
            parsed_phrase = morph.parse(word)[0]
            gent_form = parsed_phrase.inflect({'gent'})[0]
            res.append(gent_form)
        return str(' '.join(res)).title()
    return ''


def pretty_date_filter(date_value):
    if bool(date_value) or date_value is not None:
        months = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября',
                  'декабря')
        return f'"{date_value.day}" {months[date_value.month-1]} \
{date_value.year}'
    return ''


def datv_case_filter(value: str):
    if bool(value) or value is not None:
        morph = pymorphy2.MorphAnalyzer()
        normalizer_val = value.strip()
        word_list = normalizer_val.split(' ')
        res = list()
        for word in word_list:
            parsed_phrase = morph.parse(word)[0]
            gent_form = parsed_phrase.inflect({'datv'})[0]
            res.append(gent_form)
        return str(' '.join(res)).title()
    return ''


def cap_first(value: str):
    if bool(value) or value is not None:
        return value.capitalize()
    return ''


def proper_date_filter(date_value):
    if bool(date_value) or date_value is not None:
        return f'{date_value.day:02}.{date_value.month:02}.{date_value.year}'
    return ''
