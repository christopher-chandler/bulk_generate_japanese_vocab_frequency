# Standard
from enum import Enum

# Custom Error Messages
class CustomErrorMessages:
    """
    Custom error messages
    """

    class BaseCustomException(Exception):
        """
        Base class for custom exceptions
        """
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

    class NoteTypeMismatch(BaseCustomException):
        """
        Exception raised for note type mismatches.
        """
        def __init__(self, note_type):
            message = f"Note type mismatch: {note_type}. Please check your config file to set the correct note type."
            super().__init__(message)

    class VocabFieldNotFound(BaseCustomException):
        """
        Exception raised when the vocabulary input field is not found.
        """
        def __init__(self, vocab_field):
            message = f"Vocab field '{vocab_field}' not found!"
            super().__init__(message)

    class DestinationFieldNotFound(BaseCustomException):
        """
        Exception raised when the destination field is not found.
        """
        def __init__(self, destination_field):
            message = f"Destination field '{destination_field}' not found!"
            super().__init__(message)

    class VocabFieldNotEmpty(BaseCustomException):
        """
        Exception raised when the vocabulary input field is not empty.
        """
        def __init__(self, vocab_field):
            message = f"{vocab_field} is not empty. Skipping!"
            super().__init__(message)

# Example usage
try:
    raise CustomErrorMessages.NoteTypeMismatch("Basic")
except CustomErrorMessages.NoteTypeMismatch as e:
    print(e)

try:
    raise CustomErrorMessages.VocabFieldNotFound("Word")
except CustomErrorMessages.VocabFieldNotFound as e:
    print(e)

try:
    raise CustomErrorMessages.DestinationFieldNotFound("Frequency")
except CustomErrorMessages.DestinationFieldNotFound as e:
    print(e)

try:
    raise CustomErrorMessages.VocabFieldNotEmpty("Word")
except CustomErrorMessages.VocabFieldNotEmpty as e:
    print(e)
