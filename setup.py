from setuptools import find_packages, setup

setup(
    name="stepwise",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[line for line in open("requirements.txt")],
    extras_require={
        "tests": ["pytest", "pytest-cov"],
    },
    include_package_data=True,
)
