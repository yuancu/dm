"""
This module provides utility functions for parsing JSON content from Markdown format.

Functions:
- parse_md_json(text): Parses a JSON string wrapped in triple backticks from Markdown format.
- parse_md_json_with_fix(text, backend="openai"): Parse the given Markdown JSON text and fix
  any parsing errors.
- extract_last_json_code_block(text): Extracts the last JSON code block from the given text.
"""
import json
import re


def parse_md_json(text):
    """
    Parses a JSON string wrapped in triple backticks from Markdown format.

    Args:
        text (str): The input string containing the JSON content.
    Returns:
        dict: A dictionary representing the parsed JSON content.
    Raises:
        ValueError: If the input string does not follow the expected wrapping with triple
            backticks and 'json' identifier.
        ValueError: If the JSON content is invalid.
    """
    # Strip the wrapping backticks
    # The stripping assumes that the wrapping is in the format ```json<content>```
    # without any leading/trailing spaces/anomalies
    if text.startswith('```json') and text.endswith('```'):
        # Remove the '```json' prefix and '```' suffix
        json_str = text[7:-3].strip()
    else:
        raise ValueError("Input string does not follow the expected wrapping "
                         "with triple backticks and 'json' identifier")

    # Parse the JSON string into a dictionary
    try:
        json_dict = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON content") from e

    return json_dict


def parse_md_json_with_fix(text, backend="openai"):
    """
    Parse the given Markdown JSON text and fix any parsing errors.

    Args:
        text (str): The Markdown JSON text to parse.
        backend (str, optional): The backend to use for fixing the parsing errors.
            Defaults to "openai".

    Returns:
        list: A list of conclusions parsed from the Markdown JSON text.

    Raises:
        ImportError: If the 'eb' package is not installed.
        ValueError: If the Markdown JSON text cannot be parsed.

    Example:
        >>> text_with_error = '```json{"name": "John", "age\': 30}```'
        >>> parse_md_json_with_fix(text_with_error)
        {'name': 'John', 'age': 30}
    """
    try:
        from eb.single_inference import infer as single_infer
    except ImportError as e:
        raise ImportError("Please install eb package with pip install "
                          "git+https://shenyuanchun@icode.baidu.com/baidu/shenyuanchun/eb.git") \
            from e
    try:
        conclusions = parse_md_json(text)
    except ValueError:
        try:
            print("Parsing error, trying to replace ' with \" and parse again")
            text = text.replace("'", '"')
            conclusions = parse_md_json(text)
            print("Fixed")
        except ValueError:
            try:
                print(f"Parsing error, tring to fix with {backend}")
                text = single_infer("改正下列json字符串。请直接返回改正后的结果。"
                                    f"{text}", backend=backend)
                conclusions = parse_md_json(text)
                print("Fixed")
            except ValueError as e3:
                raise ValueError(f"Can't parse {text}") from e3
    return conclusions


def extract_last_json_code_block(text):
    """
    Extracts the last JSON code block from the given text.

    Args:
        text (str): The text to search for JSON code blocks.

    Returns:
        str: The last JSON code block found, wrapped in triple backticks.

    Example:
        >>> text = '''
        ... Some text before the code block.
        ... ```json
        ... {
        ...     "key": "value"
        ... }
        ... ```
        ... Some text after the code block.
        ... '''
        >>> extract_last_json_code_block(text)
        '```json\n{\n    "key": "value"\n}\n```'
    """

    # Pattern to match code blocks
    pattern = re.compile(r'```json(.*?)```', re.DOTALL)
    matches = pattern.findall(text)

    if matches:
        # Return the last match
        return '```json' + matches[-1] + '```'
    return None
