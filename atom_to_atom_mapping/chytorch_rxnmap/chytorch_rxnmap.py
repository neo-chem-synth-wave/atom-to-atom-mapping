""" The ``atom_to_atom_mapping.chytorch_rxnmap`` package ``chytorch_rxnmap`` module. """

from typing import Dict, List, Optional, Sequence, Union

from chython import smiles

from tqdm.auto import tqdm

from atom_to_atom_mapping.base.base import AtomToAtomMappingBase


class ChytorchRxnMapAtomToAtomMapping(AtomToAtomMappingBase):
    """
    The `Chytorch RxnMap <https://github.com/chython/chytorch-rxnmap>`_ chemical reaction compound atom-to-atom mapping
    class.
    """

    def _map_reaction_smiles(
            self,
            reaction_smiles: str,
            **kwargs
    ) -> Dict[str, Optional[Union[float, str]]]:
        """
        Map a chemical reaction SMILES string.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions and methods:
            { `chython.files.daylight.smiles.smiles`, `chython.algorithms.mapping.attention.Attention.reset_mapping` }.

        :returns: The mapped chemical reaction SMILES string and atom-to-atom mapping confidence score.
        """

        try:
            reaction = smiles(
                reaction_smiles,
                ignore=kwargs.get("ignore", True),
                remap=kwargs.get("remap", False),
                ignore_stereo=kwargs.get("ignore_stereo", False),
                ignore_bad_isotopes=kwargs.get("ignore_bad_isotopes", False),
                keep_implicit=kwargs.get("keep_implicit", False),
                ignore_carbon_radicals=kwargs.get("ignore_carbon_radicals", False),
                ignore_aromatic_radicals=kwargs.get("ignore_aromatic_radicals", True)
            )

            kwargs.pop("return_score", None)

            confidence_score = reaction.reset_mapping(
                return_score=True,
                multiplier=kwargs.get("multiplier", 1.75),
                keep_reactants_numbering=kwargs.get("keep_reactants_numbering", False)
            )

            return {
                "mapped_reaction_smiles": format(reaction, "m"),
                "confidence_score": confidence_score,
            }

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

            return {
                "mapped_reaction_smiles": None,
                "confidence_score": None,
            }

    def map_reaction_smiles(
            self,
            reaction_smiles: str,
            **kwargs
    ) -> Dict[str, Optional[Union[float, str]]]:
        """
        Map a chemical reaction SMILES string.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions and methods:
            { `chython.files.daylight.smiles.smiles`, `chython.algorithms.mapping.attention.Attention.reset_mapping` }.

        :returns: The mapped chemical reaction SMILES string and atom-to-atom mapping confidence score.
        """

        if self.logger is not None:
            self.logger.info(
                msg=(
                    "The atom-to-atom mapping of the chemical reaction SMILES string using the Chytorch RxnMap "
                    "approach has been started."
                )
            )

        chytorch_rxnmap_output = self._map_reaction_smiles(
            reaction_smiles=reaction_smiles,
            **kwargs
        )

        if self.logger is not None:
            self.logger.info(
                msg=(
                    "The atom-to-atom mapping of the chemical reaction SMILES string using the Chytorch RxnMap "
                    "approach has been completed."
                )
            )

        return chytorch_rxnmap_output

    def map_reaction_smiles_strings(
            self,
            reaction_smiles_strings: Sequence[str],
            **kwargs
    ) -> List[Dict[str, Optional[Union[float, str]]]]:
        """
        Map the chemical reaction SMILES strings.

        :parameter reaction_smiles_strings: The SMILES strings of the chemical reactions.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying functions and methods:
            { `chython.files.daylight.smiles.smiles`, `chython.algorithms.mapping.attention.Attention.reset_mapping` }.

        :returns: The mapped chemical reaction SMILES strings and atom-to-atom mapping confidence scores.
        """

        if self.logger is not None:
            self.logger.info(
                msg=(
                    "The atom-to-atom mapping of the chemical reaction SMILES strings using the Chytorch RxnMap "
                    "approach has been started."
                )
            )

        chytorch_rxnmap_outputs = list()

        tqdm_description = "Mapping the chemical reaction SMILES strings"

        for reaction_smiles in tqdm(
            iterable=reaction_smiles_strings,
            desc=tqdm_description,
            total=len(reaction_smiles_strings),
            ncols=len(tqdm_description) + 50
        ):
            chytorch_rxnmap_outputs.append(
                self._map_reaction_smiles(
                    reaction_smiles=reaction_smiles,
                    **kwargs
                )
            )

        if self.logger is not None:
            self.logger.info(
                msg=(
                    "The atom-to-atom mapping of the chemical reaction SMILES strings using the Chytorch RxnMap "
                    "approach has been completed."
                )
            )

        return chytorch_rxnmap_outputs
