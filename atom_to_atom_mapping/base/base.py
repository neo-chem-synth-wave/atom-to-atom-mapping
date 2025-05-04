""" The ``atom_to_atom_mapping.base`` package ``base`` module. """

from abc import ABC, abstractmethod
from logging import Logger
from typing import Any, Dict, List, Optional, Sequence


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

        return self._logger

    @logger.setter
    def logger(
            self,
            value: Optional[Logger]
    ) -> None:
        """
        Set the value of the logger.

        :parameter value: The value of the logger.
        """

        self._logger = value

    @abstractmethod
    def map_reaction_smiles(
            self,
            reaction_smiles: str
    ) -> Dict[str, Any]:
        """
        Map a chemical reaction SMILES string.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.

        :returns: The mapped chemical reaction SMILES string.
        """

    @abstractmethod
    def map_reaction_smiles_strings(
            self,
            reaction_smiles_strings: Sequence[str]
    ) -> List[Dict[str, Any]]:
        """
        Map the chemical reaction SMILES strings.

        :parameter reaction_smiles_strings: The SMILES strings of the chemical reactions.

        :returns: The mapped chemical reaction SMILES strings.
        """
