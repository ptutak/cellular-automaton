from setuptools import setup
import re


def readme():
    with open('README.md') as f:
        return f.read()


def get_version():
    version_pattern = re.compile(r'(?<=\[)\d+\.\d+\.\d+(?=\])')
    with open('CHANGELOG.md') as f:
        return version_pattern.findall(f.read())[-1]


setup(name='cellular_automaton',
      version=get_version(),
      description='The description',
      long_description=readme(),
      url='http://github.com/ptutak/cellular-automaton',
      author='Piotr Tutak',
      author_email='piotr.tutak@email.address.com',
      packages=['cellular_automaton'],
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
