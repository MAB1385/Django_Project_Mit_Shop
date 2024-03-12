from os import path
from time import time
from uuid import uuid4

from django.db import connection, reset_queries
from kavenegar import APIException, HTTPException, KavenegarAPI
import secrets


def create_random_code(number):
    """create_random_code

    Args:
        number (int): number of digits

    Returns:
        int: random number
    """
    number -= 1
    return secrets.SystemRandom().randint(10**number, 10 ** (number + 1) - 1)


# todo --------------------------------------------------------------
def send_sms(mobail_number, text):
    """send_sms

    Args:
        mobail_number (str): len=11
        text (str): text --> message
    """
    pass
    # try:
    #     api = KavenegarAPI(
    #         "4C395332786B3758536D69544B677646523637365837495351337565456154642F75654C6845785165596F3D"
    #     )
    #     params = {"sender": "10008663", "receptor": mobail_number, "message": text}
    #     response = api.sms_send(params)
    #     return response
    # except APIException as error:
    #     print(str(error))
    # except HTTPException as error:
    #     print(str(error))


# todo --------------------------------------------------------------
def price_by_delivery_tax(price, discount=0):
    delivery = 25000
    if price > 500000:
        delivery = 0
    tax = (price + delivery) * 0.09
    sum = price + delivery + tax
    sum -= sum * discount / 100
    return int(sum), delivery, int(tax)


# todo --------------------------------------------------------------
class FileUpload:
    """FileUpload"""

    def __init__(self, dir, prefix) -> None:
        """__init__

        Args:
            dir (str): dir root --> images,files,videos
            prefix (str): folder name
        """
        self.__dir = dir
        self.__prefix = prefix

    def upload_to(self, instance, filename):
        filename, ext = path.splitext(filename)
        return f"{self.__dir}/{self.__prefix}/{uuid4()}{ext}"


# todo --------------------------------------------------------------
def debugger_time_query(func):
    def wrapper(*args, **kwargs):
        reset_queries()
        st = time()
        value = func(*args, **kwargs)
        et = time()
        queries = len(connection.queries)
        print(
            f"\n---------------\nconnection number: {queries}\ntake time: {(et-st):.f3}\n---------------\n"
        )
        return value

    return wrapper
