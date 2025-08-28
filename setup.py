from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docujudge",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered document evaluation tool using GPT-4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/docujudge",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.32.0",
        "langchain>=0.1.12",
        "langchain-openai>=0.0.8",
        "python-dotenv>=1.0.1",
        "python-multipart>=0.0.9",
    ],
    entry_points={
        "console_scripts": [
            "docujudge=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "examples": ["*.md"],
    },
)
