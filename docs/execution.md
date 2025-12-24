# Execution

Based on a KISS approach:

```
$ cwl2click --help
Usage: cwl2click [OPTIONS] WORKFLOW

Options:
  --workflow-id TEXT  ID(s) of the CommandLineTools
  --output PATH       Output directory path  [required]
  --help              Show this message and exit.
```

Users can generate `Click` code by executing:

```
cwl2click \
--output /path/to/your-project/src/your-module \
https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl
```

and monitor the execution:

```
2025-12-24 10:55:57.416 | DEBUG    | cwl_loader:load_cwl_from_location:228 - Loading CWL document from https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl...
2025-12-24 10:55:57.664 | DEBUG    | cwl_loader:_load_cwl_from_stream:231 - Reading stream from https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl...
2025-12-24 10:55:57.689 | DEBUG    | cwl_loader:load_cwl_from_stream:203 - CWL data of type <class 'ruamel.yaml.comments.CommentedMap'> successfully loaded from stream
2025-12-24 10:55:57.689 | DEBUG    | cwl_loader:load_cwl_from_yaml:143 - No needs to update the Raw CWL document since it targets already the v1.2
2025-12-24 10:55:57.689 | DEBUG    | cwl_loader:load_cwl_from_yaml:145 - Parsing the raw CWL document to the CWL Utils DOM...
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:load_cwl_from_yaml:158 - Raw CWL document successfully parsed to the CWL Utils DOM!
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:load_cwl_from_yaml:160 - Dereferencing the steps[].run...
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:_on_process:78 - Checking if https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl#crop must be externally imported...
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:_on_process:82 - run_url: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl - uri: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:_on_process:78 - Checking if https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl#norm_diff must be externally imported...
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:_on_process:82 - run_url: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl - uri: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:_on_process:78 - Checking if https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl#otsu must be externally imported...
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:_on_process:82 - run_url: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl - uri: https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:load_cwl_from_yaml:167 - steps[].run successfully dereferenced! Dereferencing the FQNs...
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:load_cwl_from_yaml:171 - CWL document successfully dereferenced! Now verifying steps[].run integrity...
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:load_cwl_from_yaml:175 - All steps[].run link are resolvable! 
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:load_cwl_from_yaml:178 - Sorting Process instances by dependencies....
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:load_cwl_from_yaml:180 - Sorting process is over.
2025-12-24 10:56:04.305 | DEBUG    | cwl_loader:_load_cwl_from_stream:240 - Stream from https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl successfully load!
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:main:89 - Input CWL Document from https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl is a $graph:
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:_add_if_eligible:72 - * Checking 'norm_diff'...
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:_add_if_eligible:74 -   'norm_diff' is a CommandLineTool instance
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:_add_if_eligible:83 -   Include list not defined, processing 'norm_diff'
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:_add_if_eligible:72 - * Checking 'otsu'...
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:_add_if_eligible:74 -   'otsu' is a CommandLineTool instance
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:_add_if_eligible:83 -   Include list not defined, processing 'otsu'
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:_add_if_eligible:72 - * Checking 'crop'...
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:_add_if_eligible:74 -   'crop' is a CommandLineTool instance
2025-12-24 10:56:04.305 | DEBUG    | cwl2click.cli:_add_if_eligible:83 -   Include list not defined, processing 'crop'
2025-12-24 10:56:04.306 | DEBUG    | cwl2click.cli:_add_if_eligible:72 - * Checking 'pattern-12'...
2025-12-24 10:56:04.306 | WARNING  | cwl2click.cli:_add_if_eligible:86 -   'pattern-12' is not a CommandLineTool instance, discarding
2025-12-24 10:56:04.306 | INFO     | cwl2click.cli:main:101 - ------------------------------------------------------------------------
2025-12-24 10:56:04.306 | DEBUG    | cwl2click.cli:main:102 - Processing CommadLineTools ['norm_diff', 'otsu', 'crop']
2025-12-24 10:56:04.306 | DEBUG    | cwl2click.cli:main:110 - https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl was parsed from a URL, normalizing...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting <cwl_utils.parser.cwl_v1_2.CommandInputArraySchema object at 0x7ce30a43bf40> CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting Directory CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting Directory CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting Directory CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting Directory CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting string CWL type to the related Click type...
2025-12-24 10:56:04.309 | DEBUG    | cwl2click:to_click_type:94 - Converting https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI CWL type to the related Click type...
2025-12-24 10:56:04.310 | SUCCESS  | cwl2click.cli:main:128 - 'https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl' successfully converted to Click Python application in '/path/to/your-project/src/your-module/pattern-12.py'.
2025-12-24 10:56:04.310 | INFO     | cwl2click.cli:main:130 - ------------------------------------------------------------------------
2025-12-24 10:56:04.310 | SUCCESS  | cwl2click.cli:main:131 - BUILD SUCCESS
2025-12-24 10:56:04.310 | INFO     | cwl2click.cli:main:139 - ------------------------------------------------------------------------
2025-12-24 10:56:04.310 | INFO     | cwl2click.cli:main:140 - Total time: 6.8937 seconds
2025-12-24 10:56:04.310 | INFO     | cwl2click.cli:main:141 - Finished at: 2025-12-24T10:56:04.310
```

As reported in the `SUCCESS` logging message, the `Click` application is serialized to the `/path/to/your-project/src/your-module/pattern-12.py` file:

```pyton
# File generated by cwl2click v0.30.0
# timestamp: 2025-12-24T10:56:04.309

from norm_diff_impl import execute as norm_diff_command
from otsu_impl import execute as otsu_command
from crop_impl import execute as crop_command

from pathlib import Path

import click

@click.group()
def cli() -> None:
    pass
 
cli.add_command(
    click.Command(
        name="ndi-cli",
        callback=norm_diff_command,
        # CODE OMITTED FOR SIMPLICITY
    )
)
 
cli.add_command(
    click.Command(
        name="otsu-cli",
        callback=otsu_command,
        params=[
            click.Option(
                ["--input-ndi"],
                "raster",
                type=click.Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True),
                multiple=False,
                required=True,
                is_flag=False,
                
            ),
            click.Option(
                ["--item"],
                "item",
                type=click.Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True),
                multiple=False,
                required=True,
                is_flag=False,
                
            ),
            click.Option(
                ["None"],
                "collection",
                type=click.STRING,
                multiple=False,
                required=True,
                is_flag=False,
                
            ),
        ]
    )
)
 
cli.add_command(
    click.Command(
        name="crop-cli",
        callback=crop_command,
        # CODE OMITTED FOR SIMPLICITY
    )
)
```

#### Include list

By default, `cwl2click` will transpile _all_ the `CommandLineTool` found instances inside the CWL, in case users are interested in just one sub-set, can use the `--workflow-id` option:

```
cwl2click \
--output /path/to/your-project/src/your-module \
--workflow-id crop \
--workflow-id otsu \
https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main/cwl-workflow/pattern-12.cwl
```

By executing this example, `ndi-cli` won't be generated.
