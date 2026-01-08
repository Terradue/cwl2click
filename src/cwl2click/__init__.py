# Copyright 2025 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cwl_loader.utils import (
    contains_process,
    search_process
)
from cwl_utils.parser import CommandLineTool
from datetime import datetime
from jinja2 import (
    Environment,
    PackageLoader
)
from loguru import logger
from importlib.metadata import (
    version,
    PackageNotFoundError
)
from typing import (
    Any,
    List,
    Mapping,
    TextIO
)

import re
import time

pattern = re.compile(r'(?<!^)(?=[A-Z])')

def to_snake_case(name: str) -> str:
    return pattern.sub('_', name.replace('-', '_')).lower()

def is_array(
    type_
) -> bool:
    return isinstance(type_, list) or hasattr(type_, "items") or (hasattr(type_, "class_") and "array" == type_.class_)

def _get_array_size(
    type_: Any
) -> int:
    if isinstance(type_, list):
        return len(type_)

    if hasattr(type_, "items"):
        return _get_array_size(type_.items)

    return 0

def is_nullable(
    type_: Any
) -> bool:
    return isinstance(type_, list) and "null" in type_ or hasattr(type_, "items") and "null" in getattr(type_, "items")

def is_required(
    type_: Any
) -> bool:
    required: bool = not is_nullable(type_)

    logger.debug(f"Detected type {type_} as required: {required}")

    return required

def is_multiple(
    type_
) -> bool:
    if not is_array(type_):
        return False
    
    array_size: int = _get_array_size(type_)

    if 2 == array_size and is_nullable(type_):
        return False

    return True

def is_flag(
    type_: Any
) -> bool:
    return isinstance(type_, list) and "boolean" in type_ or "boolean" == type_

def get_base_command(
    clt: CommandLineTool
) -> str:
    if clt.baseCommand:
        if isinstance(clt.baseCommand, list):
            if len(clt.baseCommand) > 0:
                return clt.baseCommand[0]
        
        if isinstance(clt.baseCommand, str):
            return clt.baseCommand
    
    raise Exception(f"CommandLineTool '{clt.id}' does not define a 'baseCommand' property, impossible to map it to a `click.Command`")
    

def get_command_name(
    clt: CommandLineTool
) -> str | None:
    if clt.baseCommand:
        if isinstance(clt.baseCommand, list):
            if len(clt.baseCommand) > 1:
                return clt.baseCommand[1]
        
        if clt.arguments:
            if isinstance(clt.arguments, list):
                return clt.arguments[0]
            return str(clt.arguments)

    #     raise Exception(f"Impossible to extract the sub-command from CommandLineTool '{clt.id}':\n- `clt.baseCommand` contains the tool only or is empty;\n-no `clt.arguments` provided.")
    # raise Exception(f"CommandLineTool '{clt.id}' does not define a 'baseCommand' property, impossible to map it to a `click.Command`")
    return None

_STRING_FORMAT_SCHEMA_: str = "https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml"

_CWL_CLICK_MAP_: Mapping[Any, str] = {
    "int": "INT",
    "long": "INT",
    "double": "FLOAT",
    "float": "FLOAT",
    "boolean": "BOOL", 
    "string": "STRING",
    "Directory": "Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True)",
    "File": "Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=True, dir_okay=False)",
    f"{_STRING_FORMAT_SCHEMA_}#DateTime": "DateTime(formats=['%Y-%m-%dT%H:%M:%S'])",
    f"{_STRING_FORMAT_SCHEMA_}#UUID": "UUID"
}

def to_click_type(
    type_: Any
) -> str:
    key = None

    if isinstance(type_, str):
        key = type_
    elif isinstance(type_, list):
        key = [item_type for item_type in type_ if "null" != item_type][0]
    elif hasattr(type_, "items"):
        key = type_.items
    elif hasattr(type_, "class_"):
        key = type_.class_ # type: ignore
    elif hasattr(type_, "symbols"):
        return f"Choice({list(map(lambda symbol : symbol.split('/')[-1], type_.symbols))})"

    if key and not isinstance(key, str) and hasattr(key, "symbols"):
        return f"Choice({list(map(lambda symbol : symbol.split('/')[-1], key.symbols))})"

    mapped_type: str = _CWL_CLICK_MAP_.get(key, "STRING")

    logger.debug(f"Type {type_}, represented by key type {key}, mapped to {mapped_type}")

    return mapped_type

_CWL_PYTHON_MAP_: Mapping[Any, str] = {
    "int": "int",
    "long": "int",
    "double": "float",
    "float": "float",
    "boolean": "bool", 
    "string": "str",
    "Directory": "str",
    "File": "str"
}

def to_python_type(
    type_
) -> str:
    logger.debug(f"Converting {type_} CWL type to the related Python type...")

    key: str
    if isinstance(type_, str):
        key = type_
    elif isinstance(type_, list):
        key = [item_type for item_type in type_ if "null" != item_type][0]
    else:
        key = type_.class_ # type: ignore

        if "enum" == key:
            key = "string"

    return _CWL_PYTHON_MAP_.get(key, str(type_))

def _to_mapping(
    functions: List[Any]
) -> Mapping[str, Any]:
    mapping: Mapping[str, Any] = {}

    for function in functions:
        mapping[function.__name__] = function

    return mapping

def _get_version() -> str:
    try:
        return version("cwl2puml")
    except PackageNotFoundError:
        return 'N/A'

_jinja_environment = Environment(
    loader=PackageLoader(
        package_name='cwl2click'
    )
)
_jinja_environment.filters.update(
    _to_mapping(
        [
            get_base_command,
            get_command_name,
            is_array,
            is_flag,
            is_multiple,
            is_required,
            is_nullable,
            to_click_type,
            to_python_type,
            to_snake_case,
        ]
    )
)
_jinja_environment.tests.update(
    _to_mapping(
        [
            is_array
        ]
    )
)

def to_click(
    command_line_tools: List[CommandLineTool],
    module_name: str,
    output_stream: TextIO
):
    template = _jinja_environment.get_template(f"command_line_tools.py")

    output_stream.write(
        template.render(
            version=_get_version(),
            timestamp=datetime.fromtimestamp(time.time()).isoformat(timespec='milliseconds'),
            module_name=module_name,
            command_line_tools=command_line_tools
        )
    )
