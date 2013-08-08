#coding=utf8
from setuptools import setup

__author__ = 'alex'

setup(
    name='TorCast',
    version='0.0.0.3 pre',
    packages=['TorCast'],
    author='Alexander.Li',
    author_email='superpowerlee@gmail.com',
    license='LGPL',
    install_requires=["tornado>=2.4.1",],
    description="Broadcast messages to all tornado process subcribed on Redis asynchronously",
    keywords ='tornado asynchronous redis message',
    url="https://github.com/ipconfiger/TorCast"
)