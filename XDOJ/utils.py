import hashlib

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework import status
import datetime
import account.models


def response_dict(**kwargs):
    return kwargs
