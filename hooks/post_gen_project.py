import os
import shutil
import subprocess


def append_file(file_path: str, content: str) -> None:
    with open(file_path, "a") as f:
        f.write(content)


def initialize_project() -> None:
    subprocess.run(["uv", "init", "--{{ cookiecutter.uv_template }}", "."])


def add_dev_dependencies() -> None:
    subprocess.run(["uv", "add", "--dev", "ruff", "mypy"])
    append_file(
        "pyproject.toml",
        '\n[tool.ruff]\nline-length = 120\n\n[tool.ruff.lint]\nselect = ["E", "F", "I", "W"]\n',
    )


def remove_license() -> None:
    os.remove("LICENSE")


def add_pytest() -> None:
    subprocess.run(["uv", "add", "--dev", "pytest"])
    os.mkdir("tests")
    append_file("Makefile", "\n.PHONY: test\ntest:\n\tuv run pytest tests\n")


def add_pytest_step() -> None:
    append_file(
        ".github/workflows/ci.yml",
        "\n      - name: Run pytest\n        run: uv run pytest tests\n",
    )


def remove_github_actions() -> None:
    shutil.rmtree(".github")


def add_mkdocs_material() -> None:
    subprocess.run(["uv", "add", "--dev", "mkdocs-material"])
    subprocess.run(["uv", "run", "mkdocs", "new", "."])
    append_file("mkdocs.yml", "theme:\n  name: material\n")
    append_file("Makefile", "\n.PHONY: docs\ndocs:\n\tuv run mkdocs serve\n")


def add_yaml_config() -> None:
    append_file(".editorconfig", "\n[*.{yml,yaml}]\nindent_size = 2\n")


if __name__ == "__main__":
    initialize_project()
    add_dev_dependencies()

    if not {{cookiecutter.mit_license}}:  # noqa: F821
        remove_license()

    if {{cookiecutter.pytest}}:  # noqa: F821
        add_pytest()

    if {{cookiecutter.github_actions}}:  # noqa: F821
        add_pytest_step()
    else:
        remove_github_actions()

    if {{cookiecutter.mkdocs_material}}:  # noqa: F821
        add_mkdocs_material()

    if {{cookiecutter.github_actions}} or {{cookiecutter.mkdocs_material}}:  # noqa: F821
        add_yaml_config()
