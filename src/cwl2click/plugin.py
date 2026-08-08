# Copyright 2026 Terradue
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

"""Built-in plugin that serializes the resolved CWL document."""

from __future__ import annotations

from cwl_utils.parser import CommandLineTool, Process
from loguru import logger
from pathlib import Path
from pydantic import AnyUrl, BaseModel, ConfigDict, Field
from typing import TYPE_CHECKING
from transpiler_mate.api import PluginExecutionError, transpiler_plugin
from urllib.parse import urlparse

from . import to_click, to_snake_case

if TYPE_CHECKING:
    from transpiler_mate.api import TranspilerContext


class Cwl2ClickOptions(BaseModel):
    """Options accepted by the built-in bundle plugin."""

    model_config = ConfigDict(extra="forbid")

    workflow_id: list[str] = Field(description="ID(s) of the CommandLineTools")

    output: Path = Field(description="Output directory path")


def _add_if_eligible(
    process: Process,
    workflow_id: list[str],
    command_line_tools: list[CommandLineTool],
) -> None:
    logger.debug(f"* Checking '{process.id}'...")
    if not isinstance(process, CommandLineTool):
        logger.warning(
            f"  '{process.id}' is not a CommandLineTool instance, discarding"
        )
        return

    logger.debug(f"  '{process.id}' is a CommandLineTool instance")
    if workflow_id and process.id not in workflow_id:
        logger.warning(f"  '{process.id}' not in the include list, discarding")
        return

    if workflow_id:
        logger.debug(
            f"  '{process.id}' is in the include list {workflow_id}, processing"
        )
    else:
        logger.debug(f"  Include list not defined, processing '{process.id}'")
    command_line_tools.append(process)


def _get_command_line_tools(
    cwl_document: Process | tuple[Process, ...],
    workflow: Path | AnyUrl,
    workflow_id: list[str],
) -> list[CommandLineTool]:
    command_line_tools: list[CommandLineTool] = []
    if isinstance(cwl_document, list) or isinstance(cwl_document, tuple):
        logger.debug(f"Input CWL Document from {workflow} is a $graph:")
        for process in cwl_document:
            _add_if_eligible(process, workflow_id, command_line_tools)
    else:
        _add_if_eligible(cwl_document, workflow_id, command_line_tools)
    return command_line_tools


def _log_empty_selection(
    cwl_document: Process | tuple[Process, ...], workflow_id: list[str]
) -> None:
    if workflow_id:
        available_ids = (
            [process.id for process in cwl_document]
            if isinstance(cwl_document, list) or isinstance(cwl_document, tuple)
            else [cwl_document.id]
        )
        logger.error(
            f"{workflow_id} not found on in input CWL document, "
            f"only {available_ids} available."
        )
    else:
        logger.error("No CommandLineTool(s) found in input CWL document")


def _get_target(workflow: Path | AnyUrl, output: Path) -> Path:
    if isinstance(workflow, AnyUrl):
        logger.debug(f"{workflow} was parsed from a URL, normalizing...")
        file_name = Path(workflow.path).name if workflow.path else "TODO"
    else:
        logger.debug(f"{workflow} was not parsed from a URL")
        file_name = workflow.name

    return output / f"{to_snake_case(Path(file_name).stem)}.py"


def _generate_click_application(
    workflow: Path | AnyUrl, output: Path, command_line_tools: list[CommandLineTool] | tuple[CommandLineTool, ...]
) -> None:
    logger.debug(
        f"Processing CommandLineTools {[clt.id for clt in command_line_tools]}"
    )
    output.mkdir(parents=True, exist_ok=True)
    target = _get_target(workflow, output)
    module_name = target.parent.absolute().name

    try:
        with target.open("w") as stream:
            to_click(
                command_line_tools=command_line_tools,
                module_name=module_name,
                output_stream=stream,
            )

        logger.success(
            f"'{workflow}' successfully converted to Click Python application in "
            f"'{target.absolute()}'."
        )
    except Exception as error:
        raise PluginExecutionError(
            f"An unexpected error occurred while generating {target}"
        ) from error


@transpiler_plugin(
    name="cwl2click",
    description="Boostrap a Python CLI using click from a CWL CommandLineTool(s).",
    options_model=Cwl2ClickOptions,
)
def cwl2click(context: TranspilerContext, options: Cwl2ClickOptions) -> None:
    """Serialize the resolved CWL document to ``options.output``."""
    clts: list[CommandLineTool] = _get_command_line_tools(context.document, context.source, options.workflow_id)
    
    if not clts:
        _log_empty_selection(context.document, options.workflow_id)
    else:
        _generate_click_application(context.source, options.output, clts)
