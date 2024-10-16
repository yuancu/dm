"""
This module provides functionality to rename keys in a JSONL file based on a provided mapping.

Functions:
    rename_with_args(args): Renames keys in the input JSONL file according to the provided
        mapping and writes the result to the output file.
    add_rename_args(parser): Adds command-line arguments for the rename operation to the
        provided argument parser.

Usage:
    Use `rename_with_args` to perform the renaming operation with the specified arguments.
    Use `add_rename_args` to add the necessary arguments to an argument parser for
        command-line usage.
"""
from dm.utils.json_util import rename

def rename_with_args(args):
    """
    Renames items based on a mapping provided in the arguments.

    Args:
        args (Namespace): A namespace object containing the following attributes:
            - input (str): The input file or directory to be renamed.
            - output (str): The output file or directory after renaming.
            - mapping (str): A string representing the mapping of old names to new names,
              formatted as "old1:new1,old2:new2,...".

    Returns:
        None
    """
    key_map = dict([x.split(":") for x in args.mapping.split(",")])
    rename(args.input, args.output, key_map)

def add_rename_args(parser):
    """
    Adds command-line arguments for renaming keys in a JSONL file to the given argument parser.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which the arguments will be added.

    Arguments:
        -i, --input (str, required): The input JSONL file.
        -o, --output (str, optional): The output JSONL file. Defaults to 'output.jsonl'.
        --mapping (str, required): The mapping string in the format of
            'src_key1:dst_key1,src_key2:dst_key2'.
    """
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="The input jsonl file")
    parser.add_argument("-o", "--output", type=str, default="output.jsonl",
                        help="The output jsonl file (default: output.jsonl)")
    parser.add_argument("--mapping", type=str, required=True,
                        help="The mapping string in the format of"
                            "'src_key1:dst_key1,src_key2:dst_key2'")
