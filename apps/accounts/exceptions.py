from rest_framework.exceptions import APIException


class UserAlreadyActivatedException(APIException):
    status_code = 400
    default_detail = 'This account is already activated.'
    default_code = 'user_already_activated'
