from setuptools import setup

setup(
    name='xeval',
    version='0.0.1',
    packages=['xeval'],
    url='',
    license='',
    author='chris wilson',
    author_email='',
    description='RESTful server for getting and posting reputation data.',
    entry_points={
        'console_scripts': ['reptorServer = xeval.main:main']
    },
    requires=['falcon>=1.3', 'numpy', 'jsonschema', ]
)
