import nox

python_version = "3.9"
locations = "src", "tests", "noxfile.py"

max_line_length = 75


@nox.session(python=python_version)
def format(session):
    args = session.posargs or locations
    session.install("black", "isort", "docformatter", "reindent")
    session.run("isort", "--atomic", "--recursive", *args)
    session.run(
        "docformatter",
        "--wrap-summaries",
        f"{max_line_length}",
        "--wrap-descriptions",
        f"{max_line_length}",
        "--in-place",
        "--recursive",
        *args,
    )
    session.run("python", "-m", "reindent", "-r", "-n", *args)
    session.run("black", "--line-length", f"{max_line_length}", *args)


@nox.session(python=python_version)
def flake8(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-import-order", "flake8-annotations")
    session.run("flake8", *args)


@nox.session(python=python_version)
def mypy(session):
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox.session(python=python_version)
def pylama(session):
    args = session.posargs or locations
    session.install("pylama")
    session.run("pylama", *args)
