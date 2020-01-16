from rest_framework.views import exception_handler
from rest_framework import exceptions
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.views import set_rollback
from rest_framework.response import Response


def custom_exception_handler(exc, context):

    # completely rewritten exception handler
    # we did this to get a top-level “errors” wrapper over exception messages

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = {'errors': exc.detail}
        else:
            data = {'errors': {'detail': exc.detail}}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return
