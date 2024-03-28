from pointcloud.training.inference.api.domain.exceptions.application_error import ApplicationError


class AppException(ApplicationError):

    def __init__(self, message = "Client Exception", additional_info = ""):
        self.message = message + " " + additional_info
        self.status_code : int = 400
        super().__init__(message=self.message)

class NotFoundException(ApplicationError):
        def __init__(self, message : str, additional_info = ""):
            self.message = message + " " + additional_info
            self.status_code = 404
            super.__init__(message=self.message)
