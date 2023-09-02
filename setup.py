from setuptools import find_packages, setup

setup(
    name="file-time-exporter",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "file-time-exporter=file_time_exporter.app:main",
        ],
    },
)
