from setuptools import setup , find_packages
from setuptools import setup, find_packages
with open("README.md", "r") as streamr:
    long_description = streamr.read()

setup(
    name='spideyx',
    version='1.0.0',
    author='D. Sanjai Kumar',
    author_email='bughunterz0047@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RevoltSecurities/SpideyX",
    description='SpideyX - A Web Reconnaissance Penetration Testing tool for Penetration Testers and Ethical Hackers',
    packages=find_packages(),
    install_requires=[
        'aiofiles>=24.1.0',
        'alive_progress>=3.1.4',
        'appdirs>=1.4.4',
        'art>=6.2',
        'asyncclick>=8.1.7.2',
        'beautifulsoup4>=4.11.1',
        'colorama>=0.4.6',
        'dicttoxml>=1.7.16',
        'fake_useragent>=1.5.1',
        'httpx>=0.27.2',
        'PyYAML>=6.0.2',
        'Requests>=2.32.3',
        'rich>=13.8.1',
        'tldextract>=5.1.2',
        'urllib3>=1.26.18',
        'yarl>=1.9.4'
    ],
    entry_points={
        'console_scripts': [
            'spideyx = spideyx.spideyx:cli'
        ]
    },
)