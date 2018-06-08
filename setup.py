from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gitlist',
    version='0.0.1',
    description='Command line tool for listing git repositories on your machine.',
    long_description=readme,
    author='Lev Zakharov',
    author_email='l.j.zakharov@gmail.com',
    url='https://github.com/lzakharov/gitlist',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': ['gitlist=gitlist.cli:main']
    }
)
