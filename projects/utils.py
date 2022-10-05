import uuid

from django.utils.translation import gettext_lazy as _


# colors dictionary to generate QR on the opposite color background
COLORS = {'#000000': '#ffffff',
          '#0000ff': '#ffff00',
          '#840000': '#7bffff',
          '#008484': '#ff7b7b',
          '#008400': '#ff7bff',
          '#800080': '#7fff7f',
          '#000084': '#ffff7b',
          '#008080': '#ff7f7f',
          '#614051': '#9ebfae',
          }


def get_uuid_id():
    return str(uuid.uuid4())


def get_day_word(num):
    if num == 0:
        return _('дней')
    elif num % 100 >= 5 and num % 100 <= 20:
        return _('дней')
    elif num % 10 == 1:
        print('tut1')
        return _('день')
    elif num % 10 >= 2 and num % 10 <= 4:
        print('tut2')
        return _('дня')
