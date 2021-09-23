class NotFoundException(Exception):
    def __init__(self, message: str) -> None:
        """Raised when a record is not found in Database.

        In general this should be thrown whenever we get results from Database that are
        unexpected and will disrupt the rest of the program (e.g. Multiple Users are
        returned when we needed only 1 etc.)

        Args:
            message (str): Exception message.
        """
        super().__init__(message)
