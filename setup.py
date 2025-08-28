from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="docu-judge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    author="Pritam Nikam",
    author_email="pritam.nikam@example.com",
    description="AI-powered document evaluation tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/docu-judge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'docu-judge=app:main',
        ],
    },
    include_package_data=True,
)
