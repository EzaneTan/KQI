import json
from pathlib import Path
from typing import Type, Union

import yaml
from pydantic import BaseModel, ValidationError


def load_yaml(path: Union[str, Path]) -> dict:
    """
    Load a YAML file and return its contents as a dict.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"YAML config not found: {path}")
    with path.open("r") as f:
        return yaml.safe_load(f)


def load_json(path: Union[str, Path]) -> dict:
    """
    Load a JSON file and return its contents as a dict.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"JSON config not found: {path}")
    with path.open("r") as f:
        return json.load(f)


def load_config(
    path: Union[str, Path],
    schema: Type[BaseModel],
) -> BaseModel:
    """
    Load a config file (YAML or JSON), validate it against a Pydantic schema,
    and return the parsed BaseModel instance.

    :param path: Path to .yaml, .yml, or .json config file
    :param schema: Pydantic BaseModel class for validation
    :returns: instance of schema populated with config values
    :raises ValidationError: if config values don't match schema
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")

    ext = path.suffix.lower()
    if ext in (".yml", ".yaml"):  # YAML
        raw = load_yaml(path)
    elif ext == ".json":  # JSON
        raw = load_json(path)
    else:
        raise ValueError(
            f"Unsupported config format '{ext}'. Use .yaml, .yml, or .json."
        )

    try:
        return schema.parse_obj(raw)
    except ValidationError as e:
        print("Failed to validate config against schema:")
        print(e.json())
        raise
