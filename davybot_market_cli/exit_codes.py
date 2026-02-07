"""CLI exit codes."""

# Success
SUCCESS = 0

# Errors
ERROR_GENERIC = 1
ERROR_NETWORK = 2
ERROR_API = 3
ERROR_NOT_FOUND = 4
ERROR_INVALID_INPUT = 5
ERROR_FILESYSTEM = 6
ERROR_PERMISSION = 7
ERROR_TIMEOUT = 8
ERROR_API_UNHEALTHY = 10


class ExitCodeError(SystemExit):
    """Custom exception for exiting with a specific exit code."""

    def __init__(self, exit_code: int, message: str = ""):
        self.exit_code = exit_code
        self.message = message
        super().__init__(exit_code)
