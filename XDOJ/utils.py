import hashlib
import random
import threading

from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from rest_framework import status
import datetime
import account.models
from XDOJ import settings


def get_dict(**kwargs):
    return kwargs


def send_email_sync(subject, content, to, alternatives=None):
    msg = EmailMultiAlternatives(subject=subject, body=content, from_email=settings.EMAIL_HOST_USER,
                                 to=to, alternatives=alternatives)
    msg.attach_alternative(content, "text/html")
    msg.send()


def rand_str(length=32, mode="str"):
    """
    生成指定长度的随机字符串或者数字, 可以用于密钥等安全场景
    :param length: 字符串或者数字的长度
    :param mode: str 代表随机字符串，num 代表随机数字
    :return: 字符串
    """
    if mode == "str":
        return get_random_string(length, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    elif mode == "upper_str":
        return get_random_string(length, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    elif mode == "hex_str":
        return random.choice("123456789ABCDEF") + get_random_string(length - 1, allowed_chars="0123456789ABCDEF")
    else:
        return random.choice("123456789") + get_random_string(length - 1, allowed_chars="0123456789")



