""" The ``atom_to_atom_mapping.utility.chytorch`` package ``rxnmap`` module. """

import chython

from functools import partial
from logging import Logger
from typing import Dict, List, Optional, Sequence, Union

from pqdm.processes import pqdm


class RxnMapAtomToAtomMappingUtility:
    """
    The `RxnMap <https://github.com/chython/chytorch-rxnmap>`_ chemical reaction compound atom-to-atom mapping utility
    class.
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
            chytorch_rxnmap_reaction = chython.smiles(
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

            chytorch_rxnmap_score = chytorch_rxnmap_reaction.reset_mapping(
                return_score=True,
                multiplier=kwargs.pop("multiplier", 1.75),
                keep_reactants_numbering=kwargs.pop("keep_reactants_numbering", False)
            )

            return {
                "mapped_reaction_smiles": format(chytorch_rxnmap_reaction, "m"),
                "confidence_score": chytorch_rxnmap_score,
            }

        except Exception as exception_handle:
            if logger is not None:
                logger.exception(
                    msg=exception_handle
                )

            return None

    @staticmethod
    def map_reaction_smiles_strings(
            reaction_smiles_strings: Sequence[str],
            number_of_jobs: int = 1,
            torch_device: Optional[str] = None,
            **kwargs
    ) -> Optional[List[Optional[Dict[str, Union[float, str]]]]]:
        """
        Map the chemical reaction `SMILES` strings.

        :parameter reaction_smiles_strings: The chemical reaction `SMILES` strings.
        :parameter number_of_jobs: The number of jobs.
        :parameter torch_device: The indicator of the `PyTorch` device. The value `None` indicates that the default
            `PyTorch` device should be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `atom_to_atom_mapping.utility.chytorch.rxnmap.RxnMapAtomToAtomMappingUtility.map_reaction_smiles` }.

        :returns: The outputs of the chemical reaction compound atom-to-atom mapping.
        """

        chython.pickle_cache = True

        if torch_device is not None:
            chython.torch_device = torch_device

        return pqdm(
            array=reaction_smiles_strings,
            function=partial(
                RxnMapAtomToAtomMappingUtility.map_reaction_smiles,
                **kwargs
            ),
            n_jobs=number_of_jobs,
            desc="Mapping the chemical reaction SMILES strings ({parameters:s})".format(
                parameters="PyTorch Device: '{torch_device:s}', Number of Jobs: {number_of_jobs:d}".format(
                    torch_device=chython.torch_device,
                    number_of_jobs=number_of_jobs
                )
            ),
            total=len(reaction_smiles_strings),
            ncols=200
        )
