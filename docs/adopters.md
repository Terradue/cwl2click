# Adopters recommendations

## On CWL

When submitting CWL document(s) to `cwl2click`, please mind the following constraints:

- `CommandLineTool`s only will be taken in consideration;
- The `click.Command` name is derived from `baseCommand` and `arguments` declarations, accepting the patterns below:

both `baseCommand` and `arguments` are declared 

```yaml
baseCommand: runner
arguments:
- crop-cli
```

```yaml
baseCommand: 
- runner
arguments:
- crop-cli
```

`baseCommand` only is declared:

```
baseCommand:
- runner
- crop-cli
arguments: []
```

In all the cases above, the resulting `click.Command` will result being `crop-cli`
Any other case will force `cwl2click` not able to detect the command name, then an exception will be thrown.

- `click.Option` parameter declaration is derived from `inputs[].inputBinding.prefix`, i.e.

```yaml
  - class: CommandLineTool
    id: crop
    baseCommand: 
    - runner
    arguments:
    - crop-cli
    inputs:
      item:
        type: Directory
        inputBinding:
          prefix: --input-item
...
```

will result to

```python
cli.add_command(
    click.Command(
        name="crop-cli",
        callback=crop_command,
        params=[
            click.Option(
                ["--input-item"],
                "item",
                type=click.Path(path_type=Path, exists=True, readable=True, resolve_path=True, file_okay=False, dir_okay=True),
                multiple=False,
                required=True,
                is_flag=False,
                
            ),
...
```

If `inputs[].inputBinding.prefix` is not found, it will follow up on `--{{inputs[].id}}`

- Users have in charge to implement all the callback functions - `click2cwl` generates the interface only, concrete implementations must be provided by implementors!
