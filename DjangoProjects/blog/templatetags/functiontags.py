# -*- coding: utf-8 -*-
from django import template
import unicodedata

register = template.Library()


@register.filter(name='pau')
def relace_a(str, val):
    return str.replace('a', val)

@register.simple_tag
def replace_tag(str, *args):

    source = args[0]
    target = args[1]

    return str.replace(source, target)


@register.filter(name='string_to_url')
def string_to_url(string):

    import unidecode

    valid = u'qazwsxedcrfvtgbyhnujmiklopñ '
    valid += valid.upper()
    valid += '1234567890'

    new_string = ''
    string = u'{}'.format(unidecode.unidecode(string))

    for char in string:
        if char in valid:
            new_string += char

    new_string.replace(u'ñ', 'n')

    return unicodedata.normalize('NFKD', new_string).encode('ASCII', 'ignore').replace(' ', '-').lower()
