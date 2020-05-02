from rest_framework import status
from rest_framework.response import Response

from utils.tools import get_dict


def _ResultResponse(err, msg, http_status):
    return Response(get_dict(err=err, msg=msg), status=http_status)


def SuccessResponse(msg=None, err=None, http_status=status.HTTP_200_OK):
    return _ResultResponse(err, msg, http_status)


def ErrorResponse(msg=None, err='error', http_status=status.HTTP_200_OK):
    return _ResultResponse(err, msg, http_status)