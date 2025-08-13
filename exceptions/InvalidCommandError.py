class InvalidCommandError(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"InvalidCommandError: {self.message}"