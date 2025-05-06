""" The ``scripts`` directory ``map_reaction_smiles_strings`` script. """

from argparse import ArgumentParser, Namespace
from functools import partial
from logging import Formatter, Logger, StreamHandler, getLogger
from typing import Any, Callable, Dict, List, Optional, Sequence

from pandas import DataFrame, concat, read_csv


def get_script_arguments() -> Namespace:
    """
    Get the script arguments.

    :returns: The script arguments.
    """

    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        "-atama",
        "--atom_to_atom_mapping_approach",
        type=str,
        choices=[
            "chytorch_rxnmap",
            "indigo",
            "local_mapper",
            "rxnmapper",
        ],
        required=True,
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
        help="The path to the input .csv file."
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
        help="The path to the output .csv file."
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
        default=32,
        type=int,
        help="The size of the batch, if relevant."
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


def map_reaction_smiles(
        reaction_smiles: str,
        atom_to_atom_mapping_function: Callable[[str], Dict[str, Any]]
) -> None:
    """
    Map a chemical reaction SMILES string.

    :parameter reaction_smiles: The SMILES string of the chemical reaction.
    :parameter atom_to_atom_mapping_function: The atom-to-atom mapping function.
    """

    print(atom_to_atom_mapping_function(reaction_smiles))


def map_reaction_smiles_strings(
        input_csv_file_path: str,
        atom_to_atom_mapping_function: Callable[[Sequence[str]], Optional[List[Dict[str, Any]]]],
        reaction_smiles_column_name: str,
        output_csv_file_path: str
) -> None:
    """
    Map the chemical reaction SMILES strings.

    :parameter input_csv_file_path: The path to the input .csv file.
    :parameter atom_to_atom_mapping_function: The atom-to-atom mapping function.
    :parameter reaction_smiles_column_name: The name of the chemical reaction SMILES column in the input .csv file.
    :parameter output_csv_file_path: The path to the output .csv file.
    """

    input_dataframe = read_csv(
        filepath_or_buffer=input_csv_file_path,
        low_memory=False
    )

    concat(
        objs=[
            input_dataframe,
            DataFrame(
                data=atom_to_atom_mapping_function(
                    input_dataframe[reaction_smiles_column_name].values.tolist()
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
        from atom_to_atom_mapping.chytorch_rxnmap import ChytorchRxnMapAtomToAtomMapping

        chytorch_rxnmap = ChytorchRxnMapAtomToAtomMapping(
            logger=script_logger
        )

        if script_arguments.reaction_smiles is not None:
            map_reaction_smiles(
                reaction_smiles=script_arguments.reaction_smiles,
                atom_to_atom_mapping_function=chytorch_rxnmap.map_reaction_smiles
            )

        if (
            script_arguments.input_csv_file_path is not None and
            script_arguments.reaction_smiles_column_name is not None and
            script_arguments.output_csv_file_path is not None
        ):
            map_reaction_smiles_strings(
                input_csv_file_path=script_arguments.input_csv_file_path,
                atom_to_atom_mapping_function=chytorch_rxnmap.map_reaction_smiles_strings,
                reaction_smiles_column_name=script_arguments.reaction_smiles_column_name,
                output_csv_file_path=script_arguments.output_csv_file_path
            )

    elif script_arguments.atom_to_atom_mapping_approach == "indigo":
        from atom_to_atom_mapping.indigo import IndigoAtomToAtomMapping

        indigo = IndigoAtomToAtomMapping(
            logger=script_logger
        )

        if script_arguments.reaction_smiles is not None:
            map_reaction_smiles(
                reaction_smiles=script_arguments.reaction_smiles,
                atom_to_atom_mapping_function=indigo.map_reaction_smiles
            )

        if (
            script_arguments.input_csv_file_path is not None and
            script_arguments.reaction_smiles_column_name is not None and
            script_arguments.output_csv_file_path is not None
        ):
            map_reaction_smiles_strings(
                input_csv_file_path=script_arguments.input_csv_file_path,
                atom_to_atom_mapping_function=partial(
                    indigo.map_reaction_smiles_strings,
                    number_of_processes=script_arguments.number_of_processes
                ),
                reaction_smiles_column_name=script_arguments.reaction_smiles_column_name,
                output_csv_file_path=script_arguments.output_csv_file_path
            )

    elif script_arguments.atom_to_atom_mapping_approach == "local_mapper":
        from atom_to_atom_mapping.local_mapper import LocalMapperAtomToAtomMapping

        local_mapper = LocalMapperAtomToAtomMapping(
            logger=script_logger
        )

        if script_arguments.reaction_smiles is not None:
            map_reaction_smiles(
                reaction_smiles=script_arguments.reaction_smiles,
                atom_to_atom_mapping_function=local_mapper.map_reaction_smiles
            )

        if (
            script_arguments.input_csv_file_path is not None and
            script_arguments.reaction_smiles_column_name is not None and
            script_arguments.output_csv_file_path is not None
        ):
            map_reaction_smiles_strings(
                input_csv_file_path=script_arguments.input_csv_file_path,
                atom_to_atom_mapping_function=partial(
                    local_mapper.map_reaction_smiles_strings,
                    batch_size=script_arguments.batch_size
                ),
                reaction_smiles_column_name=script_arguments.reaction_smiles_column_name,
                output_csv_file_path=script_arguments.output_csv_file_path
            )

    elif script_arguments.atom_to_atom_mapping_approach == "rxnmapper":
        from atom_to_atom_mapping.rxnmapper import RXNMapperAtomToAtomMapping

        rxnmapper = RXNMapperAtomToAtomMapping(
            logger=script_logger
        )

        if script_arguments.reaction_smiles is not None:
            map_reaction_smiles(
                reaction_smiles=script_arguments.reaction_smiles,
                atom_to_atom_mapping_function=rxnmapper.map_reaction_smiles
            )

        if (
            script_arguments.input_csv_file_path is not None and
            script_arguments.reaction_smiles_column_name is not None and
            script_arguments.output_csv_file_path is not None
        ):
            map_reaction_smiles_strings(
                input_csv_file_path=script_arguments.input_csv_file_path,
                atom_to_atom_mapping_function=partial(
                    rxnmapper.map_reaction_smiles_strings,
                    batch_size=script_arguments.batch_size
                ),
                reaction_smiles_column_name=script_arguments.reaction_smiles_column_name,
                output_csv_file_path=script_arguments.output_csv_file_path
            )

    else:
        script_logger.error(
            msg="The atom-to-atom mapping approach '{atom_to_atom_mapping_approach:s}' is not supported.".format(
                atom_to_atom_mapping_approach=script_arguments.atom_to_atom_mapping_approach
            )
        )
