from setuptools import setup

import versioneer

with open('README.md') as f:
    readme = f.read()

setup(
    name='click-spinner',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description=readme,
    packages=['click_spinner'],
    url='https://github.com/click-contrib/click-spinner',
    license='MIT',
    author='Yoav Ram',
    author_email='yoav@yoavram.com',
    description='Spinner for Click',
    extras_require={
        'test': [
            'click'
            'pytest',
        ]
    }
)

