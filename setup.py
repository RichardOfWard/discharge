from setuptools import setup
import discharge

setup(
    name='Discharge',
    version=discharge.version,
    author='Richard Ward',
    author_email='richard@richard.ward.name',
    description='A modular static site generator',
    packages=['discharge'],
    test_suite='nose.collector',
    setup_requires=[],
    tests_require=['nose'],
)
