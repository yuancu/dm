import os
import argparse

from dm.utils.json_util import read_jsonl, write_jsonl

from rich.console import Console
from rich.markdown import Markdown


def pick(args):
    lines = read_jsonl(args.input)
    console = Console()

    write_jsonl(args.output, [])
    for line in lines:
        os.system('clear')
        for k, v in line.items():
            k_md = Markdown(f"**{k.upper()}**")
            console.print(k_md)
            if isinstance(v, str):
                v_md = Markdown(v)
            else:
                v_md = v
            console.print(v_md)

        user_input = input("Keep this sample? ([y]/n)")
        while user_input.strip().lower() not in ["y", "n", "yes", "no", ""]:
            user_input = input("Keep this sample? ([y]/n)")
        if user_input.strip().lower() == "n":
            continue

        write_jsonl(args.output, [line], mode="a")


def add_pick_arguments(parser):
    parser.add_argument("-i", "--input", type=str,
                        required=True, help="The input jsonl file")
    parser.add_argument("-o", "--output", type=str, required=False, default="output.jsonl",
                        help="The output jsonl file (default: output.jsonl)")
    parser.add_argument("--start-from", type=int, default=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    add_pick_arguments(parser)
    args = parser.parse_args()
    pick(args)
