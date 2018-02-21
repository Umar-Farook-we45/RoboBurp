from distutils.core import setup

install_dependencies = (
    'flextls==0.3',
    'robotframework==3.0.2',
    'six==1.11.0',
    'lxml==4.1.1',
    'selenium==3.9.0',
    'robotframework-selenium2library==1.8.0'
)

setup(
    name='RoboBurp',
    version='0.1',
    packages=[''],
    package_dir={'': 'roboburp'},
    url='www.we45.com',
    license='MIT License',
    author='Abhay Bhargav',
    author_email='Twitter: @abhaybhargav',
    description='Robot Framework Library for BurpSuite Scanner'
)