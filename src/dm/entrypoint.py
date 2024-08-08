import argparse

from dm.pick import pick, add_pick_arguments
from dm.label import label, add_label_arguments


def cli():
    parser = argparse.ArgumentParser(description="dm: A collection of tools for data management")
    subparsers = parser.add_subparsers(dest="dm help")

    parser_pick = subparsers.add_parser("pick", help="Pick samples from a jsonl file")
    add_pick_arguments(parser_pick)
    parser_pick.set_defaults(func=pick)

    parser_label = subparsers.add_parser("label", help="Write a label into each line of jsonl file")
    add_label_arguments(parser_label)
    parser_label.set_defaults(func=label)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
