from setuptools import setup, find_packages

setup(
    name="satoshi",  
    version="0.1.0",  
    description="Automated tool to buy crypto on Mercado Bitcoin",
    author="Luciano",  
    author_email="email@example.com",  
    packages=find_packages(where="src"),  
    package_dir={'': 'src'},  
    install_requires=[
        "requests>=2.28.1",
        "python-dotenv>=0.21.1"
    ],
    entry_points={
        "console_scripts": [
            "satoshi=main:main",  # Updated entry point
        ]
    },
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-mock>=3.0.0",
            "pytest-cov>=3.0.0",
        ],
    },
)
