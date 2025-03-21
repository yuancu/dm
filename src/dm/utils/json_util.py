"""
This module provides utility functions for working with JSONL files.
Module: json_util.py
Author: Yuanchun Shen
Functions:
- read_jsonl(input_path): Reads a JSONL file and returns a list of dictionaries.
- write_jsonl(output_path, data, mode="w"): Writes data to a JSONL file.
- merge_fields(paths, src_keys, merge_fn, result_key=None): Merges a field from multiple
    JSONL files.
- update_fields(base_path, other_path, keys_to_update): Updates fields in a JSONL file
    with values from another JSONL file.
- update_fields_unordered(base_path, other_path, primary_key, keys_to_update): Updates
    fields in a JSONL file with values from another JSONL file, using a primary key to
    match records.
- excel_to_jsonl(excel_path, output_path): Converts an Excel file to a JSONL file.
"""
import json
from itertools import pairwise
import logging

logger = logging.getLogger(__name__)


def read_jsonl(input_path):
    """
    Read a JSONL file and return a list of dictionaries.

    Args:
        input_path (str): The path to the JSONL file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a JSON object from the file.
    """
    lines = []
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(json.loads(line))
    return lines


def write_jsonl(output_path, data, mode="w"):
    """
    Write a list of JSON objects to a file in JSON Lines format.

    Args:
        output_path (str): The path to the output file.
        data (list): The list of JSON objects to write.
        mode (str, optional): The file mode to open the file in. Defaults to "w".

    Raises:
        FileNotFoundError: If the specified output path does not exist.

    Example:
        write_jsonl("output.jsonl", [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}])
    """
    with open(output_path, mode, encoding="utf-8") as file:
        for item in data:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")


def write_json(obj, output_path):
    """
    Write a Python object to a JSON file.

    Args:
        obj: The Python object to be written to JSON.
        output_path (str): The path to the output JSON file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)


def merge_fields(paths, src_keys, merge_fn, result_key=None):
    """Merge a field from multiple jsonl files

    Args:
        paths (list): a list of input jsonl paths
        src_keys (str | list[str]): 

    Returns:
        list: a list of merged json objects

    Raises:
        ValueError: if the lengths of jsonl files are not the same
    """
    if isinstance(src_keys, str):
        src_keys = [src_keys] * len(paths)
    results = []
    sources = [read_jsonl(path) for path in paths]
    for a, b in pairwise(sources):
        if len(a) != len(b):
            raise ValueError(
                f"Lengths of jsonl files are not the same ({len(a)} != {len(b)})")
    length = len(sources[0])
    for i in range(length):
        source_fields = [src[i][src_key]
                         for src, src_key in zip(sources, src_keys)]
        merged_field = merge_fn(source_fields)
        merged = sources[0][i]

        # It names the result key the same as the src key by default
        if not result_key:
            result_key = src_keys[0]

        merged[result_key] = merged_field
        if src_keys[0] != result_key:
            del merged[src_keys[0]]
        results.append(merged)
    return results


def update_fields(base_path, other_path, keys_to_update):
    """Update fields in a jsonl file with values from another jsonl file

    Args:
        base_path (str): The file path of the base jsonl file.
        other_path (str): The file path of the other jsonl file.
        keys_to_update (list): A list of keys to update in the base jsonl file.

    Raises:
        ValueError: If the lengths of the jsonl files are not the same.

    Returns:
        list: The updated jsonl file as a list of dictionaries.
    """
    base_jsonls = read_jsonl(base_path)
    update_jsonls = read_jsonl(other_path)
    if len(base_jsonls) != len(update_jsonls):
        raise ValueError("Lengths of jsonl files are not the same "
                         f"({len(base_jsonls) != len(update_jsonls)})")
    for base, update in zip(base_jsonls, update_jsonls):
        for key in keys_to_update:
            base[key] = update[key]
    return base_jsonls


def _update_fields_unordered(base_jsonl, other_jsonl, primary_key, keys_to_update):
    """Update fields in a jsonl file with values from another jsonl file

    Args:
        base_path (str): The file path of the base jsonl file.
        other_path (str): The file path of the other jsonl file.
        primary_key (str): The primary key to match records between the two files.
        keys_to_update (list): A list of keys to update in the base jsonl file.

    Returns:
        list: A list of dictionaries representing the updated jsonl records.
    """
    update_dict = {jsonl[primary_key]: jsonl for jsonl in other_jsonl}
    for base in base_jsonl:
        if base[primary_key] not in update_dict:
            logger.warning("Primary key %s not found in other file: %s. Skipping...",
                           primary_key, base[primary_key])
            continue
        update = update_dict[base[primary_key]]
        for key in keys_to_update:
            base[key] = update[key]
    return base_jsonl

def update_fields_unordered(base_path, other_path, primary_key, keys_to_update):
    """Update fields in a jsonl file with values from another jsonl file

    Args:
        base_path (str): The file path of the base jsonl file.
        other_path (str): The file path of the other jsonl file.
        primary_key (str): The primary key to match records between the two files.
        keys_to_update (list): A list of keys to update in the base jsonl file.

    Returns:
        list: A list of dictionaries representing the updated jsonl records.
    """
    base_jsonls = read_jsonl(base_path)
    update_jsonls = read_jsonl(other_path)
    return _update_fields_unordered(base_jsonls, update_jsonls, primary_key, keys_to_update)


def rename(src_path, dst_path, key_map):
    """Rename keys in a jsonl file

    Args:
        src_path (str): The file path of the source jsonl file.
        dst_path (str): The file path of the destination jsonl file.
        key_map (dict): A mapping of source keys to destination keys.

    Returns:
        None
    """
    src_jsonls = read_jsonl(src_path)
    dst_jsonls = []
    for src_json in src_jsonls:
        dst_json = {key_map.get(key, key): value for key,
                    value in src_json.items()}
        dst_jsonls.append(dst_json)
    write_jsonl(dst_path, dst_jsonls)


def multi_field_transform(input_path, model_names, transform_fn, param_key_fn_map, dst_key_fn):
    """
    Transform multiple fields of a jsonl file with a transform_fn.
    The source keys are derived from model_names with param_key_fn_map;
    while the target keys are derived from dst_key_fn(model_name).

    Args:
        input_path: the path of the file containing the source data
        model_names: the names of the models
        transform_fn: the function to transform the source value to the destination value
        param_key_fn_map: the functions that transform the model name to the param key of the line
            its key is the param name of the transform function; its value is the function to
            convert the model names to the corresponding keys in a line of the jsonl.
        dst_key_fn: the function to get the destination key from the model name

    Returns:
        list: the transformed data
    """
    lines = read_jsonl(input_path)
    for line in lines:
        for name in model_names:
            params = {param_name: line[param_key_fn(name)]
                      for param_name, param_key_fn in param_key_fn_map.items()}
            line[dst_key_fn(name)] = transform_fn(**params)
    return lines
