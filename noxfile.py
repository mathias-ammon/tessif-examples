# noxfile.py
"""Configure nox sessions."""

# standard library
import shutil
import tempfile
from pathlib import Path

# third pary packages
import nox

# local packages

# define default sessions:
nox.options.sessions = (
    "pre-commit",
    "lint",
    "pylint",
    "tests",
    "xdoctest",
    "safety",
    "docs_rebuild",
)


def install_with_constraints(session, *args, **kwargs):
    """Install packages constrained by Poetry's lock file."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",  # requ for working with pip resolver
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python="3.10")
def tests(session):
    """Run test suite."""
    args = session.posargs or [
        "--cov",
        "-m",
        "not e2e and not con and not slow",
        # append exlcuded markers as "and not ..."
    ]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-mock",
    )
    session.run("pytest", *args)


# locations to run linting and formatting on:
locations = "src", "tests", "noxfile.py", "docs/conf.py"


@nox.session(python="3.10")
def lint(session):
    """Lint using flake8."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "darglint",
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-isort",
        "flake8-rst-docstrings",
        "pep8-naming",
        "pre-commit",
        "pre-commit-hooks",
        "pyupgrade",
    )
    session.run("flake8", *args)


@nox.session(python="3.10")
def pylint(session):
    """Lint using pylint."""
    args = session.posargs or locations
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "pytest",
        "requests",
        "nox",
        "pylint",
    )
    session.run("pylint", "--output-format=colorized", "--recursive=y", *args)


@nox.session(python="3.10")
def black(session):
    """Reformat code using black."""
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.10")
def xdoctest(session):
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "xdoctest", "pygments")
    session.run("python", "-m", "xdoctest", "tessif_examples", *args)


@nox.session(python="3.10")
def docs(session):
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "sphinx",
        "sphinx-click",
        "furo",
        "sphinx-paramlinks",
        "sphinx-rtd-theme",
        "pytest",
    )
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python="3.10")
def docs_live(session):
    """Build and serve the documentation with live reloading on changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "sphinx",
        "sphinx-autobuild",
        "sphinx-click",
        "furo",
        "sphinx-paramlinks",
        "sphinx-rtd-theme",
        "pytest",
    )

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)


@nox.session(python="3.10")
def docs_rebuild(session):
    """Rebuild the entire sphinx documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "sphinx",
        "sphinx-click",
        "furo",
        "sphinx-paramlinks",
        "sphinx-rtd-theme",
        "pytest",
    )
    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python="3.10")
def coverage(session):
    """Produce coverage report."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")


@nox.session(python="3.10")
def codecov(session):
    """Produce coverage report and try uploading to codecov."""
    install_with_constraints(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(name="pre-commit", python="3.10")
def precommit(session):
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(
        session,
        "darglint",
        "black",
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-isort",
        "flake8-rst-docstrings",
        "pep8-naming",
        "pre-commit",
        "pre-commit-hooks",
        "pyupgrade",
        "pytest",
        "requests",
        "nox",
        "pylint",
    )
    session.run("pre-commit", *args)


@nox.session(python="3.10")
def safety(session):
    """Scan dependencies for insecure packages using safety."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")
