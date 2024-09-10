import os
from setuptools import setup, find_packages

def get_version():
    version = {}
    version_file_path = os.path.join(os.path.dirname(__file__), 'sdk', '__version__.py')
    with open(version_file_path) as fp:
        exec(fp.read(), version)
    return version['__version__']

def get_readme():
    readme_file_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_file_path, 'r', encoding='utf-8') as f:
        return f.read()
    
def get_requirements():
    requirements_file_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(requirements_file_path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

setup(
    name = 'nalamkisdk',
    version = get_version(),
    author = 'Jan Christian Redlich, Jannes Magnusson, Peter Kloke',
    author_email = 'jan.redlich@bonnconsulting.group, jannes.magnusson@hhi.fraunhofer.de, peter.kloke@hhi.fraunhofer.de',
    description = 'SDK for NaLamKI Services',
    long_description = get_readme(),
    long_description_content_type = 'text/markdown',
    packages = find_packages(),
    python_requires = '>=3.8',
    include_package_data = True,
    install_requires = get_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)