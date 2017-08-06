# !/usr/bin/env python
# -*- coding: utf-8 -*-


class CloverError(Exception):
    pass


class CloverNotImplemented(CloverError):
    pass


class CloverBadRequest(CloverError):
    """ HTTP 400 (Bad Request) """
    pass


class CloverUnauthorized(CloverError):
    """ HTTP 401 (Unauthorized)"""
    pass


class CloverAccessDenied(CloverError):
    """ HTTP 403 (Access Denied)"""
    pass


class CloverNotFound(CloverError):
    """ HTTP 404 (Not Found) """
    pass


class CloverConflict(CloverError):
    """ HTTP 409 (Conflict) """
    pass


class CloverInternalServerError(CloverError):
    """ HTTP 500 (Internal Sever Error) """
    pass


class CloverUnknown(CloverError):
    pass