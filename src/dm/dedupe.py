"""
Deduplicate lines based on a primary key.
"""
from dm.utils.json_util import read_jsonl, write_jsonl


def dedupe(input_path, primary_key, output_path):
    """
    Deduplicate the input jsonl file based on the primary key.
    Args:
        input_path (str): The input jsonl file.
        primary_key (str): The primary key to deduplicate.
        output_path (str): The output jsonl file.
    Returns:
        None
    """
    lines = read_jsonl(input_path)
    lines = {line[primary_key]: line for line in lines}.values()
    write_jsonl(output_path, lines)


def dedupe_with_args(args):
    """
    Deduplicate the input jsonl file based on the primary key.
    Args:
        args (Namespace): The command-line arguments.
    Returns:
        None
    """
    dedupe(args.input, args.primary_key, args.output)


def add_dedupe_arguments(parser):
    """
    Arguments for dedupe command.
    """
    parser.add_argument("-i", "--input", type=str, help="The input jsonl file.")
    parser.add_argument("--primary-key", type=str, help="The primary key to deduplicate.")
    parser.add_argument("-o", "--output", type=str, help="The output jsonl file.")
    return parser
