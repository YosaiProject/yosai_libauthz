import os
import sys
import shutil
import subprocess

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None

from setuptools import setup, find_packages
from distutils.command.build_py import build_py
from distutils.command.build_ext import build_ext
from setuptools.dist import Distribution


# Build with clang if not otherwise specified.
if os.environ.get('LIBAUTHZ_MANYLINUX') == '1':
    os.environ.setdefault('CC', 'gcc')
    os.environ.setdefault('CXX', 'g++')
else:
    os.environ.setdefault('CC', 'clang')
    os.environ.setdefault('CXX', 'clang++')


PACKAGE = 'libauthz'
EXT_EXT = sys.platform == 'darwin' and '.dylib' or '.so'


def build_libauthz(base_path):
    lib_path = os.path.join(base_path, '_libauthz.so')
    here = os.path.abspath(os.path.dirname(__file__))
    cmdline = ['cargo', 'build', '--release']
    if not sys.stdout.isatty():
        cmdline.append('--color=always')
    rv = subprocess.Popen(cmdline, cwd=here).wait()
    if rv != 0:
        sys.exit(rv)
    src_path = os.path.join(here, 'target', 'release',
                            'liblibauthz' + EXT_EXT)
    if os.path.isfile(src_path):
        shutil.copy2(src_path, lib_path)


class CustomBuildPy(build_py):
    def run(self):
        build_py.run(self)
        build_libauthz(os.path.join(self.build_lib, *PACKAGE.split('.')))


class CustomBuildExt(build_ext):
    def run(self):
        build_ext.run(self)
        if self.inplace:
            build_py = self.get_finalized_command('build_py')
            build_libauthz(build_py.get_package_dir(PACKAGE))


class BinaryDistribution(Distribution):
    """This is necessary because otherwise the wheel does not know that
    we have non pure information.
    """
    def has_ext_modules(foo):
        return True


cmdclass = {
    'build_ext': CustomBuildExt,
    'build_py': CustomBuildPy,
}


setup(
    name='libauthz',
    version='0.1.0',
    url='http://github.com/YosaiProject/yosai_libauthz',
    description='Rust extensions for Yosai',
    license='Apache License 2.0',
    author='Darin Gordon',
    author_email='dkcdkg@gmail.com',
    packages=find_packages(),
    cffi_modules=['build.py:ffi'],
    cmdclass=cmdclass,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'cffi>=1.6.0',
    ],
    setup_requires=[
        'cffi>=1.6.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    ext_modules=[],
    distclass=BinaryDistribution
)
