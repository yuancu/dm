import argparse
from dm.utils.json_util import read_jsonl, write_jsonl


def remove_other_columns(lines, kept_columns):
    """
    Remove rest columns from lines (other than kept_columns)
    """
    output_lines = []
    for line in lines:
        output_line = {}
        for col in kept_columns:
            output_line[col] = line[col]
        output_lines.append(output_line)
    return output_lines

def remove_columns(lines, dropped_columns):
    output_lines = []
    for line in lines:
        output_line = {k: v for k, v in line.items() if k not in dropped_columns}
        output_lines.append(output_line)
    return output_lines

def filter_(args):
    """Filter lines by conditions"""
    lines = read_jsonl(args.input_path)
    columns = args.columns
    mode = args.mode.strip()
    if mode == "keepcols":
        output_lines = remove_other_columns(lines, columns)
    elif mode == "dropcols":
        output_lines = remove_columns(lines, columns)
    else:
        raise ValueError(f"Unknown mode: {args.mode}")
    write_jsonl(args.output_path, output_lines)


def add_filter_arguments(parser: argparse.ArgumentParser):
    """
    Add command line arguments for the convert function.

    Args:
        parser (argparse.ArgumentParser): The argument parser object.

    Returns:
        None
    """
    parser.add_argument("mode", type=str, choices=["keepcols", "dropcols"])
    parser.add_argument("input_path", nargs="?", type=str)
    parser.add_argument("output_path", nargs="?", type=str)
    parser.add_argument("-i", "--input-path", dest="input_path", type=str)
    parser.add_argument("-o", "--output-path", dest="output_path", type=str)
    parser.add_argument("--columns", nargs="+", default=None,
                        help="List of columns to transform. Only effective to keepcols")
