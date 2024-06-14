""" The ``atom_to_atom_mapping.utility.epam`` package ``indigo`` module. """

from functools import partial
from logging import Logger
from typing import Dict, List, Optional, Sequence, Union

from indigo.indigo.indigo import Indigo

from pqdm.processes import pqdm

from atom_to_atom_mapping.utility.abstract_base.abstract_base import AbstractBaseAtomToAtomMappingUtility


class IndigoAtomToAtomMappingUtility(AbstractBaseAtomToAtomMappingUtility):
    """
    The `Indigo <https://github.com/epam/Indigo>`_ chemical reaction compound atom-to-atom mapping utility class.
    """

    @staticmethod
    def map_reaction_smiles(
            reaction_smiles: str,
            timeout_period_in_milliseconds: int = 10000,
            handle_existing_atom_to_atom_mapping: str = "discard",
            ignore_atom_charges: bool = False,
            ignore_atom_isotopes: bool = False,
            ignore_atom_valences: bool = False,
            ignore_atom_radicals: bool = False,
            canonicalize_reaction_smiles: bool = False,
            logger: Optional[Logger] = None
    ) -> Optional[Dict[str, Union[None, bool, str]]]:
        """
        Map a chemical reaction `SMILES` string.

        :parameter reaction_smiles: The chemical reaction `SMILES` string.
        :parameter timeout_period_in_milliseconds: The timeout period in milliseconds.
        :parameter handle_existing_atom_to_atom_mapping: The indicator of how the existing chemical reaction compound
            atom-to-atom mapping should be handled. The value choices are: { `alter`, `clear`, `discard`, `keep` }.
        :parameter ignore_atom_charges: The indicator of whether the chemical reaction compound atom charges should be
            ignored.
        :parameter ignore_atom_isotopes: The indicator of whether the chemical reaction compound atom isotopes should be
            ignored.
        :parameter ignore_atom_valences: The indicator of whether the chemical reaction compound atom valences should be
            ignored.
        :parameter ignore_atom_radicals: The indicator of whether the chemical reaction compound atom radicals should be
            ignored.
        :parameter canonicalize_reaction_smiles: The indicator of whether the chemical reaction `SMILES` string should
            be canonicalized.
        :parameter logger: The logger. The value `None` indicates that the logger should not be utilized.

        :returns: The output of the chemical reaction compound atom-to-atom mapping.
        """

        try:
            epam_indigo = Indigo()

            epam_indigo.setOption(
                option="aam-timeout",
                value1=timeout_period_in_milliseconds
            )

            epam_indigo_reaction = epam_indigo.loadReactionSmarts(
                string=reaction_smiles
            )

            epam_indigo_status_code = epam_indigo_reaction.automap(
                mode="".join([
                    handle_existing_atom_to_atom_mapping
                    if handle_existing_atom_to_atom_mapping in [
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
                    epam_indigo_reaction.canonicalSmiles()
                    if canonicalize_reaction_smiles else epam_indigo_reaction.smiles()
                ),
                "completed_without_errors": True if epam_indigo_status_code == 1 else False,
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
            **kwargs
    ) -> Optional[List[Optional[Dict[str, Union[None, bool, str]]]]]:
        """
        Map the chemical reaction `SMILES` strings.

        :parameter reaction_smiles_strings: The chemical reaction `SMILES` strings.
        :parameter number_of_jobs: The number of jobs.
        :parameter kwargs: The keyword arguments for the adjustment of the following underlying methods: {
            `atom_to_atom_mapping.utility.epam.indigo.IndigoAtomToAtomMappingUtility.map_reaction_smiles` }.

        :returns: The outputs of the chemical reaction compound atom-to-atom mapping.
        """

        return pqdm(
            array=reaction_smiles_strings,
            function=partial(
                IndigoAtomToAtomMappingUtility.map_reaction_smiles,
                **kwargs
            ),
            n_jobs=number_of_jobs,
            desc="Mapping the chemical reaction SMILES strings (Number of Jobs: {number_of_jobs:d})".format(
                number_of_jobs=number_of_jobs
            ),
            total=len(reaction_smiles_strings),
            ncols=200
        )
