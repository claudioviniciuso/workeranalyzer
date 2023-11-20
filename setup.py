from setuptools import setup, find_packages

setup(
    name='worker_analyzer',
    version='0.1.0',
    description='Your package description',
    author='Claudio Vinicius Oliveira',
    author_email='claudiovinicius.o@hotmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy==1.26.2',
        'pandas==2.1.3',
        'python-dateutil==2.8.2',
        'pytz==2023.3.post1',
        'tzdata==2023.3'
    ],
)