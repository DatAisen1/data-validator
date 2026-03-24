class ValidationError(Exception):
    
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(message)