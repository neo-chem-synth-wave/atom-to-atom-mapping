""" The ``scripts`` directory ``map_reaction_smiles_using_chytorch_rxnmap`` script. """

from argparse import ArgumentParser, Namespace
from logging import Formatter, Logger, StreamHandler, getLogger

from pandas import DataFrame, concat, read_csv

from atom_to_atom_mapping.utility.cimm_kfu import ChytorchRxnMapAtomToAtomMappingUtility


def get_script_arguments() -> Namespace:
    """
    Get the script arguments.

    :returns: The script arguments.
    """

    argument_parser = ArgumentParser()

    argument_parser.add_argument(
        "-rs",
        "--reaction_smiles",
        default=None,
        type=str,
        help="The chemical reaction SMILES string."
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
        "-np",
        "--number_of_processes",
        default=1,
        type=int,
        help="The number of processes."
    )

    return argument_parser.parse_args()


def get_script_logger() -> Logger:
    """
    Get the script logger.

    :returns: The script logger.
    """

    logger = getLogger(
        name=__name__
    )

    logger.setLevel(
        level="INFO"
    )

    formatter = Formatter(
        fmt="[{asctime:s}] {levelname:s}: \"{message:s}\"",
        style="{"
    )

    stream_handler = StreamHandler()

    stream_handler.setLevel(
        level="INFO"
    )

    stream_handler.setFormatter(
        fmt=formatter
    )

    logger.addHandler(
        hdlr=stream_handler
    )

    return logger


if __name__ == "__main__":
    script_logger = get_script_logger()

    try:
        script_arguments = get_script_arguments()

        if script_arguments.reaction_smiles is not None:
            print({
                "reaction_smiles": script_arguments.reaction_smiles,
            })

            print(ChytorchRxnMapAtomToAtomMappingUtility.map_reaction_smiles(
                reaction_smiles=script_arguments.reaction_smiles,
                logger=script_logger
            ))

        if (
            script_arguments.input_csv_file_path is not None and
            script_arguments.reaction_smiles_column_name is not None and
            script_arguments.output_csv_file_path is not None
        ):
            input_csv_file_data = read_csv(
                filepath_or_buffer=script_arguments.input_csv_file_path
            )[0:100]

            concat(
                objs=[
                    input_csv_file_data,
                    DataFrame(
                        data=ChytorchRxnMapAtomToAtomMappingUtility.map_reaction_smiles_strings(
                            reaction_smiles_strings=input_csv_file_data[
                                script_arguments.reaction_smiles_column_name
                            ].values.tolist(),
                            number_of_processes=script_arguments.number_of_processes,
                            logger=script_logger
                        )
                    ),
                ],
                axis=1
            ).to_csv(
                path_or_buf=script_arguments.output_csv_file_path,
                index=False
            )

    except Exception as exception_handle:
        script_logger.exception(
            msg=exception_handle
        )
