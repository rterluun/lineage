import nox


@nox.session
def tests(session):
    requirements = nox.project.load_toml("pyproject.toml")["tool"]["poetry"][
        "dependencies"
    ]
    del requirements["python"]

    session.install(*requirements)
    session.install("coverage")
    session.install("pytest")

    session.run("coverage", "run", "--source", "src", "-m", "pytest", "tests")
    session.run("coverage", "report", "-m")


@nox.session
def lint(session):
    requirements = nox.project.load_toml("pyproject.toml")["tool"]["poetry"]["group"][
        "dev"
    ]["dependencies"]
    session.install(*requirements)

    session.run("black", "--check", ".")
    session.run("flake8", "--max-line-length", "120", ".")
    session.run("isort", "--profile", "black", "--check", ".")
    session.run("mypy", "--ignore-missing-imports", ".")
    session.run("yamllint", "--no-warnings", ".")
