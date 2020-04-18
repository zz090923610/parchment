from setuptools import setup

setup(
    name='parchment',
    version='0.0.0.0.1',
    packages=['src'],
    url='',
    entry_points="""
[console_scripts]
parchment_repo = src.repo_mgr:main
parchment_words = src.topic_mgr:parchment_words
parchment_para = src.topic_mgr:parchment_para
parchment_ref = src.topic_mgr:parchment_ref
parchment_timeline = src.topic_mgr:parchment_timeline
""",
    license='MIT',
    author='zhangzhao',
    author_email='zz156@georgetown.edu',
    description='Easy tool to log your short message direct from cmd anytime you like, ',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
