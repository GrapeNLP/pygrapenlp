"""
Create pygrapenlp as a Python package

Two environment variables modify build behaviour:
 * GRAPENLP_DEBUG: if 1, a debug version will be compiled (needs GRAPENLP_DIR)
 * GRAPENLP_DIR: if defined, points to the source folder for grapenlp-core
"""

from __future__ import print_function
import io
import os
import os.path
import sys
from distutils.command.clean import clean
from shutil import copyfile

from typing import List

from setuptools import setup, find_packages, Extension
from setuptools.command.build_py import build_py

MIN_PYTHON_VERSION = (3, 6)

PKGNAME = 'pygrapenlp'
GITHUB_URL = 'https://github.com/GrapeNLP/pygrapenlp.git'
DESC = '''
Python package enabling the usage of the grapenlp-core library from Python; for more information about GrapeNLP please
visit https://github.com/GrapeNLP/grapenlp-core
'''


def pkg_version() -> str:
    """Read the package version from VERSION.txt"""
    basedir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(basedir, 'VERSION.txt'), 'r') as f:
        return f.readline().strip()


def requirements(filename: str='requirements.txt') -> List[str]:
    """Read the requirements file"""
    pathname = os.path.join(os.path.dirname(__file__), filename)
    with io.open(pathname, 'r') as f:
        return [line.strip() for line in f if line.strip() and line[0] != '#']


VERSION = pkg_version()
REQUIREMENTS = requirements()

if sys.version_info < MIN_PYTHON_VERSION:
    sys.exit('**** Sorry, {} {} needs at least Python {}'.format(
        PKGNAME, VERSION, '.'.join(map(str, MIN_PYTHON_VERSION))))


# --------------------------------------------------------------------------

GRAPENLP_DEBUG = os.environ.get('GRAPENLP_DEBUG')
GRAPENLP_SRC_DIR = os.environ.get('GRAPENLP_DIR')


print(". DEBUG mode =", GRAPENLP_DEBUG is not None)
print(". SOURCE DIR =", GRAPENLP_SRC_DIR)

# --------------------------------------------------------------------------

def include_dirs(basedir: str) -> List[str]:
    if not basedir:
        return ['/usr/include']
    basedir = os.path.join(basedir, 'src')
    incdir = lambda d: os.path.join(basedir, d, 'include')
    #print(list(os.listdir(basedir)))
    return [subdir for subdir in map(incdir, os.listdir(basedir))
            if os.path.isdir(os.path.join(subdir, 'grapenlp'))]


INCLUDES = {
    'linux': include_dirs(GRAPENLP_SRC_DIR)
}


DISABLE_FLAGS = [
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
    '-DDISABLE_LRB_TREE_3W_BS'
]

LINUX_FLAGS = [
    '-D_pygrapenlp_EXPORTS',
    '-pthread',
    '-DNDEBUG',
    '-fwrapv',
    '-fstack-protector-strong',
    '-Wformat',
    '-Werror=format-security',
    '-Wdate-time',
    '-D_FORTIFY_SOURCE=2',
    '-pedantic',
    '-ansi',
    '-DSIMPLIFIED_OUTPUT',
    '-DUNIX',
    '-fpermissive',
    '-DSWIG_STD_MODERN_STL',
    '-DSWIG_EXPORT_ITERATOR_METHODS',
    '-std=gnu++11'
]

if not GRAPENLP_SRC_DIR:
    LINUX_FLAGS += DISABLE_FLAGS

CFLAGS = {
    'linux': LINUX_FLAGS + (['-O0', '-g', '-DTRACE'] if GRAPENLP_DEBUG else ['-g0'])
}

LIBDIR = ('/usr/lib/grapenlp' if not GRAPENLP_SRC_DIR else
          os.path.join(GRAPENLP_SRC_DIR, 'build', 'debug' if GRAPENLP_DEBUG
                       else 'release', 'lib'))

LFLAGS = {
    'linux': ['-L' + LIBDIR]
}

LIBRARIES = {
    'linux': ['grapenlp']
}

SWIG_SRC = {
    'linux': '/usr/src/grapenlp/python' if not GRAPENLP_SRC_DIR
             else os.path.join(GRAPENLP_SRC_DIR, 'python')
}


# --------------------------------------------------------------------------

platform = sys.platform
print(". Detected platform: " + platform)
if platform.startswith(('linux', 'gnu')):
    platform = 'linux'
elif platform.startswith('freebsd'):
    platform = 'freebsd'

_includes = INCLUDES[platform]
_cflags = CFLAGS[platform]
_lflags = LFLAGS[platform]
_libraries = LIBRARIES[platform]
_swig_src = SWIG_SRC[platform]
_swig_src_pygrapenlp_py = _swig_src + '/pygrapenlp/pygrapenlp.py'
_swig_src_pygrapenlp_cxx = _swig_src + '/pygrapenlp/pygrapenlpPYTHON_wrap.cxx'
_src_pygrapenlp_py = 'src/pygrapenlp/pygrapenlp.py'
_src_pygrapenlp_cxx = 'src/pygrapenlp/pygrapenlpPYTHON_wrap.cxx'


# --------------------------------------------------------------------------

def copy_swig_file(src_file, dst_file):
    if not os.path.exists(src_file):
        sys.exit("ERROR: file " + src_file + " doesn't exist; is libgrapenlp-dev installed?")
    if not os.path.exists(dst_file) or os.path.getmtime(dst_file) < os.path.getmtime(src_file):
        print(". Copying file:", src_file)
        copyfile(src_file, dst_file)


class my_build_py(build_py):

    def run(self):
        """Copies SWIG autogenerated source code files then runs standard build"""
        copy_swig_file(_swig_src_pygrapenlp_py, _src_pygrapenlp_py)
        copy_swig_file(_swig_src_pygrapenlp_cxx, _src_pygrapenlp_cxx)
        build_py.run(self)


class my_clean(clean):

    def run(self):
        """Deletes copied SWIG files and compiled .so then runs standard build"""
        if os.path.exists(_src_pygrapenlp_py):
            os.remove(_src_pygrapenlp_py)
        if os.path.exists(_src_pygrapenlp_cxx):
            os.remove(_src_pygrapenlp_cxx)
        for file in os.listdir('src'):
            if file.endswith('.so'):
                os.remove('src/' + file)
        for file in os.listdir('src/pygrapenlp'):
            if file.endswith('.so'):
                os.remove('src/pygrapenlp/' + file)
        clean.run(self)


setup_args = dict(
    # Metadata
    name=PKGNAME,
    version=VERSION,
    description=DESC.split('\n')[0],
    long_description=DESC,
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

    # pytest requirements
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    cmdclass={'build_py': my_build_py,
              'clean': my_clean},

    entry_points={'console_scripts': [
        'pygrape_extract = pygrapenlp.app.extract:main'
        'pygrape_extract_raw = pygrapenlp.app.extract_raw:main'
    ]},

    # Native library compilation
    ext_modules=[Extension('pygrapenlp._pygrapenlp',
                           sources=[_src_pygrapenlp_cxx],
                           include_dirs=_includes,
                           extra_compile_args=_cflags,
                           extra_link_args=_lflags,
                           libraries=_libraries
                           )
                 ],
    py_modules=['pygrapenlp.pygrapenlp'],

    # More metadata
    keywords=['GrapeNLP', 'grammar engine', 'NLP'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)
