""" The ``scripts`` directory ``map_reactions`` script. """

from argparse import ArgumentParser, Namespace
from functools import partial
from logging import Formatter, Logger, StreamHandler, getLogger
from typing import Any, Callable, Collection, Dict, List, Optional

from pandas.core.frame import DataFrame
from pandas.core.reshape.concat import concat
from pandas.io.parsers.readers import read_csv


def get_script_arguments() -> Namespace:
    """
    Get the script arguments.

    :returns: The script arguments.
    """

    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        "-atama",
        "--atom_to_atom_mapping_approach",
        default="indigo",
        type=str,
        choices=[
            "chytorch_rxnmap",
            "indigo",
            "local_mapper",
            "rxnmapper",
        ],
        help="The indicator of the atom-to-atom mapping approach."
    )

    argument_parser.add_argument(
        "-rs",
        "--reaction_smiles",
        default=None,
        type=str,
        help="The SMILES string of the chemical reaction."
    )

    argument_parser.add_argument(
        "-icfp",
        "--input_csv_file_path",
        default=None,
        type=str,
        help="The path of the input .csv file."
    )

    argument_parser.add_argument(
        "-rscn",
        "--reaction_smiles_column_name",
        default=None,
        type=str,
        help="The name of the chemical reaction SMILES column in the input .csv file."
    )

    argument_parser.add_argument(
        "-ocfp",
        "--output_csv_file_path",
        default=None,
        type=str,
        help="The path of the output .csv file."
    )

    argument_parser.add_argument(
        "-nop",
        "--number_of_processes",
        default=1,
        type=int,
        help="The number of processes, if relevant."
    )

    argument_parser.add_argument(
        "-bs",
        "--batch_size",
        default=10,
        type=int,
        help="The batch size, if relevant."
    )

    return argument_parser.parse_args()


def get_script_logger() -> Logger:
    """
    Get the script logger.

    :returns: The script logger.
    """

    logger = getLogger(
        name="script_logger"
    )

    logger.setLevel(
        level="DEBUG"
    )

    formatter = Formatter(
        fmt="[{name:s} @ {asctime:s}] {levelname:s}: \"{message:s}\"",
        style="{"
    )

    stream_handler = StreamHandler()

    stream_handler.setLevel(
        level="DEBUG"
    )

    stream_handler.setFormatter(
        fmt=formatter
    )

    logger.addHandler(
        hdlr=stream_handler
    )

    return logger


def map_reaction(
        reaction_smiles: str,
        atom_to_atom_mapping_function: Callable[[str], Optional[Dict[str, Any]]]
) -> None:
    """
    Map a chemical reaction.

    :parameter reaction_smiles: The SMILES string of the chemical reaction.
    :parameter atom_to_atom_mapping_function: The atom-to-atom-mapping function of the chemical reaction.
    """

    print({
        "reaction_smiles": reaction_smiles,
    })

    print(atom_to_atom_mapping_function(
        reaction_smiles
    ))


def map_reactions(
        input_csv_file_path: str,
        atom_to_atom_mapping_function: Callable[[Collection[str]], Optional[List[Optional[Dict[str, Any]]]]],
        reaction_smiles_column_name: str,
        output_csv_file_path: str
) -> None:
    """
    Map the chemical reactions.

    :parameter input_csv_file_path: The path of the input .csv file.
    :parameter atom_to_atom_mapping_function: The atom-to-atom-mapping function of the chemical reactions.
    :parameter reaction_smiles_column_name: The name of the chemical reaction SMILES column in the input .csv file.
    :parameter output_csv_file_path: The path of the output .csv file.
    """

    input_csv_file_dataframe = read_csv(
        filepath_or_buffer=input_csv_file_path
    )

    concat(
        objs=[
            input_csv_file_dataframe,
            DataFrame(
                data=atom_to_atom_mapping_function(
                    input_csv_file_dataframe[reaction_smiles_column_name].values.tolist()
                )
            ),
        ],
        axis=1
    ).to_csv(
        path_or_buf=output_csv_file_path,
        index=False
    )


if __name__ == "__main__":
    script_arguments = get_script_arguments()

    script_logger = get_script_logger()

    if script_arguments.atom_to_atom_mapping_approach == "chytorch_rxnmap":
        from atom_to_atom_mapping.utility.chytorch_rxnmap import ChytorchRxnMapAtomToAtomMappingUtility

        if script_arguments.reaction_smiles is not None:
            map_reaction(
                reaction_smiles=script_arguments.reaction_smiles,
                atom_to_atom_mapping_function=partial(
                    ChytorchRxnMapAtomToAtomMappingUtility.map_reaction,
                    logger=script_logger
                )
            )

        if (
            script_arguments.input_csv_file_path is not None and
            script_arguments.reaction_smiles_column_name is not None and
            script_arguments.output_csv_file_path is not None
        ):
            map_reactions(
                input_csv_file_path=script_arguments.input_csv_file_path,
                atom_to_atom_mapping_function=partial(
                    ChytorchRxnMapAtomToAtomMappingUtility.map_reactions,
                    logger=script_logger
                ),
                reaction_smiles_column_name=script_arguments.reaction_smiles_column_name,
                output_csv_file_path=script_arguments.output_csv_file_path
            )

    elif script_arguments.atom_to_atom_mapping_approach == "indigo":
        from atom_to_atom_mapping.utility.indigo import IndigoAtomToAtomMappingUtility

        if script_arguments.reaction_smiles is not None:
            map_reaction(
                reaction_smiles=script_arguments.reaction_smiles,
                atom_to_atom_mapping_function=partial(
                    IndigoAtomToAtomMappingUtility.map_reaction,
                    logger=script_logger
                )
            )

        if (
            script_arguments.input_csv_file_path is not None and
            script_arguments.reaction_smiles_column_name is not None and
            script_arguments.output_csv_file_path is not None
        ):
            map_reactions(
                input_csv_file_path=script_arguments.input_csv_file_path,
                atom_to_atom_mapping_function=partial(
                    IndigoAtomToAtomMappingUtility.map_reactions,
                    number_of_processes=script_arguments.number_of_processes,
                    logger=script_logger
                ),
                reaction_smiles_column_name=script_arguments.reaction_smiles_column_name,
                output_csv_file_path=script_arguments.output_csv_file_path
            )

    elif script_arguments.atom_to_atom_mapping_approach == "local_mapper":
        from atom_to_atom_mapping.utility.local_mapper import LocalMapperAtomToAtomMappingUtility

        if script_arguments.reaction_smiles is not None:
            map_reaction(
                reaction_smiles=script_arguments.reaction_smiles,
                atom_to_atom_mapping_function=partial(
                    LocalMapperAtomToAtomMappingUtility.map_reaction,
                    logger=script_logger
                )
            )

        if (
            script_arguments.input_csv_file_path is not None and
            script_arguments.reaction_smiles_column_name is not None and
            script_arguments.output_csv_file_path is not None
        ):
            map_reactions(
                input_csv_file_path=script_arguments.input_csv_file_path,
                atom_to_atom_mapping_function=partial(
                    LocalMapperAtomToAtomMappingUtility.map_reactions,
                    batch_size=script_arguments.batch_size,
                    logger=script_logger
                ),
                reaction_smiles_column_name=script_arguments.reaction_smiles_column_name,
                output_csv_file_path=script_arguments.output_csv_file_path
            )

    elif script_arguments.atom_to_atom_mapping_approach == "rxnmapper":
        from atom_to_atom_mapping.utility.rxnmapper import RXNMapperAtomToAtomMappingUtility

        if script_arguments.reaction_smiles is not None:
            map_reaction(
                reaction_smiles=script_arguments.reaction_smiles,
                atom_to_atom_mapping_function=partial(
                    RXNMapperAtomToAtomMappingUtility.map_reaction,
                    logger=script_logger
                )
            )

        if (
            script_arguments.input_csv_file_path is not None and
            script_arguments.reaction_smiles_column_name is not None and
            script_arguments.output_csv_file_path is not None
        ):
            map_reactions(
                input_csv_file_path=script_arguments.input_csv_file_path,
                atom_to_atom_mapping_function=partial(
                    RXNMapperAtomToAtomMappingUtility.map_reactions,
                    batch_size=script_arguments.batch_size,
                    logger=script_logger
                ),
                reaction_smiles_column_name=script_arguments.reaction_smiles_column_name,
                output_csv_file_path=script_arguments.output_csv_file_path
            )

    else:
        raise ValueError(
            "The atom-to-atom mapping approach '{atom_to_atom_mapping_approach:s}' is not supported.".format(
                atom_to_atom_mapping_approach=script_arguments.atom_to_atom_mapping_approach
            )
        )
