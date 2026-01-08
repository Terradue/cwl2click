import importlib.util
import sys
import tempfile
from pathlib import Path

from click.testing import CliRunner

from cwl2click.cli import main


class CWLClickTestCase:
    """
    Mixin providing helpers to generate and import Click CLIs from CWL files.
    """

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmpdir.name)
        self._imported_modules = []

    def tearDown(self):
        for name in self._imported_modules:
            sys.modules.pop(name, None)
        self._tmpdir.cleanup()

    def generate_cli(self, cwl_path: str | Path):
        runner = CliRunner()

        result = runner.invoke(
            main,
            [str(cwl_path), "--output", str(self.tmp_path)]
        )

        if result.exit_code != 0:
            raise AssertionError(result.output)

        py_files = list(self.tmp_path.glob("*.py"))
        if len(py_files) != 1:
            raise AssertionError(f"Expected 1 generated file, got {py_files}")
        
        self._stub_impl_modules(py_files[0])

        return self._import_cli(py_files[0])

    def _stub_impl_modules(self, py_file: Path):
        """
        Create dummy implementation modules as a proper Python package
        so imports like `from tmp.foo_impl import execute` succeed.
        """
        text = py_file.read_text()

        for line in text.splitlines():
            if "_impl import execute" in line:
                module_path = line.split()[1]      # module.cli_impl
                pkg, mod = module_path.split(".")

                pkg_dir = self.tmp_path / pkg
                pkg_dir.mkdir(exist_ok=True)

                # make it a package
                init_file = pkg_dir / "__init__.py"
                init_file.touch(exist_ok=True)

                impl_file = pkg_dir / f"{mod}.py"
                impl_file.write_text(
                    "def execute(*args, **kwargs):\n"
                    "    pass\n"
                )

    def _import_cli(self, py_file: Path):
        module_name = f"cwl2click_test_{py_file.stem}"

        # make generated package importable
        sys.path.insert(0, str(py_file.parent))

        spec = importlib.util.spec_from_file_location(module_name, py_file)
        module = importlib.util.module_from_spec(spec)

        sys.modules[module_name] = module
        self._imported_modules.append(module_name)

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e 

        if not hasattr(module, "basecommand"):
            raise AssertionError("Generated module does not expose `basecommand`")

        return module.basecommand
