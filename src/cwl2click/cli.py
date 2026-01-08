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

from . import (
    to_click,
    to_snake_case
)
from cwl_loader import load_cwl_from_location
from cwl_utils.parser import (
    Process,
    CommandLineTool
)
from datetime import datetime
from loguru import logger
from pathlib import Path
from os.path import (
    basename,
    splitext
)
from typing import List
from urllib.parse import urlparse

import click
import time

@click.command()
@click.argument(
    'workflow',
    required=True
)
@click.option(
    '--workflow-id',
    required=False,
    type=click.STRING,
    multiple=True,
    help="ID(s) of the CommandLineTools"
)
@click.option(
    '--output',
    type=click.Path(
        path_type=Path
    ),
    required=True,
    default=Path("."),
    help="Output directory path"
)
def main(
    workflow: str,
    workflow_id: List[str],
    output: Path
):
    start_time = time.time()

    click.STRING

    cwl_document: Process | List[Process] = load_cwl_from_location(path=workflow)

    clts: List[CommandLineTool] = []

    def _add_if_eligible(process: Process):
        logger.debug(f"* Checking '{process.id}'...")
        if isinstance(process, CommandLineTool):
            logger.debug(f"  '{process.id}' is a CommandLineTool instance")
            if workflow_id:
                logger.debug(f"  Checking if '{process.id}' is in the include list {workflow_id}...")
                if process.id in workflow_id:
                    logger.debug(f"  '{process.id}' is in the include list {workflow_id}, processing")
                    clts.append(process)
                else:
                    logger.warning(f"  '{process.id}' not in the include list, discarding")
            else:
                logger.debug(f"  Include list not defined, processing '{process.id}'")
                clts.append(process)
        else:
            logger.warning(f"  '{process.id}' is not a CommandLineTool instance, discarding")

    if isinstance(cwl_document, list):
        logger.debug(f"Input CWL Document from {workflow} is a $graph:")
        for process in cwl_document:
            _add_if_eligible(process)
    else:
        _add_if_eligible(cwl_document)

    if not clts:
        if workflow_id:
            logger.error(f"{workflow_id} not found on in input CWL document, only {list(map(lambda p: p.id, cwl_document)) if isinstance(cwl_document, list) else [cwl_document.id]} available.")
        else:
            logger.error("No CommandLineTool(s) found in input CWL document")
    else:
        logger.info('------------------------------------------------------------------------')
        logger.debug(f"Processing CommandLineTools {[clt.id for clt in clts]}")

        output.mkdir(parents=True, exist_ok=True)

        file_name = basename(workflow)
        try:
            result = urlparse(workflow)
            if result.scheme in ('http', 'https') and result.netloc:
                logger.debug(f"{workflow} was parsed from a URL, normalizing...")
                file_name = basename(result.path)
            else:
                logger.debug(f"{workflow} was not parsed from a URL")
        except Exception:
            logger.debug(f"{workflow} was not parsed from a URL")

        file_name, _ = splitext(file_name)

        target: Path = Path(output, f"{to_snake_case(file_name)}.py")
        module_name = basename(target.parent.absolute().as_posix())

        try:
            with target.open('w') as stream:
                to_click(
                    command_line_tools=clts,
                    module_name=module_name,
                    output_stream=stream
                )

            logger.success(f"'{workflow}' successfully converted to Click Python application in '{target.absolute()}'.")

            logger.info('------------------------------------------------------------------------')
            logger.success('BUILD SUCCESS')
        except Exception as e:
            logger.info('------------------------------------------------------------------------')
            logger.error('BUILD FAILED')
            logger.error(f"An unexpected error occurred while generating {target}: {e}")

    end_time = time.time()

    logger.info('------------------------------------------------------------------------')
    logger.info(f"Total time: {end_time - start_time:.4f} seconds")
    logger.info(f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}")
