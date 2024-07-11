from setuptools import setup, find_packages

setup(
    name='pyorganoid',
    version='0.1.0',
    packages=find_packages(),
    author='Daniel Szelogowski',
    description='A Python package for the simulation of organoids for the purpose of studying '
                'Organoid Intelligence (OI) and Organoid Learning (OL).',
    long_description=open('README.md').read(),
    install_requires=[
        'numpy',
        'matplotlib',
        'graphviz',
    ],
    extras_require={
        "tensorflow": ["tensorflow<=2.15"],
        "torch": ["torch"],
        "sklearn": ["scikit-learn", "joblib"],
        "onnx": ["onnxruntime", "onnxmltools"],
        "all": ["tensorflow<=2.15", "torch", "scikit-learn", "joblib", "onnxruntime", "onnxmltools"]
    },
    entry_points={
        'console_scripts': [
            'pyorganoid=pyorganoid:main',
        ],
    },
)
