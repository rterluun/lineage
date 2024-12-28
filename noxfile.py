import nox


@nox.session
def tests(session):
    session.install("coverage==7.6.9")
    session.install("pytest==8.3.4")

    session.run("coverage", "run", "--source", "src", "-m", "pytest", "tests")
    session.run("coverage", "report", "-m")


@nox.session
def lint(session):
    session.install("black==24.10.0")
    session.install("flake8==7.1.1")
    session.install("isort==5.13.2")
    session.install("mypy==1.14.0")
    session.install("yamllint==1.35.1")

    session.run("black", "--check", ".")
    session.run("flake8", "--max-line-length", "120", ".")
    session.run("isort", "--check", ".")
    session.run("mypy", ".")
    session.run("yamllint", "--no-warnings", ".")
