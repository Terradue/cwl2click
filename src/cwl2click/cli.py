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

from . import to_click
from cwl_loader import load_cwl_from_location
from datetime import datetime
from loguru import logger
from pathlib import Path

import click
import time

@click.command()
@click.argument(
    'workflow',
    required=True
)
@click.option(
    '--workflow-id',
    required=True,
    type=click.STRING,
    help="ID of the main Workflow"
)
@click.option(
    '--output',
    type=click.Path(
        path_type=Path
    ),
    required=True,
    help="Output directory path"
)
def main(
    workflow: str,
    workflow_id: str,
    output: Path
):
    start_time = time.time()

    cwl_document = load_cwl_from_location(path=workflow)

    logger.info('------------------------------------------------------------------------')

    output.mkdir(parents=True, exist_ok=True)
    target: Path = Path(output, f"{workflow_id}.py")

    try:
        with target.open('w') as stream:
            to_click(
                cwl_document=cwl_document,
                workflow_id=workflow_id,
                output_stream=stream
            )

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
