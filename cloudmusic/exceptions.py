from rest_framework.exceptions import APIException


class NotFound(APIException):
    status_code = 404
