"""
Setup script for Mobinet NextGen Test Automation Framework.
Provides installation and configuration utilities.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements from requirements.txt
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='mobinet-nextgen-automation',
    version='1.0.0',
    author='Mobinet Test Automation Team',
    author_email='test-automation@mobinet.com',
    description='Comprehensive Selenium WebDriver automation framework for Mobinet NextGen Non-Payment Reason Management',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mobinet/nextgen-automation',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
    ],
    python_requires='>=3.8',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'mypy>=1.0.0',
            'isort>=5.10.0',
        ],
        'reporting': [
            'allure-pytest>=2.13.0',
            'pytest-html>=3.1.0',
            'pytest-json-report>=1.5.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'mobinet-test=scripts.run_tests:main',
            'mobinet-setup=scripts.setup_environment:main',
        ],
    },
    include_package_data=True,
    package_data={
        'mobinet_automation': [
            'config/*.yaml',
            'templates/*.html',
            'reports/templates/*.html'
        ]
    },
    project_urls={
        'Bug Reports': 'https://github.com/mobinet/nextgen-automation/issues',
        'Source': 'https://github.com/mobinet/nextgen-automation',
        'Documentation': 'https://mobinet-automation.readthedocs.io/',
    },
)