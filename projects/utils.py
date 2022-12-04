import os
import uuid

import fitz
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from Krone.settings import MEDIA_ROOT

load_dotenv()

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
        return _('день')
    elif num % 10 >= 2 and num % 10 <= 4:
        return _('дня')


def pdf2png(obj):
    print('__________________im in pdf2png, obj is: ', obj)
    filepath = obj.file.path
    name = filepath.split('/')[-1]
    img_filepath = f'{MEDIA_ROOT}/{name}.png'
    doc = fitz.open(filepath)  # open document's first page
    page = doc[0]
    dpi = 300  # the desired image resolution
    zoom = dpi / 72  # zoom factor, standard dpi is 72
    magnify = fitz.Matrix(zoom, zoom)  # takes care of zooming
    image = page.get_pixmap(matrix=magnify)  # make page image
    image.set_dpi(dpi, dpi)  # store dpi info in image
    # image.pil_save(img_filepath)
    print('__________________im in pdf2png, returning: ', img_filepath)
    return image

# image_temp_file = NamedTemporaryFile(delete=True)
#
# in_memory_image = open('/path/to/file', 'rb')
# # Write the in-memory file to the temporary file
# # Read the streamed image in sections
#
# for block in in_memory_image.read(1024 * 8):
#
#     # If no more file then stop
#     if not block:
#         break  # Write image block to temporary file
#     image_temp_file.write(block)
#
# file_name = 'temp.png'  # Choose a unique name for the file
# image_temp_file.flush()
# temp_file = files.File(image_temp_file, name=file_name)


# PAYMENTS

import decimal
import hashlib
from urllib import parse
from urllib.parse import urlparse


def calculate_signature(*args) -> str:
    """Create signature MD5.
    """
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def parse_response(request: str) -> dict:
    """
    :param request: Link.
    :return: Dictionary.
    """
    params = {}

    for item in urlparse(request).query.split('&'):
        key, value = item.split('=')
        params[key] = value
    return params


def check_signature_result(
        order_number: int,  # invoice number
        received_sum: decimal,  # cost of goods, RU
        received_signature: hex,  # SignatureValue
        password: str  # Merchant password
) -> bool:
    signature = calculate_signature(received_sum, order_number, password)
    if signature.lower() == received_signature.lower():
        return True
    return False


# Формирование URL переадресации пользователя на оплату.

def generate_payment_link(
        cost: decimal,  # Cost of goods, RU
        description: str = 'donation',  # Description of the purchase
) -> str:
    """URL for redirection of the customer to the service.
    """
    merchant_login = os.environ['PAYMENT_LOGIN']
    merchant_password_1 = os.environ['PAYMENT_PASSWORD1']
    payment_url = os.environ['PAYMENT_URL']
    is_test = 1

    signature = calculate_signature(
        merchant_login,
        cost,
        merchant_password_1
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        'Description': description,
        'SignatureValue': signature,
        'IsTest': is_test,
    }
    return f'{payment_url}?{parse.urlencode(data)}'


# Проверка параметров в скрипте завершения операции (SuccessURL).

def check_success_payment(request: str) -> bool:
    """ Verification of operation parameters ("cashier check") in SuccessURL script.
    :param request: HTTP parameters
    """
    merchant_password_1 = os.environ['PAYMENT_PASSWORD1']
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']

    signature = calculate_signature(cost, number, signature)

    if check_signature_result(number, cost, signature, merchant_password_1):
        return True
    return False
