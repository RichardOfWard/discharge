from setuptools import setup, find_packages
import discharge

setup(
    name='Discharge',
    version=discharge.version,
    author='Richard Ward',
    author_email='richard@richard.ward.name',
    description='A modular static site generator',
    packages=find_packages(exclude=['tests']),
    test_suite='nose.collector',
    setup_requires=['Jinja2'],
    tests_require=['nose'],
)
