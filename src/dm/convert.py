"""
Converts data between different file formats.

This module provides functions to convert data between Excel, JSONL, and CSV file formats.

Functions:
- excel_to_jsonl(excel_path, output_path): Convert an Excel file to a JSONL file.
- jsonl_to_excel(jsonl_path, output_path): Convert a JSONL file to an Excel file.
- excel_to_csv(excel_path, output_path): Convert an Excel file to a CSV file.
- convert(args): Convert data from one format to another based on the specified mode.
- add_convert_arguments(parser): Add command line arguments for the convert function.
"""
import argparse
import json
from datetime import datetime

import markdown
import pandas as pd

from dm.utils.json_util import read_jsonl, write_json, write_jsonl


def _write_dicts_to_file(lines, output_path):
    for line in lines:
        for k, v in line.items():
            if isinstance(v, datetime):
                line[k] = v.strftime("%Y-%m-%d")
    write_jsonl(output_path, lines)


def excel_to_jsonl(excel_path, output_path):
    """
    Convert an Excel file to a JSONL file.

    Args:
        excel_path (str): The path to the Excel file.
        output_path (str): The path to save the JSONL file.

    Returns:
        None
    """
    df = pd.read_excel(excel_path)
    if "-" in df.columns:
        df = df.drop(columns="-")
    lines = df.to_dict(orient="records")
    _write_dicts_to_file(lines, output_path)


def jsonl_to_excel(jsonl_path, output_path):
    """
    Converts a JSONL file to an Excel file.
    Args:
        jsonl_path (str): The path to the JSONL file.
        output_path (str): The path to save the Excel file.
    Returns:
        None
    """
    lines = read_jsonl(jsonl_path)
    df = pd.DataFrame(lines)
    df.to_excel(output_path, engine="xlsxwriter")


def excel_to_csv(excel_path, output_path):
    """
    Convert an Excel file to a CSV file.
    Args:
        excel_path (str): The path to the Excel file.
        output_path (str): The path to save the CSV file.
    Returns:
        None
    """
    df = pd.read_excel(excel_path)
    if "-" in df.columns:
        df = df.drop(columns="-")
    df.to_csv(output_path)


def markdown_to_html(jsonl_path, output_path, columns=None):
    """
    Convert markdown text in a JSONL file to HTML format.

    Args:
        jsonl_path (str): The path to the JSONL file containing markdown text.
        output_path (str): The path to save the converted HTML output.
        columns (list, optional): A list of column names to convert. If None,
            all columns will be converted.
    Returns:
        None
    """
    lines = read_jsonl(jsonl_path)
    for line in lines:
        if columns is None:
            columns = line.keys()
        for col in columns:
            line[col] = markdown.markdown(str(line[col]), extensions=['extra'])
    write_jsonl(output_path, lines)


def csv_to_jsonl(csv_path, output_path):
    """
    Convert a CSV file to JSONL format.

    Args:
        csv_path (str): The path to the CSV file.
        output_path (str): The path to save the JSONL file.

    Returns:
        None
    """
    csv_content = pd.read_csv(csv_path)
    lines = csv_content.to_dict(orient="records")
    _write_dicts_to_file(lines, output_path)


def jsonl_to_csv(jsonl_path, output_path):
    """
    Convert a JSONL file to a CSV file.

    Args:
        jsonl_path (str): The path to the JSONL file.
        output_path (str): The path to save the CSV file.

    Returns:
        None
    """
    lines = read_jsonl(jsonl_path)
    df = pd.DataFrame(lines)
    df.to_csv(output_path)


def jsonl_to_json(jsonl_path, output_path):
    """
    Convert a JSONL file to a JSON file.

    Args:
        jsonl_path (str): The path to the JSONL file.
        output_path (str): The path to save the JSON file.

    Returns:
        None
    """
    lines = read_jsonl(jsonl_path)
    write_json(lines, output_path)


def json_to_jsonl(json_path, output_path):
    """
    Converts a JSON file to a JSONL (JSON Lines) file.

    Args:
        json_path (str): The path to the input JSON file.
        output_path (str): The path to the output JSONL file.

    Raises:
        FileNotFoundError: If the input JSON file does not exist.
        json.JSONDecodeError: If the input file is not a valid JSON.
    """
    with open(json_path, 'r', encoding="utf-8") as f:
        lines = json.load(f)
    write_jsonl(output_path, lines)


def convert(args):
    """
    Convert data from one format to another based on the specified mode.

    Args:
        args (Namespace): The command line arguments.

    Raises:
        ValueError: If the mode is not recognized.

    """
    input_path = args.input_path
    output_path = args.output_path
    if args.mode == "excel2jsonl":
        excel_to_jsonl(input_path, output_path)
    elif args.mode == "excel2csv":
        excel_to_csv(input_path, output_path)
    elif args.mode == "jsonl2excel":
        jsonl_to_excel(input_path, output_path)
    elif args.mode == "jsonl2csv":
        jsonl_to_csv(input_path, output_path)
    elif args.mode == "csv2jsonl":
        csv_to_jsonl(input_path, output_path)
    elif args.mode == "md2html":
        markdown_to_html(input_path, output_path, args.columns)
    elif args.mode == "jsonl2json":
        jsonl_to_json(input_path, output_path)
    elif args.mode == "json2jsonl":
        json_to_jsonl(input_path, output_path)
    else:
        raise ValueError(f"Unrecognised mode {args.mode}")


def add_convert_arguments(parser: argparse.ArgumentParser):
    """
    Add command line arguments for the convert function.

    Args:
        parser (argparse.ArgumentParser): The argument parser object.

    Returns:
        None
    """
    parser.add_argument("mode", type=str, choices=["excel2jsonl", "excel2csv", "jsonl2excel",
                                                   "csv2jsonl", "jsonl2csv", "md2html",
                                                   "jsonl2json", "json2jsonl"])
    parser.add_argument("input_path", nargs="?", type=str)
    parser.add_argument("output_path", nargs="?", type=str)
    parser.add_argument("-i", "--input-path", dest="input_path", type=str)
    parser.add_argument("-o", "--output-path", dest="output_path", type=str)
    parser.add_argument("--columns", nargs="+", default=None,
                        help="List of columns to transform. Only effective to md2html")
