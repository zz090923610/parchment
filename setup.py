from setuptools import setup

setup(
    name='OhMyLifeRecorder',
    version='0.0.0.2',
    packages=['src'],
    url='',
    entry_points="""
[console_scripts]
lrecorder = src.recorder:main
""",
    license='MIT',
    author='zhangzhao',
    author_email='zz156@georgetown.edu',
    description='Easy tool to log your short message direct from cmd anytime you like, generate a diary-like document afterday.',
classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
