""" The ``atom_to_atom_mapping.utility.ibm_rxn4chemistry`` package ``rxnmapper`` module. """

from logging import Logger
from math import ceil
from typing import Dict, List, Optional, Sequence, Union
from warnings import filterwarnings

from rxnmapper.core import RXNMapper

from tqdm.auto import tqdm


class RXNMapperAtomToAtomMappingUtility:
    """
    The `RXNMapper <https://github.com/rxn4chemistry/rxnmapper>`_ chemical reaction compound atom-to-atom mapping
    utility class.
    """

    @staticmethod
    def map_reaction_smiles(
            reaction_smiles: str,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> Optional[Dict[str, Union[None, float, str]]]:
        """
        Map a chemical reaction `SMILES` string.

        :parameter reaction_smiles: The chemical reaction `SMILES` string.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `rxnmapper.core.RXNMapper.get_attention_guided_atom_maps` }.

        :returns: The output of the chemical reaction compound atom-to-atom mapping.
        """

        try:
            filterwarnings(
                action="ignore",
                category=UserWarning
            )

            rxnmapper = RXNMapper()

            rxnmapper_output = rxnmapper.get_attention_guided_atom_maps(
                rxns=[
                    reaction_smiles,
                ],
                **kwargs
            )

            return {
                "mapped_reaction_smiles": rxnmapper_output[0].get("mapped_rxn", None),
                "confidence_score": rxnmapper_output[0].get("confidence", None),
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
            batch_size: int = 10,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> Optional[List[Optional[Dict[str, Union[None, float, str]]]]]:
        """
        Map the chemical reaction `SMILES` strings.

        :parameter reaction_smiles_strings: The chemical reaction `SMILES` strings.
        :parameter batch_size: The batch size.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `rxnmapper.core.RXNMapper.get_attention_guided_atom_maps` }.

        :returns: The outputs of the chemical reaction compound atom-to-atom mapping.
        """

        try:
            filterwarnings(
                action="ignore",
                category=UserWarning
            )

            rxnmapper = RXNMapper()

            rxnmapper_outputs = list()

            for reaction_smiles_index in tqdm(
                iterable=range(0, len(reaction_smiles_strings), batch_size),
                desc="Mapping the chemical reaction SMILES strings (Batch Size: {batch_size:d})".format(
                    batch_size=batch_size
                ),
                total=ceil(len(reaction_smiles_strings) / batch_size),
                ncols=150
            ):
                rxnmapper_batch_outputs = rxnmapper.get_attention_guided_atom_maps(
                    rxns=list(reaction_smiles_strings[reaction_smiles_index: reaction_smiles_index + batch_size]),
                    **kwargs
                )

                for rxnmapper_batch_output in rxnmapper_batch_outputs:
                    rxnmapper_outputs.append({
                        "mapped_reaction_smiles": rxnmapper_batch_output.get("mapped_rxn", None),
                        "confidence_score": rxnmapper_batch_output.get("confidence", None),
                    })

            return rxnmapper_outputs

        except Exception as exception_handle:
            if logger is not None:
                logger.debug(
                    msg=exception_handle,
                    exc_info=True
                )

            return None
