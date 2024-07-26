""" The ``atom_to_atom_mapping.utility.cimm_kfu`` package ``chytorch_rxnmap`` module. """

from functools import partial
from logging import Logger
from typing import Dict, List, Optional, Sequence, Union

from chython.files.daylight.smiles import smiles

from pqdm.processes import pqdm


class ChytorchRxnMapAtomToAtomMappingUtility:
    """
    The `Chytorch RxnMap <https://github.com/chython/chytorch-rxnmap>`_ chemical reaction compound atom-to-atom mapping
    utility class.
    """

    @staticmethod
    def map_reaction_smiles(
            reaction_smiles: str,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> Optional[Dict[str, Union[float, str]]]:
        """
        Map a chemical reaction `SMILES` string.

        :parameter reaction_smiles: The chemical reaction `SMILES` string.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions and methods:
            { `chython.algorithms.mapping.attention.Attention.reset_mapping`, `chython.files.daylight.smiles.smiles` }.

        :returns: The output of the chemical reaction compound atom-to-atom mapping.
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
                logger.debug(
                    msg=exception_handle,
                    exc_info=True
                )

            return None

    @staticmethod
    def map_reaction_smiles_strings(
            reaction_smiles_strings: Sequence[str],
            number_of_processes: int = 1,
            **kwargs
    ) -> Optional[List[Optional[Dict[str, Union[float, str]]]]]:
        """
        Map the chemical reaction `SMILES` strings.

        :parameter reaction_smiles_strings: The chemical reaction `SMILES` strings.
        :parameter number_of_processes: The number of processes.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `ChytorchRxnMapAtomToAtomMappingUtility.map_reaction_smiles` }.

        :returns: The outputs of the chemical reaction compound atom-to-atom mapping.
        """

        return pqdm(
            array=reaction_smiles_strings,
            function=partial(
                ChytorchRxnMapAtomToAtomMappingUtility.map_reaction_smiles,
                **kwargs
            ),
            n_jobs=number_of_processes,
            desc="Mapping the chemical reaction SMILES strings (Number of Processes: {number_of_processes:d})".format(
                number_of_processes=number_of_processes
            ),
            total=len(reaction_smiles_strings),
            ncols=150
        )
