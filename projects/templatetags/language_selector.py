from django import template

register = template.Library()


@register.filter
def new_lang_code(current_lang_code):
    if current_lang_code == 'en':
        print(1, current_lang_code)
        return 'ru'
    else:
        print(2, current_lang_code)
        return 'en'


@register.filter
def new_lang_name(current_lang_code):
    if current_lang_code == 'en':
        return 'Russian'
    else:
        return 'English'
