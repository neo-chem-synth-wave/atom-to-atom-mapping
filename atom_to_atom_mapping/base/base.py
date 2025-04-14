""" The ``atom_to_atom_mapping.base`` package ``base`` module. """

from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional


class AtomToAtomMappingBase(ABC):
    """ The chemical reaction compound atom-to-atom mapping base class. """

    def __init__(
            self,
            logger: Optional[Logger] = None
    ) -> None:
        """
        The `__init__` method of the class.

        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        """

        self.logger = logger

    @property
    def logger(
            self
    ) -> Optional[Logger]:
        """
        Get the value of the logger.

        :returns: The value of the logger.
        """

        return self.__logger

    @logger.setter
    def logger(
            self,
            value: Optional[Logger]
    ) -> None:
        """
        Set the value of the logger.

        :parameter value: The value of the logger. The value `None` indicates that the logger should not be utilized.
        """

        self.__logger = value

    @abstractmethod
    def map_reaction_smiles(
            self,
            **kwargs
    ) -> None:
        """ Map a chemical reaction SMILES string. """

    @abstractmethod
    def map_reaction_smiles_strings(
            self,
            **kwargs
    ) -> None:
        """ Map the chemical reaction SMILES strings. """
