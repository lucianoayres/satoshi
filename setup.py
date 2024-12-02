from setuptools import setup, find_packages

setup(
    name="satoshi",  
    version="0.1.0",  
    description="Automated tool to buy crypto on Mercado Bitcoin",
    author="Luciano",  
    author_email="email@example.com",  
    packages=find_packages(where="src"),  
    install_requires=[
        "requests>=2.28.1",
        "python-dotenv>=0.21.1"
    ],
    entry_points={
        "console_scripts": [
            "your_project_name=src.main:main",
        ]
    },
)