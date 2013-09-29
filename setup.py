from setuptools import setup, find_packages
import discharge

setup(
    name='Discharge',
    version=discharge.version,
    author='Richard Ward',
    author_email='richard@richard.ward.name',
    description='A modular static site generator',
    packages=find_packages(exclude=['tests']),
    scripts=['scripts/discharge'],
    install_requires=[
        'Jinja2',
        'jinja2-highlight',
        'Markdown',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
