"""
Create pygrapenlp as a Python package
"""

from __future__ import print_function
import io
import os
import os.path
import sys

from setuptools import setup, find_packages, Extension

MIN_PYTHON_VERSION = (3, 5)

PKGNAME = 'pygrapenlp'
GITHUB_URL = 'https://github.com/GrapeNLP/pygrapenlp.git'
DESC = '''
Python package enabling the usage of grape-core from Python; for more information about GrapeNLP please visit
https://github.com/GrapeNLP/grape-core
'''

INCLUDES = {
    'linux': [],
    'darwin': []
}

CFLAGS = {
    'linux': [
        '-pedantic',
        '-ansi',
        '-DSIMPLIFIED_OUTPUT',
        '-DUNIX',
        # '-fpermissive',
        '-DSIMPLIFIED_OUTPUT',
        '-DSWIG_STD_MODERN_STL',
        '-DSWIG_EXPORT_ITERATOR_METHODS',
        '-DDISABLE_TEXT_DICO',
        '-DDISABLE_LUA_GRAMMAR',
        '-DDISABLE_LUAW_GRAMMAR',
        '-DDISABLE_LUT_GRAMMAR',
        '-DDISABLE_LUX_GRAMMAR',
        '-DDISABLE_DEPTH_FIRST_PARSER',
        '-DDISABLE_BREADTH_FIRST_PARSER',
        '-DDISABLE_EARLEY_PARSER',
        '-DDISABLE_TO_FPRTN_PARSER',
        '-DDISABLE_TO_FPRTN_TOP_PARSER',
        '-DDISABLE_TO_FPRTN_ZPPS_PARSER',
        '-DDISABLE_TO_FPRTN_PARSER_AND_BREADTH_FIRST_EXPANDER',
        '-DDISABLE_TO_FPRTN_PARSER_AND_BLACKBOARD_SET_EXPANDER',
        '-DDISABLE_STD_SES',
        '-DDISABLE_LRB_TREE_3W_SES',
        '-DDISABLE_LRB_TREE_BS',
        '-DDISABLE_LRB_TREE_3W_BS',
        '-std=gnu++11'
    ],
    'darwin': [
        '-pedantic',
        '-ansi',
        '-DSIMPLIFIED_OUTPUT',
        '-DUNIX',
        # '-fpermissive',
        '-DSIMPLIFIED_OUTPUT',
        '-DSWIG_STD_MODERN_STL',
        '-DSWIG_EXPORT_ITERATOR_METHODS',
        '-DDISABLE_TEXT_DICO',
        '-DDISABLE_LUA_GRAMMAR',
        '-DDISABLE_LUAW_GRAMMAR',
        '-DDISABLE_LUT_GRAMMAR',
        '-DDISABLE_LUX_GRAMMAR',
        '-DDISABLE_DEPTH_FIRST_PARSER',
        '-DDISABLE_BREADTH_FIRST_PARSER',
        '-DDISABLE_EARLEY_PARSER',
        '-DDISABLE_TO_FPRTN_PARSER',
        '-DDISABLE_TO_FPRTN_TOP_PARSER',
        '-DDISABLE_TO_FPRTN_ZPPS_PARSER',
        '-DDISABLE_TO_FPRTN_PARSER_AND_BREADTH_FIRST_EXPANDER',
        '-DDISABLE_TO_FPRTN_PARSER_AND_BLACKBOARD_SET_EXPANDER',
        '-DDISABLE_STD_SES',
        '-DDISABLE_LRB_TREE_3W_SES',
        '-DDISABLE_LRB_TREE_BS',
        '-DDISABLE_LRB_TREE_3W_BS',
        '-std=gnu++11'
    ]
}

LFLAGS = {
    'linux': ['-L/usr/lib'],
    'darwin': ['-L/usr/lib']
}

LIBRARIES = {
    'linux': ['grape'],
    'darwin': ['grape']
}

SHARE_PATHS = {
    'linux': '/usr/share',
    'darwin': '/usr/local/share'
}


platform = sys.platform
if platform.startswith(('linux', 'gnu')):
    platform = 'linux'
elif platform.startswith('freebsd'):
    platform = 'freebsd'

_includes = INCLUDES[platform]
_cflags = CFLAGS[platform]
_lflags = LFLAGS[platform]
_libraries = LIBRARIES[platform]
_share_path = SHARE_PATHS[platform]


def pkg_version():
    """Read the package version from VERSION.txt"""
    basedir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(basedir, 'VERSION.txt'), 'r') as f:
        return f.readline().strip()


def requirements(filename='requirements.txt'):
    """Read the requirements file"""
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
        'test': ['pytest', 'nose', 'coverage'],
    },

    entry_points={'console_scripts': [
        'pygrapenlp = pygrapenlp.pygrapenlp:main',
    ]},

    # pytest requirements
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    # Include Resources
    ext_modules=[Extension('pygrape/_pygrape',
                           sources=[_share_path + '/pygrapePYTHON_wrap.cxx'],
                           include_dirs=_includes,
                           extra_compile_args=_cflags,
                           extra_link_args=_lflags,
                           libraries=_libraries
                           )
                 ],
    py_modules=['pygrape/pygrape'],

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
