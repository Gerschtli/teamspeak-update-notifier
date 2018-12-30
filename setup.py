from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode()

with open("requirements.txt", "rb") as f:
    requirements = f.read().decode().splitlines()

setup(
    name="teamspeak-update-notifier",
    packages=["notifier"],
    entry_points={"console_scripts": ["teamspeak-update-notifier = notifier.__main__:main"]},
    version="1.3.1",
    description="Sends update notifications to server admins for teamspeak server.",
    long_description=long_descr,
    author="Tobias Happ",
    author_email="tobias.happ@gmx.de",
    url="https://github.com/Gerschtli/teamspeak-update-notifier",
    license="MIT",
    install_requires=requirements,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
