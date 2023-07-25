from setuptools import setup, find_namespace_packages

setup(
    name="clean_folder",
    version="0.0.1",
    description="To get rid of mess in foldres",
    author="Ivan Markovskyi",
    author_email="test@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    entry_points={
        "console_scripts": ["clean_folder = clean_folder.clean:clean_folder"]
    },
)
