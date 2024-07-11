from setuptools import setup, find_packages

# Be sure to update the version number in both "setup.py" and "meta.yaml" files.
setup(
    name='pyorganoid',
    version='0.1.3',
    packages=find_packages(),
    author='Daniel Szelogowski',
    description='A Python package for the simulation of organoids for the purpose of studying '
                'Organoid Intelligence (OI) and Organoid Learning (OL).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://danielathome19.github.io/pyorganoid',
    project_urls={
        'Documentation': 'https://danielathome19.github.io/pyorganoid',
        'Source': 'https://github.com/danielathome19/pyorganoid',
        'Tracker': 'https://github.com/danielathome19/pyorganoid/issues',
    },
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
