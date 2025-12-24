# Crosswalk

| CWL Type                                                                          | Click Type                                        |
|-----------------------------------------------------------------------------------|---------------------------------------------------|
| `int`                                                                             | `click.INT`                                       |
| `long`                                                                            | `click.INT`                                       |
| `double`                                                                          | `click.FLOAT`                                     |
| `float`                                                                           | `click.FLOAT`                                     |
| `boolean`                                                                         | `click.BOOL`                                      |
| `string`                                                                          | `click.STRING`                                    |
| `Directory`                                                                       | `click.Path(file_okay=False, dir_okay=True)`      |
| `File`                                                                            | `click.Path(file_okay=True, dir_okay=False)`      |
| `https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#DateTime` | `click.DateTime(formats=['%Y-%m- %d T%H:%M:%S'])` |
| `https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#UUID`     | `click.UUID`                                      |

Any other unsupported type is threated like a `click.STRING`.
