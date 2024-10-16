"""
This module provides functionality to update JSONL files with data
from another JSONL file based on a specified key.
"""
import logging

from dm.utils.json_util import read_jsonl, update_fields_unordered, write_jsonl

logger = logging.getLogger(__name__)


def update_with_args(args):
    """
    Updates the contents of a JSONL file based on another JSONL file and specified arguments.

    Args:
        args: An argparse.Namespace object containing the following attributes:
            - input (str): Path to the input JSONL file.
            - other (str): Path to the other JSONL file used for updates.
            - key (str): The primary key used to match records between the input and other files.
            - columns (list, optional): Specific columns to update. If not provided, all
                columns will be updated.
            - overwirte (bool, optional): If True, all columns from the other file will overwrite
                the input file's columns.
            - output (str): Path to the output JSONL file where updated records will be written.

    Returns:
        None
    """
    other_lines = read_jsonl(args.other)
    if len(other_lines) == 0:
        logger.error("The other file is empty")
        return
    lines = read_jsonl(args.input)
    if len(lines) == 0:
        logger.warning("The input file is empty")
        return

    if args.columns:
        keys_to_update = args.columns
    elif args.overwrite:
        keys_to_update = other_lines[0].keys()
    else:
        keys_to_update = set(other_lines[0].keys()) - set(lines[0].keys())
    updated_lines = update_fields_unordered(
        base_path=args.input,
        other_path=args.other,
        primary_key=args.key,
        keys_to_update=keys_to_update)
    write_jsonl(args.output, updated_lines)


def add_update_args(parser):
    """
    Adds command-line arguments to the given parser for updating JSONL files.

    Arguments:
        parser (argparse.ArgumentParser): The argument parser to which the arguments will be added.

    The following arguments are added to the parser:
        -i, --input (str, required): The input JSONL file.
        -o, --output (str, optional): The output JSONL file (default: "output.jsonl").
        --other (str, required): The other JSONL file where the new data comes from.
        --key (str, required): The key to join the two JSONL files.
        --overwrite (bool, optional): Whether to overwrite the original data with the new data.
        --mode (str, optional): The join mode (choices: "left", "right", "inner", "outer";
            default: "left"). Note: Not implemented yet.
        --columns (list of str, optional): List of columns to update.
    """
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="The input jsonl file")
    parser.add_argument("-o", "--output", type=str, default="output.jsonl",
                        help="The output jsonl file (default: output.jsonl)")
    parser.add_argument("--other", type=str, required=True,
                        help="The other jsonl file where the new data comes from")
    parser.add_argument("--key", type=str, required=True,
                        help="The key to join the two jsonl files")
    parser.add_argument("--overwrite", action="store_true",
                        help="Whether to overwrite the original data with the new data")
    parser.add_argument("--mode", type=str, choices=["left", "right", "inner", "outer"],
                        default="left", help="The join mode (Not implemented yet)")
    parser.add_argument("--columns", nargs="+", default=None,
                        help="List of columns to update")
