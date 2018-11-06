from setuptools import setup

setup(
    name='pyning',
    version='0.1a1',
    packages=[ 'tests', 'tests.test_pyning', 'pyning' ],
    package_dir={ '': 'src' },
    url='',
    license='MIT',
    author='Steve Love',
    author_email='steve@arventech.com',
    description='A quick and extensible configuration management system'
)
