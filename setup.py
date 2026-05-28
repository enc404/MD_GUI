from setuptools import setup, find_packages

setup(
    name="markitdown-app",
    version="1.0.0",
    description="Windows GUI application to convert files to Markdown using Microsoft's MarkItDown",
    author="enc404",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "markitdown[all]>=0.1.0",
    ],
    entry_points={
        "gui_scripts": [
            "markitdown-app=markitdown_app.main:main",
        ],
    },
)
