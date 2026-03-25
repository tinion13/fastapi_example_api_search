from exceptions.base import ClientError, ServiceError


class WeathersClientError(ClientError):
    pass


class WeathersClientTransportError(WeathersClientError):
    pass


class WeathersClientResponseError(WeathersClientError):
    pass


class WeathersServiceError(ServiceError):
    pass


class WeathersServiceBadResponseError(WeathersServiceError):
    pass


class WeathersServiceValidationError(WeathersServiceError):
    pass


class WeathersProviderUnavailable(WeathersServiceError):
    pass
