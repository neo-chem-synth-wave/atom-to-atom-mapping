""" The ``atom_to_atom_mapping.local_mapper`` package ``local_mapper`` module. """

from logging import Logger
from math import ceil
from typing import Dict, List, Optional, Sequence, Union

from localmapper.localmapper import localmapper

from tqdm.auto import tqdm

from atom_to_atom_mapping.base.base import AtomToAtomMappingBase


class LocalMapperAtomToAtomMapping(AtomToAtomMappingBase):
    """
    The `LocalMapper <https://github.com/snu-micc/LocalMapper>`_ chemical reaction compound atom-to-atom mapping class.
    """

    def __init__(
            self,
            logger: Optional[Logger] = None,
            **kwargs
    ) -> None:
        """
        The `__init__` method of the class.

        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `localmapper.localmapper.localmapper.__init__` }.
        """

        super().__init__(
            logger=logger
        )

        self.local_mapper = localmapper(
            **kwargs
        )

    def map_reaction_smiles(
            self,
            reaction_smiles: str
    ) -> Dict[str, Optional[Union[bool, str]]]:
        """
        Map a chemical reaction SMILES string.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.

        :returns: The mapped chemical reaction, mapped chemical reaction template, and atom-to-atom mapping confidence
            indicator.
        """

        local_mapper_output = dict()

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The atom-to-atom mapping of the chemical reaction SMILES string using the LocalMapper "
                        "approach has been started."
                    )
                )

            local_mapper_output = self.local_mapper.get_atom_map(
                rxns=reaction_smiles,
                return_dict=True
            )

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg=(
                        "The atom-to-atom mapping of the chemical reaction SMILES string '{reaction_smiles:s}' has "
                        "been unsuccessful."
                    ).format(
                        reaction_smiles=reaction_smiles
                    )
                )

                self.logger.debug(
                    msg=exception_handle,
                    exc_info=True
                )

        finally:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The atom-to-atom mapping of the chemical reaction SMILES string using the LocalMapper "
                        "approach has been completed."
                    )
                )

            return {
                "mapped_reaction_smiles": local_mapper_output.get("mapped_rxn", None),
                "mapped_reaction_template_smarts": local_mapper_output.get("template", None),
                "is_confident": local_mapper_output.get("confident", None),
            }

    def map_reaction_smiles_strings(
            self,
            reaction_smiles_strings: Sequence[str],
            batch_size: int = 10
    ) -> List[Dict[str, Optional[Union[bool, str]]]]:
        """
        Map the chemical reaction SMILES strings.

        :parameter reaction_smiles_strings: The SMILES strings of the chemical reactions.
        :parameter batch_size: The size of the batch.

        :returns: The mapped chemical reactions, mapped chemical reaction templates, and atom-to-atom mapping confidence
            indicators.
        """

        local_mapper_outputs = list()

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The atom-to-atom mapping of the chemical reaction SMILES strings using the LocalMapper "
                        "approach has been started."
                    )
                )

            tqdm_description = "Mapping the chemical reaction SMILES strings (Batch Size: {batch_size:d})".format(
                batch_size=batch_size
            )

            for reaction_smiles_index in tqdm(
                iterable=range(0, len(reaction_smiles_strings), batch_size),
                desc=tqdm_description,
                total=ceil(len(reaction_smiles_strings) / batch_size),
                ncols=len(tqdm_description) + 50
            ):
                try:
                    local_mapper_batch_outputs = self.local_mapper.get_atom_map(
                        rxns=reaction_smiles_strings[
                            reaction_smiles_index: min(reaction_smiles_index + batch_size, len(reaction_smiles_strings))
                        ],
                        return_dict=True
                    )

                    for local_mapper_batch_output in local_mapper_batch_outputs:
                        local_mapper_outputs.append({
                            "mapped_reaction_smiles": local_mapper_batch_output.get("mapped_rxn", None),
                            "mapped_reaction_template_smarts": local_mapper_batch_output.get("template", None),
                            "is_confident": local_mapper_batch_output.get("confident", None),
                        })

                except Exception as exception_handle:
                    if self.logger is not None:
                        self.logger.warning(
                            msg=(
                                "The atom-to-atom mapping of the chemical reaction SMILES string batch has been "
                                "unsuccessful. Switching to the atom-to-atom mapping of the individual chemical "
                                "reaction SMILES strings of the batch."
                            )
                        )

                        self.logger.debug(
                            msg=exception_handle,
                            exc_info=True
                        )

                    for reaction_smiles in reaction_smiles_strings[
                        reaction_smiles_index: min(reaction_smiles_index + batch_size, len(reaction_smiles_strings))
                    ]:
                        try:
                            local_mapper_output = self.local_mapper.get_atom_map(
                                rxns=reaction_smiles,
                                return_dict=True
                            )

                            local_mapper_outputs.append({
                                "mapped_reaction_smiles": local_mapper_output.get("mapped_rxn", None),
                                "mapped_reaction_template_smarts": local_mapper_output.get("template", None),
                                "is_confident": local_mapper_output.get("confident", None),
                            })

                        except Exception as exception_handle:
                            if self.logger is not None:
                                self.logger.error(
                                    msg=(
                                        "The atom-to-atom mapping of the chemical reaction SMILES string "
                                        "'{reaction_smiles:s}' has been unsuccessful."
                                    ).format(
                                        reaction_smiles=reaction_smiles
                                    )
                                )

                                self.logger.debug(
                                    msg=exception_handle,
                                    exc_info=True
                                )

                            local_mapper_outputs.append({
                                "mapped_reaction_smiles": None,
                                "mapped_reaction_template_smarts": None,
                                "is_confident": None,
                            })

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The atom-to-atom mapping of the chemical reaction SMILES strings using the LocalMapper "
                        "approach has been completed."
                    )
                )

            return local_mapper_outputs

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg="The atom-to-atom mapping of the chemical reaction SMILES strings has been unsuccessful."
                )

                self.logger.debug(
                    msg=exception_handle,
                    exc_info=True
                )

            return local_mapper_outputs
