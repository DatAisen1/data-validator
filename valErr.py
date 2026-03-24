class ValidationError(Exception):
    
    def __init__(self, field: str, message: str) -> str:
        self.field = field
        self.message = message
        super().__init__(message)