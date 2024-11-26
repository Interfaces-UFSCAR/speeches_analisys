from pathlib import Path
import sys
import setuptools

sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor" / "pbg"))

setuptools.setup(
    name="speeches_analisys",
    packages=setuptools.find_packages(),
    install_requires=[
        "annotated-types==0.7.0",
        "asyncio==3.4.3",
        "certifi==2024.7.4",
        "charset-normalizer==3.3.2",
        "idna==3.7",
        "numpy==2.0.1",
        "pandas==2.2.2",
        "pandas-stubs==2.2.2.240807",
        "pydantic==2.8.2",
        "pydantic_core==2.20.1",
        "python-dateutil==2.9.0.post0",
        "pytz==2024.1",
        "requests==2.32.3",
        "six==1.16.0",
        "types-pytz==2024.1.0.20240417",
        "types-requests==2.32.0.20240712",
        "typing_extensions==4.12.2",
        "tzdata==2024.1",
        "urllib3==2.2.2",
    ],
    version='0.1.0',
    description="A analysis tool for the brazilian chmaber of deputies speeches",
    author="Matteus Guilherme de Souza",
    author_email="matteusgui@hotmail.com"
)
