from django import template
from django.template.defaultfilters import stringfilter
from .num2t4ru import decimal2text
import decimal


register = template.Library()


@register.filter(name='literal')
@stringfilter
def literal(value):
    return decimal2text(decimal.Decimal(value),
                        int_units=((u'рубль', u'рубля', u'рублей'), 'm'),
                        exp_units=((u'копейка', u'копейки', u'копеек'), 'f'))
