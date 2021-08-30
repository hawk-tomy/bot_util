from setuptools import setup

with open('README.md', encoding='utf-8')as f:
    readme = f.read()

with open('requirements.txt', encoding='utf8')as f:
    requires = f.readlines()

setup(
    name='bot_util',
    author='hawk_tomy',
    url='https://github.com/hawk-tomy/bot_util',
    version='0.4.0',
    packages=['bot_util'],
    license='MIT',
    description='自作bot用の便利関数など',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requires,
)
