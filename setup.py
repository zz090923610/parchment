from setuptools import setup

setup(
    name='parchment',
    version='0.0.0.0.1',
    packages=['src'],
    url='',
    entry_points="""
[console_scripts]
parchment_repo = src.repo_mgr:main
""",
    license='MIT',
    author='zhangzhao',
    author_email='zz156@georgetown.edu',
    description='Easy tool to log your short message direct from cmd anytime you like, ',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
