from setuptools import setup, find_packages
import discharge

setup(
    name='Discharge',
    version=discharge.version,
    author='Richard Ward',
    author_email='richard@richard.ward.name',
    url='https://github.com/RichardOfWard/discharge',
    description='A static site generator',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    scripts=['scripts/discharge'],
    install_requires=[
        'Jinja2',
        'Markdown',
        'Pygments',
        'Werkzeug',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
