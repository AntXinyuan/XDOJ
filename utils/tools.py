import random
import re
import time
import threading
from base64 import b64encode
from io import BytesIO
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from XDOJ import settings


class ImageStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        import os
        ext = os.path.splitext(name)[1]
        _dir = os.path.dirname(name)
        fn = rand_str(mode='time') + rand_str()
        name = os.path.join(_dir, fn + ext)
        return super(ImageStorage, self)._save(name, content)


def get_dict(**kwargs):
    return kwargs


def send_email_sync(subject, content, to, alternatives=None):
    msg = EmailMultiAlternatives(subject=subject, body=content, from_email=settings.EMAIL_HOST_USER,
                                 to=to, alternatives=alternatives)
    msg.attach_alternative(content, "text/html")
    msg.send()

def send_email_async(subject, content, to, alternatives=None):
    threading.Thread(target=send_email_sync, args=(subject, content, to, alternatives)).start()

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
    elif mode == 'time':
        return time.strftime('%Y%m%d%H%M%S')
    else:
        return random.choice("123456789") + get_random_string(length - 1, allowed_chars="0123456789")


def img2base64(img):
    with BytesIO() as buf:
        img.save(buf, "gif")
        buf_str = buf.getvalue()
    img_prefix = "data:image/png;base64,"
    b64_str = img_prefix + b64encode(buf_str).decode("utf-8")
    return b64_str


def natural_sort_key(s, _nsre=re.compile(r"(\d+)")):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def str2bool(value):
    if value is None:
        return None
    else:
        _value = str.lower(value)
        if _value == 'true':
            return True
        elif _value == 'false':
            return False
        else:
            return None
