from setuptools import setup, find_packages

setup(
    name='pyorganoid',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    extras_require={
        "tensorflow": ["tensorflow<=2.15"],
        "torch": ["torch"],
        "sklearn": ["scikit-learn", "joblib"],
        "all": ["tensorflow<=2.15", "torch", "scikit-learn", "joblib"]
    },
    entry_points={
        'console_scripts': [
            'pyorganoid=pyorganoid:main',
        ],
    },
)
