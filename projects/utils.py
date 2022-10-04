import uuid


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

