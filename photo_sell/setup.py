from setuptools import setup, find_packages

setup(
    name='photo_sell',
    version='0.1',
    description='Program made to experiment with online payment systems.',
    url='https://github.com/vasilyrud/photo_sell',
    author='Vasily Rudchenko',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pytest', 
        'Flask', 
        'Flask-SQLAlchemy',
        'google-api-python-client',
        'Flask-WTF',
        'WTForms',
        'requests',
        'Flask-Caching',
    ],
)
