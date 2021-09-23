from abc import ABCMeta, abstractmethod
from typing import Optional

from pawtrails.models.user import User


# Abstract metaclass so that we do not instance a hidden ObjectCreator instance
class BaseDatabase(metaclass=ABCMeta):
    """
    Base database client from which all other database clients should inherit.
    This abstract class should contain all the pydoc details.
    It should also only contain methods and constants.
    """

    @abstractmethod
    def get_user(
        self,
        *,
        uuid: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Optional[User]:
        """Gets user from the database based on either the UUID, Username or Email.

        If multiple fields are provided, the precedence is UUID > Username > Email, and
        the first positive match should return the user.

        Args:
            uuid (str, optional): Unique identifier for the User node. Defaults to None.
            username (str, optional): Name of the user. Defaults to None.
            email (str, optional): Email of the user. Defaults to None.

        Raises:
            NotImplementedError: Derived class did not provide an implementation.
            ValueError: Neither uuid, username or email has been specified.
            NotFoundException: More than one user has been found.

        Returns:
            Optional[User]: User node if user is found
        """
        raise NotImplementedError

    @abstractmethod
    def create_user(self, *, user: User) -> Optional[User]:
        """Creates the user in the database.

        Returns the user with the created_at and updated_at fields.

        Args:
            user (User): The User object we wish to save to the database.

        Raises:
            NotImplementedError: Derived class did not provide an implementation.
            ValueError: Either username, password or email is missing.

        Returns:
            Optional[User]: User node if it was sucessfully created
        """
        raise NotImplementedError
