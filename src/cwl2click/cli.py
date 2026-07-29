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

import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import click
from cwl_loader import load_cwl_from_location
from cwl_utils.parser import CommandLineTool, Process
from loguru import logger

from . import to_click, to_snake_case


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
    cwl_document: Process | list[Process],
    workflow: str,
    workflow_id: list[str],
) -> list[CommandLineTool]:
    command_line_tools: list[CommandLineTool] = []
    if isinstance(cwl_document, list):
        logger.debug(f"Input CWL Document from {workflow} is a $graph:")
        for process in cwl_document:
            _add_if_eligible(process, workflow_id, command_line_tools)
    else:
        _add_if_eligible(cwl_document, workflow_id, command_line_tools)
    return command_line_tools


def _log_empty_selection(
    cwl_document: Process | list[Process], workflow_id: list[str]
) -> None:
    if workflow_id:
        available_ids = (
            [process.id for process in cwl_document]
            if isinstance(cwl_document, list)
            else [cwl_document.id]
        )
        logger.error(
            f"{workflow_id} not found on in input CWL document, "
            f"only {available_ids} available."
        )
    else:
        logger.error("No CommandLineTool(s) found in input CWL document")


def _get_target(workflow: str, output: Path) -> Path:
    file_name = Path(workflow).name
    try:
        result = urlparse(workflow)
        if result.scheme in ("http", "https") and result.netloc:
            logger.debug(f"{workflow} was parsed from a URL, normalizing...")
            file_name = Path(result.path).name
        else:
            logger.debug(f"{workflow} was not parsed from a URL")
    except Exception:
        logger.debug(f"{workflow} was not parsed from a URL")

    return output / f"{to_snake_case(Path(file_name).stem)}.py"


def _generate_click_application(
    workflow: str, output: Path, command_line_tools: list[CommandLineTool]
) -> None:
    logger.info(
        "------------------------------------------------------------------------"
    )
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
        logger.info(
            "------------------------------------------------------------------------"
        )
        logger.success("BUILD SUCCESS")
    except Exception as error:
        logger.info(
            "------------------------------------------------------------------------"
        )
        logger.error("BUILD FAILED")
        logger.error(f"An unexpected error occurred while generating {target}: {error}")


@click.command()
@click.argument("workflow", required=True)
@click.option(
    "--workflow-id",
    required=False,
    type=click.STRING,
    multiple=True,
    help="ID(s) of the CommandLineTools",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    required=True,
    default=Path(),
    help="Output directory path",
)
def main(workflow: str, workflow_id: list[str], output: Path):
    start_time = time.time()

    cwl_document: Process | list[Process] = load_cwl_from_location(path=workflow)
    clts = _get_command_line_tools(cwl_document, workflow, workflow_id)

    if not clts:
        _log_empty_selection(cwl_document, workflow_id)
    else:
        _generate_click_application(workflow, output, clts)

    end_time = time.time()

    logger.info(
        "------------------------------------------------------------------------"
    )
    logger.info(f"Total time: {end_time - start_time:.4f} seconds")
    logger.info(
        f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}"
    )
