from setuptools import setup, find_packages


setup(
    name="document_portal",
    author="Matt Sikes",
    version="0.1",
    description="A document management portal built with FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/emsikes/document_portal",
    packages=find_packages()
)

