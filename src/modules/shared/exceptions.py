class AppError(Exception):
    pass


class ServiceError(AppError):
    pass


class ClientError(AppError):
    pass
