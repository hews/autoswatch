from setuptools import setup

VERSION = '0.1.0'

install_requires = [
    'flask>=0.12.2,<0.13.0',
    'pillow>=4.2.1,<4.3.0'
]

tests_require = [
    'nose>=1.3.7,<1.4.0',
    'coverage>=4.4.1,<4.5.0'
]

guard_requires = [
    'pyinotify>=0.9.6,<0.10.0',
    'sniffer>=0.4.0,<0.4.1'
]

setup(
    name='autoswatch',
    version=VERSION,
    author='Philip Hughes',
    author_email='p@hews.co',
    url='https://github.com/hews/autoswatch',
    description='Generate color swatches on the fly.',
    license='MIT',

    packages=['autoswatch'],
    include_package_data=True,

    install_requires=install_requires,
    extras_require={
      'tests':       tests_require,
      'tests-guard': tests_require + guard_requires
    }
)
