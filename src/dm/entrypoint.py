"""
dm: A collection of tools for data management

Usage:
    python entrypoint.py pick [options]
    python entrypoint.py label [options]
    python entrypoint.py convert [options]

Options:
    -h, --help            show this help message and exit

Commands:
    pick                  Pick samples from a jsonl file
    label                 Write a label into each line of jsonl file
    convert               Convert file formats
"""
import argparse

from dm.pick import pick, add_pick_arguments
from dm.label import label, add_label_arguments
from dm.convert import convert, add_convert_arguments
from dm.filter import filter_, add_filter_arguments
from dm.dedupe import dedupe_with_args, add_dedupe_arguments
from dm.rename import rename_with_args, add_rename_args


def cli():
    """
    dm: A collection of tools for data m_____

    Usage:
        dm pick [options] <input_file> <output_file>
        dm label [options] <input_file> <output_file> <label>
        dm convert [options] <input_file> <output_file>

    Options:
        -h, --help     Show this help message and exit.
    """
    parser = argparse.ArgumentParser(description="dm: A collection of tools for data management")
    subparsers = parser.add_subparsers(dest="dm help")

    parser_pick = subparsers.add_parser("pick", help="Pick samples from a jsonl file")
    add_pick_arguments(parser_pick)
    parser_pick.set_defaults(func=pick)

    parser_label = subparsers.add_parser("label", help="Write a label into each line of jsonl file")
    add_label_arguments(parser_label)
    parser_label.set_defaults(func=label)

    parser_convert = subparsers.add_parser("convert", help="Convert file formats")
    add_convert_arguments(parser_convert)
    parser_convert.set_defaults(func=convert)

    parser_filter = subparsers.add_parser("filter", help="Filter lines by conditions")
    add_filter_arguments(parser_filter)
    parser_filter.set_defaults(func=filter_)

    parser_dedupe = subparsers.add_parser("dedupe", help="Deduplicate lines based on a primary key")
    add_dedupe_arguments(parser_dedupe)
    parser_dedupe.set_defaults(func=dedupe_with_args)

    parser_rename = subparsers.add_parser("rename", help="Rename keys in a JSONL file based on"
                                          " a provided mapping")
    add_rename_args(parser_rename)
    parser_rename.set_defaults(func=rename_with_args)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
