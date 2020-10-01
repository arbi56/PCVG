
from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name="pcvg",
    version="0.9.0",
    description="Package providing PCVG and various utilities",
    long_description=readme(),
    long_description_content_type='text/markdown',
    license="MIT License",
    url="https://github.com/arbi56/PCVG",
    packages=[
        'pcvg',
        "pcvg.processing",
        "pcvg.utils",
        "pcvg.plotting"],
    python_requires='>=3.5',
    install_requires=[
        "bokeh>=1.0.0",
        "numpy",
        "pandas"],
    author='Ron Bonner',
    author_email='ron@bonners.ca'
)