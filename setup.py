from setuptools import setup

setup(
    name="autoswatch",
    packages=["autoswatch"],
    include_package_data=True,
    install_requires=[
        "flask==0.12.2",
        "pillow==4.2.1"
    ],
    setup_requires=[
    ],
    tests_require=[
    ]
)

