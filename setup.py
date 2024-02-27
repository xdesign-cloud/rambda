from setuptools import setup, find_packages

setup(
    name="rambda",
    version="1.1.0",
    description="Mature AWS LAMBda utilites",
    author="Harry Reeder",
    author_email="harry.reeder@xdesign.com",
    packages=find_packages(),
    install_requires=[
        "aws-xray-sdk~=2.12",
        "aws_lambda_typing~=2.18",
    ]
)
