from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

with open("requirements.txt", "rb") as f:
    requirements = f.read().decode("utf-8").splitlines()

setup(
    name="teamspeak-update-notifier",
    packages=["notifier"],
    entry_points={
        "console_scripts":
        ["teamspeak-update-notifier = notifier.notifier:main"]
    },
    version="1.3.1",
    description=("Sends update notifications to server admins for teamspeak "
                 "server."),
    long_description=long_descr,
    author="Tobias Happ",
    author_email="tobias.happ@gmx.de",
    url="https://github.com/Gerschtli/teamspeak-update-notifier",
    license="MIT",
    install_requires=requirements,
    test_suite="tests",
)
