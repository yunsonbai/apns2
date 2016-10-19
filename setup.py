# coding=utf-8
import os
from setuptools import setup


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(
    name="apns2",
    version="0.2",
    packages=get_packages('apns2'),
    author="yunsonbai",
    author_email='1942893504@qq.com',
    url="http://www.yunsonbai.top",
    description='Tool integration:db data statistics/diagram/email',
    install_requires=[],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
