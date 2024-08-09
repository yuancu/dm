import json
from itertools import pairwise


def read_jsonl(input_path):
    """
    读取 JSONL 格式的文件，返回一个列表，每个元素是一个字典。

    Args:
        input_path (str): JSONL 格式的文件路径。

    Returns:
        list[dict]: 包含所有记录的列表，每个记录是一个字典。
    """
    querys = []
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            querys.append(json.loads(line))
    return querys


def write_jsonl(output_path, data, mode="w"):
    """
    将数据写入 JSONL 格式的文件。

    Args:
        output_path (str): 输出文件路径。
        data (list[dict]): 待写入的数据，每个元素是一个字典。
        mode (str, optional): 写入模式，默认为"w"。

    Returns:
        None
    """
    with open(output_path, mode, encoding="utf-8") as file:
        for item in data:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")


def merge_fields(paths, src_keys, merge_fn, result_key='result'):
    """Merge a field from multiple jsonl files"""
    if isinstance(src_keys, str):
        src_keys = [src_keys] * len(paths)
    results = []
    sources = [read_jsonl(path) for path in paths]
    for a, b in pairwise(sources):
        if len(a) != len(b):
            raise ValueError(f"Lengths of jsonl files are not the same ({len(a)} != {len(b)})")
    length = len(sources[0])
    for i in range(length):
        source_fields = [src[i][src_key]
                         for src, src_key in zip(sources, src_keys)]
        merged_field = merge_fn(source_fields)
        merged = sources[0][i]
        merged[result_key] = merged_field
        if src_keys[0] != result_key:
            del merged[src_keys[0]]
        results.append(merged)
    return results


def update_fields(base_path, update_path, keys_to_update):
    """Update fields in a jsonl file with values from another jsonl file"""
    base_jsonls = read_jsonl(base_path)
    update_jsonls = read_jsonl(update_path)
    if len(base_jsonls) != len(update_jsonls):
        raise ValueError(f"Lengths of jsonl files are not the same ({len(base_jsonls) != len(update_jsonls)})")
    for base, update in zip(base_jsonls, update_jsonls):
        for key in keys_to_update:
            base[key] = update[key]
    return base_jsonls

def update_fields_unordered(base_path, update_path, primary_key, keys_to_update):
    """Update fields in a jsonl file with values from another jsonl file"""
    base_jsonls = read_jsonl(base_path)
    update_jsonls = read_jsonl(update_path)
    update_dict = {jsonl[primary_key]: jsonl for jsonl in update_jsonls}
    for base in base_jsonls:
        update = update_dict[base[primary_key]]
        for key in keys_to_update:
            base[key] = update[key]
    return base_jsonls