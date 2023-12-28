class ResponseException(Exception):
    error_code: str
    message: str | None
    
    def __init__(self, error_code=None, message=None):
        super().__init__()

        self.error_code = error_code
        self.message = message
        
    
