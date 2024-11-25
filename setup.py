import setuptools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor" / "pbg"))

setuptools.setup(
    name="speeches_analysis",
    packages=setuptools.find_packages(include=['src/speeches_scrap',
                                               'src/extract_topics']),
    version='0.1.0',
    description="A analysis tool for the brazilian chmaber of deputies speeches",
    author="Matteus Guilherme de Souza",
    author_email="matteusgui@hotmail.com"
)
