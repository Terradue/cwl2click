# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Release sections were reconstructed from version changes in
`src/cwl2click/__about__.py` because this repository does not currently contain
release tags.

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.8.0] - 2026-08-24

### Fixed

- Multiline doc addressed.
- Generated Click DateTime format omits trailing 'Z'.

## [0.7.0] - 2026-07-29

### Added

- Dependabot configuration for automated dependency update checks.
- Stronger code chekers with Ruff+McCabe & Bandit.
- Taskfile-based quality workflow integration.

### Changed

- Reused remote quality tasks to avoid duplicated local task definitions.
- Excluded generated templates from Ruff checks.
- Aligned package workflow repository configuration.
- Dependencies bump:
  - `cwl-loader` to `0.24.0`.
  - `cwl-utils` to `0.42`.
  - `click` to `8.4.2`.

### Fixed

- Removed an unnecessary formatter character from package initialization.
- Removed unused imports found by linting.
- Declared the missing Hatch test environment.
- Stopped the package workflow from building an unnecessary Docker image.

### Security

- [CWE-94](https://cwe.mitre.org/data/definitions/94.html) Jinja2 [XSS vulnerability]( https://bandit.readthedocs.io/en/1.9.4/plugins/b701_jinja2_autoescape_false.html).

## [0.6.0] - 2026-01-26

### Fixed

- Converted generated Python parameter names to `snake_case` while preserving
  the original Click option flags.
- Handled a null-pointer edge case during command generation.

## [0.5.0] - 2026-01-22

### Changed

- Removed a debug statement from generated command templates.

### Fixed

- Declared each generated `base_command` only once.
- Removed trailing newline characters from generated Click help text.
- Corrected module version handling in package initialization.

## [0.4.0] - 2026-01-22

### Added

- Test coverage for CWL inputs whose Click option prefixes are inferred from
  input IDs.
- License headers across the test suite.

### Fixed

- Used `baseCommand` as the script name in the generated `project.scripts`
  sample.

## [0.3.0] - 2026-01-08

### Added

- Test coverage for input type mapping, arrays, optional inputs, files,
  directories, documentation labels, string formats, no-argument tools, and
  multiple base commands.

### Changed

- Regrouped generated Click commands dynamically according to CWL CLI
  definitions.
- Tidied test utilities.

### Fixed

- Generated no-argument tools as directly invokable Click commands.
- Correctly handled options that are both multiple and required.
- Corrected a typo in the CLI implementation.

## [0.2.0] - 2025-12-24

### Added

- Documentation site scaffold with MkDocs pages for usage, execution,
  crosswalk notes, and adopters.
- GitHub Actions workflow for publishing documentation.
- Fallback Click option names from `inputs[].id` when
  `inputs[].inputBinding.prefix` is not provided.

### Fixed

- Generated output filenames now follow the expected filename pattern.
- Generated filenames now respect snake-case normalization.
- Generated callback imports now include the module name.
- Removed trailing lines from generated Python output.

## [0.1.0] - 2025-12-24

### Added

- Initial CWL `CommandLineTool` to Click CLI conversion implementation.
- CWL input type handling for Click option generation.
- Multiple command and sub-command generation support.
- CI workflow and placeholder tests.

### Changed

- Decoupled the CLI interface layer from the implementation layer.
- Improved command output messages.
- Removed trailing lines from serialized Python output.

### Fixed

- Enum and nullable enum handling.
- Output file generation when CWL documents are loaded from URLs.

## [0.0.1] - 2025-12-18

### Added

- Initial project skeleton for `cwl2click`.
- Python package metadata, CLI entry point, and package version module.
- Apache-2.0 license and notice files.
- README with the initial project purpose and installation instructions.

[Unreleased]: https://github.com/Terradue/cwl2click/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/Terradue/cwl2click/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/Terradue/cwl2click/compare/d1a796c...v0.7.0
[0.6.0]: https://github.com/Terradue/cwl2click/compare/d1a796c...13aedf7
[0.5.0]: https://github.com/Terradue/cwl2click/compare/f176901...d1a796c
[0.4.0]: https://github.com/Terradue/cwl2click/compare/0663ebe...f176901
[0.3.0]: https://github.com/Terradue/cwl2click/compare/a1cfa6c...0663ebe
[0.2.0]: https://github.com/Terradue/cwl2click/compare/5c960db...a1cfa6c
[0.1.0]: https://github.com/Terradue/cwl2click/compare/d4a8b09...5c960db
[0.0.1]: https://github.com/Terradue/cwl2click/commit/d4a8b09
