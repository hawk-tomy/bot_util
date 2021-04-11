from setuptools import setup

with open('README.md')as f:
    readme = f.read()

setup(
    name='bot_util',
    author='hawk_tomy',
    url='https://github.com/hawk-tomy/bot_util',
    version='0.0.3',
    packages=['bot_util'],
    license='MIT',
    description='自作bot用の便利関数など',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'pyyaml',
        'discord_ext_menus@git+https://github.com/Rapptz/discord-ext-menus'
        ],
)