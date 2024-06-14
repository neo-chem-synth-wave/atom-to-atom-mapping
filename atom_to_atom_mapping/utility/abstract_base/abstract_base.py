""" The ``atom_to_atom_mapping.utility.abstract_base`` package ``abstract_base`` module. """

from abc import ABC, abstractmethod

from typing import Any, Dict, List, Optional, Sequence


class AbstractBaseAtomToAtomMappingUtility(ABC):
    """ The abstract base chemical reaction compound atom-to-atom mapping utility class. """

    @staticmethod
    @abstractmethod
    def map_reaction_smiles(
            reaction_smiles: str,
            **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Map a chemical reaction `SMILES` string.

        :parameter reaction_smiles: The chemical reaction `SMILES` string.
        :parameter kwargs: The keyword arguments for the adjustment of the underlying functions and methods.

        :returns: The output of the chemical reaction compound atom-to-atom mapping.
        """

    @staticmethod
    @abstractmethod
    def map_reaction_smiles_strings(
            reaction_smiles_strings: Sequence[str],
            **kwargs
    ) -> Optional[List[Optional[Dict[str, Any]]]]:
        """
        Map the chemical reaction `SMILES` strings.

        :parameter reaction_smiles_strings: The chemical reaction `SMILES` strings.
        :parameter kwargs: The keyword arguments for the adjustment of the underlying functions and methods.

        :returns: The outputs of the chemical reaction compound atom-to-atom mapping.
        """
