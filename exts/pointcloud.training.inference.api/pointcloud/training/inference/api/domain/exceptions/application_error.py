class ApplicationError(Exception):
    def __init__(self, message = "An error occured"):
        self.message = message
        super().__init__(self.message)