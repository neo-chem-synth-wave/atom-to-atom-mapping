""" The ``atom_to_atom_mapping.rxnmapper`` package ``rxnmapper`` module. """

from logging import Logger
from math import ceil
from typing import Dict, List, Optional, Sequence, Union

from rxnmapper import RXNMapper

from tqdm.auto import tqdm

from atom_to_atom_mapping.base.base import AtomToAtomMappingBase


class RXNMapperAtomToAtomMapping(AtomToAtomMappingBase):
    """
    The `RXNMapper <https://github.com/rxn4chemistry/rxnmapper>`_ chemical reaction compound atom-to-atom mapping class.
    """

    def __init__(
            self,
            logger: Optional[Logger] = None
    ) -> None:
        """
        The `__init__` method of the class.

        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.
        """

        super().__init__(
            logger=logger
        )

        self.rxnmapper = RXNMapper()

    def map_reaction_smiles(
            self,
            reaction_smiles: str,
            **kwargs
    ) -> Dict[str, Optional[Union[float, str]]]:
        """
        Map a chemical reaction SMILES string.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `rxnmapper.core.RXNMapper.get_attention_guided_atom_maps` }.

        :returns: The mapped chemical reaction SMILES string and atom-to-atom mapping confidence score.
        """

        rxnmapper_output = dict()

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The atom-to-atom mapping of the chemical reaction SMILES string using the RXNMapper approach "
                        "has been started."
                    )
                )

            rxnmapper_output = self.rxnmapper.get_attention_guided_atom_maps(
                rxns=[reaction_smiles, ],
                **kwargs
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
                        "The atom-to-atom mapping of the chemical reaction SMILES string using the RXNMapper approach "
                        "has been completed."
                    )
                )

            return {
                "mapped_reaction_smiles": rxnmapper_output[0].get("mapped_rxn", None),
                "confidence_score": rxnmapper_output[0].get("confidence", None),
            }

    def map_reaction_smiles_strings(
            self,
            reaction_smiles_strings: Sequence[str],
            batch_size: int = 10,
            **kwargs
    ) -> List[Dict[str, Optional[Union[float, str]]]]:
        """
        Map the chemical reaction SMILES strings.

        :parameter reaction_smiles_strings: The SMILES strings of the chemical reactions.
        :parameter batch_size: The size of the batch.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods:
            { `rxnmapper.core.RXNMapper.get_attention_guided_atom_maps` }.

        :returns: The mapped chemical reaction SMILES strings and atom-to-atom mapping confidence scores.
        """

        rxnmapper_outputs = list()

        try:
            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The atom-to-atom mapping of the chemical reaction SMILES strings using the RXNMapper approach "
                        "has been started."
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
                    rxnmapper_batch_outputs = self.rxnmapper.get_attention_guided_atom_maps(
                        rxns=list(reaction_smiles_strings[
                            reaction_smiles_index: min(reaction_smiles_index + batch_size, len(reaction_smiles_strings))
                        ]),
                        **kwargs
                    )

                    for rxnmapper_batch_output in rxnmapper_batch_outputs:
                        rxnmapper_outputs.append({
                            "mapped_reaction_smiles": rxnmapper_batch_output.get("mapped_rxn", None),
                            "confidence_score": rxnmapper_batch_output.get("confidence", None),
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
                            rxnmapper_output = self.rxnmapper.get_attention_guided_atom_maps(
                                rxns=[reaction_smiles, ],
                                **kwargs
                            )

                            rxnmapper_outputs.append({
                                "mapped_reaction_smiles": rxnmapper_output[0].get("mapped_rxn", None),
                                "confidence_score": rxnmapper_output[0].get("confidence", None),
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

                            rxnmapper_outputs.append({
                                "mapped_reaction_smiles": None,
                                "confidence_score": None,
                            })

            if self.logger is not None:
                self.logger.info(
                    msg=(
                        "The atom-to-atom mapping of the chemical reaction SMILES strings using the RXNMapper approach "
                        "has been completed."
                    )
                )

            return rxnmapper_outputs

        except Exception as exception_handle:
            if self.logger is not None:
                self.logger.error(
                    msg="The atom-to-atom mapping of the chemical reaction SMILES strings has been unsuccessful."
                )

                self.logger.debug(
                    msg=exception_handle,
                    exc_info=True
                )

            return rxnmapper_outputs
