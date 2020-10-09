"""Setup script for gitlab-bk"""

import os.path
import setuptools

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setuptools.setup(
    name="gitlab-bk",
    version="0.0.7",
    license="MIT",
    description="Clone all projects in Gitlab account by group at once.",
    author="Cinna Karimi",
    author_email="sinakarimi76@gmail.com",
    url="https://github.com/SinaKarimi7/Gitlab-Backup",
    download_url = 'https://github.com/SinaKarimi7/Gitlab-Backup/archive/v_01.tar.gz',
    keywords = ['GITLAB', 'BACKUP', 'CLONE', 'SANCTION'],
    install_requires=[
        "alive_progress>=1.6.1"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Archiving :: Backup',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
    ],
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['gitlab-bk=cli.cli:main'],
    }
)
