import setuptools

setuptools.setup(
    name="speeches_analysis",
    packages=setuptools.find_packages(include=['src/speeches_scrap',
                                               'src/extract_topics']),
    version='0.1.0',
    description="A analysis tool for the brazilian chmaber of deputies speeches",
    author="Matteus Guilherme de Souza",
    author_email="matteusgui@hotmail.com"
)
