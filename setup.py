"""
Create pygrapenlp as a Python package
"""

from __future__ import print_function
import io
import os
import os.path
import sys

from setuptools import setup, find_packages

MIN_PYTHON_VERSION = (3, 5)

PKGNAME = 'pygrapenlp'
GITHUB_URL = 'https://github.com/GrapeNLP/pygrapenlp.git'
DESC = '''
Python package enabling the usage of grape-core from Python; for more information about GrapeNLP please visit
https://github.com/GrapeNLP/grape-core
'''


def pkg_version():
    '''Read the package version from VERSION.txt'''
    basedir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(basedir, 'VERSION.txt'), 'r') as f:
        return f.readline().strip()


def requirements(filename='requirements.txt'):
    '''Read the requirements file'''
    pathname = os.path.join(os.path.dirname(__file__), filename)
    with io.open(pathname, 'r') as f:
        return [line.strip() for line in f if line.strip() and line[0] != '#']


VERSION = pkg_version()
REQUIREMENTS = requirements()

if sys.version_info < MIN_PYTHON_VERSION:
    sys.exit('**** Sorry, {} {} needs at least Python {}'.format(
        PKGNAME, VERSION, '.'.join(map(str, MIN_PYTHON_VERSION))))

setup_args = dict(
    # Metadata
    name=PKGNAME,
    version=VERSION,
    description=DESC.split('\n')[0],
    long_description=DESC,
    license='LGPL v2.1',
    url=GITHUB_URL,
    author='Javier Sastre',
    author_email='javier.sastre@telefonica.net',

    # Locate packages
    packages=find_packages('src'),
    package_dir={'': 'src'},

    # Requirements
    python_requires='>=' + '.'.join(map(str, MIN_PYTHON_VERSION)),
    install_requires=requirements(),

    # Optional requirements
    extras_require={
        'test': ['pytest'],
    },

    entry_points={'console_scripts': [
        'pygrapenlp = pygrapenlp.pygrapenlp:main',
    ]},

    # pytest requirements
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    include_package_data=False,  # otherwise package_data is not used
    package_data={
        PKGNAME: ['_pygrapenlp.so'],
    },
    # unittest requirements
    test_suite='setup.test_suite',

    # More metadata
    keywords=['GrapeNLP', 'grammar engine', 'NLP'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: LGPL v2.1',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)
