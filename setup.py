from setuptools import setup

setup(
    name="autoswatch",
    packages=["autoswatch"],
    include_package_data=True,
    install_requires=[
        "flask>=0.12.2,<0.13.0",
        "pillow>=4.2.1,<4.3.0"
    ],
    setup_requires=[
        "nose>=1.3.7,<1.4.0"
    ],
    tests_require=[
        "nose>=1.3.7,<1.4.0",
        "coverage"
    ]
)
