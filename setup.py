import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.0'
PACKAGE_NAME = 'insiderTrades'
AUTHOR = 'Joe Hancuch'
AUTHOR_EMAIL = 'joseph.hancuch1@gmail.com'
URL = 'https://github.com/jhancuch/insiderTrades'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Download insider trading transactions and insider holdings from a public NoSQL SEC database (<https://www.sec.gov/Archives/edgar/full-index/>) using keyword criteria and generate a relational dataframe.'

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'requests'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
