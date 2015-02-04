from . import constants


class RestlessError(Exception):
    """
    A common base exception from which all other exceptions in ``restless``
    inherit from.

    No special attributes or behaviors.
    """
    pass


class HttpError(RestlessError):
    """
    The foundational HTTP-related error.

    All other HTTP errors in ``restless`` inherit from this one.

    Has a ``status`` attribute. If present, ``restless`` will use this as the
    ``status_code`` in the response.

    Has a ``msg`` attribute. Has a reasonable default message (override-able
    from the constructor).
    """
    status = constants.APPLICATION_ERROR
    msg = "Application Error"
    code = constants.CUSTOM_APPLICATION_ERROR
    resolution = "The server encountered an internal error. Please retry the request."

    def __init__(self, msg=None, code=None, resolution=None):
        if not msg:
            msg = self.__class__.msg

        if code:
            self.code = code

        if resolution:
            self.resolution = resolution

        super(HttpError, self).__init__(msg)


class BadRequest(HttpError):
    status = constants.BAD_REQUEST
    msg = "Bad request."


class Unauthorized(HttpError):
    status = constants.UNAUTHORIZED
    msg = "Unauthorized."


class Forbidden(HttpError):
    status = constants.FORBIDDEN
    msg = 'Resource forbidden.'


class NotFound(HttpError):
    status = constants.NOT_FOUND
    msg = "Resource not found."


class Conflict(HttpError):
    status = constants.CONFLICT
    message = "Resource conflict."


class MethodNotAllowed(HttpError):
    status = constants.METHOD_NOT_ALLOWED
    msg = "The specified HTTP method is not allowed."


class MethodNotImplemented(HttpError):
    status = constants.METHOD_NOT_IMPLEMENTED
    msg = "The specified HTTP method is not implemented."


# Validation
class InvalidDataType(BadRequest):
    code = constants.CUSTOM_INVALID_DATA_TYPE
    resolution = "Ensure the parameters of your request include the required valid data types."


class MissingRequiredField(BadRequest):
    code = constants.CUSTOM_MISSING_REQUIRED_FIELD
    resolution = "Ensure you include all required fields in the body of the request."


class IncorrectFormat(BadRequest):
    code = constants.CUSTOM_INCORRECT_FORMAT
    resolution = "Ensure you properly format your request."


class InvalidMessageFormat(BadRequest):
    code = constants.CUSTOM_INVALID_MESSAGE_FORMAT
    resolution = "Serialization error, please ensure the body has balanced braces and brackets."


class InvalidValue(BadRequest):
    code = constants.CUSTOM_INVALID_VALUE
    resolution = "Ensure you provide valid values in your request."


# Authorization
class AccountUnauthorized(Unauthorized):
    code = constants.CUSTOM_ACCOUNT_UNAUTHORIZED
    resolution = "Ensure you provide a valid token."


# Authentication
class NotAuthenticated(Forbidden):
    code = constants.CUSTOM_NOT_AUTHENTICATED
    resolution = "You account lacks the privileges necessary to perform the request."


# Runtime
class ObjectNotFound(NotFound):
    code = constants.CUSTOM_OBJECT_NOT_FOUND
    resolution = "Your request cannot find any available data."


class ObjectAlreadyExists(Conflict):
    code = constants.CUSTOM_OBJECT_ALREADY_EXISTS
    resolution = "Another object with the same credentials already exists."