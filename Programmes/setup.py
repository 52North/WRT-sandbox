from setuptools import setup, find_packages

setup(
    name='WRT',
    version='0.1.0',
    description='Weather Routing Tool for sandbox use',
    url='https://github.com/jonathanbauer03/WRT-for-sandbox',
    packages=find_packages(),  # findet alle Python-Module (mit __init__.py)
    include_package_data=True,  # nimmt auch Dateien mit auf, die in MANIFEST.in definiert sind
    install_requires=[
        'python-dotenv',
        'ipyleaflet',
        'ipyopenlayers',
        'ipywidgets',
        'Pillow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
