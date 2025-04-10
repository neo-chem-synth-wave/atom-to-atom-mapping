""" The ``atom_to_atom_mapping.utility`` package ``rxnmapper`` module. """

from logging import Logger
from math import ceil
from typing import Collection, Dict, List, Optional, Union

from rxnmapper.core import RXNMapper

from tqdm.auto import tqdm


class RXNMapperAtomToAtomMappingUtility:
    """
    The `RXNMapper <https://github.com/rxn4chemistry/rxnmapper>`_ chemical reaction compound atom-to-atom mapping
    utility class.
    """

    @staticmethod
    def map_reaction(
            reaction_smiles: str,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> Optional[Dict[str, Union[None, float, str]]]:
        """
        Map a chemical reaction.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `rxnmapper.core.RXNMapper.get_attention_guided_atom_maps` }.

        :returns: The mapped chemical reaction and confidence score.
        """

        try:
            rxnmapper = RXNMapper()

            rxnmapper_output = rxnmapper.get_attention_guided_atom_maps(
                rxns=[reaction_smiles, ],
                **kwargs
            )

            return {
                "mapped_reaction_smiles": rxnmapper_output[0].get("mapped_rxn", None),
                "confidence_score": rxnmapper_output[0].get("confidence", None),
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
            batch_size: int = 10,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> Optional[List[Optional[Dict[str, Union[None, float, str]]]]]:
        """
        Map the chemical reactions.

        :parameter reaction_smiles_strings: The SMILES strings of the chemical reactions.
        :parameter batch_size: The size of the batch.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `rxnmapper.core.RXNMapper.get_attention_guided_atom_maps` }.

        :returns: The mapped chemical reactions and confidence scores.
        """

        try:
            rxnmapper = RXNMapper()

            rxnmapper_outputs = list()

            tqdm_description = "Mapping the chemical reactions in batches (Batch Size: {batch_size:d})".format(
                batch_size=batch_size
            )

            for reaction_smiles_index in tqdm(
                iterable=range(0, len(reaction_smiles_strings), batch_size),
                desc=tqdm_description,
                total=ceil(len(reaction_smiles_strings) / batch_size),
                ncols=len(tqdm_description) + 50
            ):
                try:
                    rxnmapper_batch_outputs = rxnmapper.get_attention_guided_atom_maps(
                        rxns=list(reaction_smiles_strings[reaction_smiles_index: reaction_smiles_index + batch_size]),
                        **kwargs
                    )

                    for rxnmapper_batch_output in rxnmapper_batch_outputs:
                        rxnmapper_outputs.append({
                            "mapped_reaction_smiles": rxnmapper_batch_output.get("mapped_rxn", None),
                            "confidence_score": rxnmapper_batch_output.get("confidence", None),
                        })

                except:
                    for reaction_smiles in reaction_smiles_strings[
                        reaction_smiles_index: reaction_smiles_index + batch_size
                    ]:
                        try:
                            rxnmapper_output = rxnmapper.get_attention_guided_atom_maps(
                                rxns=[reaction_smiles, ],
                                **kwargs
                            )

                            rxnmapper_outputs.append({
                                "mapped_reaction_smiles": rxnmapper_output[0].get("mapped_rxn", None),
                                "confidence_score": rxnmapper_output[0].get("confidence", None),
                            })

                        except Exception as exception_handle:
                            if logger is not None:
                                logger.error(
                                    msg=exception_handle,
                                    exc_info=True
                                )

                            rxnmapper_outputs.append({
                                "mapped_reaction_smiles": None,
                                "confidence_score": None,
                            })

            return rxnmapper_outputs

        except Exception as exception_handle:
            if logger is not None:
                logger.error(
                    msg=exception_handle,
                    exc_info=True
                )

            return list()
