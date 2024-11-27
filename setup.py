from pathlib import Path
import sys
import setuptools

sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor" / "pbg"))

setuptools.setup(
    name="speeches_analisys",
    packages=setuptools.find_packages(exclude=['vendor']),
    install_requires=[
        "annotated-types",
        "asyncio",
        "certifi",
        "charset-normalizer",
        "idna",
        "numpy",
        "pandas",
        "pandas-stubs",
        "pydantic",
        "pydantic_core",
        "python-dateutil",
        "pytz",
        "requests",
        "six",
        "types-pytz",
        "types-requests",
        "typing_extensions",
        "tzdata",
        "urllib3",
    ],
    version='0.1.0',
    description="A analysis tool for the brazilian chmaber of deputies speeches",
    author="Matteus Guilherme de Souza",
    author_email="matteusgui@hotmail.com"
)
