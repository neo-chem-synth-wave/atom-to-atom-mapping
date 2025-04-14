""" The ``atom_to_atom_mapping.indigo`` package ``indigo`` module. """

from functools import partial
from typing import Dict, List, Optional, Sequence, Union

from indigo.indigo.indigo import Indigo

from pqdm.processes import pqdm

from atom_to_atom_mapping.base.base import AtomToAtomMappingBase


class IndigoAtomToAtomMapping(AtomToAtomMappingBase):
    """ The `Indigo <https://github.com/epam/Indigo>`_ chemical reaction compound atom-to-atom mapping class. """

    def _map_reaction_smiles(
            self,
            reaction_smiles: str,
            timeout_period_in_ms: int = 10000,
            handle_existing_atom_map_numbers: str = "discard",
            ignore_atom_charges: bool = False,
            ignore_atom_isotopes: bool = False,
            ignore_atom_valences: bool = False,
            ignore_atom_radicals: bool = False,
            canonicalize_reaction_smiles: bool = False
    ) -> Dict[str, Optional[Union[int, str]]]:
        """
        Map a chemical reaction SMILES string.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.
        :parameter timeout_period_in_ms: The timeout period in milliseconds.
        :parameter handle_existing_atom_map_numbers: The indicator of how the existing chemical reaction compound atom
            map numbers should be handled. The value choices are: { `alter`, `clear`, `discard`, `keep` }.
        :parameter ignore_atom_charges: The indicator of whether the chemical reaction compound atom charges should be
            ignored.
        :parameter ignore_atom_isotopes: The indicator of whether the chemical reaction compound atom isotopes should be
            ignored.
        :parameter ignore_atom_valences: The indicator of whether the chemical reaction compound atom valences should be
            ignored.
        :parameter ignore_atom_radicals: The indicator of whether the chemical reaction compound atom radicals should be
            ignored.
        :parameter canonicalize_reaction_smiles: The indicator of whether the chemical reaction SMILES string should be
            canonicalized.

        :returns: The mapped chemical reaction SMILES string and atom-to-atom mapping status code.
        """

        try:
            indigo = Indigo()

            indigo.setOption(
                option="aam-timeout",
                value1=timeout_period_in_ms
            )

            reaction = indigo.loadReactionSmarts(
                string=reaction_smiles
            )

            status_code = reaction.automap(
                mode="".join([
                    handle_existing_atom_map_numbers if handle_existing_atom_map_numbers in [
                        "alter",
                        "clear",
                        "discard",
                        "keep",
                    ] else "discard",
                    " ignore_charges" if ignore_atom_charges else "",
                    " ignore_isotopes" if ignore_atom_isotopes else "",
                    " ignore_valence" if ignore_atom_valences else "",
                    " ignore_radicals" if ignore_atom_radicals else "",
                ])
            )

            return {
                "mapped_reaction_smiles": (
                    reaction.canonicalSmiles() if canonicalize_reaction_smiles else reaction.smiles()
                ),
                "status_code": status_code,
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
                "status_code": None,
            }

    def map_reaction_smiles(
            self,
            reaction_smiles: str,
            timeout_period_in_ms: int = 10000,
            handle_existing_atom_map_numbers: str = "discard",
            ignore_atom_charges: bool = False,
            ignore_atom_isotopes: bool = False,
            ignore_atom_valences: bool = False,
            ignore_atom_radicals: bool = False,
            canonicalize_reaction_smiles: bool = False
    ) -> Dict[str, Optional[Union[int, str]]]:
        """
        Map a chemical reaction SMILES string.

        :parameter reaction_smiles: The SMILES string of the chemical reaction.
        :parameter timeout_period_in_ms: The timeout period in milliseconds.
        :parameter handle_existing_atom_map_numbers: The indicator of how the existing chemical reaction compound atom
            map numbers should be handled. The value choices are: { `alter`, `clear`, `discard`, `keep` }.
        :parameter ignore_atom_charges: The indicator of whether the chemical reaction compound atom charges should be
            ignored.
        :parameter ignore_atom_isotopes: The indicator of whether the chemical reaction compound atom isotopes should be
            ignored.
        :parameter ignore_atom_valences: The indicator of whether the chemical reaction compound atom valences should be
            ignored.
        :parameter ignore_atom_radicals: The indicator of whether the chemical reaction compound atom radicals should be
            ignored.
        :parameter canonicalize_reaction_smiles: The indicator of whether the chemical reaction SMILES string should be
            canonicalized.

        :returns: The mapped chemical reaction SMILES string and atom-to-atom mapping status code.
        """

        if self.logger is not None:
            self.logger.info(
                msg=(
                    "The atom-to-atom mapping of the chemical reaction SMILES string using the Indigo approach has "
                    "been started."
                )
            )

        indigo_output = self._map_reaction_smiles(
            reaction_smiles=reaction_smiles,
            timeout_period_in_ms=timeout_period_in_ms,
            handle_existing_atom_map_numbers=handle_existing_atom_map_numbers,
            ignore_atom_charges=ignore_atom_charges,
            ignore_atom_isotopes=ignore_atom_isotopes,
            ignore_atom_valences=ignore_atom_valences,
            ignore_atom_radicals=ignore_atom_radicals,
            canonicalize_reaction_smiles=canonicalize_reaction_smiles
        )

        if self.logger is not None:
            self.logger.info(
                msg=(
                    "The atom-to-atom mapping of the chemical reaction SMILES string using the Indigo approach has "
                    "been completed."
                )
            )

        return indigo_output

    def map_reaction_smiles_strings(
            self,
            reaction_smiles_strings: Sequence[str],
            timeout_period_in_ms: int = 10000,
            handle_existing_atom_map_numbers: str = "discard",
            ignore_atom_charges: bool = False,
            ignore_atom_isotopes: bool = False,
            ignore_atom_valences: bool = False,
            ignore_atom_radicals: bool = False,
            canonicalize_reaction_smiles: bool = False,
            number_of_processes: int = 1
    ) -> List[Dict[str, Optional[Union[int, str]]]]:
        """
        Map the chemical reaction SMILES strings.

        :parameter reaction_smiles_strings: The SMILES strings of the chemical reactions.
        :parameter timeout_period_in_ms: The timeout period in milliseconds.
        :parameter handle_existing_atom_map_numbers: The indicator of how the existing chemical reaction compound atom
            map numbers should be handled. The value choices are: { `alter`, `clear`, `discard`, `keep` }.
        :parameter ignore_atom_charges: The indicator of whether the chemical reaction compound atom charges should be
            ignored.
        :parameter ignore_atom_isotopes: The indicator of whether the chemical reaction compound atom isotopes should be
            ignored.
        :parameter ignore_atom_valences: The indicator of whether the chemical reaction compound atom valences should be
            ignored.
        :parameter ignore_atom_radicals: The indicator of whether the chemical reaction compound atom radicals should be
            ignored.
        :parameter canonicalize_reaction_smiles: The indicator of whether the chemical reaction SMILES string should be
            canonicalized.
        :parameter number_of_processes: The number of processes.

        :returns: The mapped chemical reaction SMILES strings and atom-to-atom mapping status codes.
        """

        if self.logger is not None:
            self.logger.info(
                msg=(
                    "The atom-to-atom mapping of the chemical reaction SMILES strings using the Indigo approach has "
                    "been started."
                )
            )

        pqdm_description = (
            "Mapping the chemical reaction SMILES strings (Number of Processes: {number_of_processes:d})"
        ).format(
            number_of_processes=number_of_processes
        )

        indigo_outputs = pqdm(
            array=reaction_smiles_strings,
            function=partial(
                self._map_reaction_smiles,
                timeout_period_in_ms=timeout_period_in_ms,
                handle_existing_atom_map_numbers=handle_existing_atom_map_numbers,
                ignore_atom_charges=ignore_atom_charges,
                ignore_atom_isotopes=ignore_atom_isotopes,
                ignore_atom_valences=ignore_atom_valences,
                ignore_atom_radicals=ignore_atom_radicals,
                canonicalize_reaction_smiles=canonicalize_reaction_smiles
            ),
            n_jobs=number_of_processes,
            desc=pqdm_description,
            total=len(reaction_smiles_strings),
            ncols=len(pqdm_description) + (50 if number_of_processes == 1 else 75)
        )

        if self.logger is not None:
            self.logger.info(
                msg=(
                    "The atom-to-atom mapping of the chemical reaction SMILES strings using the Indigo approach has "
                    "been completed."
                )
            )

        return indigo_outputs
