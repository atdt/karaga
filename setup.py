"""
Karaga
=========

Karaga is the Wikimedia Foundation's Experiments Team's Selenium test runner.

"""
from setuptools import Command, setup


setup(
    name='Karaga',
    version='0.10-dev',
    url='http://github.com/mitsuhiko/karaga/',
    license='BSD',
    author='Ori Livneh',
    author_email='ori@wikimedia.org',
    description='E3 selenium test runner',
    long_description=__doc__,
    packages=['karaga'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['selenium>=2.26.0'],
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
