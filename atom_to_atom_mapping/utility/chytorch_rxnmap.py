""" The ``atom_to_atom_mapping.utility`` package ``chytorch_rxnmap`` module. """

from functools import partial
from logging import Logger
from typing import Collection, Dict, List, Optional, Union

from chython.files.daylight.smiles import smiles

from pqdm.processes import pqdm


class ChytorchRxnMapAtomToAtomMappingUtility:
    """
    The `Chytorch RxnMap <https://github.com/chython/chytorch-rxnmap>`_ chemical reaction compound atom-to-atom mapping
    utility class.
    """

    @staticmethod
    def map_reaction(
            reaction_smiles: str,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> Dict[str, Optional[Union[float, str]]]:
        """
        Map a chemical reaction.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions and methods:
            { `chython.files.daylight.smiles.smiles`, `chython.algorithms.mapping.attention.Attention.reset_mapping` }.

        :returns: The mapped chemical reaction and confidence score.
        """

        try:
            chython_reaction = smiles(
                reaction_smiles,
                ignore=kwargs.pop("ignore", True),
                remap=kwargs.pop("remap", False),
                ignore_stereo=kwargs.pop("ignore_stereo", False),
                ignore_bad_isotopes=kwargs.pop("ignore_bad_isotopes", False),
                keep_implicit=kwargs.pop("keep_implicit", False),
                ignore_carbon_radicals=kwargs.pop("ignore_carbon_radicals", False),
                ignore_aromatic_radicals=kwargs.pop("ignore_aromatic_radicals", True)
            )

            kwargs.pop("return_score", None)

            chytorch_rxnmap_confidence_score = chython_reaction.reset_mapping(
                return_score=True,
                multiplier=kwargs.pop("multiplier", 1.75),
                keep_reactants_numbering=kwargs.pop("keep_reactants_numbering", False)
            )

            return {
                "mapped_reaction_smiles": format(chython_reaction, "m"),
                "confidence_score": chytorch_rxnmap_confidence_score,
            }

        except Exception as exception_handle:
            if logger is not None:
                logger.error(
                    msg=exception_handle,
                    exc_info=True
                )

            return {
                "mapped_reaction_smiles": None,
                "confidence_score": None,
            }

    @staticmethod
    def map_reactions(
            reaction_smiles_strings: Collection[str],
            number_of_processes: int = 1,
            **kwargs
    ) -> List[Dict[str, Optional[Union[float, str]]]]:
        """
        Map the chemical reactions.

        :parameter reaction_smiles_strings: The SMILES strings of the chemical reactions.
        :parameter number_of_processes: The number of processes.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `atom_to_atom_mapping.utility.chytorch_rxnmap.ChytorchRxnMapAtomToAtomMappingUtility.map_reaction` }.

        :returns: The mapped chemical reactions and confidence scores.
        """

        pqdm_description = "Mapping the chemical reactions (Number of Processes: {number_of_processes:d})".format(
            number_of_processes=number_of_processes
        )

        return pqdm(
            array=reaction_smiles_strings,
            function=partial(
                ChytorchRxnMapAtomToAtomMappingUtility.map_reaction,
                **kwargs
            ),
            n_jobs=number_of_processes,
            desc=pqdm_description,
            total=len(reaction_smiles_strings),
            ncols=len(pqdm_description) + (50 if number_of_processes == 1 else 75)
        )
