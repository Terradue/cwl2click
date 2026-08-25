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

from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

from cwl_utils.parser import CommandLineTool, Process
from loguru import logger
from pydantic import AnyUrl, BaseModel, ConfigDict, Field
from transpiler_mate.api import PluginExecutionError, transpiler_plugin

from . import to_click, to_snake_case

if TYPE_CHECKING:
    from transpiler_mate.api import TranspilerContext


class Cwl2ClickOptions(BaseModel):
    """Options accepted by the built-in bundle plugin."""

    model_config = ConfigDict(extra="forbid")

    clt_id: list[str] = Field(
        default_factory=list, description="ID(s) of the CommandLineTools"
    )

    output: Path = Field(description="Output directory path")


def _get_target(workflow: AnyUrl, output: Path) -> Path:
    file_name = Path(workflow.path).name if workflow.path else "UNDEF" # TODO

    return output / f"{to_snake_case(Path(file_name).stem)}.py"


@transpiler_plugin(
    name="cwl2click",
    description="Boostrap a Python CLI using click from a CWL CommandLineTool(s).",
    options_model=Cwl2ClickOptions,
)
def cwl2click(context: TranspilerContext, options: Cwl2ClickOptions) -> None:
    """Serialize the resolved CWL document to ``options.output``."""

    clt_ids: Iterable[str] = options.clt_id if options.clt_id else context.document.keys()

    command_line_tools: list[CommandLineTool] = []

    for clt_id in clt_ids:
        process: Process | None = context.document.get(clt_id)

        logger.debug(f"* Checking '{clt_id}'...")

        if not process:
            logger.warning(f"  '{clt_id}' does not exist in {context.source} CWL document, discarding.")
            continue

        if not isinstance(process, CommandLineTool):
            logger.warning(
                f"  '{process.id}' is not a CommandLineTool instance, discarding"
            )
            continue

        logger.debug(f"  Processing '{process.id}'")
        command_line_tools.append(process)

    if not command_line_tools:
        raise PluginExecutionError(f"No CommandLineTool(s) found in input {context.source} CWL document")

    logger.debug(
        f"Processing CommandLineTools {[clt.id for clt in command_line_tools]}..."
    )

    try:
        options.output.mkdir(parents=True, exist_ok=True)
        target = _get_target(context.source, options.output)
        module_name = target.parent.absolute().name

        with target.open("w") as stream:
            to_click(
                command_line_tools=command_line_tools,
                module_name=module_name,
                output_stream=stream,
            )

        logger.success(
            f"'{context.source}' successfully converted to Click Python application in "
            f"'{target.absolute()}'."
        )
    except Exception as error:
        raise PluginExecutionError(
            f"An unexpected error occurred while generating CommandLineTool(s) found in input {context.source} CWL document"
        ) from error