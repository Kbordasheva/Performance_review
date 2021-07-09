from abc import ABC, abstractmethod


class BaseService(ABC):
    """ Base class for all project services.
    """

    @abstractmethod
    def perform(self, **kwargs) -> bool:
        """ Service entry point.
        """
        pass
