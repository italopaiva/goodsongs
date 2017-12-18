from setuptools import find_packages, setup

setup(
    name='goodsongs',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-mongoengine',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
