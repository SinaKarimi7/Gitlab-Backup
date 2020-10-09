#!/usr/bin/env python3

"""Setup script for gitlab-bk"""

import os.path
from setuptools import setup, find_packages
from cli.constants import VERSION

with open('README.md') as f:
    README = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="gitlab-bk",
    version=VERSION,
    license="MIT",
    description="Clone all projects in Gitlab account by group at once.",
    author="Cinna Karimi",
    author_email="sinakarimi76@gmail.com",
    url="https://github.com/SinaKarimi7/Gitlab-Backup",
    download_url = "https://github.com/SinaKarimi7/Gitlab-Backup/archive/v_01.tar.gz",
    keywords = ["GITLAB", "BACKUP", "CLONE", "SANCTION"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: System :: Archiving :: Backup",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=requirements,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    entry_points = {
        "console_scripts": ["gitlab-bk=cli.cli:main"],
    }
)
