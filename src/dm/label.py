"""
Write a simple label into each line of a jsonl file
"""
import os

from dm.utils.json_util import read_jsonl, write_jsonl

from rich.console import Console
from rich.markdown import Markdown


def label(args):
    lines = read_jsonl(args.input)
    console = Console()

    write_jsonl(args.output, [])
    for line in lines:
        os.system('clear')
        for k, v in line.items():
            k_md = Markdown(f"**{k.upper()}**")
            v_md = Markdown(v)
            console.print(k_md)
            console.print(v_md)

        user_input = input("\nLabel: ")
        line[args.label] = user_input
        write_jsonl(args.output, [line], mode="a")


def add_label_arguments(parser):
    parser.add_argument("-i", "--input", type=str,
                        required=True, help="The input jsonl file")
    parser.add_argument("-o", "--output", type=str, required=False, default="output.jsonl",
                        help="The output jsonl file (default: output.jsonl)")
    parser.add_argument("--start-from", type=int, default=0)
    parser.add_argument("--label", type=str, default="label", help="The result key to add to each line")
