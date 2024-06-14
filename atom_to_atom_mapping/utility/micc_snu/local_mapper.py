""" The ``atom_to_atom_mapping.utility.micc_snu`` package ``local_mapper`` module. """

from logging import Logger
from math import ceil
from typing import Dict, List, Optional, Sequence, Union

from localmapper import localmapper

from tqdm.auto import tqdm

from atom_to_atom_mapping.utility.abstract_base.abstract_base import AbstractBaseAtomToAtomMappingUtility


class LocalMapperAtomToAtomMappingUtility(AbstractBaseAtomToAtomMappingUtility):
    """
    The `LocalMapper <https://github.com/snu-micc/LocalMapper>`_ chemical reaction compound atom-to-atom mapping utility
    class.
    """

    @staticmethod
    def map_reaction_smiles(
            reaction_smiles: str,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> Optional[Dict[str, Union[None, bool, str]]]:
        """
        Map a chemical reaction `SMILES` string.

        :parameter reaction_smiles: The chemical reaction `SMILES` string.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `localmapper.localmapper.__init__` }.

        :returns: The output of the chemical reaction compound atom-to-atom mapping.
        """

        try:
            local_mapper = localmapper(**kwargs)

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
                logger.exception(
                    msg=exception_handle
                )

            return None

    @staticmethod
    def map_reaction_smiles_strings(
            reaction_smiles_strings: Sequence[str],
            batch_size: int = 10,
            torch_device: Optional[str] = None,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> Optional[List[Optional[Dict[str, Union[None, bool, str]]]]]:
        """
        Map the chemical reaction `SMILES` strings.

        :parameter reaction_smiles_strings: The chemical reaction `SMILES` strings.
        :parameter batch_size: The batch size.
        :parameter torch_device: The indicator of the `PyTorch` device. The value `None` indicates that the default
            `PyTorch` device should be utilized.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `localmapper.localmapper.__init__` }.

        :returns: The outputs of the chemical reaction compound atom-to-atom mapping.
        """

        try:
            local_mapper = localmapper(**kwargs)

            local_mapper_outputs = list()

            for reaction_smiles_index in tqdm(
                iterable=range(0, len(reaction_smiles_strings), batch_size),
                desc="Mapping the chemical reaction SMILES strings ({parameters:s})".format(
                    parameters="Batch Size: {batch_size:d}, PyTorch Device: '{torch_device:}'".format(
                        batch_size=batch_size,
                        torch_device=torch_device
                    )
                ),
                total=ceil(len(reaction_smiles_strings) / batch_size),
                ncols=200
            ):
                local_mapper_batch_outputs = local_mapper.get_atom_map(
                    rxns=reaction_smiles_strings[reaction_smiles_index: reaction_smiles_index + batch_size],
                    return_dict=True
                )

                for local_mapper_batch_output in local_mapper_batch_outputs:
                    local_mapper_outputs.append({
                        "mapped_reaction_smiles": local_mapper_batch_output.get("mapped_rxn", None),
                        "mapped_reaction_template_smarts": local_mapper_batch_output.get("template", None),
                        "confidence": local_mapper_batch_output.get("confident", None),
                    })

            return local_mapper_outputs

        except Exception as exception_handle:
            if logger is not None:
                logger.exception(
                    msg=exception_handle
                )

            return None
