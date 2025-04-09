""" The ``atom_to_atom_mapping.utility`` package ``local_mapper`` module. """

from logging import Logger
from math import ceil
from typing import Collection, Dict, List, Optional, Union

from localmapper.localmapper import localmapper

from tqdm.auto import tqdm


class LocalMapperAtomToAtomMappingUtility:
    """
    The `LocalMapper <https://github.com/snu-micc/LocalMapper>`_ chemical reaction compound atom-to-atom mapping utility
    class.
    """

    @staticmethod
    def map_reaction(
            reaction_smiles: str,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> Dict[str, Optional[Union[bool, str]]]:
        """
        Map a chemical reaction.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `localmapper.localmapper.localmapper.__init__` }.

        :returns: The mapped chemical reaction, mapped chemical reaction template, and confidence indicator.
        """

        try:
            local_mapper = localmapper(
                **kwargs
            )

            local_mapper_output = local_mapper.get_atom_map(
                rxns=reaction_smiles,
                return_dict=True
            )

            return {
                "mapped_reaction_smiles": local_mapper_output.get("mapped_rxn", None),
                "mapped_reaction_template_smarts": local_mapper_output.get("template", None),
                "is_confident": local_mapper_output.get("confident", None),
            }

        except Exception as exception_handle:
            if logger is not None:
                logger.error(
                    msg=exception_handle,
                    exc_info=True
                )

            return {
                "mapped_reaction_smiles": None,
                "mapped_reaction_template_smarts": None,
                "is_confident": None,
            }

    @staticmethod
    def map_reactions(
            reaction_smiles_strings: Collection[str],
            batch_size: int = 10,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> List[Dict[str, Optional[Union[bool, str]]]]:
        """
        Map the chemical reactions.

        :parameter reaction_smiles_strings: The SMILES strings of the chemical reactions.
        :parameter batch_size: The batch size.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `localmapper.localmapper.localmapper.__init__` }.

        :returns: The mapped chemical reactions, mapped chemical reaction templates, and confidence indicators.
        """

        try:
            local_mapper = localmapper(
                **kwargs
            )

            local_mapper_outputs = list()

            tqdm_description = "Mapping the chemical reactions in batches (Batch Size: {batch_size:d})".format(
                batch_size=batch_size
            )

            for reaction_smiles_index in tqdm(
                iterable=range(0, len(reaction_smiles_strings), batch_size),
                desc=tqdm_description,
                total=ceil(len(reaction_smiles_strings) / batch_size),
                ncols=len(tqdm_description) + 50
            ):
                # noinspection PyBroadException
                try:
                    local_mapper_batch_outputs = local_mapper.get_atom_map(
                        rxns=reaction_smiles_strings[reaction_smiles_index: reaction_smiles_index + batch_size],
                        return_dict=True
                    )

                    for local_mapper_batch_output in local_mapper_batch_outputs:
                        local_mapper_outputs.append({
                            "mapped_reaction_smiles": local_mapper_batch_output.get("mapped_rxn", None),
                            "mapped_reaction_template_smarts": local_mapper_batch_output.get("template", None),
                            "is_confident": local_mapper_batch_output.get("confident", None),
                        })

                except:
                    for reaction_smiles in reaction_smiles_strings[
                        reaction_smiles_index: reaction_smiles_index + batch_size
                    ]:
                        try:
                            local_mapper_output = local_mapper.get_atom_map(
                                rxns=reaction_smiles,
                                return_dict=True
                            )

                            local_mapper_outputs.append({
                                "mapped_reaction_smiles": local_mapper_output.get("mapped_rxn", None),
                                "mapped_reaction_template_smarts": local_mapper_output.get("template", None),
                                "is_confident": local_mapper_output.get("confident", None),
                            })

                        except Exception as exception_handle:
                            if logger is not None:
                                logger.error(
                                    msg=exception_handle,
                                    exc_info=True
                                )

                            local_mapper_outputs.append({
                                "mapped_reaction_smiles": None,
                                "mapped_reaction_template_smarts": None,
                                "is_confident": None,
                            })

            return local_mapper_outputs

        except Exception as exception_handle:
            if logger is not None:
                logger.error(
                    msg=exception_handle,
                    exc_info=True
                )

            return list()
