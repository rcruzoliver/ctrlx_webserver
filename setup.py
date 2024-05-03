from setuptools import setup

setup(
    name='webserver-flask',
    version='2.0.0',
    description='This sample shows how to provide data to ctrlX Data Layer',
    author='SDK Team',
    packages = ['app', 'appdata', 'motion.core.fbtypes', 'robot.core.fbtypes'],
    install_requires = ['flask', 'ctrlx-datalayer', 'ctrlx-fbs', 'pyopenssl'],
    # https://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
    package_data={},
    scripts=['main.py','datalayerProvider.py','fbsFunction.py'],
    #package_data={'./': ['sampleSchema.bfbs']},
    license='Copyright (c) 2020-2021 Bosch Rexroth AG, Licensed under MIT License'
)
