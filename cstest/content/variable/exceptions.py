class NoVariableNameValue(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class VariableStructureInvalid(Exception):
    def __init__(self, message: str):
        super().__init__(message)
