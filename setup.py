#-*- coding: utf-8 -*-
from setuptools import setup
import os

CLASSIFIERS = []

setup(
    author="QDQ media",
    author_email="dpto-tecnico@qdqmedia.com",
    name='django-actions',
    version='0.0.1',
    description='',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    url='https://github.com/qdqmedia/django-actions/',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    zip_safe=False,
)
