import sys
import os
from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = (3, 6)

if CURRENT_PYTHON < MIN_PYTHON:
    sys.stderr.write("""
        ============================
        Unsupported Python Version
        ============================

        Python {}.{} is unsupported. Please use a version newer than Python {}.{}.
    """.format(*CURRENT_PYTHON, *MIN_PYTHON))
    sys.exit(1)

with open('requirements.txt', 'r') as f:
    install_requires = f.readlines()

with open('README.rst') as f:
    README = f.read()

if os.path.isfile('VERSION'):
  with open('VERSION') as f:
    VERSION = f.read()
else:
  VERSION = os.environ.get('TRAVIS_PULL_REQUEST_BRANCH') or os.environ.get('TRAVIS_BRANCH') or 'dev'

setup(name='gym-2048',
      description='OpenAI Gym Environment for 2048',
      long_description=README,
      long_description_content_type='text/x-rst',
      version=VERSION,
      url='https://www.github.com/activatedgeek/gym-2048',
      author='Sanyam Kapoor',
      license='MIT',
      packages=find_packages(),
      install_requires=install_requires,
      extras_require={},
)
