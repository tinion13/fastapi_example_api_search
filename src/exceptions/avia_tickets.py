from exceptions.base import ClientError, ServiceError


class AviaTicketsClientError(ClientError):
    pass


class AviaTicketsClientTransportError(AviaTicketsClientError):
    pass


class AviaTicketsClientResponseError(AviaTicketsClientError):
    pass


class AviaTicketsServiceError(ServiceError):
    pass


class AviaTicketsServiceBadResponseError(AviaTicketsServiceError):
    pass


class AviaTicketsServiceValidationError(AviaTicketsServiceError):
    pass


class AviaTicketsProviderUnavailable(AviaTicketsServiceError):
    pass
