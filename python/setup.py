from setuptools import setup, find_packages
from pathlib import Path


def parse_requirements(file_path: Path):
    """
    Parse a requirements.txt file, ignoring lines that start with '#' and any text after '#'.

    Args:
        file_path (str | Path): Path to the requirements.txt file.

    Returns:
        (List[str]): List of parsed requirements.
    """

    requirements = []
    for line in Path(file_path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            # ignore inline comments
            requirements.append(line.split('#')[0].strip())

    return requirements


print(find_packages(where='src'))

setup(
    name='pywui',
    description='Use Ultralytics YOLO V8 to take the control of scene objects in unity.',
    version='0.1',
    packages=find_packages(where='src'),
    url='https://github.com/mathis-lambert/Python-Yolo-Wrapper-for-Unity-interactions',
    install_requires=parse_requirements(
        Path(__file__).parent / 'requirements.txt'),
    entry_points={
        'console_scripts': [
            'pywui=scripts.main:main',  # Si votre fichier main.py contient une fonction main()
            'pywui-test=pywui:test'         # Si vous souhaitez également l'ajouter ici
        ]
    },
)
