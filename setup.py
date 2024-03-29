from setuptools import setup, find_packages
from d2lbook2 import __version__

requirements = [
    'jupyter',
    'regex',
    'sphinx>=2.2.1',
    'recommonmark',
    'nbformat',
    'nbconvert<=5.6.1',  # there is an issue with the newest 6.0.0a1
    'sphinxcontrib-bibtex<2.0.0',
    'pybtex-apa-style',
    'mu-notedown',
    'mxtheme>=0.3.11',
    'sphinxcontrib-svg2pdfconverter',
    'numpydoc',
    'awscli',
    'gitpython',
    'sphinx_autodoc_typehints',
    'astor',
    'yapf',
    'fasteners',
    'isort'
]

setup(
    name='d2lbook2',
    version=__version__,
    install_requires=requirements,
    python_requires='>=3.8',
    author='StevenJokess, D2L Developers',
    author_email='llgg8679@qq.com',
    description="Create an online book in docswith Jupyter Notebooks and Sphinx",
    license='Apache-2.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={'d2lbook2':['config_default.ini', 'upload_doc_s3.sh', 'upload_github.sh']},
    entry_points={
        'console_scripts': [
            'd2lbook2 = d2lbook2.main:main',
        ]
    },
)
