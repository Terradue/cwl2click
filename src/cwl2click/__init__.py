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
from cwl_utils.parser import (
    CommandLineTool,
    InputArraySchema,
    Process
)
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
    return pattern.sub('_', name).lower()

def is_nullable(
    type_: Any
) -> bool:
    return isinstance(type_, list) and "null" in type_

def is_required(
    type_: Any
) -> bool:
    return not is_nullable(type_)

_CWL_CLICK_MAP_: Mapping[Any, str] = {
    "int": "INT",
    "long": "INT",
    "double": "FLOAT",
    "float": "FLOAT",
    "boolean": "BOOL", 
    "string": "STRING",
    "Directory": "STRING",
    "File": "STRING"
}

def to_click_type(
    type_: Any
) -> str:
    logger.debug(f"Converting {type_} CWL type to the related Click type...")

    key: str
    if isinstance(type_, str):
        key = type_
    elif isinstance(type_, list):
        key = [item_type for item_type in type_ if "null" != item_type][0]
    else:
        key = type_.class_ # type: ignore

        if "enum" == key:
            return f"Choice([{list(map(lambda symbol : symbol.split('/')[-1], type_.symbols))}])"

    return _CWL_CLICK_MAP_.get(key, str(type_))

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

def is_array(
    type_
) -> bool:
    return isinstance(type, list) or hasattr(type_, "class_") and "array" == type_.class_

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
            is_array,
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
        [ is_array ]
    )
)

def to_click(
    cwl_document: Process | List[Process],
    workflow_id: str,
    output_stream: TextIO
):
    logger.info(f"Looking to {workflow_id} in the CWL document source...")

    process: Process | None = search_process(
        process_id=workflow_id,
        process=cwl_document
    )
    
    if not contains_process(
        process_id=workflow_id,
        process=cwl_document
    ):
        raise ValueError(f"Process {workflow_id} does not exist in input CWL document, only {list(map(lambda p: p.id, cwl_document)) if isinstance(cwl_document, list) else [cwl_document.id]} available.")


    logger.info(f"Process {workflow_id} found in the CWL document source, veryfying it is a legit {CommandLineTool} instance...")

    if not isinstance(process, CommandLineTool):
        raise ValueError(f"Process {workflow_id} expected to tbe a {CommandLineTool} instance, found {type(process)}") 

    # can't be None and correctly found it, at that point

    logger.info(f"Process {workflow_id} found in the CWL document source and legit {type(process)}, converting...")

    template = _jinja_environment.get_template(f"process_cli.py")

    output_stream.write(
        template.render(
            version=_get_version(),
            timestamp=datetime.fromtimestamp(time.time()).isoformat(timespec='milliseconds'),
            process=process
        )
    )
