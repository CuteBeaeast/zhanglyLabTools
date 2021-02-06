class LabTools_exception(BaseException):
    pass

class cli_input_error(LabTools_exception):
    def __init__(self, message=''):
        self.message = message
    
    def __str__(self):
        return "CLI input Error: " + self.message
