from django import template

register = template.Library()


@register.filter
def new_lang_code(current_lang_code):
    if current_lang_code == 'en':
        return 'ru'
    else:
        return 'en'


@register.filter
def new_lang_name(current_lang_code):
    if current_lang_code == 'en':
        return 'Russian'
    else:
        return 'English'
