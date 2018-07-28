class RequestHandler:
    def can_handle(self, request):
        return False
    
    def handle(self, request):
        raise NotImplementedError

class ErrorHandler:
    def handle(self, request, exception):
        raise NotImplementedError

class Alexa:
    def __init__(self):
        self.handlers = []
    
    def add_handler(self, handler):
        self.handlers.append(handler)
        return self
    
    def add_error_handler(self, handler):
        self.error_handler = handler
        return self
    
    def handle_request(self, request):
        try:
            for handler in self.handlers:
                if handler.can_handle(request):
                    return handler.handle(request)
        except Exception as e:
            return self.error_handler.handle(request, e)
